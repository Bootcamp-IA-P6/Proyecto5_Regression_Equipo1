import streamlit as st
import joblib
import pandas as pd
import os

# 1. Configuración de página
st.set_page_config(page_title="Predicción Académica", layout="wide")

# 2. Selector de Modelo en el Sidebar
with st.sidebar:
    st.title("Settings")
    tipo_modelo = st.radio(
        "Elige el modelo:",
        ["Completo (5 variables)", "Básico (2 variables)"]
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
st.title("🎓 Predictor de Rendimiento Académico")
st.write(f"Utilizando: **{tipo_modelo}**")

if predict_btn:
    if model:
        # Creamos el DataFrame con los nombres de columnas exactos que espera el modelo
        df_input = pd.DataFrame([datos_para_df], columns=columnas_modelo)
        
        try:
            prediction = model.predict(df_input)[0]
            
            # Estilo visual magenta/oscuro para el resultado
            st.markdown(f"""
                <div style="background-color: #241B35; padding: 30px; border-radius: 15px; border: 2px solid #E800FF; text-align: center;">
                    <h2 style="color: #FAFAFA; margin-bottom: 0;">Performance Index Estimado</h2>
                    <h1 style="color: #E800FF; font-size: 70px; margin-top: 10px;">{prediction:.2f}</h1>
                </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error en la predicción: {e}")
            st.info("Asegúrate de que el modelo esté entrenado con el mismo orden de columnas.")
    else:
        st.error("No se pudo cargar el archivo del modelo. Verifica la carpeta 'notebooks'.")
else:
    st.info("👈 Ajusta los valores en el panel izquierdo y pulsa el botón para ver el resultado.")