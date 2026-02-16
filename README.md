# 📚 Análisis de Hábitos de Estudio y Rendimiento Académico

Este módulo del proyecto se centra en la creación de un modelo de regresión para predecir el **Performance Index** de los estudiantes, basándose exclusivamente en sus hábitos actuales (horas de estudio, sueño, etc.) y excluyendo variables de rendimiento pasado para obtener un análisis más puro del comportamiento actual.

## 🎯 Objetivo y Hipótesis
La mayoría de los modelos dependen fuertemente de los **Previous Scores** (correlación de 0.92). Mi enfoque decidió **eliminar esta variable** para responder a la pregunta: 
> *"¿Cuánto impacto real tienen las horas de estudio y otros hábitos diarios en el rendimiento, sin considerar el pasado académico del estudiante?"*

## 📊 Variables Utilizadas

Para este análisis se utilizaron únicamente variables relacionadas con los hábitos actuales del estudiante, excluyendo deliberadamente la variable **Previous Scores**.

Variables incluidas en el modelo:

- **Hours Studied:** Número total de horas dedicadas al estudio.
- **Extracurricular Activities:** Participación en actividades extracurriculares (Yes/No).
- **Sleep Hours:** Promedio de horas de sueño por día.
- **Sample Question Papers Practiced:** Número de exámenes de práctica realizados.

Variable excluida:

- **Previous Scores:** Puntajes obtenidos en exámenes anteriores (eliminada para evitar que el modelo dependa del rendimiento pasado).

## 🛠️ Metodología Utilizada

### 1. Análisis Exploratorio de Datos (EDA)
- **Distribución:** Se confirmó que la variable objetivo `Performance Index` sigue una distribución normal, ideal para modelos de regresión.
- **Correlación:** Se identificó que, tras eliminar los puntajes previos, la variable con mayor peso es **Hours Studied**.

### 2. Estrategia de Validación (Split 70/15/15 & 80/20)
Para asegurar la robustez del modelo, se implementaron dos estrategias:
- **Split 70/15/15:** 70% Entrenamiento, 15% Validación (ajuste de parámetros) y 15% Prueba (evaluación final).
- **Split 80/20:** Para comparar la estabilidad del modelo con una mayor cantidad de datos de entrenamiento.
- **K-Fold Cross Validation:** Se aplicó validación cruzada para garantizar que el rendimiento del modelo no dependa de una partición específica de los datos.

### 3. Modelos de Regresión con Regularización
Se implementaron y compararon dos modelos avanzados para evitar el sobreajuste:
- **Ridge Regression (L2):** Para manejar la estabilidad de los coeficientes.
- **Lasso Regression (L1):** Utilizado para la **selección automática de características**, lo que permitió identificar qué variables no aportan valor real.

## 📈 Resultados Clave

- **Impacto de las Horas de Estudio:** El modelo Lasso determinó un coeficiente de **2.65**. Esto significa que por cada hora adicional de estudio, el índice de rendimiento aumenta en promedio 2.65 puntos.
- **Selección de Variables:** Lasso redujo a **cero** el coeficiente de `Extracurricular Activities`, demostrando que no es un predictor relevante en este conjunto de datos.
- **Control de Sobreajuste (Overfitting):** 
    - Diferencia entre Train y Validation: **3.10%** (Cumple con el requisito de < 5%).
    - La estabilidad se confirmó con la división 80/20, reduciendo la diferencia a un **0.72%**.

## 📊 Visualizaciones Incluidas
- **Heatmap de correlación:** Para identificar predictores clave.
- **Gráfico de Actual vs. Predicted:** Para evaluar visualmente el ajuste del modelo.
- **Análisis de Residuos:** Histograma de errores para verificar la normalidad del modelo.

---
Created by Mirae Kang