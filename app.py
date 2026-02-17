import streamlit as st
from streamlit_lottie import st_lottie
import json
import joblib
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuración de página
st.set_page_config(page_title="Predicción Académica", layout="wide")

st.markdown("""
    <style>
    /* Importar fuente moderna */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* ====== FONDO PRINCIPAL CON GRADIENTE PÚRPURA ====== */
    .main {
        background: linear-gradient(135deg, #5a67d8 0%, #764ba2 50%, #4a5568 100%) !important;
        font-family: 'Poppins', sans-serif;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #5a67d8 0%, #764ba2 50%, #4a5568 100%) !important;
    }
    
    .block-container {
        background: transparent !important;
        padding-top: 2rem;
    }
    
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* ====== SIDEBAR ====== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%) !important;
        border-right: 2px solid rgba(232, 0, 255, 0.3);
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: white !important;
        font-family: 'Poppins', sans-serif;
        font-size: 1.5em;
    }
    
    /* ====== OCULTAR BLOQUES VACÍOS - SOLUCIÓN DEFINITIVA ====== */
    div[data-testid="stVerticalBlock"] > div:empty {
        display: none !important;
    }
    
    /* Solo mostrar bordes en elementos con contenido */
    div[data-testid="stVerticalBlock"] > div:not(:empty) {
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px;
        padding: 25px;
        margin: 10px 0;
        border: 2px solid rgba(232, 0, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Ocultar elementos que solo tienen espacios en blanco */
    div[data-testid="stVerticalBlock"] > div:not(:has(*)):not(:has(img)):not(:has(svg)) {
        display: none !important;
    }
    
    /* ====== BOTONES ====== */
    .stButton>button {
        background: linear-gradient(90deg, #E800FF 0%, #FF00B8 100%) !important;
        color: white !important;
        font-weight: 600;
        border: 2px solid rgba(255, 255, 255, 0.3);
        padding: 12px 30px;
        border-radius: 25px;
        font-size: 1.1em;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(232, 0, 255, 0.4);
        font-family: 'Poppins', sans-serif;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(232, 0, 255, 0.6);
        border-color: rgba(255, 255, 255, 0.5);
    }
    
    /* ====== TÍTULOS ====== */
    h1, h2, h3 {
        color: #FAFAFA !important;
        font-family: 'Poppins', sans-serif;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
    }
    
    h1 {
        background: linear-gradient(90deg, #E800FF, #FF00B8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: none;
        filter: drop-shadow(2px 2px 4px rgba(232, 0, 255, 0.5));
    }
    
    /* ====== INPUTS EN SIDEBAR ====== */
    [data-testid="stSidebar"] .stNumberInput input,
    [data-testid="stSidebar"] .stSlider,
    [data-testid="stSidebar"] .stSelectbox select {
        background: rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    [data-testid="stSidebar"] .stNumberInput input {
        font-size: 1.1em;
        font-weight: 600;
    }
    
    /* ====== RADIO BUTTONS ====== */
    [data-testid="stSidebar"] .stRadio > label {
        color: white !important;
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
        background: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        color: white !important;
    }
    
    /* ====== SELECTBOX ====== */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px;
    }
    
    /* ====== SLIDER ====== */
    [data-testid="stSidebar"] .stSlider > div > div {
        background: rgba(255, 255, 255, 0.2);
    }
    
    /* ====== DIVIDER ====== */
    hr {
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, #E800FF, transparent);
        margin: 30px 0;
        box-shadow: 0 0 10px rgba(232, 0, 255, 0.5);
    }
    
    /* ====== GRÁFICOS ====== */
    .plotly-graph-div {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px;
        padding: 15px;
        border: 2px solid rgba(232, 0, 255, 0.3);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* ====== COLUMNAS ====== */
    div[data-testid="column"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 15px;
        border: 2px solid rgba(232, 0, 255, 0.2);
        margin: 5px;
    }
    
    /* ====== MÉTRICAS ====== */
    [data-testid="stMetricValue"] {
        font-size: 2.5em;
        color: #E800FF !important;
        font-family: 'Poppins', sans-serif;
        text-shadow: 0 0 20px rgba(232, 0, 255, 0.5);
    }
    
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.08);
        border: 2px solid rgba(232, 0, 255, 0.3);
        border-radius: 15px;
        padding: 15px;
    }
    
    /* ====== ALERTS ====== */
    .stAlert {
        background: rgba(102, 126, 234, 0.2) !important;
        border: 2px solid rgba(232, 0, 255, 0.4);
        border-radius: 15px;
        color: white !important;
        backdrop-filter: blur(10px);
    }
    
    /* ====== SPINNER ====== */
    .stSpinner > div {
        border-top-color: #E800FF !important;
    }
    
    /* ====== TEXTOS ====== */
    p, span, label, div {
        color: #FAFAFA;
    }
    
    .stMarkdown {
        color: #FAFAFA;
    }
    
    /* ====== TARJETAS PERSONALIZADAS ====== */
    div[style*="background-color: #241B35"],
    div[style*="border: 2px solid #E800FF"] {
        border: 3px solid #E800FF !important;
        box-shadow: 0 0 30px rgba(232, 0, 255, 0.4);
    }
    
    </style>
""", unsafe_allow_html=True)

