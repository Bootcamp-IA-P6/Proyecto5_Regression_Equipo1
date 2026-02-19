# 🎓 Predicción de Rendimiento Académico
### *Student Performance Regression Project*

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

*Aplicación de Machine Learning para predecir el índice de desempeño estudiantil a partir de factores socio-educativos*

</div>

---

## 📌 Descripción del Proyecto

Este proyecto aplica técnicas de **regresión supervisada** para predecir el rendimiento académico de estudiantes basándose en variables socio-educativas clave. El objetivo es doble: identificar qué factores tienen mayor impacto en el éxito escolar y ofrecer una herramienta predictiva interactiva y funcional desplegada con Streamlit.

El dataset utilizado es el clásico **Student Performance Dataset**, que recoge información sobre hábitos de estudio, sueño, actividades extracurriculares, motivación y notas previas, entre otras variables.

---

## 🤝 Metodología de Equipo

El equipo adoptó un enfoque **colaborativo y paralelo**, dividiendo el trabajo en tres fases bien definidas:

### 1️⃣ Análisis Exploratorio de Datos (EDA) — Individual
Cada miembro del equipo realizó su propio EDA de forma **independiente**, lo que permitió:
- Obtener **múltiples perspectivas** sobre la calidad y estructura del dataset.
- Detectar valores atípicos y distribuciones anómalas desde distintos ángulos.
- Construir hipótesis propias sobre las correlaciones entre variables.

> Esta fase garantizó que ningún sesgo individual condicionara el análisis colectivo.

### 2️⃣ Entrenamiento de Modelos — Individual
Siguiendo la misma dinámica, cada integrante desarrolló y entrenó su **propio modelo de regresión**, experimentando con:
- Distintas combinaciones de variables predictoras.
- Diferentes algoritmos (Regresión Lineal, Ridge, Lasso, etc.).
- Ajuste de hiperparámetros y validación cruzada.

### 3️⃣ Selección de Modelos Finales — Colaborativa
Tras una **puesta en común de resultados**, el equipo evaluó todos los modelos y seleccionó los dos enfoques más sólidos para integrar en la aplicación final.

---

## 🧠 Los Dos Modelos

### 🔵 Modelo Multivariable — *Completo* (`modelo_multiple.pkl`)
> **"Máxima precisión con todas las variables significativas"**

Este modelo incorpora **5 variables** que demostraron tener impacto estadísticamente significativo en el rendimiento académico. Es el modelo recomendado cuando se dispone de información completa del estudiante.

| Métrica | Valor |
|---|---|
| R² Score | **0.98** |
| Variables de entrada | `Hours Studied`, `Previous Scores`, `Extracurricular Activities`, `Sleep Hours`, `Sample Question Papers Practiced` |
| Uso ideal | Evaluación completa y detallada del perfil estudiantil |

**¿Por qué funciona tan bien?** Al combinar factores académicos históricos (*Previous Scores*) con conductuales y de estilo de vida, el modelo captura la complejidad real del rendimiento estudiantil, logrando predicciones muy cercanas a los valores reales.

---

### 🟢 Modelo de Dos Variables — *Básico* (`modelo_notas.pkl`)
> **"Predicción rápida centrada en hábitos y trayectoria"**

Este modelo fue construido específicamente a partir de tan solo **dos variables**:
- 📚 **Horas de Estudio** (*Hours Studied*)
- 📊 **Notas Anteriores** (*Previous Scores*)

| Métrica | Valor |
|---|---|
| Variables de entrada | `Hours Studied` + `Previous Scores` |
| Fortaleza | Simplicidad, interpretabilidad y mínima fricción de datos |
| Uso ideal | Orientación rápida cuando solo se dispone de datos básicos |

**¿Por qué estas dos variables?** Representan la combinación más poderosa entre **trayectoria académica** (lo que el estudiante ya ha conseguido) y **esfuerzo actual** (el factor más accionable). Este modelo es especialmente útil para intervenciones tempranas con información limitada.

---

## 📊 Hallazgos Principales

Los análisis exploratorios del equipo convergieron en los siguientes *insights* clave:

