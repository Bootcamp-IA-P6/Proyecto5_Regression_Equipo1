import streamlit as st
import joblib
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuración de página
st.set_page_config(page_title="Predicción Académica", layout="wide")

# 2. Selector de Modelo en el Sidebar
with st.sidebar:
    st.title("Settings")
    tipo_modelo = st.radio(
        "Elige el modelo:",
        ["Completo", "Básico"]
    )
    st.markdown("---")

# 3. Carga de Modelos
@st.cache_resource
def load_selected_model(name):
    path = os.path.join("notebooks", name)
    if os.path.exists(path):
        return joblib.load(path)
    return None

if tipo_modelo == "Completo (5 variables)":
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
    
    # Solo mostramos estos si elegimos el modelo completo
    if tipo_modelo == "Completo (5 variables)":
        extracurriculares = st.selectbox("🎯 Actividades Extracurriculares", ["No", "Sí"])
        horas_sueno = st.number_input("😴 Horas de sueño", 0, 24, 7)
        examenes_practica = st.number_input("📝 Exámenes realizados", 0, 50, 2)
        
        # Convertimos Sí/No a 1/0 para el modelo
        extra_val = 1 if extracurriculares == "Sí" else 0
        datos_para_df = [horas_estudio, promedio_anterior, extra_val, horas_sueno, examenes_practica]
    else:
        datos_para_df = [horas_estudio, promedio_anterior]

    st.markdown("---")
    predict_btn = st.button("🔘 Predecir rendimiento", use_container_width=True)

# 5. Área Principal y Predicción
st.markdown(f"""
    <h1 style="text-align: center; font-size: 3.5rem; color: #FAFAFA; margin-bottom: 5px;">
        🎓 Predictor de Rendimiento Académico
    </h1>
""", unsafe_allow_html=True)

st.markdown(f"""
    <h3 style="text-align: center; font-size: 1.8rem; color: #E800FF; margin-top: 0; font-weight: 300;">
       <strong>MODELO: {tipo_modelo}</strong>
    </h3>
    <br>
""", unsafe_allow_html=True)

if predict_btn:
    if model:
        df_input = pd.DataFrame([datos_para_df], columns=columnas_modelo)
        
        try:
            prediction = model.predict(df_input)[0]
            
            # 1. Contenedor del Resultado Principal
            st.markdown(f"""
                <div style="background-color: #241B35; padding: 30px; border-radius: 15px; border: 2px solid #E800FF; text-align: center; margin-bottom: 25px;">
                    <h2 style="color: #FAFAFA; margin-bottom: 0; font-family: sans-serif;">Performance Index Estimado</h2>
                    <h1 style="color: #E800FF; font-size: 80px; margin-top: 10px; font-family: sans-serif;">{prediction:.2f}</h1>
                </div>
            """, unsafe_allow_html=True)

            # 2. SECCIÓN DE GRÁFICOS
            st.markdown("### 📊 Análisis del Modelo")
            col_graf1, col_graf2 = st.columns(2)

            with col_graf1:
                # Gráfico de Importancia de Variables (Extraído de tus pesos de modelo)
                pesos = model.coef_
                df_pesos = pd.DataFrame({'Variable': columnas_modelo, 'Impacto': pesos}).sort_values(by='Impacto', ascending=True)
                
                fig_importancia = px.bar(
                    df_pesos, 
                    x='Impacto', 
                    y='Variable', 
                    orientation='h',
                    title="¿Qué influye más en tu nota?",
                    color_discrete_sequence=['#E800FF'] # Color magenta
                )
                fig_importancia.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color="#FAFAFA",
                    title_font_size=20
                )
                st.plotly_chart(fig_importancia, use_container_width=True)

            with col_graf2:
                # Gráfico de Indicador (Gauge) para ver dónde cae la nota
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = prediction,
                    title = {'text': "Nivel de Rendimiento", 'font': {'size': 20}},
                    gauge = {
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#FAFAFA"},
                        'bar': {'color': "#E800FF"},
                        'bgcolor': "#241B35",
                        'borderwidth': 2,
                        'bordercolor': "#FAFAFA",
                        'steps': [
                            {'range': [0, 40], 'color': '#3b003d'},
                            {'range': [40, 70], 'color': '#6e0073'},
                            {'range': [70, 100], 'color': '#a100a8'}],
                    }
                ))
                fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#FAFAFA")
                st.plotly_chart(fig_gauge, use_container_width=True)

        except Exception as e:
            st.error(f"Error en la predicción: {e}")