# 🧪 Proyecto Integrador: Análisis Estadístico de un Sistema Termodinámico Real

## 🎯 Objetivo General

Aplicar herramientas de probabilidad y estadística para analizar datos experimentales obtenidos en un sistema de compresión de gas (émbolo-cilindro), evaluando su comportamiento, la calidad de las mediciones y su relación con la Primera Ley de la Termodinámica.

---

## 📂 Datos Experimentales Proporcionados

Se les entregarán **10 datasets** (archivos CSV) con las siguientes columnas:

- **Timestamp** - Marca temporal de cada medición
- **Presion (kPa)** - Presión registrada en kilopascales
- **Temperatura (C)** - Temperatura registrada en grados Celsius

### 📏 Especificaciones del sistema:

- **Diámetro del cilindro**: D = 46 mm
- **Desplazamiento máximo del émbolo** (xₘₐₓ): valor único para cada dataset (ver tabla abajo)

### 📊 Tabla de desplazamientos máximos:

| Dataset | Desplazamiento (mm) |
|---------|---------------------|
| 1       | 8.3               |
| 2       |8.2               |
| 3       | 12.2              |
| 4       | 12.0               |
| 5       | 12.2              |
| 6       | 12.3              |
| 7       | 11.9              |
| 8       |11.0               |
| 9       | 10.9               |
| 10       | 10.8              |


### ⚠️ Nota sobre el experimento

Durante las pruebas, el cambio de temperatura fue **menor al esperado** (aproximadamente 1°C de variación). Esto sugiere un proceso **cuasi-isotérmico**, lo cual NO invalida el experimento, sino que nos permite analizar otros aspectos termodinámicos importantes como la relación presión-volumen y la evolución temporal del sistema.

---

## 🧭 FASES DEL PROYECTO

---

## 1️⃣ Estadística Descriptiva y Calidad Experimental (20 pts)

### 🎯 Objetivo
Evaluar la estabilidad, precisión y reproducibilidad del sistema experimental.

### 📝 Instrucciones

#### Paso 1.1: Carga y consolidación de datos
1. **Sube los 10 archivos CSV** a tu Google Colab (puedes usar el ícono de carpeta 📁 o `files.upload()`)
2. **Crea un diccionario** con los desplazamientos máximos
3. **Lee cada archivo** y agrega dos columnas nuevas:
   - `Dataset` (número de 1 a 10)
   - `Desplazamiento_mm` (del diccionario)
4. **Combina todos los DataFrames** en uno solo usando `pd.concat()`
5. **Guarda el resultado** como `datos_completos.csv`
6. **Verifica** que tu DataFrame tenga todas las columnas y que no haya valores nulos

💡 **Tip**: Usa `glob` para leer múltiples archivos automáticamente, o un bucle `for` si prefieres más control.

#### Paso 1.2: Análisis descriptivo por dataset

Para **cada uno de los 10 datasets**, calcula:

**Para la Presión:**
- Media (P̄)
- Desviación estándar (σₚ)
- Varianza (σ²ₚ)
- Coeficiente de variación (CV = σ/μ × 100%)
- Valores mínimo y máximo

**Para la Temperatura:**
- Media (T̄)
- Desviación estándar (σₜ)
- Rango de variación (ΔT = Tₘₐₓ - Tₘᵢₙ)

**Crea una tabla resumen** con estos resultados (puedes usar `groupby()` y `agg()` de pandas).

💡 **Tip**: Usa `.groupby('Dataset').agg({'Presion (kPa)': ['mean', 'std', 'var'], ...})`

#### Paso 1.3: Identificación de valores atípicos

