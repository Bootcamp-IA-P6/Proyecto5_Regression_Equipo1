import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
import warnings
import os
from datetime import datetime

warnings.filterwarnings("ignore")

# ── Configuración ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Performance Simulator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS Pastel Soft ───────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
* { font-family: 'Nunito', sans-serif !important; }
.stApp { background: #faf7ff; }

.app-header {
    background: linear-gradient(135deg, #e8d5ff 0%, #d5e8ff 100%);
    border-radius: 24px;
    padding: 28px 36px;
    margin-bottom: 24px;
    text-align: center;
}
.app-header h1 { font-size: 2.2rem; font-weight: 900; color: #5b4e8a; margin: 0 0 6px 0; }
.app-header p  { color: #9b8fc0; font-size: 1rem; margin: 0; }

.card-title {
    font-size: 1rem; font-weight: 800; color: #5b4e8a;
    margin-bottom: 14px;
}
.score-card {
    background: linear-gradient(135deg, #e8d5ff, #d5e8ff);
    border-radius: 20px; padding: 28px; text-align: center;
}
.score-number { font-size: 5.5rem; font-weight: 900; line-height: 1; margin-bottom: 4px; }
.score-grade  { font-size: 1.2rem; font-weight: 800; margin-top: 4px; }
.score-message { font-size: 0.85rem; color: #7c6fb0; margin-top: 8px; }

.slider-label {
    font-size: 0.78rem; font-weight: 700; color: #9b8fc0;
    text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 2px;
}
.history-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 10px 14px; border-radius: 12px; margin-bottom: 8px;
    background: #f9f7ff; border: 1px solid #ede8ff;
}
.history-time { font-size: 0.7rem; color: #b0a4d4; }

.stButton > button {
    background: linear-gradient(135deg, #a78bfa, #818cf8) !important;
    color: white !important; border: none !important;
    border-radius: 16px !important; padding: 14px !important;
    font-weight: 800 !important; font-size: 1rem !important;
    width: 100% !important;
    box-shadow: 0 4px 15px rgba(167,139,250,0.4) !important;
}
            
div[data-testid="stNumberInput"] input {
    border-radius: 10px !important; border: 2px solid #e8d5ff !important;
    font-weight: 700 !important; color: #5b4e8a !important;
    background: #faf7ff !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []


# ── Modelo ────────────────────────────────────────────────────────────────────

MODELS = {
    "Linear Regression": {
        "path": "notebooks/modelo_performance.pkl",
        "r2": 0.9890, "mae": 1.61
    },
    "Random Forest": {
        "path": "notebooks/modelo_performance_copy.pkl",
        "r2": 0.000, "mae": 00.0
    },
}
model_name = st.selectbox("🤖 Selecciona el modelo", list(MODELS.keys()), label_visibility="collapsed")
meta = MODELS[model_name]

# 3. Carga dinámica según selección
@st.cache_resource
def load_model(name):
    path = MODELS[name]["path"]
    if os.path.exists(path):
        return joblib.load(path)
    return None

model = load_model(model_name)

# ── Helpers ───────────────────────────────────────────────────────────────────
def predict(hours, prev, sleep, papers, extra):
    extra_val = 1 if extra == "Sí" else 0
    if model is not None:
        features = pd.DataFrame(
            [[hours, prev, extra_val, sleep, papers]],
            columns=["Hours Studied", "Previous Scores",
                    "Extracurricular Activities", "Sleep Hours",
                    "Sample Question Papers Practiced"]
        )
        return round(float(model.predict(features)[0]), 1)
    
    val = (2.852484 * hours) + (1.016988 * prev) + (0.476941 * sleep) + \
          (0.191831 * papers) + (0.608617 * extra_val) + 33.921946
    return round(min(max(val, 0), 100), 1)

def get_grade(score):
    if score >= 90: return "#22c55e", "🏆", "EXCELENTE",  "¡Increíble! Estás en el camino al éxito académico."
    if score >= 75: return "#3b82f6", "🌟", "MUY BUENO",  "¡Gran rendimiento! Sigue así."
    if score >= 60: return "#f59e0b", "👍", "BUENO",      "Buen trabajo. Un poco más y llegarás lejos."
    if score >= 45: return "#f97316", "📚", "REGULAR",    "Hay oportunidades de mejora."
    return                 "#ef4444", "💪", "A MEJORAR",  "Con dedicación puedes subir tu rendimiento."


# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>🎓 Student Performance Simulator</h1>
    <p>Predice tu índice de rendimiento académico con Inteligencia Artificial</p>
</div>
""", unsafe_allow_html=True)

if model is not None:
    # Mostrar qué modelo está activo
    meta = MODELS[model_name]
    st.success(f"✅ {model_name} activo — R² {meta['r2']} · MAE ±{meta['mae']}")
else:
    st.error(f"❌ {model_name} no encontrado — ⚠️ usando fórmula de respaldo")


# ── LAYOUT: 2 columnas ────────────────────────────────────────────────────────
col_in, col_out = st.columns([1, 1.4], gap="large")

# ─────────────────────────────────────────────────────────────────────────────
# COLUMNA IZQUIERDA — Inputs
# ─────────────────────────────────────────────────────────────────────────────
with col_in:
    st.markdown('<div class="card-title">⚙️ Panel de Variables</div>', unsafe_allow_html=True)

    def var_input(label, emoji, key, mn, mx, default):
        """Slider sincronizado con number input."""
        st.markdown(f'<div class="slider-label">{emoji} {label}</div>', unsafe_allow_html=True)
        
        s = st.slider("inputs", mn, mx, default, key=f"s_{key}", label_visibility="collapsed")

        return s

    hours = var_input("Horas de estudio semanales", "📗", "hours",  1,  9, 5)
    prev = var_input("Promedio de notas anteriores", "📘", "prev",  40, 99, 70)
    sleep = var_input("Horas de sueño diarias", "😴", "sleep",  4,  9,  7)
    papers = var_input("Exámenes de práctica", "📝", "papers", 0,  9,  2)

    st.markdown('<div class="slider-label">🎯 Actividades extracurriculares</div>', unsafe_allow_html=True)
    extra = st.selectbox("extra", ["Sí", "No"], label_visibility="collapsed")

    score = predict(hours, prev, sleep, papers, extra)
    st.session_state["last_score"]  = score
    st.session_state["last_inputs"] = (hours, prev, sleep, papers, extra)
    color, emoji, grade, msg = get_grade(score)

    if st.button("✨ Guardar información"):
        st.session_state.history.insert(0, {
            "score": score, "grade": grade, "emoji": emoji,
            "hours": hours, "prev": prev, "sleep": sleep,
            "papers": papers, "extra": extra,
            "time": datetime.now().strftime("%H:%M:%S")
        })
        st.session_state.history = st.session_state.history[:8]


# ─────────────────────────────────────────────────────────────────────────────
# COLUMNA DERECHA — Resultados
# ─────────────────────────────────────────────────────────────────────────────
with col_out:

    # Score principal
    st.markdown(f"""
    <div class="score-card">
        <div style="color:{color};font-size:0.82rem;font-weight:700;
                    text-transform:uppercase;letter-spacing:2px;margin-bottom:8px">
            Predicción de Rendimiento
        </div>
        <div class="score-number" style="color:{color}">{score}</div>
        <div class="score-grade"  style="color:{color}">{emoji} {grade}</div>
        <div class="score-message">{msg}</div>
    </div>
    """, unsafe_allow_html=True)

    #st.markdown("<br>", unsafe_allow_html=True)
    # ── Tab 2: Historial ──────────────────────────────────────────────────
    if st.session_state.history:
        if st.button("🗑️ Limpiar"):
            st.session_state.history = []
            st.session_state.pop("last_score", None)
            st.rerun()
        
        # Filas de historial
        for h in st.session_state.history:
            c, *_ = get_grade(h["score"])
            st.markdown(f"""
            <div class="history-row">
                <div style="display:flex;align-items:center;gap:10px">
                    <div style="background:{c}22;color:{c};border-radius:10px;
                                padding:4px 12px;font-weight:900;font-size:1rem">
                        {h['emoji']} {h['score']}
                    </div>
                    <div>
                        <div style="color:#5b4e8a;font-size:0.78rem;font-weight:700">{h['grade']}</div>
                        <div style="color:#b0a4d4;font-size:0.68rem">
                            {h['hours']}h · {h['prev']} previas · {h['sleep']}h sueño · {h['papers']} exámenes
                        </div>
                    </div>
                </div>
                <div class="history-time">{h['time']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center;padding:24px;color:#c4b5fd">
            <div style="font-size:2rem">📊</div>
            <div style="font-weight:700;margin-top:6px">Sin predicciones aún</div>
            <div style="font-size:0.78rem;margin-top:4px">Ajusta las variables y presiona Predecir</div>
        </div>
        """, unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:#c4b5fd;font-size:0.75rem;padding:20px 0 8px">
    🎓 Student Performance Simulator · LinearRegression · scikit-learn
</div>
""", unsafe_allow_html=True)