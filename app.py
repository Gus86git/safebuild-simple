import streamlit as st
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
    .scenario-image {
        border-radius: 10px;
        border: 3px solid #E2E8F0;
        margin: 1rem 0;
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
# IMÁGENES BASE64 INTEGRADAS
# =============================================
def get_base64_image(scenario):
    """Imágenes SVG simples integradas en el código"""
    if scenario == "seguro":
        return """
        <svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
            <rect width="100%" height="100%" fill="#e0e0e0"/>
            <rect x="50" y="250" width="500" height="100" fill="#8B4513"/>
            <rect x="100" y="150" width="100" height="100" fill="#CD853F"/>
            <rect x="300" y="100" width="100" height="150" fill="#A9A9A9"/>
            
            <!-- Trabajador 1 con EPP completo -->
            <circle cx="150" cy="120" r="25" fill="#00FF00"/>
            <rect x="125" y="145" width="50" height="80" fill="#00FF00"/>
            <circle cx="150" cy="100" r="15" fill="#0000FF"/>
            <rect x="140" y="160" width="20" height="40" fill="#FF0000"/>
            
            <!-- Trabajador 2 con EPP completo -->
            <circle cx="350" cy="170" r="25" fill="#00FF00"/>
            <rect x="325" y="195" width="50" height="80" fill="#00FF00"/>
            <circle cx="350" cy="150" r="15" fill="#0000FF"/>
            <rect x="340" y="210" width="20" height="40" fill="#FF0000"/>
            
            <text x="10" y="30" font-family="Arial" font-size="20" fill="black">✅ Escenario Seguro - EPP Completo</text>
        </svg>
        """
    elif scenario == "alerta":
        return """
        <svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
            <rect width="100%" height="100%" fill="#e0e0e0"/>
            <rect x="50" y="250" width="500" height="100" fill="#8B4513"/>
            <rect x="100" y="150" width="100" height="100" fill="#CD853F"/>
            <rect x="300" y="100" width="100" height="150" fill="#A9A9A9"/>
            
            <!-- Trabajador 1 con casco pero sin chaleco -->
            <circle cx="150" cy="120" r="25" fill="#00FF00"/>
            <rect x="125" y="145" width="50" height="80" fill="#00FF00"/>
            <circle cx="150" cy="100" r="15" fill="#0000FF"/>
            <!-- Sin chaleco -->
            
            <!-- Trabajador 2 con chaleco pero sin casco -->
            <circle cx="350" cy="170" r="25" fill="#00FF00"/>
            <rect x="325" y="195" width="50" height="80" fill="#00FF00"/>
            <!-- Sin casco -->
            <rect x="340" y="210" width="20" height="40" fill="#FF0000"/>
            
            <text x="10" y="30" font-family="Arial" font-size="20" fill="black">⚠️ Escenario con Alertas - EPP Incompleto</text>
        </svg>
        """
    else:  # critico
        return """
        <svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
            <rect width="100%" height="100%" fill="#e0e0e0"/>
            <rect x="50" y="250" width="500" height="100" fill="#8B4513"/>
            <rect x="100" y="150" width="100" height="100" fill="#CD853F"/>
            <rect x="300" y="100" width="100" height="150" fill="#A9A9A9"/>
            
            <!-- Trabajador 1 sin EPP -->
            <circle cx="150" cy="120" r="25" fill="#00FF00"/>
            <rect x="125" y="145" width="50" height="80" fill="#00FF00"/>
            <!-- Sin casco -->
            <!-- Sin chaleco -->
            
            <!-- Trabajador 2 sin EPP -->
            <circle cx="350" cy="170" r="25" fill="#00FF00"/>
            <rect x="325" y="195" width="50" height="80" fill="#00FF00"/>
            <!-- Sin casco -->
            <!-- Sin chaleco -->
            
            <text x="10" y="30" font-family="Arial" font-size="20" fill="black">🚨 Escenario Crítico - Sin EPP</text>
        </svg>
        """

# =============================================
# FUNCIONES DE SIMULACIÓN
# =============================================
def simulate_detections(scenario_type):
    """Simular detecciones de YOLO"""
    if scenario_type == "seguro":
        return [
            {'class_name': 'person', 'confidence': 0.95, 'bbox': [100, 100, 180, 250]},
            {'class_name': 'helmet', 'confidence': 0.92, 'bbox': [110, 90, 140, 120]},
            {'class_name': 'safety_vest', 'confidence': 0.89, 'bbox': [100, 120, 180, 170]},
            {'class_name': 'person', 'confidence': 0.88, 'bbox': [300, 150, 380, 300]},
            {'class_name': 'helmet', 'confidence': 0.91, 'bbox': [310, 140, 340, 170]},
            {'class_name': 'safety_vest', 'confidence': 0.87, 'bbox': [300, 170, 380, 220]}
        ]
    elif scenario_type == "alerta":
        return [
            {'class_name': 'person', 'confidence': 0.95, 'bbox': [100, 100, 180, 250]},
            {'class_name': 'helmet', 'confidence': 0.92, 'bbox': [110, 90, 140, 120]},
            # Falta chaleco para primera persona
            {'class_name': 'person', 'confidence': 0.88, 'bbox': [300, 150, 380, 300]},
            {'class_name': 'safety_vest', 'confidence': 0.87, 'bbox': [300, 170, 380, 220]}
            # Falta casco para segunda persona
        ]
    else:  # critico
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
alert_system = st.sidebar.checkbox("Sistema de Alertas Activo", True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.header("🎯 Modo de Operación")
mode = st.sidebar.radio(
    "Selecciona el modo:",
    ["📊 Demo con Escenarios", "ℹ️ Solo Análisis"],
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
            "✅ Condiciones Seguras": "seguro",
            "⚠️ Alertas Parciales": "alerta", 
            "🚨 Condiciones Críticas": "critico"
        }
        
        selected_scenario = scenario_map[scenario]
        
        if st.button("🚀 Ejecutar Análisis de Seguridad", use_container_width=True):
            with st.spinner("🔍 Analizando condiciones de seguridad..."):
                # Simular detecciones
                detections = simulate_detections(selected_scenario)
                analysis = expert_system.analyze_detections(detections)
                time.sleep(1)
            
            st.success("✅ Análisis completado")
            
            # Mostrar imagen del escenario
            svg_image = get_base64_image(selected_scenario)
            st.markdown(f'<div class="scenario-image">{svg_image}</div>', unsafe_allow_html=True)
            
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
            st.info("👆 **Presiona el botón para ejecutar el análisis**")
            
    else:
        # Modo solo análisis
        st.info("🔍 **Análisis directo de condiciones**")
        
        # Inputs manuales para simular
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            workers = st.number_input("👥 Trabajadores detectados", 0, 10, 2)
        with col_b:
            helmets = st.number_input("🪖 Cascos detectados", 0, 10, 2)
        with col_c:
            vests = st.number_input("🦺 Chalecos detectados", 0, 10, 2)
        
        if st.button("📊 Analizar Condiciones", use_container_width=True):
            # Crear detecciones simuladas
            simulated_detections = []
            for i in range(workers):
                simulated_detections.append({'class_name': 'person', 'confidence': 0.9, 'bbox': [0,0,0,0]})
            for i in range(helmets):
                simulated_detections.append({'class_name': 'helmet', 'confidence': 0.9, 'bbox': [0,0,0,0]})
            for i in range(vests):
                simulated_detections.append({'class_name': 'safety_vest', 'confidence': 0.9, 'bbox': [0,0,0,0]})
            
            analysis = expert_system.analyze_detections(simulated_detections)
            
            # Mostrar resultados
            alert_level = analysis['alert_level']
            if alert_level == "ALTA":
                st.error(f"🚨 {analysis['alert_message']}")
                st.warning(f"📋 **Acción:** {analysis['recommended_action']}")
            elif alert_level == "MEDIA":
                st.warning(f"⚠️ {analysis['alert_message']}")
                st.info(f"📋 **Acción:** {analysis['recommended_action']}")
            else:
                st.success(f"✅ {analysis['alert_message']}")
                st.info(f"📋 **Acción:** {analysis['recommended_action']}")

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
        st.info("👀 No hay trabajadores")
    
    # Historial simplificado
    st.subheader("📋 Actividad Reciente")
    st.write("• Análisis actual: " + analysis.get('alert_level', 'N/A') if 'analysis' in locals() else "N/A")
    st.write("• Inspección Zona B: MEDIA")
    st.write("• Revisión matutina: OK")

# =============================================
# SECCIÓN DE ESTADÍSTICAS
# =============================================
st.markdown("---")
st.subheader("📈 Estadísticas del Sistema")

col3, col4, col5, col6 = st.columns(4)
with col3:
    st.metric("Inspecciones Hoy", "24")
with col4:
    st.metric("Alertas Totales", "8")
with col5:
    st.metric("Cumplimiento", "83%")
with col6:
    st.metric("Respuesta Promedio", "2.1 min")

# =============================================
# INFORMACIÓN DEL SISTEMA
# =============================================
st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.subheader("ℹ️ Información del Sistema")
st.sidebar.info("""
**SafeBuild v1.0**  

🚧 **Sistema Integrado de:**  
• Sistema Experto de Reglas  
• Análisis de Seguridad Automático  
• Alertas Inteligentes  

🎓 **Para TP Integrador IA:**  
• Sistemas Expertos  
• Automatización Inteligente  
• Aplicación Práctica
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
    <p style="font-size: 0.8rem;">Integra: Sistemas Expertos + Automatización Inteligente</p>
</div>
""", unsafe_allow_html=True)
