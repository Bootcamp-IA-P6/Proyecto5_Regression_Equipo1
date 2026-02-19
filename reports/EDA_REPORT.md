# 📊 Informe de Análisis Exploratorio de Datos (EDA)
**Proyecto:** Predicción de Rendimiento Académico  
**Dataset:** Student_Performance.csv

## 1. Introducción y Limpieza de Datos
Antes de proceder al modelado, realizamos un proceso de auditoría y limpieza para asegurar la calidad de los datos:

- **Valores Nulos:** No se detectaron valores ausentes en ninguna columna.
- **Duplicados:** Se identificaron **127 filas duplicadas** (registros idénticos). Estas fueron eliminadas para evitar sesgos, quedando un dataset final de **9,873 registros**.
- **Transformación de Variables:** La variable `Extracurricular Activities` (Yes/No) fue codificada numéricamente (1/0) para permitir el análisis de correlación y el entrenamiento del modelo.

### 🧪 Naturaleza del Dataset

Es importante destacar que este dataset es sintético y fue creado con fines ilustrativos.

Por lo tanto, las relaciones observadas representan patrones simulados y no necesariamente reflejan dinámicas reales del mundo académico. Sin embargo, el conjunto de datos resulta adecuado para fines educativos y para la aplicación de técnicas de modelado predictivo.

---

## 2. Estadísticas Descriptivas (Describe)
El análisis de los valores mínimos, máximos y promedios nos permite entender el rango de nuestros estudiantes:

| Variable | Media | Mínimo | Máximo | Observación |
| :--- | :---: | :---: | :---: | :--- |
| **Hours Studied** | 4.99 | 1.0 | 9.0 | Distribución uniforme de tiempo de estudio. |
| **Previous Scores** | 69.44 | 40.0 | 99.0 | Gran variedad en el historial académico. |
| **Sleep Hours** | 6.53 | 4.0 | 9.0 | Rango saludable de descanso en general. |
| **Sample Papers** | 4.15 | 0.0 | 10.0 | Práctica variable entre estudiantes. |
| **Performance Index** | 55.21 | 10.0 | 100.0 | **Variable Objetivo (Target).** |

### 🔎 Análisis de Valores Atípicos (Outliers)

Se realizó una revisión de los valores mínimos y máximos de cada variable para identificar posibles valores atípicos extremos.

No se detectaron valores fuera de los límites lógicos del dataset. Todas las variables se encuentran dentro de rangos coherentes (por ejemplo, horas de estudio entre 1 y 9, horas de sueño entre 4 y 9).

Dado que el dataset es sintético y no presenta inconsistencias evidentes, no fue necesario aplicar técnicas de eliminación de outliers.

---

## 3. Análisis Univariado
Analizamos cada variable de forma individual para entender su comportamiento:

- **Variable Objetivo (Performance Index):** Sigue una **distribución normal** casi perfecta (forma de campana). La mayoría de los estudiantes se encuentran en el rango de 40 a 70 puntos.
- **Variables Predictoras:** 
  - Las `Hours Studied` y `Sleep Hours` muestran distribuciones uniformes, lo que significa que el dataset está bien balanceado y contiene ejemplos de todo tipo de hábitos.

---

## 4. Análisis Bivariado y Correlaciones
Estudiamos la relación entre los factores y el rendimiento final mediante una matriz de correlación de Pearson:

1. **Puntaje Anterior vs. Rendimiento (0.92):** 
   - Existe una relación lineal extremadamente fuerte. El éxito pasado es el indicador más fiable del éxito actual.
2. **Horas de Estudio vs. Rendimiento (0.37):** 
   - Relación positiva moderada. Es la variable **accionable** más importante: aunque no define el 100% de la nota, es el factor que el estudiante puede cambiar para mejorar.
3. **Otros factores (Sueño, Actividades, Exámenes):**
   - Presentan correlaciones muy bajas (< 0.05). Esto indica que, de forma aislada, no garantizan un cambio drástico en la nota, sino que actúan como complementos.


### 📐 Evaluación de Multicolinealidad

Se analizó la posible multicolinealidad entre las variables predictoras mediante la matriz de correlación.

No se observaron correlaciones elevadas entre las variables independientes, lo que sugiere que el riesgo de inestabilidad en los coeficientes del modelo es bajo.

La única correlación extremadamente alta corresponde a `Previous Scores` con la variable objetivo, lo cual es esperado dado su fuerte carácter predictivo.

---

## 5. Insights y Conclusiones del Negocio

Tras el análisis exhaustivo, hemos obtenido los siguientes hallazgos clave:

1. **El "Factor Multiplicador" del Estudio:** 
   - Aunque la base académica (`Previous Scores`) es crucial, el modelo de regresión indica que **cada hora adicional de estudio suma aproximadamente 2.85 puntos** al índice de rendimiento.
   
2. **Desmitificación de las Actividades Extracurriculares:** 
   - El análisis bivariado demuestra que participar en actividades extraescolares **no perjudica el rendimiento académico**. El coeficiente de impacto es cercano a cero, lo que sugiere que los estudiantes pueden mantener una vida equilibrada sin sacrificar sus notas.

3. **Intervención Temprana:** 
   - Dado que el historial previo (`Previous Scores`) tiene un peso del 92%, el sistema educativo debería enfocarse en tutorías tempranas para aquellos con bases débiles, ya que les resultará más difícil compensar la diferencia solo con horas de estudio de último minuto.

4. **Estabilidad del Modelo:**
   - La consistencia entre los diferentes splits de datos (70/15/15 y 80/20) y los resultados de **K-Fold Cross Validation** confirman que los hallazgos son estadísticamente significativos y no fruto del azar.

---

## 6. Conclusión General del Análisis

El análisis exploratorio permitió comprender en profundidad la estructura del dataset, la distribución de las variables y la magnitud de su impacto sobre el rendimiento académico.

Los resultados muestran que el rendimiento no depende de un único factor aislado, sino de la combinación entre la base académica previa y los hábitos actuales del estudiante. Mientras que el historial previo (`Previous Scores`) actúa como el principal predictor estructural, variables como `Hours Studied` representan el componente accionable que puede influir en la mejora del desempeño.

Desde una perspectiva de negocio o intervención educativa, esto implica que las estrategias deben enfocarse tanto en el fortalecimiento temprano de las bases académicas como en la promoción de hábitos de estudio consistentes.

Finalmente, la consistencia de los resultados a través de distintos métodos de validación (splits y K-Fold) respalda la robustez del modelo y confirma que los hallazgos obtenidos no son producto del azar, sino de patrones estadísticamente significativos dentro del dataset.