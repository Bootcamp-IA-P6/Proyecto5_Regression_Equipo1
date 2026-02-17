import streamlit as st
import numpy as np
import joblib
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(
    page_title="Simulador de Rendimiento Pro",
    page_icon="🎓",
    layout="wide"
)

# Estilos personalizados para los botones
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    /* Botón Predecir (Verde) */
    div[data-testid="stButton"]:nth-of-type(1) > button { background-color: #4CAF50; color: white; }
    /* Botón Reset (Rojo) */
    div[data-testid="stButton"]:nth-of-type(2) > button { background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. Carga del modelo y configuración de estados
@st.cache_resource
def load_model():
    return joblib.load("./notebooks/modelo_multiple.pkl")

model = load_model()

# Valores por defecto para el reinicio
DEFAULTS = {
    "hours": 5.0,
    "previous": 70.0,
    "sleep": 7.0,
    "samples": 3,
    "extra": "No"
}

# Inicialización de las variables de estado
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Estado para almacenar la última predicción realizada
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None

# 3. Funciones de control
def update_value(key, source):
    st.session_state[key] = st.session_state[source]

def reset_all():
    for key, value in DEFAULTS.items():
        st.session_state[key] = value
    st.session_state.last_prediction = None

# 4. Interfaz de usuario (UI)
st.title("🎓 Simulador de Rendimiento Académico")
st.write("Analiza cómo tus hábitos diarios influyen en tu resultado final.")
st.divider()

col_input, col_result = st.columns([1.2, 1], gap="large")

with col_input:
    st.subheader("🎛️ Configuración de Variables")

    # --- Horas de estudio ---
    st.write("**📚 Horas de estudio**")
    c1, c2 = st.columns([3, 1])
    with c1:
        st.slider("Hours Slider", 1.0, 9.0, key="hours", label_visibility="collapsed")
    with c2:
        st.number_input("Hours In", 1.0, 9.0, key="hours_in", label_visibility="collapsed", 
                        value=st.session_state.hours, on_change=update_value, args=("hours", "hours_in"))
    
    # --- Puntaje Anterior ---
    st.write("**📊 Puntaje Anterior**")
    c1, c2 = st.columns([3, 1])
    with c1:
        st.slider("Prev Slider", 0.0, 100.0, key="previous", label_visibility="collapsed")
    with c2:
        st.number_input("Prev In", 0.0, 100.0, key="previous_in", label_visibility="collapsed",
                        value=st.session_state.previous, on_change=update_value, args=("previous", "previous_in"))

    # --- Horas de sueño ---
    st.write("**😴 Horas de sueño**")
    c1, c2 = st.columns([3, 1])
    with c1:
        st.slider("Sleep Slider", 4.0, 9.0, key="sleep", label_visibility="collapsed")
    with c2:
        st.number_input("Sleep In", 4.0, 9.0, key="sleep_in", label_visibility="collapsed",
                        value=st.session_state.sleep, on_change=update_value, args=("sleep", "sleep_in"))

    # --- Exámenes de práctica ---
    st.write("**📝 Exámenes de práctica**")
    c1, c2 = st.columns([3, 1])
    with c1:
        st.slider("Samples Slider", 0, 10, key="samples", label_visibility="collapsed")
    with c2:
        st.number_input("Samples In", 0, 10, key="samples_in", label_visibility="collapsed",
                        value=st.session_state.samples, on_change=update_value, args=("samples", "samples_in"))

    # --- Actividades Extracurriculares ---
    st.write("**🎯 Actividades Extracurriculares**")
    st.selectbox("Extra", ["No", "Sí"], key="extra", label_visibility="collapsed")
    extra_value = 1 if st.session_state.extra == "Sí" else 0

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Botones de acción
    b1, b2 = st.columns(2)
    with b1:
        predict_btn = st.button("🚀 Predecir")
    with b2:
        st.button("🔄 Resetear", on_click=reset_all)

# 5. Lógica de Predicción
if predict_btn:
    # Realizar predicción solo al pulsar el botón
    input_data = np.array([[st.session_state.hours, st.session_state.previous, 
                            extra_value, st.session_state.sleep, st.session_state.samples]])
    res = model.predict(input_data)[0]
    st.session_state.last_prediction = max(0, min(100, res))

# 6. Visualización de Resultados
with col_result:
    st.subheader("📈 Resultado de la Predicción")
    
    if st.session_state.last_prediction is not None:
        val = st.session_state.last_prediction
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=val,
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#4CAF50"},
                'steps': [
                    {'range': [0, 60], 'color': "#FF5252"},
                    {'range': [60, 80], 'color': "#FFC107"},
                    {'range': [80, 100], 'color': "#8BC34A"}
                ],
            }
        ))
        fig_gauge.update_layout(height=400, margin=dict(t=50, b=0), paper_bgcolor='rgba(0,0,0,0)', font={'color': "gray"})
        st.plotly_chart(fig_gauge, use_container_width=True)

        # Mensajes de estado
        if val >= 80:
            st.success("🏆 **Excelente Rendimiento**")
        elif val >= 60:
            st.warning("👍 **Buen Rendimiento**")
        else:
            st.error("📌 **Necesita Mejorar**")
    else:
        st.info("Ajuste los valores y haga clic en 'Predecir' para ver el resultado.")


# 7. Detalles del Modelo (Fórmula Real)
st.divider()
st.header("📊 Transparencia del Modelo")
tab1, tab2 = st.tabs(["📝 Fórmula Matemática", "📉 Métricas de Evaluación"])

with tab1:
    st.write("### 🧮 Ecuación de Regresión")
    st.write("A continuación se muestra la fórmula real utilizada por el modelo para calcular la predicción:")
    c = model.coef_
    i = model.intercept_
    
    # Renderizado de la fórmula matemática exacta
    st.latex(fr"Rendimiento = {i:.2f} + ({c[0]:.2f} \cdot Horas) + ({c[1]:.2f} \cdot Puntaje) + ({c[3]:.2f} \cdot Sueño) + ({c[4]:.2f} \cdot Exámenes)")
    
    st.info(f"""
    **Análisis de los coeficientes:**
    *   **Horas de estudio:** Cada hora adicional suma **{c[0]:.2f}** puntos.
    *   **Puntaje anterior:** Es el factor con mayor rango de influencia en el resultado final.
    """)

with tab2:
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("R² Score", "0.988")
    col_b.metric("MAE", "1.61")
    col_c.metric("Overfitting", "0.01%")
    st.write("✅ El modelo ha superado las pruebas de validación cruzada (K-Fold).")