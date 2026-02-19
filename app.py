import streamlit as st
from streamlit_lottie import st_lottie
import json
import joblib
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime


#  CONFIGURACIÓN DE PÁGINA

st.set_page_config(
    page_title="Academic Performance Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)
# CSS GLOBAL
st.markdown("""
<style>
/* ── Fuentes ──────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── Variables CSS ────────────────────────────────────────── */
:root {
    --navy:       #0F172A;
    --slate:      #1E293B;
    --slate-md:   #334155;
    --slate-lt:   #475569;
    --gold:       #F59E0B;
    --gold-light: #FCD34D;
    --gold-dim:   rgba(245, 158, 11, 0.15);
    --gold-glow:  rgba(245, 158, 11, 0.35);
    --text:       #E2E8F0;
    --text-dim:   #94A3B8;
    --glass:      rgba(30, 41, 59, 0.7);
    --glass-border: rgba(245, 158, 11, 0.2);
    --radius:     16px;
    --radius-sm:  10px;
}

/* ── Reset y fondo principal ──────────────────────────────── */
html, body, [data-testid="stAppViewContainer"], .main {
    background: var(--navy) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text) !important;
}

/* Sutil patrón de puntos en el fondo */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: radial-gradient(circle, rgba(245,158,11,0.06) 1px, transparent 1px);
    background-size: 32px 32px;
    pointer-events: none;
    z-index: 0;
}

.block-container {
    background: transparent !important;
    padding-top: 2rem;
    padding-bottom: 3rem;
    position: relative;
    z-index: 1;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

/* ── SIDEBAR ──────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%) !important;
    border-right: 1px solid var(--glass-border) !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

/* Logo / título sidebar */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--gold) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.1rem !important;
}

/* Sección separadora sidebar */
[data-testid="stSidebar"] hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, var(--gold), transparent) !important;
    margin: 1.5rem 0 !important;
    opacity: 0.5;
}

/* ── WIDGETS EN SIDEBAR ──────────────────────────────────── */
/* Radio buttons */
[data-testid="stSidebar"] .stRadio > label {
    color: var(--text-dim) !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    background: var(--glass) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-sm) !important;
    padding: 8px !important;
    gap: 4px !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    color: var(--text) !important;
    font-size: 0.95rem !important;
    text-transform: none !important;
    letter-spacing: normal !important;
    font-weight: 400 !important;
    padding: 6px 10px !important;
    border-radius: 6px !important;
    transition: background 0.2s !important;
}

/* Number inputs */
[data-testid="stSidebar"] .stNumberInput input {
    background: var(--slate) !important;
    border: 1px solid var(--slate-md) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    transition: border-color 0.2s !important;
}

[data-testid="stSidebar"] .stNumberInput input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px var(--gold-dim) !important;
}

/* Slider */
[data-testid="stSidebar"] .stSlider > div > div > div {
    background: var(--gold) !important;
}

/* Selectbox */
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: var(--slate) !important;
    border: 1px solid var(--slate-md) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-size: 0.82rem !important;
}

/* Labels generales de inputs */
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stSelectbox label {
    color: var(--text-dim) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    margin-bottom: 4px !important;
}

/* ── BOTÓN PRINCIPAL ──────────────────────────────────────── */
.stButton > button {
    background: var(--gold) !important;
    color: var(--navy) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 12px 24px !important;
    width: 100% !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px var(--gold-glow) !important;
    cursor: pointer !important;
}
.stButton > button p {
    font-size: 1.5rem !important;
}

.stButton > button:hover {
    background: var(--gold-light) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px var(--gold-glow) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── TÍTULOS PRINCIPALES ──────────────────────────────────── */
h1, h2, h3 {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    color: var(--text) !important;
}

/* ── TARJETAS GLASSMORPHISM (contenedores generales) ──────── */
# div[data-testid="stVerticalBlock"] > div {
#     background: transparent !important;
#     border: none !important;
#     box-shadow: none !important;
#     backdrop-filter: none !important;
#     padding: 0 !important;
#     margin: 0 !important;
#     border-radius: 0 !important;
# }

/* ── COLUMNAS ─────────────────────────────────────────────── */
div[data-testid="column"] {
    background: var(--glass) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius) !important;
    padding: 24px !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    transition: border-color 0.3s !important;
}

div[data-testid="column"]:hover {
    border-color: rgba(245, 158, 11, 0.4) !important;
}

/* ── MÉTRICAS ─────────────────────────────────────────────── */
[data-testid="stMetricValue"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 2rem !important;
    font-weight: 600 !important;
    color: var(--gold) !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-dim) !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    font-weight: 500 !important;
}

div[data-testid="stMetric"] {
    background: var(--glass) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius) !important;
    padding: 20px !important;
}

/* ── DIVIDER ──────────────────────────────────────────────── */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, var(--gold), transparent) !important;
    margin: 2rem 0 !important;
    opacity: 0.4 !important;
}

/* ── ALERTS ───────────────────────────────────────────────── */
.stAlert {
    background: rgba(245, 158, 11, 0.08) !important;
    border: 1px solid rgba(245, 158, 11, 0.25) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
}

/* ── SPINNER ──────────────────────────────────────────────── */
.stSpinner > div {
    border-top-color: var(--gold) !important;
}

/* ── SCROLLBAR CUSTOM ─────────────────────────────────────── */
::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-track { background: var(--navy); }
::-webkit-scrollbar-thumb { background: var(--slate-md); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold); }

  /* ── RADIO TIPO TOGGLE ────────────────────────────────────── */
[data-testid="stSidebar"] div[role="radiogroup"] {
    display: flex !important;
    flex-direction: row !important;
    background: var(--navy) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-sm) !important;
    padding: 4px !important;
    gap: 0 !important;
    width: 100% !important;
    box-sizing: border-box !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label {
    flex: 1 1 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: 8px !important;
    padding: 8px 4px !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    color: var(--text-dim) !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    white-space: nowrap !important;
    min-width: 0 !important;
}

/* Ocultar el círculo del radio en TODAS las opciones */
[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child,
[data-testid="stSidebar"] div[role="radiogroup"] label > span:first-child,
[data-testid="stSidebar"] div[role="radiogroup"] input[type="radio"] {
    display: none !important;
}

/* Opción seleccionada */
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: var(--gold) !important;
    color: var(--navy) !important;
    font-weight: 700 !important;
}
            
/* ── Ocultar botón colapsar sidebar ──────────────────────── */
[data-testid="collapsedControl"],
button[kind="header"],
[data-testid="stSidebarCollapseButton"] {
    display: none !important;
    visibility: hidden !important;
}

</style>
""", unsafe_allow_html=True)


# FUNCION PARA CARGAR MI GIT
def load_lottiefile(filepath: str):
    """Carga una animación Lottie desde un archivo JSON local."""
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return None
# FUNCION PARA CARGAR LOS MODELOS
@st.cache_resource
def load_selected_model(name):
    path = os.path.join("notebooks", name)
    if os.path.exists(path):
        return joblib.load(path)
    return None

# History

if "history" not in st.session_state:
    st.session_state.history = []
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None

# SIDEBAR — Logo + Selector de modelo + Inputs
with st.sidebar:

    # Logo 
    st.markdown("""
        <div style="text-align:center; padding: 8px 0 24px 0;">
            <div style="font-size:5.8rem; line-height:1;">🎓</div>
            <div style="
                font-family:'DM Sans',sans-serif;
                font-weight:700;
                font-size:2.15rem;
                color:#F59E0B;
                letter-spacing:-0.01em;
                margin-top:8px;
            ">Academic Predictor</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Selector de modelO
    st.markdown("""
        <div style="font-size:1.4rem;color:#64748B;text-transform:uppercase;
                    letter-spacing:0.1em;font-weight:600;margin-bottom:8px;">
            Modelo de predicción
        </div>
    """, unsafe_allow_html=True)

    tipo_modelo = st.radio(
        label="Modelo",
        options=["Completo", "Básico"],
        label_visibility="collapsed",
        horizontal= True,
        )

    st.markdown("---")

    # ── Inputs del estudiante 
    st.markdown("""
        <div style="font-size:1.4rem;color:#64748B;text-transform:uppercase;
                    letter-spacing:0.1em;font-weight:600;margin-bottom:16px;">
            Datos del estudiante
        </div>
    """, unsafe_allow_html=True)

    horas_estudio = st.slider("📚 Horas de estudio", 0, 24, 5)
    promedio_anterior = st.slider("📊 Promedio anterior", 0, 100, 70)

    if tipo_modelo == "Completo":
        
        horas_sueno      = st.slider("😴 Horas de sueño", 0, 24, 7)
        examenes_practica = st.slider("📝 Exámenes de práctica", 0, 50, 2)
        extracurriculares = st.selectbox("🎯 Actividades extracurriculares", ["No", "Sí"])
        extra_val        = 1 if extracurriculares == "Sí" else 0
        datos_para_df    = [horas_estudio, promedio_anterior, extra_val, horas_sueno, examenes_practica]
    else:
        datos_para_df = [horas_estudio, promedio_anterior]

    st.markdown("---")

    # ── Botón de predicción 
    predict_btn = st.button("⚡ Predecir rendimiento", width='stretch')
    save_btn    = st.button("💾 Guardar predicción",   width='stretch')

    # ── Info modelo activo 
    st.markdown(f"""
        <div style="
            margin-top:16px;
            background:rgba(245,158,11,0.08);
            border:1px solid rgba(245,158,11,0.2);
            border-radius:10px;
            padding:10px 14px;
            font-size:1.1rem;
            color:#94A3B8;
            text-align:center;
        ">
            Modelo activo<br>
            <span style="color:#F59E0B;font-weight:600;font-size:0.98rem;">
                {'✦ Completo' if tipo_modelo == 'Completo' else '◈ Básico'}
            </span>
        </div>
    """, unsafe_allow_html=True)

#  CARGA DE MODELO
if tipo_modelo == "Completo":
    model= load_selected_model("modelo_multiple.pkl")
    columnas_modelo = ['Hours Studied', 'Previous Scores', 'Extracurricular Activities','Sleep Hours', 'Sample Question Papers Practiced']
else:
    model= load_selected_model("modelo_notas.pkl")
    columnas_modelo = ['Hours Studied', 'Previous Scores']

#  ZONA PRINCIPAL — Header
# Llamamos a mi git
lottie_robot= load_lottiefile("assets/niu.json")

# Badge del modelo activo
badge_color = "#F59E0B" if tipo_modelo == "Completo" else "#38BDF8"
badge_label = "Modelo Completo" if tipo_modelo == "Completo" else "Modelo Básico"

st.markdown(f"""
<div style="text-align:center; padding: 10px 0 30px 0;">
        <div style="display:inline-block; margin-bottom:14px;">
            <span style="
                background: rgba(245,158,11,0.12);
                border: 1px solid rgba(245,158,11,0.35);
                color: {badge_color};
                font-size:1rem;
                font-weight:600;
                letter-spacing:0.1em;
                text-transform:uppercase;
                padding:5px 14px;
                border-radius:20px;
            ">{badge_label}</span>
</div>
        <h1 style="
            font-family:'DM Sans',sans-serif;
            font-weight:700;
            font-size:clamp(2.5rem, 4vw, 3.7rem);
            color:#E2E8F0;
            letter-spacing:-0.03em;
            margin:0 0 8px 0;
            line-height:1.1;
        ">Predictor de Rendimiento<br>
            <span style="color:#F59E0B;">Académico</span>
        </h1>
        <p style="
            color:#64748B;
            font-size:1.3rem;
            font-weight:400;
            margin:0;
            max-width:520px;
            margin-inline:auto;
        ">
            Introduce los datos del estudiante en el panel izquierdo<br>y pulsa <strong style="color:#F59E0B;">Predecir</strong> para obtener el índice estimado.
        </p>
</div>
""", unsafe_allow_html=True)

# CONTENIDO CENTRAL

main_placeholder = st.empty()
# ── Controlar vista con session_state ─────────────────────
if predict_btn and model:
    df_input = pd.DataFrame([datos_para_df], columns=columnas_modelo)
    try:
        prediction = model.predict(df_input)[0]
        nivel = "Alto" if prediction >= 70 else ("Medio" if prediction >= 45 else "Bajo")
        nivel_color  = "#22C55E" if prediction >= 70 else ("#F59E0B" if prediction >= 45 else "#EF4444")
        nivel_bg     = "rgba(34,197,94,0.1)"  if prediction >= 70 else ("rgba(245,158,11,0.1)" if prediction >= 45 else "rgba(239,68,68,0.1)")
        nivel_border = "rgba(34,197,94,0.3)"  if prediction >= 70 else ("rgba(245,158,11,0.3)" if prediction >= 45 else "rgba(239,68,68,0.3)")

        st.session_state.last_prediction = {
            "score": round(float(prediction), 1),
            "modelo": tipo_modelo,
            "horas": horas_estudio,
            "prev": promedio_anterior,
            "nivel": nivel,
            "nivel_color": nivel_color,
            "nivel_bg": nivel_bg,
            "nivel_border": nivel_border,
            "datos_para_df": datos_para_df,
            "columnas_modelo": columnas_modelo,
            "coef": model.coef_.tolist(),
            "intercept": float(model.intercept_),
        }
    except Exception as e:
        st.error(f"⚠️ Error en la predicción: {e}")

# ── Guardar en historial ───────────────────────────────────
if save_btn and st.session_state.last_prediction:
    lp = st.session_state.last_prediction
    st.session_state.history.insert(0, {
        "score":  lp["score"],
        "modelo": lp["modelo"],
        "horas":  lp["horas"],
        "prev":   lp["prev"],
        "nivel":  lp["nivel"],
        "time":   datetime.now().strftime("%H:%M:%S")
    })
    st.session_state.history = st.session_state.history[:8]

# ── Mostrar resultados o lottie ────────────────────────────
if st.session_state.last_prediction:
    lp           = st.session_state.last_prediction
    prediction   = lp["score"]
    nivel        = lp["nivel"]
    nivel_color  = lp["nivel_color"]
    nivel_bg     = lp["nivel_bg"]
    nivel_border = lp["nivel_border"]
    c            = lp["coef"]
    i            = lp["intercept"]

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid rgba(245,158,11,0.3); border-radius: 20px;
        padding: 36px 40px; text-align: center; margin-bottom: 28px;
        position: relative; overflow: hidden;">
        <div style="position:absolute;top:-50px;left:50%;transform:translateX(-50%);
            width:300px;height:300px;
            background:radial-gradient(circle,rgba(245,158,11,0.08) 0%,transparent 70%);
            pointer-events:none;"></div>
        <div style="color:#64748B;font-size:0.78rem;text-transform:uppercase;
            letter-spacing:0.12em;font-weight:600;margin-bottom:10px;">
            Performance Index Estimado</div>
        <div style="font-family:'DM Mono',monospace;font-size:clamp(3.5rem,8vw,6rem);
            font-weight:600;color:#F59E0B;line-height:1;margin-bottom:16px;
            filter:drop-shadow(0 0 24px rgba(245,158,11,0.4));">
            {prediction}<span style="font-size:0.35em;color:#475569;">/100</span></div>
        <span style="background:{nivel_bg};border:1px solid {nivel_border};
            color:{nivel_color};font-size:0.82rem;font-weight:600;
            letter-spacing:0.08em;text-transform:uppercase;
            padding:5px 16px;border-radius:20px;">● Rendimiento {nivel}</span>
    </div>
    """, unsafe_allow_html=True)

    met1, met2, met3 = st.columns(3)
    with met1: st.metric("Horas de estudio",  f"{lp['horas']}h")
    with met2: st.metric("Promedio anterior",  f"{lp['prev']}/100")
    with met3: st.metric("Score estimado",     f"{prediction:.0f} pts")

    st.markdown("<br>", unsafe_allow_html=True)

    col_g1, col_g2 = st.columns(2, gap="medium")
    DARK_BG = "rgba(0,0,0,0)"; GRID_COLOR = "rgba(255,255,255,0.05)"
    FONT_COLOR = "#94A3B8";    GOLD = "#F59E0B"

    with col_g1:
        st.markdown('<div style="font-size:0.78rem;color:#64748B;text-transform:uppercase;letter-spacing:0.1em;font-weight:600;margin-bottom:12px;">Importancia de variables</div>', unsafe_allow_html=True)
        df_pesos = pd.DataFrame({'Variable': lp["columnas_modelo"], 'Impacto': c}).sort_values('Impacto', ascending=True)
        colors_bar = [GOLD if v >= 0 else "#EF4444" for v in df_pesos['Impacto']]
        fig_bar = go.Figure(go.Bar(x=df_pesos['Impacto'], y=df_pesos['Variable'], orientation='h', marker_color=colors_bar, marker_line_width=0))
        fig_bar.update_layout(paper_bgcolor=DARK_BG, plot_bgcolor=DARK_BG, font=dict(family="DM Sans", color=FONT_COLOR, size=12), margin=dict(l=0,r=0,t=10,b=0), height=280, xaxis=dict(gridcolor=GRID_COLOR, zeroline=True, zerolinecolor="rgba(255,255,255,0.1)"), yaxis=dict(gridcolor=GRID_COLOR))
        st.plotly_chart(fig_bar, width='stretch')

    with col_g2:
        st.markdown('<div style="font-size:0.78rem;color:#64748B;text-transform:uppercase;letter-spacing:0.1em;font-weight:600;margin-bottom:12px;">Nivel de rendimiento</div>', unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=prediction,
            number=dict(font=dict(family="DM Mono", color=GOLD, size=42)),
            gauge=dict(
                axis=dict(range=[0,100], tickcolor=FONT_COLOR, tickfont=dict(color=FONT_COLOR, size=10)),
                bar=dict(color=GOLD, thickness=0.25), bgcolor="#1E293B", bordercolor="rgba(0,0,0,0)",
                steps=[dict(range=[0,45], color="rgba(239,68,68,0.15)"), dict(range=[45,70], color="rgba(245,158,11,0.12)"), dict(range=[70,100], color="rgba(34,197,94,0.12)")],
                threshold=dict(line=dict(color=nivel_color, width=3), thickness=0.8, value=prediction)
            )
        ))
        fig_gauge.update_layout(paper_bgcolor=DARK_BG, font=dict(family="DM Sans", color=FONT_COLOR), margin=dict(l=20,r=20,t=20,b=20), height=280)
        st.plotly_chart(fig_gauge, width='stretch')

    st.write("### 🧮 Ecuación de Regresión")
    if lp["modelo"] == "Completo":

        st.latex(
                    fr"Rendimiento = {i:.2f} "
                    fr"+ ({c[0]:.2f} \cdot Horas) "
                    fr"+ ({c[1]:.2f} \cdot Puntaje) "
                    fr"+ ({c[2]:.2f} \cdot Extra) "
                    fr"+ ({c[3]:.2f} \cdot Sue\tilde{{n}}o) "
                    fr"+ ({c[4]:.2f} \cdot Ex\acute{{a}}menes)"
                )
        st.info(f"""
                **Análisis de los coeficientes:**
                * **Horas de estudio:** Cada hora adicional suma **{c[0]:.2f}** puntos.
                * **Puntaje anterior:** Es el factor con mayor rango de influencia en el resultado final.
                * **Actividades extracurriculares:** Aporta **{c[2]:.2f}** puntos.
                * **Horas de sueño:** Cada hora suma **{c[3]:.2f}** puntos.
                * **Exámenes de práctica:** Cada examen suma **{c[4]:.2f}** puntos.
                """)

    else:
        st.latex(
            fr"Rendimiento = {i:.2f} "
            fr"+ ({c[0]:.2f} \cdot Horas) "
            fr"+ ({c[1]:.2f} \cdot Puntaje)"
        )
        st.info(f"""
                **Análisis de los coeficientes:**
                * **Horas de estudio:** Cada hora adicional suma **{c[0]:.2f}** puntos.
                * **Puntaje anterior:** Es el factor con mayor rango de influencia en el resultado final.
        """)
