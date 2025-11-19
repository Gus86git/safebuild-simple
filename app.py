import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from datetime import datetime
import time

# =============================================
# CONFIGURACIÓN DE LA PÁGINA
# =============================================
st.set_page_config(
    page_title="SafeBuild - Monitoreo de Seguridad",
    page_icon="🦺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# CSS PERSONALIZADO
# =============================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .alert-high {
        background-color: #FEE2E2;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 6px solid #DC2626;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .alert-medium {
        background-color: #FEF3C7;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 6px solid #D97706;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .alert-ok {
        background-color: #D1FAE5;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 6px solid #059669;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background-color: #F8FAFC;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #E2E8F0;
        margin: 0.5rem 0;
    }
    .sidebar-section {
        background-color: #F1F5F9;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stButton button {
        width: 100%;
        background-color: #1E40AF;
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
    }
    .detection-box {
        border: 3px solid;
        position: absolute;
        background-color: transparent;
    }
    .person-box { border-color: #00FF00; }
    .helmet-box { border-color: #0000FF; }
    .vest-box { border-color: #FF0000; }
</style>
""", unsafe_allow_html=True)

# =============================================
# SISTEMA EXPERTO (INTEGRADO EN EL MISMO ARCHIVO)
# =============================================
class SafetyExpertSystem:
    def __init__(self):
        self.rules = {
            'no_helmet_critical': {
                'condition': lambda stats: stats['persons'] > 0 and stats['helmets'] == 0,
                'message': "CRÍTICO: Ningún trabajador usa casco de seguridad",
                'level': "ALTA",
                'action': "DETENER actividades inmediatamente y notificar al supervisor de seguridad"
            },
            'no_helmet_partial': {
                'condition': lambda stats: stats['persons'] > 0 and stats['helmets'] < stats['persons'],
                'message': "ALTA: Trabajadores detectados sin casco de seguridad",
                'level': "ALTA", 
                'action': "Aislar el área y proveer EPP inmediatamente"
            },
            'no_vest_critical': {
                'condition': lambda stats: stats['persons'] > 0 and stats['vests'] == 0,
                'message': "MEDIA: Ningún trabajador usa chaleco reflectante",
                'level': "MEDIA",
                'action': "Notificar al supervisor y proveer chalecos de seguridad"
            },
            'no_vest_partial': {
                'condition': lambda stats: stats['persons'] > 0 and stats['vests'] < stats['persons'],
                'message': "MEDIA: Trabajadores detectados sin chaleco reflectante",
                'level': "MEDIA",
                'action': "Recordar uso obligatorio de chaleco en reunión de seguridad"
            },
            'proper_equipment': {
                'condition': lambda stats: stats['persons'] > 0 and stats['helmets'] >= stats['persons'] and stats['vests'] >= stats['persons'],
                'message': "OK: Todo el personal cuenta con Equipo de Protección Personal completo",
                'level': "OK",
                'action': "Continuar monitoreo y mantener los estándares de seguridad"
            },
            'no_persons': {
                'condition': lambda stats: stats['persons'] == 0,
                'message': "OK: No se detectaron trabajadores en el área analizada",
                'level': "OK", 
                'action': "Continuar con el monitoreo rutinario del área"
            }
        }
    
    def analyze_detections(self, detections):
        person_count = sum(1 for det in detections if det['class_name'] == 'person')
        helmet_count = sum(1 for det in detections if det['class_name'] == 'helmet') 
        vest_count = sum(1 for det in detections if det['class_name'] == 'safety_vest')
        
        detection_stats = {
            'persons': person_count,
            'helmets': helmet_count,
            'vests': vest_count
        }
        
        for rule_name, rule in self.rules.items():
            if rule['condition'](detection_stats):
                return {
                    'alert_level': rule['level'],
                    'alert_message': rule['message'],
                    'recommended_action': rule['action'],
                    'statistics': detection_stats
                }
        
        return {
            'alert_level': "OK",
            'alert_message': "Condiciones normales de seguridad detectadas",
            'recommended_action': "Continuar con el monitoreo rutinario",
            'statistics': detection_stats
        }

# =============================================
# FUNCIONES DE VISUALIZACIÓN CON PIL
# =============================================
def create_demo_image(scenario_type, width=600, height=400):
    """Crear imagen de demo con PIL (sin OpenCV)"""
    # Crear imagen base (fondo de obra)
    img = Image.new('RGB', (width, height), color=(200, 200, 200))
    draw = ImageDraw.Draw(img)
    
    # Dibujar elementos de construcción
    draw.rectangle([50, 200, 550, 250], fill=(139, 69, 19), outline=(0,0,0), width=2)  # tierra
    draw.rectangle([100, 150, 200, 200], fill=(210, 180, 140), outline=(0,0,0), width=2)  # ladrillo
    draw.rectangle([300, 100, 400, 200], fill=(192, 192, 192), outline=(0,0,0), width=2)  # estructura
    
    # Añadir texto de fondo
    try:
        font = ImageFont.load_default()
        draw.text((10, 10), "SafeBuild - Obra en Progreso", fill=(0,0,0), font=font)
    except:
        draw.text((10, 10), "SafeBuild - Obra en Progreso", fill=(0,0,0))
    
    return img, draw

def draw_detections_pil(image, draw, detections):
    """Dibujar detecciones usando PIL"""
    colors = {
        'person': 'green',
        'helmet': 'blue', 
        'safety_vest': 'red'
    }
    
    for detection in detections:
        class_name = detection['class_name']
        x1, y1, x2, y2 = detection['bbox']
        color = colors.get(class_name, 'black')
        
        # Dibujar bounding box
        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
        
        # Dibujar etiqueta
        label = f"{class_name}"
        bbox = draw.textbbox((0, 0), label)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        draw.rectangle([x1, y1-text_height-10, x1+text_width+10, y1], fill=color)
        draw.text((x1+5, y1-text_height-5), label, fill='white')
    
    return image

def simulate_detections(scenario_type):
    """Simular detecciones de YOLO"""
    if scenario_type == "escenario_seguro":
        return [
            {'class_name': 'person', 'confidence': 0.95, 'bbox': [100, 100, 180, 250]},
            {'class_name': 'helmet', 'confidence': 0.92, 'bbox': [110, 90, 140, 120]},
            {'class_name': 'safety_vest', 'confidence': 0.89, 'bbox': [100, 120, 180, 170]},
            {'class_name': 'person', 'confidence': 0.88, 'bbox': [300, 150, 380, 300]},
            {'class_name': 'helmet', 'confidence': 0.91, 'bbox': [310, 140, 340, 170]},
            {'class_name': 'safety_vest', 'confidence': 0.87, 'bbox': [300, 170, 380, 220]}
        ]
    elif scenario_type == "escenario_alerta":
        return [
            {'class_name': 'person', 'confidence': 0.95, 'bbox': [100, 100, 180, 250]},
            {'class_name': 'helmet', 'confidence': 0.92, 'bbox': [110, 90, 140, 120]},
            # Falta chaleco para primera persona
            {'class_name': 'person', 'confidence': 0.88, 'bbox': [300, 150, 380, 300]},
            {'class_name': 'safety_vest', 'confidence': 0.87, 'bbox': [300, 170, 380, 220]}
            # Falta casco para segunda persona
        ]
    else:  # escenario_critico
        return [
            {'class_name': 'person', 'confidence': 0.95, 'bbox': [100, 100, 180, 250]},
            {'class_name': 'person', 'confidence': 0.88, 'bbox': [300, 150, 380, 300]},
            # Faltan ambos EPPs
        ]

# =============================================
# INICIALIZACIÓN
# =============================================
expert_system = SafetyExpertSystem()

# =============================================
# SIDEBAR
# =============================================
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.header("⚙️ Configuración")
min_confidence = st.sidebar.slider("Confianza Mínima", 0.1, 0.9, 0.6, 0.05)
alert_system = st.sidebar.checkbox("Alertas Activas", True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.header("🎯 Modo de Operación")
mode = st.sidebar.radio(
    "Selecciona el modo:",
    ["📊 Demo con Escenarios", "📸 Subir Imagen"],
    index=0
)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# =============================================
# HEADER PRINCIPAL
# =============================================
st.markdown('<h1 class="main-header">🦺 SafeBuild</h1>', unsafe_allow_html=True)
st.markdown("### Sistema Inteligente de Monitoreo de Seguridad en Obras")
st.markdown("---")

# =============================================
# CONTENIDO PRINCIPAL
# =============================================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("👁️ Monitoreo en Tiempo Real")
    
    if mode == "📊 Demo con Escenarios":
        st.info("🎯 **Selecciona un escenario para analizar:**")
        
        scenario = st.radio(
            "Escenarios de Obra:",
            ["✅ Condiciones Seguras", "⚠️ Alertas Parciales", "🚨 Condiciones Críticas"],
            horizontal=True
        )
        
        scenario_map = {
            "✅ Condiciones Seguras": "escenario_seguro",
            "⚠️ Alertas Parciales": "escenario_alerta", 
            "🚨 Condiciones Críticas": "escenario_critico"
        }
        
        selected_scenario = scenario_map[scenario]
        
        if st.button("🚀 Ejecutar Análisis de Seguridad", use_container_width=True):
            with st.spinner("🖼️ Generando escenario de obra..."):
                # Crear imagen de demo
                demo_img, draw_obj = create_demo_image(selected_scenario)
                time.sleep(1)
            
            with st.spinner("🔍 Analizando condiciones de seguridad..."):
                # Simular detecciones
                detections = simulate_detections(selected_scenario)
                analysis = expert_system.analyze_detections(detections)
                time.sleep(1)
                
                # Dibujar detecciones en la imagen
                result_img = draw_detections_pil(demo_img, draw_obj, detections)
            
            st.success("✅ Análisis completado")
            
            # Mostrar imagen resultante
            st.image(result_img, caption=f"Escenario: {scenario}", use_column_width=True)
            
            # Mostrar resultados del análisis
            alert_level = analysis['alert_level']
            if alert_level == "ALTA":
                st.markdown(f"""
                <div class="alert-high">
                    <h3>🚨 ALERTA CRÍTICA</h3>
                    <p><strong>{analysis['alert_message']}</strong></p>
                    <p>📋 <strong>Acción:</strong> {analysis['recommended_action']}</p>
                </div>
                """, unsafe_allow_html=True)
            elif alert_level == "MEDIA":
                st.markdown(f"""
                <div class="alert-medium">
                    <h3>⚠️ ALERTA MEDIA</h3>
                    <p><strong>{analysis['alert_message']}</strong></p>
                    <p>📋 <strong>Acción:</strong> {analysis['recommended_action']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="alert-ok">
                    <h3>✅ CONDICIONES SEGURAS</h3>
                    <p><strong>{analysis['alert_message']}</strong></p>
                    <p>📋 <strong>Acción:</strong> {analysis['recommended_action']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.info("👆 **Presiona el botón para ejecutar el análisis**")
            
    else:
        # Modo subir imagen
        st.info("📸 **Sube una imagen de tu obra**")
        uploaded_file = st.file_uploader("Selecciona imagen:", type=['jpg', 'jpeg', 'png'])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Imagen subida", use_column_width=True)
            
            # Simular análisis
            with st.spinner("🔍 Analizando imagen..."):
                file_name = uploaded_file.name.lower()
                if "safe" in file_name:
                    detections = simulate_detections("escenario_seguro")
                elif "alert" in file_name:
                    detections = simulate_detections("escenario_alerta")
                else:
                    detections = simulate_detections("escenario_critico")
                
                analysis = expert_system.analyze_detections(detections)
                time.sleep(1)
            
            # Mostrar resultados
            alert_level = analysis['alert_level']
            if alert_level == "ALTA":
                st.error(f"🚨 {analysis['alert_message']}")
            elif alert_level == "MEDIA":
                st.warning(f"⚠️ {analysis['alert_message']}")
            else:
                st.success(f"✅ {analysis['alert_message']}")
            
            st.info(f"📋 **Acción recomendada:** {analysis['recommended_action']}")

with col2:
    st.subheader("📊 Panel de Control")
    
    # Mostrar estadísticas
    if 'analysis' in locals():
        stats = analysis.get('statistics', {})
        persons = stats.get('persons', 0)
        helmets = stats.get('helmets', 0)
        vests = stats.get('vests', 0)
        compliance = min(helmets, vests) / persons * 100 if persons > 0 else 0
    else:
        persons = helmets = vests = compliance = 0
    
    # Métricas
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("👥 Trabajadores", persons)
        st.metric("🪖 Cascos", helmets)
    with col_b:
        st.metric("🦺 Chalecos", vests)
        st.metric("📈 Cumplimiento", f"{compliance:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Alertas
    st.subheader("🚨 Estado Actual")
    if persons > 0:
        if helmets < persons:
            st.error(f"❌ {persons - helmets} sin casco")
        else:
            st.success("✅ Cascos OK")
        
        if vests < persons:
            st.warning(f"⚠️ {persons - vests} sin chaleco")
        else:
            st.success("✅ Chalecos OK")
    else:
        st.info("👀 No hay trabajadores")
    
    # Historial
    st.subheader("📋 Actividad Reciente")
    activity_data = {
        'Hora': [datetime.now().strftime("%H:%M"), '10:30', '09:15'],
        'Evento': ['Análisis Actual', 'Zona B', 'Revisión'],
        'Resultado': [analysis['alert_level'] if 'analysis' in locals() else 'N/A', 'MEDIA', 'OK']
    }
    df = pd.DataFrame(activity_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# =============================================
# ESTADÍSTICAS
# =============================================
st.markdown("---")
st.subheader("📈 Estadísticas del Sistema")

col3, col4, col5, col6 = st.columns(4)
with col3:
    st.metric("Inspecciones Hoy", "24", "12%")
with col4:
    st.metric("Alertas Totales", "8", "-3%")
with col5:
    st.metric("Cumplimiento", "83%", "5%")
with col6:
    st.metric("Respuesta", "2.1 min", "0.3 min")

# =============================================
# FOOTER
# =============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p><strong>SafeBuild v1.0</strong> - Sistema Inteligente de Monitoreo | 🚧 TP Integrador IA 🚧</p>
</div>
""", unsafe_allow_html=True)

# Información en sidebar
st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.info("""
**SafeBuild v1.0**  
Sistema de monitoreo inteligente  
para obras de construcción

🚧 **Integra:**  
• Sistema experto de reglas  
• Análisis de seguridad  
• Alertas automáticas
""")
st.sidebar.markdown('</div>', unsafe_allow_html=True)