1. **Calcula el rango intercuartílico (IQR)** para la presión de cada dataset [INFO AQUI ](https://docs.oracle.com/cloud/help/es/pbcs_common/PFUSU/insights_metrics_IQR.htm#PFUSU-GUID-CF37CAEA-730B-4346-801E-64612719FF6B)
2. **Identifica outliers** usando el criterio: valores fuera de [Q1 - 1.5×IQR, Q3 + 1.5×IQR]
3. **Documenta** cuántos outliers encontraste y en qué datasets

💡 **Tip**: Puedes usar `df.quantile([0.25, 0.75])` para calcular cuartiles.

#### Paso 1.4: Visualizaciones requeridas

Crea las siguientes gráficas usando `matplotlib` o `seaborn`:

1. **Histograma de Presión** (todas las mediciones combinadas)
   - Incluye línea de densidad normal ajustada
   
2. **Histograma de Temperatura** (todas las mediciones combinadas)

3. **Boxplots comparativos de Presión** por dataset (10 cajas en una sola gráfica)
   - Identifica visualmente outliers y diferencias entre datasets

4. **Boxplots comparativos de Temperatura** por dataset

5. **Series de tiempo** para 3 datasets representativos:
   - Presión vs Tiempo
   - Temperatura vs Tiempo
   - Usa subplots para mejor comparación

💡 **Tip para Google Colab**: Usa `%matplotlib inline` y `plt.figure(figsize=(12,6))` para gráficas más grandes.

### 💬 Preguntas de análisis (para el reporte final)

1. ¿Qué dataset mostró la **mayor estabilidad** en presión? (menor coeficiente de variación)
2. ¿La temperatura puede considerarse **constante** durante cada experimento? Justifica con ΔT.
3. ¿Qué tan **homogéneos** fueron los resultados entre los 10 datasets?
4. ¿Encontraste **outliers** significativos? ¿Cómo los manejarías?
5. ¿El sistema puede considerarse **cuasiestático**? ¿Por qué?

---

## 2️⃣ Correlación y Relación P-T (15 pts)

### 🎯 Objetivo
Analizar la relación estadística entre presión y temperatura en cada experimento.

### 📝 Instrucciones

#### Paso 2.1: Cálculo de coeficientes de correlación

Para **cada uno de los 10 datasets**, calcula:

1. **Coeficiente de Pearson** (r) - mide correlación lineal
2. **Coeficiente de Spearman** (ρ) - mide correlación monotónica
3. **Coeficiente de Kendall** (τ) - robusto a outliers  [info aqui]( https://numiqo.es/tutorial/kendalls-tau)

💡 **Tip**: Usa `scipy.stats.pearsonr()`, `.spearmanr()` y `.kendalltau()`. Cada función devuelve el coeficiente y el p-value.

#### Paso 2.2: Tabla resumen de correlaciones

Crea una tabla con las columnas:

| Dataset | Pearson (r) | p-value | Spearman (ρ) | p-value | Kendall (τ) | p-value |
|---------|-------------|---------|--------------|---------|-------------|---------|
| 1       | ...         | ...     | ...          | ...     | ...         | ...     |

#### Paso 2.3: Interpretación de significancia

Para cada coeficiente:
- Si **p-value < 0.05**: la correlación es estadísticamente significativa
- Interpreta el **signo** (positivo/negativo)
- Interpreta la **magnitud**:
  - |r| < 0.3: correlación débil
  - 0.3 ≤ |r| < 0.7: correlación moderada
  - |r| ≥ 0.7: correlación fuerte

### 💬 Preguntas de análisis

1. ¿Existe una **correlación significativa** entre P y T en tus datos?
2. ¿Qué tipo de relación observas: **lineal, débil, inexistente**?
3. ¿Los tres coeficientes dan resultados similares? ¿Cuál es más apropiado para estos datos?
4. ¿Cómo interpretas **físicamente** el resultado? ¿Es consistente con un gas ideal (P ∝ T)?
5. Dado que la temperatura cambió poco (~1°C), ¿esperabas una correlación fuerte? ¿Por qué?

---

## 3️⃣ Regresión Lineal P-T (20 pts)

### 🎯 Objetivo
Ajustar un modelo empírico y evaluar su validez estadística.

### 📝 Instrucciones

#### Paso 3.1: Regresión lineal simple

Para **cada dataset**, ajusta el modelo:

**P = a·T + b**

Donde:
- **a** = pendiente
- **b** = intercepto

Reporta para cada dataset:
1. Pendiente (a)
2. Intercepto (b)
3. Coeficiente de determinación (R²)
4. Error estándar de la estimación

💡 **Tip**: Puedes usar:
- `scipy.stats.linregress()` - más simple
- `sklearn.linear_model.LinearRegression()` - más completo
- O calcular manualmente usando las fórmulas de mínimos cuadrados

#### Paso 3.2: Visualización

Crea **al menos 3 gráficas de dispersión** P vs T con:
- Puntos de datos originales
- Línea de regresión ajustada
- Ecuación del modelo en el título
- Valor de R² anotado

Selecciona datasets representativos (por ejemplo: mejor R², peor R², y uno intermedio).

#### Paso 3.3: Comparación de pendientes

1. **Crea una lista** con las 10 pendientes obtenidas
2. **Calcula estadísticos**: media, desviación estándar, min, max
3. **Grafica** las pendientes en un histograma o gráfico de barras
4. **Visualiza la distribución:** ¿Parece simétrica? ¿Hay valores extremos?
5. Calcula el coeficiente de variación de las pendientes: CV = (σ/μ) × 100%

#### Paso 3.4: Prueba de hipótesis sobre las pendientes

**Si hay normalidad:**
- Realiza una **prueba t de una muestra** comparando la media de las pendientes con un valor teórico esperado (por ejemplo, 0 si esperarías proceso isotérmico perfecto)

**Si NO hay normalidad:**
- Usa la **mediana** en lugar de la media
- O aplica una transformación a los datos

### 💬 Preguntas de análisis

1. ¿Qué representa **físicamente** la pendiente del modelo P-T?
2. ¿Los valores de R² indican un **buen ajuste lineal**? ¿Por qué son bajos (si lo son)?
3. ¿Existe **consistencia** entre las pendientes de los 10 datasets?
4. ¿Las pendientes son consistentes entre corridas? Usa el CV para cuantificar.
5. ¿Qué tan dispersos están los valores? ¿Hay alguna pendiente muy diferente?
6. ¿La media es representativa o hay mucha variabilidad?

---

## 4️⃣ Análisis Complementario: Presión vs Tiempo (15 pts)

### 🎯 Objetivo
Analizar la evolución temporal de la presión durante la compresión.

### 📝 Instrucciones

#### Paso 4.1: Preparación de datos temporales

1. **Convierte** la columna `Timestamp` a formato datetime (si no lo está ya)
2. **Calcula** el tiempo transcurrido desde el inicio de cada dataset:
   ```
   t = (Timestamp - Timestamp_inicial).total_seconds()
   ```
3. Agrega esta columna como `Tiempo_s` a tu DataFrame

#### Paso 4.2: Regresión P vs t

Para cada dataset, ajusta:

**P = m·t + c**

Donde:
- **m** = tasa de compresión (kPa/s)
- **c** = presión inicial

Reporta:
- Tasa de compresión (m)
- R²
- Tiempo total de compresión

#### Paso 4.3: Análisis de tasas de compresión

1. **Compara** las tasas entre los 10 datasets
2. **Calcula** la tasa promedio y su desviación estándar
3. **Identifica** el dataset con compresión más rápida y más lenta

### 💬 Preguntas de análisis

1. ¿La presión aumenta **linealmente** con el tiempo?
2. ¿Las tasas de compresión son **consistentes** entre datasets?
3. ¿Qué factores experimentales podrían explicar diferencias en las tasas?

---

## 5️⃣ Trabajo Mecánico e Incertidumbre (20 pts)

### 🎯 Objetivo
Vincular los datos experimentales con magnitudes termodinámicas y cuantificar la incertidumbre.

### 📝 Instrucciones

#### Paso 5.1: Cálculo del área del pistón

Calcula el área transversal en metros cuadrados:

**A = π(D/2)²**

Donde D = 46 mm = 0.046 m

💡 Convierte todo a unidades del SI para consistencia.

#### Paso 5.2: Cálculo del trabajo

Para cada dataset, calcula el trabajo realizado sobre el gas usando:

**W ≈ P̄ × A × xₘₐₓ**

Donde:
- P̄ = presión promedio (conviértela a Pa = kPa × 1000)
- A = área en m²
- xₘₐₓ = desplazamiento máximo (conviértelo a m)

El resultado estará en **Joules (J)**.

💡 **Tip**: Esta es una aproximación simplificada. En realidad, W = ∫P dV, pero la fórmula simplificada es adecuada para este proyecto.

#### Paso 5.3: Tabla de resultados de trabajo

Crea una tabla:

| Dataset | P̄ (kPa) | xₘₐₓ (mm) | W (J) |
|---------|---------|-----------|-------|
| 1       | ...     | 12.4      | ...   |
| ...     | ...     | ...       | ...   |

#### Paso 5.4: Análisis de incertidumbre

Supón las siguientes **incertidumbres instrumentales**:
- Presión: σₚ = ±0.01 kPa
- Desplazamiento: σₓ = ±0.1 mm
- Diámetro: σ_D = ±0.05 mm

**Propaga el error** usando la fórmula de propagación de incertidumbres para W = P̄ × A × x:

**σ²_W = (∂W/∂P)² σ²ₚ + (∂W/∂x)² σ²ₓ + (∂W/∂D)² σ²_D**

Las derivadas parciales son:
- ∂W/∂P = A × x
- ∂W/∂x = P̄ × A
- ∂W/∂D = P̄ × x × (πD/2)

💡 **Tip**: Calcula numéricamente o usa las fórmulas. También puedes usar la desviación estándar de P en lugar de la incertidumbre instrumental para tener una estimación más realista.

#### Paso 5.5: Intervalo de confianza del 95%

Para cada dataset, calcula:

**IC₉₅% = W ± 1.96 × σ_W**

Reporta:

| Dataset | W (J) | σ_W (J) | Límite inferior | Límite superior |
|---------|-------|---------|-----------------|-----------------|
| 1       | ...   | ...     | ...             | ...             |

#### Paso 5.6: Análisis de sensibilidad

Calcula qué porcentaje de la incertidumbre total aporta cada variable:

```
Contribución_P = [(∂W/∂P × σₚ)² / σ²_W] × 100%
Contribución_x = [(∂W/∂x × σₓ)² / σ²_W] × 100%
Contribución_D = [(∂W/∂D × σ_D)² / σ²_W] × 100%
```

### 💬 Preguntas de análisis

1. ¿Cuál es el **rango probable** del trabajo real para cada experimento?
2. ¿Qué magnitud aporta **más incertidumbre**: presión, desplazamiento o diámetro?
3. ¿Las diferencias de W entre datasets son **estadísticamente significativas** considerando sus intervalos de confianza?
4. ¿Qué tan **reproducibles** son los valores de trabajo entre experimentos?
5. ¿Cómo podrías **reducir la incertidumbre** en mediciones futuras?

---

## 6️⃣ Inferencia y Simulación Térmica (15 pts)

### 🎯 Objetivo
Extender los resultados a un escenario hipotético donde la temperatura SÍ cambia significativamente.

### 📝 Instrucciones

#### Paso 6.1: Generación de datos simulados

Dado que la temperatura real cambió muy poco, vamos a simular un escenario "qué pasaría si...":

1. **Crea una nueva columna** `Temp_simulada` en tu DataFrame:
   ```python
   import numpy as np
   datos['Temp_simulada'] = datos['Temperatura (C)'] + np.random.normal(0, 5, len(datos))
   ```
   Esto agrega una variación aleatoria de ±5°C a las temperaturas originales.

2. **Nota importante**: Esto es solo un ejercicio de análisis de sensibilidad, NO datos reales.

#### Paso 6.2: Re-análisis con temperatura simulada

Repite los siguientes análisis usando `Temp_simulada` en lugar de `Temperatura (C)`:

1. **Correlación P-T simulada**
   - Calcula nuevamente Pearson, Spearman, Kendall
   - Compara con los valores originales

2. **Regresión lineal P-T simulada**
   - Ajusta nuevamente el modelo lineal
   - Compara R² y pendientes con el análisis original

3. **Visualización comparativa**
   - Grafica P vs T_original y P vs T_simulada en la misma figura
   - Muestra ambas líneas de regresión

#### Paso 6.3: Cálculo de cambio de energía interna

Asumiendo aire como gas ideal:

**ΔU = m × Cᵥ × ΔT**

Donde:
- m = 0.01 kg (masa estimada de aire en el cilindro)
- Cᵥ ≈ 718 J/(kg·K) (calor específico a volumen constante para aire)
- ΔT = T_final - T_inicial (en Kelvin, suma 273.15 a °C)

Calcula ΔU para:
1. El escenario **real** (ΔT ~ 1°C)
2. El escenario **simulado** (ΔT mayor)

#### Paso 6.4: Aplicación de la Primera Ley

La Primera Ley de la Termodinámica establece:

**ΔU = Q - W**

Donde:
- ΔU = cambio de energía interna (calculado arriba)
- Q = calor transferido (desconocido)
- W = trabajo mecánico (calculado en Etapa 5)

Despeja:

**Q = ΔU + W**

Calcula Q para cada dataset en ambos escenarios (real y simulado).

#### Paso 6.5: Interpretación termodinámica

Analiza el signo de Q:
- Si **Q > 0**: el sistema **absorbe** calor del entorno
- Si **Q < 0**: el sistema **libera** calor al entorno
- Si **Q ≈ 0**: proceso aproximadamente adiabático

### 💬 Preguntas de análisis

1. ¿Cómo cambia la **correlación P-T** en el escenario simulado vs el real?
2. ¿El modelo lineal mejora su R² con mayor variación térmica? ¿Por qué?
3. En el escenario **real**, ¿el sistema intercambió calor significativo? ¿Qué tipo de proceso fue?
4. En el escenario **simulado**, ¿cómo cambiaría la interpretación del proceso?
5. ¿Se cumple la **Primera Ley** razonablemente dentro de las incertidumbres?
6. Considerando que T cambió poco, ¿qué mecanismo de transferencia de calor fue dominante?

---

## 7️⃣ Conclusiones Generales (10 pts)

### 📝 Instrucciones

Redacta una sección de conclusiones (1-2 páginas) que responda a las siguientes preguntas de manera integrada y coherente:

### 🔍 Aspectos a cubrir:

#### 1. Calidad y reproducibilidad del experimento
- ¿Qué tan consistentes fueron las mediciones entre los 10 datasets?
- ¿Las varianzas fueron homogéneas o heterogéneas?
- ¿El sistema demostró estabilidad y precisión adecuadas?

#### 2. Relaciones estadísticas observadas
- ¿Qué relación predominó: P-T, P-t, o ninguna significativa?
- ¿Los modelos lineales fueron apropiados para estos datos?
- ¿Qué nos dice la debilidad de la correlación P-T?

#### 3. Interpretación termodinámica
- ¿El proceso fue isotérmico, adiabático, o intermedio (politrópico)?
- ¿Cómo lo sabes? Cita evidencia estadística.
- ¿El trabajo calculado tiene sentido físicamente?

#### 4. Incertidumbre y propagación de errores
- ¿Cuál fue el principal factor de incertidumbre en tus cálculos?
- ¿Las incertidumbres afectan tus conclusiones cualitativas?
- ¿Qué tan confiables son tus estimaciones de trabajo?

#### 5. Validación de la Primera Ley
- ¿Se cumplió la conservación de energía dentro de las incertidumbres?
- ¿El balance Q = ΔU + W es razonable?
- ¿Qué limitaciones tiene tu análisis?

#### 6. Mejoras propuestas para el diseño experimental
- ¿Qué modificarías para obtener mejores datos?
- ¿Qué instrumentación adicional sería útil?
- ¿Qué variables adicionales medirías?
- ¿Cómo aumentarías el cambio de temperatura?

### ✍️ Estilo de redacción esperado:
- Usa lenguaje técnico pero claro
- Cita evidencia numérica de tu análisis
- Sé crítico pero constructivo
- No solo describas qué hiciste, **interpreta** qué significa

---

## 📋 CRITERIOS DE EVALUACIÓN (110 pts)

| Etapa | Ponderación | Criterios específicos |
|-------|-------------|----------------------|
| **1. Descriptiva** | 20 pts | Tabla resumen completa y correcta (5), visualizaciones claras y apropiadas (8), análisis de outliers (4), interpretación razonada (3) |
| **2. Correlación** | 15 pts | Cálculo correcto de los 3 coeficientes (6), interpretación de p-values (3), discusión física (3), tabla resumen (3) |
| **3. Regresión P-T** | 20 pts | Modelos correctamente ajustados (6), visualizaciones con líneas de ajuste (5), prueba de normalidad de pendientes (4), interpretación estadística (3), discusión física (2) |
| **4. Análisis P-t** | 15 pts | Cálculo de tasas de compresión (6), comparación entre datasets (5), interpretación (4) |
| **5. Trabajo e incertidumbre** | 20 pts | Cálculo correcto de trabajo (5), propagación de errores bien ejecutada (8), intervalos de confianza (4), análisis de sensibilidad (3) |
| **6. Simulación e inferencia** | 15 pts | Simulación correcta (3), re-análisis completo (5), cálculo de ΔU y Q (4), interpretación termodinámica (3) |
| **7. Conclusiones** | 10 pts | Claridad y coherencia (3), profundidad del análisis (3), pensamiento crítico (2), redacción técnica (2) |
| **Presentación general** | -5 pts | Código limpio y comentado, organización lógica, gráficas con etiquetas, sin errores de ejecución |

### Escala de calificación:
- **100-110 pts**: Excelente (10) - Análisis profundo, interpretación sofisticada
- **90-99 pts**: Muy bueno (9) - Completo y bien fundamentado
- **80-89 pts**: Bueno (8) - Cumple todos los requisitos básicos
- **70-79 pts**: Satisfactorio (7) - Cumple parcialmente o con errores menores
- **< 70 pts**: Insuficiente - Trabajo incompleto o con errores graves

---

## 📎 FORMATO DE ENTREGA

### 📧 Entrega por Microsoft Teams

**Fecha límite**: [DEFINE LA FECHA - sugerencia: 3 días hábiles]

**Formato**: Subir a la **Asignación de Teams** correspondiente

### 📂 Archivos a entregar:

1. **Notebook de Google Colab** (`.ipynb`)
   - Descárgalo desde Colab: File → Download → Download .ipynb
   - **IMPORTANTE**: Asegúrate de que todas las celdas estén ejecutadas antes de descargar
   
2. **Archivo de datos consolidados**: `datos_completos.csv`

3. **PDF del notebook** (opcional pero recomendado)
   - En Colab: File → Print → Guardar como PDF
   - Facilita la revisión si hay problemas de compatibilidad

### 📝 Estructura esperada del notebook:

```
# Proyecto Integrador - Análisis Termodinámico
# Nombre(s): [Tu nombre o nombres del equipo]
# Fecha: [Fecha de entrega]

## Introducción
[Breve descripción del experimento]

## Etapa 1: Estadística Descriptiva
[Código, tablas, gráficas, interpretación]

## Etapa 2: Análisis de Correlación
[Código, resultados, interpretación]

## Etapa 3: Regresión Lineal P-T
[Código, visualizaciones, análisis]

## Etapa 4: Análisis Temporal P-t
[Código, resultados, interpretación]

## Etapa 5: Trabajo Mecánico e Incertidumbre
[Cálculos, propagación de errores, discusión]

## Etapa 6: Simulación e Inferencia Termodinámica
[Simulación, re-análisis, Primera Ley]

## Etapa 7: Conclusiones
[Síntesis integrada del proyecto]

## Referencias
[Libros, documentación de Python, etc.]
```

### ✅ Checklist pre-entrega:

- [ ] Todas las celdas de código se ejecutan sin errores
- [ ] Las gráficas tienen títulos, etiquetas en ejes y leyendas cuando es necesario
- [ ] El código está comentado y es legible
- [ ] Se responden TODAS las preguntas de análisis
- [ ] Las conclusiones integran resultados de todas las etapas
- [ ] El archivo `datos_completos.csv` está incluido
- [ ] Nombres de los autores están claramente indicados
- [ ] El formato es profesional y organizado

---

## 🛠️ HERRAMIENTAS Y RECURSOS

### 📚 Librerías de Python recomendadas:

```python
import pandas as pd              # Manipulación de datos
import numpy as np               # Operaciones numéricas
import matplotlib.pyplot as plt  # Visualizaciones
import seaborn as sns            # Visualizaciones estadísticas
from scipy import stats          # Pruebas estadísticas
from scipy.optimize import curve_fit  # Ajuste de curvas (opcional)
```

### 📖 Recursos de ayuda:

**Documentación oficial:**
- [Pandas](https://pandas.pydata.org/docs/)
- [Matplotlib](https://matplotlib.org/stable/contents.html)
- [SciPy Stats](https://docs.scipy.org/doc/scipy/reference/stats.html)

**Tutoriales útiles:**
- Google Colab: [Guía básica](https://colab.research.google.com/notebooks/basic_features_overview.ipynb)
- Pandas: `.groupby()`, `.agg()`, `.pivot_table()`
- Matplotlib: subplots, personalización de gráficas
- SciPy: correlaciones, regresión, pruebas de normalidad

### 💡 Tips para Google Colab:

1. **Montar Google Drive** para guardar tu trabajo:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

2. **Subir archivos temporalmente**:
   ```python
   from google.colab import files
   uploaded = files.upload()
   ```

3. **Mantener la sesión activa**: Colab desconecta después de 90 minutos de inactividad. Guarda tu trabajo frecuentemente.

4. **Instalar librerías adicionales** (si es necesario):
   ```python
   !pip install nombre_libreria
   ```

5. **Ver DataFrames grandes**: Usa `df.head()`, `df.tail()`, o ajusta las opciones de visualización:
   ```python
   pd.set_option('display.max_columns', None)
   pd.set_option('display.max_rows', 100)
   ```

---

## 🎯 APRENDIZAJES ESPERADOS

Al completar este proyecto, habrás desarrollado habilidades para:

### 📊 Estadística aplicada:
- ✅ Aplicar medidas de tendencia central y dispersión a datos experimentales
- ✅ Identificar y manejar valores atípicos
- ✅ Calcular e interpretar coeficientes de correlación
- ✅ Realizar regresiones lineales y evaluar su calidad
- ✅ Aplicar pruebas de normalidad e hipótesis
- ✅ Propagar incertidumbres en cálculos derivados

### 🔬 Análisis de datos experimentales:
- ✅ Consolidar múltiples datasets en un análisis unificado
- ✅ Evaluar la calidad y reproducibilidad de mediciones
- ✅ Visualizar datos de manera efectiva para comunicar resultados
- ✅ Distinguir entre variabilidad aleatoria y tendencias reales

### 🌡️ Termodinámica aplicada:
- ✅ Relacionar mediciones experimentales con principios teóricos
- ✅ Calcular trabajo mecánico en procesos termodinámicos
- ✅ Aplicar la Primera Ley de la Termodinámica
- ✅ Identificar tipos de procesos (isotérmico, adiabático, politrópico)
- ✅ Evaluar balances de energía con datos reales

### 💻 Programación científica:
- ✅ Manipular y analizar datos con pandas
- ✅ Crear visualizaciones profesionales con matplotlib/seaborn
- ✅ Usar librerías científicas (NumPy, SciPy)
- ✅ Documentar y organizar código reproducible

### 🧠 Pensamiento crítico:
- ✅ Interpretar resultados en contexto físico y estadístico
- ✅ Identificar limitaciones experimentales y analíticas
- ✅ Proponer mejoras a diseños experimentales
- ✅ Comunicar hallazgos técnicos de manera clara

---

## ❓ PREGUNTAS FRECUENTES (FAQ)

### 🤔 Sobre los datos:

**P: ¿Qué hago si encuentro valores que parecen errores de medición?**  
R: Documéntalos como outliers usando métodos estadísticos (IQR, Z-score). Decide si los excluyes o mantienes, pero justifica tu decisión. En ciencia real, no eliminamos datos solo porque no nos gustan.

**P: ¿Por qué la temperatura casi no cambió?**  
R: El proceso fue rápido (~10 segundos) y el aire tiene baja capacidad térmica. Además, pudo haber intercambio de calor con el ambiente. Esto NO es un error, es una observación válida que debes analizar.

**P: ¿Tengo que usar los 10 datasets para todo?**  
R: Sí, el análisis debe incluir todos. Sin embargo, para algunas visualizaciones puedes mostrar solo ejemplos representativos para no saturar las gráficas.

### 🤔 Sobre el análisis:

**P: Mi correlación P-T es muy débil. ¿Hice algo mal?**  
R: Probablemente no. Si la temperatura varió poco, es normal que la correlación sea débil. Analiza por qué ocurrió esto y qué otras relaciones son más informativas (como P-t).

**P: ¿Cómo sé si mi R² es "bueno"?**  
R: Depende del contexto. En datos experimentales con ruido, R² > 0.7 es bueno. Pero más importante que el valor es entender QUÉ significa. Un R² bajo puede indicar que el modelo lineal no es apropiado.

**P: ¿Tengo que programar todo desde cero?**  
R: No. Usa las funciones de pandas, NumPy y SciPy. El objetivo es que ENTIENDAS qué estás calculando, no que reinventes la rueda. Pero sí debes saber interpretar los resultados.

**P: ¿Qué hacer si mis pendientes NO siguen distribución normal?**  
R: Está bien, documéntalo. Usa estadísticos robustos (mediana en lugar de media) o explica qué factores podrían causar la no-normalidad.

### 🤔 Sobre la programación:

**P: ¿Puedo usar ChatGPT u otras IA para ayudarme con el código?**  
R: Si, no es una clase de programación, pueden apoyarse de la herramienta y sobre todo usarla para depurar errores o aprender sintaxis, pero DEBES entender el código que entregas. Será evidente si copias sin comprender.

**P: No me funciona una librería en Colab. ¿Qué hago?**  
R: Primero intenta `!pip install --upgrade nombre_libreria`. Si persiste el problema, busca el mensaje de error en Google/Stack Overflow, o usa la documentación oficial. Aprende a depurar por tu cuenta.

**P: ¿Cómo hago que mis gráficas se vean profesionales?**  
R: Incluye siempre:
- Títulos descriptivos
- Etiquetas en los ejes con unidades
- Leyendas cuando hay múltiples series
- Tamaño de fuente legible (`plt.rcParams['font.size'] = 12`)
- Colores distinguibles
---

## 🎓 POLÍTICAS ACADÉMICAS

### 📋 Integridad académica:

- ✅ **Está permitido**: Consultar documentación, tutoriales, discutir conceptos con compañeros, usar IA para depurar código
- ❌ **NO está permitido**: Copiar código completo de otros equipos, presentar trabajo ajeno como propio, compartir tu notebook completo con otros

### 👥 Colaboración vs Copia:

**Colaboración aceptable:**
- "¿Cómo interpretas tú este resultado?"
- "¿Qué función de pandas usaste para agrupar datos?"
- "Mi gráfica no se ve bien, ¿alguna sugerencia?"

**Copia no aceptable:**
- Compartir notebooks completos
- Copiar código sin entender qué hace
- Dividir el trabajo sin que ambos entiendan todo

### ⚠️ Consecuencias:

El plagio o deshonestidad académica resultará en:
1. Calificación de 0 en el proyecto
2. Reporte al departamento académico
3. Posibles consecuencias adicionales según el reglamento institucional

**Recuerda**: El objetivo es que APRENDAS, no solo que completes la tarea.

---
 

## 🏆 CRITERIOS DE EXCELENCIA

¿Quieres una calificación sobresaliente? Ve más allá de lo básico:

### Para un 9-10 excepcional:

- 📊 **Análisis profundo**: No solo calcules, interpreta con profundidad física y estadística
- 🎨 **Visualizaciones impecables**: Gráficas que comuniquen claramente tus hallazgos
- 🔍 **Pensamiento crítico**: Identifica limitaciones, propón mejoras, cuestiona supuestos
- 📝 **Documentación ejemplar**: Código limpio, comentado, reproducible
- 🧪 **Rigor científico**: Citas apropiadas, unidades correctas, redacción técnica precisa
- 💡 **Creatividad**: Análisis adicionales relevantes (sin salirte del tema)

### Señales de excelencia:

- Tus conclusiones conectan resultados de múltiples etapas de manera coherente
- Usas evidencia cuantitativa para respaldar cada afirmación
- Identificas cuando algo no tiene sentido y explicas por qué
- Tu código es lo suficientemente claro que alguien más podría reproducir tu análisis
- Propones mejoras experimentales específicas y factibles

-- 
## 📚 REFERENCIAS BIBLIOGRÁFICAS

### Libros de texto recomendados:

**Termodinámica:**
- Çengel, Y. A., & Boles, M. A. (2015). *Thermodynamics: An Engineering Approach*. McGraw-Hill.
- Moran, M. J., Shapiro, H. N. (2010). *Fundamentals of Engineering Thermodynamics*. Wiley.

**Estadística:**
- Montgomery, D. C., & Runger, G. C. (2018). *Applied Statistics and Probability for Engineers*. Wiley.
- Devore, J. L. (2015). *Probability and Statistics for Engineering and the Sciences*. Cengage.

**Análisis de errores:**
- Taylor, J. R. (1997). *An Introduction to Error Analysis: The Study of Uncertainties in Physical Measurements*. University Science Books.

### Recursos en línea:

**Python y análisis de datos:**
- [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/) - Jake VanderPlas
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/index.html)
- [SciPy Stats Tutorial](https://docs.scipy.org/doc/scipy/tutorial/stats.html)

**Estadística aplicada:**
- [Seeing Theory](https://seeing-theory.brown.edu/) - Visualización interactiva de conceptos estadísticos
- [StatQuest with Josh Starmer](https://www.youtube.com/c/joshstarmer) - Videos explicativos

---

## 🎯 MENSAJE FINAL

Este proyecto es una oportunidad para aplicar herramientas de probabilidad y estadística a un problema real de ingeniería. Los datos provienen de un experimento genuino con limitaciones reales, no de un problema idealizado de libro de texto.

**Algunas cosas que aprenderás:**

✓ No todos los experimentos dan los resultados "perfectos" que esperabas  
✓ Los datos reales tienen ruido, variabilidad y sorpresas  
✓ La estadística te ayuda a extraer información valiosa incluso de datos imperfectos  
✓ La incertidumbre es inherente a la medición y debe cuantificarse  
✓ El análisis crítico es más valioso que solo "hacer cálculos"  

**El objetivo NO es que todos obtengan los mismos números**, sino que desarrollen criterio para:
- Evaluar la calidad de datos experimentales
- Seleccionar métodos de análisis apropiados
- Interpretar resultados en contexto físico y estadístico
- Comunicar hallazgos de manera clara y honesta

**¿Tus resultados no son "bonitos"?** Perfecto. La ciencia real trata sobre entender QUÉ pasó y POR QUÉ, no sobre obtener números predeterminados.
 
---

**¡Éxito en tu proyecto!** 🚀
Si tienes dudas, no esperes al último momento. La planificación y el trabajo constante son claves para un resultado excelente.