else:
    if lottie_robot:
        st_lottie(lottie_robot, height=580, key="robot_inicio")

# ── HISTORIAL — siempre visible ────────────────────────────
if st.session_state.history:
    st.markdown("<br>", unsafe_allow_html=True)
    col_titulo, col_clear = st.columns([5, 1])
    with col_titulo:
        st.markdown("### 🕓 Historial de predicciones")
    with col_clear:
        if st.button("🗑️ Limpiar"):
            st.session_state.history = []
            st.rerun()

    for h in st.session_state.history:
        color_h = "#22C55E" if h["score"] >= 70 else ("#F59E0B" if h["score"] >= 45 else "#EF4444")
        badge_h = "✦ Completo" if h["modelo"] == "Completo" else "◈ Básico"
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
            background:rgba(30,41,59,0.7);border:1px solid rgba(245,158,11,0.2);
            border-radius:12px;padding:12px 18px;margin-bottom:8px;">
            <div style="display:flex;align-items:center;gap:14px">
                <div style="background:{color_h}22;color:{color_h};border-radius:10px;
                    padding:4px 14px;font-family:'DM Mono',monospace;font-weight:700;font-size:1.1rem;">
                    {h['score']}</div>
                <div>
                    <div style="color:#E2E8F0;font-size:0.85rem;font-weight:600">Rendimiento {h['nivel']}</div>
                    <div style="color:#64748B;font-size:0.72rem;margin-top:2px">
                        {badge_h} · {h['horas']}h estudio · Prev: {h['prev']}</div>
                </div>
            </div>
            <div style="color:#475569;font-size:0.72rem">{h['time']}</div>
        </div>
        """, unsafe_allow_html=True)

    if len(st.session_state.history) >= 2:
        scores_h = [h["score"] for h in reversed(st.session_state.history)]
        times_h  = [h["time"]  for h in reversed(st.session_state.history)]
        colors_h = ["#22C55E" if s >= 70 else ("#F59E0B" if s >= 45 else "#EF4444") for s in scores_h]
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Scatter(x=times_h, y=scores_h, fill="tozeroy", fillcolor="rgba(245,158,11,0.06)", line=dict(width=0), showlegend=False, hoverinfo="skip"))
        fig_hist.add_trace(go.Scatter(x=times_h, y=scores_h, mode="lines+markers", line=dict(color="#F59E0B", width=3, shape="spline", smoothing=1.2), marker=dict(size=10, color=colors_h, line=dict(color="#0F172A", width=2)), text=[f"{s} pts" for s in scores_h], hovertemplate="<b>%{text}</b><br>%{x}<extra></extra>", showlegend=False))
        for thr, lbl, col in [(70,"Alto","#22C55E"),(45,"Medio","#F59E0B")]:
            fig_hist.add_hline(y=thr, line_dash="dot", line_color=col, opacity=0.4, annotation_text=lbl, annotation_position="right", annotation_font=dict(color=col, size=10))
        fig_hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10,r=60,t=10,b=10), height=220, xaxis=dict(showgrid=False, tickfont=dict(color="#475569", size=10)), yaxis=dict(range=[0,105], gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#475569", size=10)))
        st.plotly_chart(fig_hist, width='stretch')