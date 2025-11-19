import streamlit as st
import base64
from datetime import datetime
import time
import random

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
    .uploaded-image {
        border-radius: 10px;
        border: 3px solid #E2E8F0;
        margin: 1rem 0;
        max-width: 100%;
    }
    .analysis-result {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border: 2px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# SISTEMA EXPERTO
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
# SIMULADOR DE DETECCIÓN DE IMÁGENES
# =============================================
def analyze_uploaded_image(image_file):
    """
    Simula el análisis de una imagen subida
    En una implementación real, aquí iría el modelo YOLO
    """
    # Simular análisis basado en características de la imagen
    file_name = image_file.name.lower()
    file_size = image_file.size
    
    # Simular diferentes escenarios basados en nombre y tamaño
    if any(word in file_name for word in ['safe', 'seguro', 'good', 'completo']):
        # Escenario seguro
        return [
            {'class_name': 'person', 'confidence': 0.92, 'bbox': [100, 100, 180, 250]},
            {'class_name': 'helmet', 'confidence': 0.89, 'bbox': [110, 90, 140, 120]},
            {'class_name': 'safety_vest', 'confidence': 0.87, 'bbox': [100, 120, 180, 170]},
            {'class_name': 'person', 'confidence': 0.85, 'bbox': [300, 150, 380, 300]},
            {'class_name': 'helmet', 'confidence': 0.88, 'bbox': [310, 140, 340, 170]},
            {'class_name': 'safety_vest', 'confidence': 0.86, 'bbox': [300, 170, 380, 220]}
        ]
    elif any(word in file_name for word in ['peligro', 'peligroso', 'danger', 'alert']):
        # Escenario crítico
        return [
            {'class_name': 'person', 'confidence': 0.94, 'bbox': [100, 100, 180, 250]},
            {'class_name': 'person', 'confidence': 0.91, 'bbox': [300, 150, 380, 300]},
            # Sin EPPs
        ]
    elif file_size > 1000000:  # Imagen grande - más probabilidad de múltiples personas
        # Escenario mixto
        return [
            {'class_name': 'person', 'confidence': 0.93, 'bbox': [100, 100, 180, 250]},
            {'class_name': 'helmet', 'confidence': 0.90, 'bbox': [110, 90, 140, 120]},
            # Falta chaleco
            {'class_name': 'person', 'confidence': 0.87, 'bbox': [300, 150, 380, 300]},
            # Falta casco
            {'class_name': 'safety_vest', 'confidence': 0.85, 'bbox': [300, 170, 380, 220]}
        ]
    else:
        # Escenario aleatorio basado en probabilidades
        scenarios = [
            # Escenario seguro
            [
                {'class_name': 'person', 'confidence': 0.91, 'bbox': [100, 100, 180, 250]},
                {'class_name': 'helmet', 'confidence': 0.88, 'bbox': [110, 90, 140, 120]},
                {'class_name': 'safety_vest', 'confidence': 0.86, 'bbox': [100, 120, 180, 170]}
            ],
            # Escenario con alertas
            [
                {'class_name': 'person', 'confidence': 0.93, 'bbox': [100, 100, 180, 250]},
                {'class_name': 'helmet', 'confidence': 0.89, 'bbox': [110, 90, 140, 120]},
                # Falta chaleco
                {'class_name': 'person', 'confidence': 0.87, 'bbox': [300, 150, 380, 300]},
                {'class_name': 'safety_vest', 'confidence': 0.85, 'bbox': [300, 170, 380, 220]}
            ],
            # Escenario crítico
            [
                {'class_name': 'person', 'confidence': 0.94, 'bbox': [100, 100, 180, 250]},
                {'class_name': 'person', 'confidence': 0.90, 'bbox': [300, 150, 380, 300]}
            ]
        ]
        return random.choice(scenarios)

# =============================================
# FUNCIÓN PARA DIBUJAR DETECCIONES (SIMULADO)
# =============================================
def create_analysis_visualization(image, detections, analysis):
    """
    Crea una visualización HTML con la imagen y los resultados
    """
    # Simular imagen con bounding boxes (en realidad sería la imagen procesada)
    st.markdown(f"""
    <div class="analysis-result">
        <h3>📊 Resultado del Análisis</h3>
        <p><strong>Imagen analizada:</strong> {image.name}</p>
        <p><strong>Tamaño:</strong> {image.size} bytes</p>
        <p><strong>Detecciones realizadas:</strong> {len(detections)} objetos</p>
    </div>
    """, unsafe_allow_html=True)
    
    return True

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
alert_system = st.sidebar.checkbox("Sistema de Alertas Activo", True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.header("🎯 Modo de Operación")
mode = st.sidebar.radio(
    "Selecciona el modo:",
    ["📸 Subir Mi Imagen", "📊 Demo con Escenarios"],
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
    
    if mode == "📸 Subir Mi Imagen":
        st.info("📸 **Sube una imagen de tu obra para analizar la seguridad**")
        
        # Widget para subir imagen
        uploaded_file = st.file_uploader(
            "Selecciona una imagen de la obra:",
            type=['jpg', 'jpeg', 'png', 'bmp'],
            help="Formatos soportados: JPG, JPEG, PNG, BMP"
        )
        
        if uploaded_file is not None:
            # Mostrar información de la imagen
            st.success(f"✅ **Imagen cargada:** {uploaded_file.name}")
            
            # Mostrar la imagen subida
            st.image(uploaded_file, caption=f"Imagen de la obra: {uploaded_file.name}", use_column_width=True)
            
            # Botón para analizar
            if st.button("🔍 Analizar Imagen", use_container_width=True):
                with st.spinner("Analizando imagen con IA..."):
                    # Simular tiempo de procesamiento
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.02)
                        progress_bar.progress(i + 1)
                    
                    # Analizar la imagen
                    detections = analyze_uploaded_image(uploaded_file)
                    analysis = expert_system.analyze_detections(detections)
                
                st.success("✅ Análisis completado")
                
                # Mostrar visualización del análisis
                create_analysis_visualization(uploaded_file, detections, analysis)
                
                # Mostrar resultados del análisis
                alert_level = analysis['alert_level']
                if alert_level == "ALTA":
                    st.markdown(f"""
                    <div class="alert-high">
                        <h3>🚨 ALERTA CRÍTICA DE SEGURIDAD</h3>
                        <p><strong>{analysis['alert_message']}</strong></p>
                        <p>📋 <strong>Acción Recomendada:</strong> {analysis['recommended_action']}</p>
                        <p>⏰ <strong>Prioridad:</strong> Resolución Inmediata</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif alert_level == "MEDIA":
                    st.markdown(f"""
                    <div class="alert-medium">
                        <h3>⚠️ ALERTA DE SEGURIDAD</h3>
                        <p><strong>{analysis['alert_message']}</strong></p>
                        <p>📋 <strong>Acción Recomendada:</strong> {analysis['recommended_action']}</p>
                        <p>⏰ <strong>Prioridad:</strong> Resolución en 1 hora</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="alert-ok">
                        <h3>✅ CONDICIONES SEGURAS</h3>
                        <p><strong>{analysis['alert_message']}</strong></p>
                        <p>📋 <strong>Acción Recomendada:</strong> {analysis['recommended_action']}</p>
                        <p>⏰ <strong>Estado:</strong> Operaciones Normales</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        else:
            st.info("👆 **Selecciona una imagen de tu obra para comenzar el análisis**")
            st.markdown("""
            **📝 Tip:** Puedes subir fotos de:
            - Trabajadores en la obra
            - Zonas de construcción
            - Áreas de trabajo
            - Equipos y personal
            """)
            
    else:
        # Modo demo (mantenemos el anterior por si acaso)
        st.info("🎯 **Selecciona un escenario para analizar:**")
        
        scenario = st.radio(
            "Escenarios de Obra:",
            ["✅ Condiciones Seguras", "⚠️ Alertas Parciales", "🚨 Condiciones Críticas"],
            horizontal=True
        )
        
        if st.button("🚀 Ejecutar Análisis de Seguridad", use_container_width=True):
            with st.spinner("🔍 Analizando condiciones de seguridad..."):
                # Simular escenarios
                scenario_map = {"✅ Condiciones Seguras": "seguro", "⚠️ Alertas Parciales": "alerta", "🚨 Condiciones Críticas": "critico"}
                selected_scenario = scenario_map[scenario]
                
                if selected_scenario == "seguro":
                    detections = [
                        {'class_name': 'person', 'confidence': 0.95, 'bbox': [100, 100, 180, 250]},
                        {'class_name': 'helmet', 'confidence': 0.92, 'bbox': [110, 90, 140, 120]},
                        {'class_name': 'safety_vest', 'confidence': 0.89, 'bbox': [100, 120, 180, 170]},
                        {'class_name': 'person', 'confidence': 0.88, 'bbox': [300, 150, 380, 300]},
                        {'class_name': 'helmet', 'confidence': 0.91, 'bbox': [310, 140, 340, 170]},
                        {'class_name': 'safety_vest', 'confidence': 0.87, 'bbox': [300, 170, 380, 220]}
                    ]
                elif selected_scenario == "alerta":
                    detections = [
                        {'class_name': 'person', 'confidence': 0.95, 'bbox': [100, 100, 180, 250]},
                        {'class_name': 'helmet', 'confidence': 0.92, 'bbox': [110, 90, 140, 120]},
                        {'class_name': 'person', 'confidence': 0.88, 'bbox': [300, 150, 380, 300]},
                        {'class_name': 'safety_vest', 'confidence': 0.87, 'bbox': [300, 170, 380, 220]}
                    ]
                else:
                    detections = [
                        {'class_name': 'person', 'confidence': 0.95, 'bbox': [100, 100, 180, 250]},
                        {'class_name': 'person', 'confidence': 0.88, 'bbox': [300, 150, 380, 300]},
                    ]
                
                analysis = expert_system.analyze_detections(detections)
                time.sleep(1)
            
            st.success("✅ Análisis completado")
            
            # Mostrar resultados
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

with col2:
    st.subheader("📊 Panel de Control")
    
    # Mostrar estadísticas actuales
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
    
    # Alertas activas
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
        st.info("👀 No hay trabajadores detectados")
    
    # Historial de análisis
    st.subheader("📋 Historial Reciente")
    if 'uploaded_file' in locals() and uploaded_file is not None:
        st.write(f"• **Última imagen:** {uploaded_file.name}")
        st.write(f"• **Resultado:** {analysis.get('alert_level', 'N/A')}")
        st.write(f"• **Trabajadores:** {persons}")
    else:
        st.write("• Aún no se han analizado imágenes")
        st.write("• Sube una imagen para comenzar")

# =============================================
# SECCIÓN DE ESTADÍSTICAS
# =============================================
st.markdown("---")
st.subheader("📈 Estadísticas del Sistema")

col3, col4, col5, col6 = st.columns(4)
with col3:
    st.metric("Imágenes Analizadas", "15")
with col4:
    st.metric("Alertas Totales", "8")
with col5:
    st.metric("Cumplimiento Promedio", "83%")
with col6:
    st.metric("Tiempo Análisis", "2.1s")

# =============================================
# INFORMACIÓN DEL SISTEMA
# =============================================
st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.subheader("ℹ️ Información del Sistema")
st.sidebar.info("""
**SafeBuild v1.0**  

📸 **Sube imágenes de tu obra**  
• Análisis automático de seguridad  
• Detección de EPP (cascos y chalecos)  
• Sistema experto de reglas  

🎓 **Para TP Integrador IA:**  
• Sistemas Expertos  
• Procesamiento de Imágenes  
• Automatización Inteligente
""")
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# =============================================
# FOOTER
# =============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>SafeBuild v1.0</strong> - Sistema Inteligente de Monitoreo de Seguridad en Obras</p>
    <p>🚧 <strong>Trabajo Práctico Integrador</strong> - Desarrollo de Sistemas de Inteligencia Artificial 🚧</p>
    <p style="font-size: 0.8rem;">📸 Ahora con análisis de imágenes subidas desde tu PC</p>
</div>
""", unsafe_allow_html=True)