# Función para cargar el Lottie local
def load_lottiefile(filepath: str):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return None

lottie_robot = load_lottiefile("assets/niu.json")

# 2. Selector de Modelo en el Sidebar
with st.sidebar:
    st.markdown(
        "<h2 style='text-align: center; font-size: 40px;'>OPCIONES</h2>",
        unsafe_allow_html=True
    )
    tipo_modelo = st.radio(
        "Elige el modelo:",
        ["Completo", "Básico"]
    )
    st.markdown("---")

# 3. Carga de Modelos y Configuración de Columnas
@st.cache_resource
def load_selected_model(name):
    path = os.path.join("notebooks", name)
    if os.path.exists(path):
        return joblib.load(path)
    return None

# Corregimos la comparación para que coincida con el st.radio
if tipo_modelo == "Completo":
    model = load_selected_model("modelo_multiple.pkl")
    columnas_modelo = ['Hours Studied', 'Previous Scores', 'Extracurricular Activities', 'Sleep Hours', 'Sample Question Papers Practiced']
else:
    model = load_selected_model("modelo_notas.pkl")
    columnas_modelo = ['Hours Studied', 'Previous Scores']

# 4. Inputs dinámicos en el Sidebar
with st.sidebar:
    st.subheader("Datos del Estudiante")
    horas_estudio = st.number_input("📚 Horas de estudio", 0, 24, 5)
    promedio_anterior = st.slider("📊 Promedio anterior", 0, 100, 70)
    
    # Aquí es donde se activan las variables extra
    if tipo_modelo == "Completo":
        extracurriculares = st.selectbox("🎯 Actividades Extracurriculares", ["No", "Sí"])
        horas_sueno = st.number_input("😴 Horas de sueño", 0, 24, 7)
        examenes_practica = st.number_input("📝 Exámenes realizados", 0, 50, 2)
        
        extra_val = 1 if extracurriculares == "Sí" else 0
        datos_para_df = [horas_estudio, promedio_anterior, extra_val, horas_sueno, examenes_practica]
    else:
        datos_para_df = [horas_estudio, promedio_anterior]

    st.markdown("---")
    predict_btn = st.button("🔘 Predecir rendimiento", use_container_width=True)

# 5. Títulos Principales
# 5. Títulos Principales
st.markdown(f"""
    <h1 style="text-align: center; font-size: 3.5rem; color: #FAFAFA; margin-bottom: 5px;">
        🎓 Predictor de Rendimiento Académico
    </h1>
""", unsafe_allow_html=True)

st.markdown(f"""
    <h3 style="text-align: center; font-size: 1.8rem; color: #E800FF; margin-top: 0; font-weight: 300;">
        <strong>MODELO SELECCIONADO: {tipo_modelo.upper()}</strong>
    </h3>
""", unsafe_allow_html=True)
# ← QUITÉ el <br> de aquí

main_placeholder = st.empty()

if not predict_btn:
    with main_placeholder.container():
        if lottie_robot:
            st_lottie(lottie_robot, height=500, key="robot_inicio")
        else:
            st.info("🤖 Configura los datos a la izquierda y pulsa el botón.")

else:
    main_placeholder.empty()
    
    if model:
        
        df_input = pd.DataFrame([datos_para_df], columns=columnas_modelo)
        
        try:
            with st.spinner('⌛ Analizando datos...'):
                prediction = model.predict(df_input)[0]

            # Resultado Principal
            st.markdown(f"""
                <div style="background-color: #241B35; padding: 30px; border-radius: 15px; border: 2px solid #E800FF; text-align: center; margin-bottom: 25px;">
                    <h2 style="color: #FAFAFA; margin-bottom: 0;">Performance Index Estimado</h2>
                    <h1 style="color: #E800FF; font-size: 80px; margin-top: 10px;">{prediction:.2f}</h1>
                </div>
            """, unsafe_allow_html=True)

            # Gráficos
            st.markdown("### 📊 Análisis del Modelo")
            col_graf1, col_graf2 = st.columns(2)

            with col_graf1:
                pesos = model.coef_
                df_pesos = pd.DataFrame({'Variable': columnas_modelo, 'Impacto': pesos}).sort_values(by='Impacto', ascending=True)
                fig_importancia = px.bar(df_pesos, x='Impacto', y='Variable', orientation='h', 
                title="Importancia de Variables", color_discrete_sequence=['#E800FF'])
                fig_importancia.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#FAFAFA")
                st.plotly_chart(fig_importancia, use_container_width=True)

            with col_graf2:
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number", value = prediction,
                    title = {'text': "Nivel de Rendimiento", 'font': {'size': 20}},
                    gauge = {'axis': {'range': [0, 100], 'tickcolor': "#FAFAFA"}, 'bar': {'color': "#E800FF"}, 'bgcolor': "#241B35"}
                ))
                fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#FAFAFA")
                st.plotly_chart(fig_gauge, use_container_width=True)

        except Exception as e:
            st.error(f"Error en la predicción: {e}")