- **📈 Notas Anteriores** es el predictor más sólido del dataset, con una correlación de **0.92** con el rendimiento final. La consistencia académica previa es el indicador más fiable del éxito futuro.

- **📚 Horas de Estudio** es el factor *accionable* más relevante. Por cada hora adicional de estudio, el rendimiento mejora en promedio **2.85 puntos** — el mayor retorno por variable modificable.

- **😴 Horas de Sueño** fue identificada como variable crítica para el mantenimiento del rendimiento a largo plazo, incluida en el modelo completo.

---

## 🖥️ Interfaz de la Aplicación

La app está construida con **Streamlit** y tiene un diseño oscuro personalizado con paleta *navy + gold*, tipografía **DM Sans / DM Mono** y efectos glassmorphism.

### Panel Lateral — Sidebar

El sidebar es el **centro de control** de la aplicación. Desde aquí el usuario gestiona todo:

**`🔘 Selector de modelo`** — Un radio button permite cambiar entre el Modelo Completo y el Modelo Básico. La selección actualiza dinámicamente los campos de entrada disponibles y el badge visible en la cabecera principal.

**`📝 Formulario de datos del estudiante`** — Los inputs varían según el modelo activo:

| Input | Modelo Básico | Modelo Completo |
|---|:---:|:---:|
| 📚 Horas de estudio (`number_input`, 0–24) | ✅ | ✅ |
| 📊 Promedio anterior (`slider`, 0–100) | ✅ | ✅ |
| 🎯 Actividades extracurriculares (`selectbox`: Sí / No) | ❌ | ✅ |
| 😴 Horas de sueño (`number_input`, 0–24) | ❌ | ✅ |
| 📝 Exámenes de práctica (`number_input`, 0–50) | ❌ | ✅ |

**`⚡ Botón "Predecir rendimiento"`** — Botón dorado de ancho completo que lanza la predicción. Al pulsarlo, la zona central se transforma y muestra los resultados.

**`ℹ️ Badge de modelo activo`** — Indicador visual en la parte inferior del sidebar que confirma qué modelo está cargado (`✦ Completo` o `◈ Básico`).

---

### Zona Principal — Pantalla de Inicio

Antes de realizar una predicción, la pantalla muestra:

- **Badge dinámico** en la cabecera que indica el modelo seleccionado (dorado para Completo, azul para Básico).
- **Título principal** con el nombre de la app y las instrucciones de uso.
- **Animación Lottie** (`assets/niu.json`) a pantalla completa, que desaparece en el momento de predecir.

---

### Zona Principal — Resultado de Predicción

Al pulsar el botón, la animación se sustituye por el panel de resultados:

**`🎯 Tarjeta de resultado principal`**

Muestra el **Performance Index estimado** en formato grande con fuente monoespaciada (`DM Mono`), acompañado de un badge de nivel de rendimiento con código de colores:

| Rango | Nivel | Color |
|---|---|---|
| 70 – 100 | 🟢 Rendimiento Alto | Verde `#22C55E` |
| 45 – 69 | 🟡 Rendimiento Medio | Dorado `#F59E0B` |
| 0 – 44 | 🔴 Rendimiento Bajo | Rojo `#EF4444` |

**`📊 Métricas rápidas`** — Fila de 3 tarjetas resumen con los valores clave introducidos y el score final estimado.

**`📉 Gráfico: Importancia de variables`** (columna izquierda)

Gráfico de barras horizontal (Plotly) que muestra el coeficiente de cada variable del modelo. Las barras en **dorado** indican impacto positivo y en **rojo** impacto negativo, permitiendo interpretar visualmente qué factores impulsan o frenan el rendimiento.

**`🔵 Gráfico: Gauge de nivel`** (columna derecha)

Medidor tipo velocímetro (Plotly `Indicator`) con tres zonas coloreadas (rojo / dorado / verde) que sitúa visualmente la predicción en la escala 0–100, con la aguja apuntando al valor estimado.

---

## 🎨 Diseño y Estilo

La aplicación usa CSS personalizado inyectado directamente en Streamlit con `st.markdown(..., unsafe_allow_html=True)`:

- **Fondo principal**: `#0F172A` (navy oscuro) con patrón de puntos sutiles via `radial-gradient`.
- **Sidebar**: gradiente vertical `#1E293B → #0F172A` con borde dorado semitransparente.
- **Glassmorphism**: columnas y métricas con fondo `rgba(30,41,59,0.7)`, `backdrop-filter: blur(12px)` y borde `rgba(245,158,11,0.2)`.
- **Scrollbar personalizada**: track navy, thumb slate que vira a dorado en hover.
- **Inputs**: fondo `#1E293B`, borde que resalta en dorado al hacer focus con glow exterior.
- **Botón**: dorado sólido con sombra difusa y animación `translateY(-2px)` en hover.

---

## 🛠️ Tecnologías Utilizadas

| Categoría | Herramientas |
|---|---|
| **Lenguaje** | Python 3.12 |
| **Machine Learning** | Scikit-Learn |
| **Manipulación de datos** | Pandas, NumPy |
| **Visualización** | Matplotlib, Seaborn, Plotly |
| **Despliegue UI** | Streamlit + streamlit-lottie |
| **Animaciones** | Lottie (JSON) |
| **Serialización de modelos** | Joblib (`.pkl`) |
| **Gestión de dependencias** | uv / pip |

---

## 🚀 Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/Bootcamp-IA-P6/Proyecto5_Regression_Equipo1.git
cd proyecto5_regression_equipo1
```

### 2. Instalar dependencias
```bash
uv sync
```

### 3. Ejecutar la aplicación
```bash
uv run streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`. Selecciona el modelo en el sidebar, introduce los datos del estudiante y pulsa **⚡ Predecir rendimiento**.

---

## 📁 Estructura del Proyecto

```
Proyecto5_Regression_Equipo1/
│
├── 📂 .streamlit/
│   └── config.toml                              # Configuración de tema y servidor
│
├── 📂 assets/
│   └── niu.json                                 # Animación Lottie (pantalla de inicio)
│
├── 📂 data/
│   └── Student_Performance.csv                  # Dataset original
│
├── 📂 notebooks/
│   ├── 01_eda_student_g.ipynb                   # EDA individual — Miembro G
│   ├── 02_entrenamiento_modelo_g.ipynb          # Entrenamiento individual — Miembro G
│   ├── horas_estudio_sueno_I.ipynb              # EDA + entrenamiento — Miembro I
│   ├── student_perfomance_regression_j.ipynb    # EDA + entrenamiento — Miembro J
│   ├── student_perfomance_regression_m.ipynb    # EDA + entrenamiento — Miembro M
│   ├── modelo_multiple.pkl                      # Modelo completo exportado ✦
│   └── modelo_notas.pkl                         # Modelo básico exportado ◈
│
├── 📂 reports/
│   └── ...                                      # Informes y análisis finales
│
├── app.py                                       # Aplicación Streamlit principal
├── pyproject.toml
└── README.md

```

---

## 👥 Equipo

Proyecto desarrollado en equipo como parte del aprendizaje de técnicas de Machine Learning aplicadas a datos reales.


| Desarrolladores | GitHub | LinkedIn |
|----------------|--------|----------|
| **Mirae Kang** | [GitHub](https://github.com/KangMirae) | [LinkedIn](https://www.linkedin.com/in/kangmirae/) |
| **Gema Yébenes** | [GitHub](https://github.com/gemayc) | [LinkedIn](https://www.linkedin.com/in/gemayebenes-tech/) |
| **Jonathan Brasales** | [GitHub](https://github.com/JonnyBP) | [LinkedIn](https://www.linkedin.com/in/jbrasales/) |
| **Ingrid Martínez** | [GitHub](https://github.com/IngridMartinezB) | [LinkedIn](https://www.linkedin.com/in/ingridmartinezb/) |



**Bootcamp:** Inteligencia Artificial 
**Organización:**  Factoría F5  
**Año:** 2026

---

<div align="center">
<sub>Hecho con ❤️ y muchas horas de estudio · <i>que también mejoran el rendimiento 2.85 puntos por hora</i></sub>
</div>