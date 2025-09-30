# 📋 Template de Documentación de Experimento

Use este template para documentar cada serie de experimentos realizados.

---

## Información General

- **Fecha:** YYYY-MM-DD
- **Experimentador:** [Nombre]
- **Objetivo:** [Descripción breve del objetivo del experimento]
- **Número de Serie:** [Ej: EXP-001]

---

## Configuración del Sistema

### Hardware

- **Actuador Lineal:** [Modelo, voltaje, carrera]
- **Fuente de Alimentación:** [Voltaje, corriente]
- **Sensor de Presión:** MPX5700AP
- **Volumen de Jeringa:** [mL]
- **Temperatura Ambiente:** [°C]
- **Presión Atmosférica:** [kPa]

### Software

- **Duración del Movimiento:** [ms]
- **Frecuencia de Muestreo:** [Hz o cada X ms]
- **Versión del Código Arduino:** [Ej: v1.0, commit hash]
- **Versión de la Interfaz Python:** [Ej: v1.0]

---

## Condiciones Iniciales

- **Volumen Inicial del Gas:** [mL]
- **Presión Inicial:** [kPa]
- **Temperatura Inicial:** [°C]
- **Estado del Sistema:** [Ej: sellado, con válvula abierta, etc.]

### Notas sobre el Setup

[Cualquier observación relevante sobre la configuración física del experimento]

---

## Experimentos Realizados

### Experimento 1: [Nombre Descriptivo]

**Archivo CSV:** `presion_extension_YYYYMMDD_HHMMSS.csv`

#### Parámetros
- Tipo: Extensión / Retracción
- Duración: [ms]
- Velocidad del actuador: [% PWM o mm/s]

#### Observaciones
[Describir lo observado durante el experimento]

#### Resultados
- Presión Inicial: [kPa]
- Presión Final: [kPa]
- Cambio de Presión (ΔP): [kPa]
- Presión Máxima: [kPa]
- Presión Mínima: [kPa]

#### Gráfica
![Gráfica Experimento 1](ruta/a/grafica.png)

---

### Experimento 2: [Nombre Descriptivo]

**Archivo CSV:** `presion_retraccion_YYYYMMDD_HHMMSS.csv`

#### Parámetros
- Tipo: Extensión / Retracción
- Duración: [ms]
- Velocidad del actuador: [% PWM o mm/s]

#### Observaciones
[Describir lo observado durante el experimento]

#### Resultados
- Presión Inicial: [kPa]
- Presión Final: [kPa]
- Cambio de Presión (ΔP): [kPa]
- Presión Máxima: [kPa]
- Presión Mínima: [kPa]

#### Gráfica
![Gráfica Experimento 2](ruta/a/grafica.png)

---

## Análisis de Resultados

### Cálculos Termodinámicos

#### Trabajo Realizado (W)
```
W = ∫P dV
W ≈ [Valor calculado] J
```

#### Cambio de Energía Interna (ΔU)
```
Para proceso adiabático: ΔU = -W
ΔU ≈ [Valor calculado] J
```

#### Relación PV^γ (proceso adiabático)
```
P₁V₁^γ = P₂V₂^γ
γ calculado ≈ [valor]
γ teórico (aire) ≈ 1.4
Error: [%]
```

### Verificación de la Primera Ley

```
ΔU = Q - W
[Desarrollar cálculos]
```

### Gráficas Comparativas

#### Presión vs Tiempo (Extensión vs Retracción)
![Comparación](ruta/a/comparacion.png)

#### Diagrama P-V
![Diagrama PV](ruta/a/pv_diagram.png)

---

## Observaciones y Anomalías

### Problemas Encontrados

1. [Describir cualquier problema técnico]
2. [Describir lecturas anómalas]
3. [Describir fallos del sistema]

### Soluciones Aplicadas

1. [Cómo se resolvió cada problema]

---

## Conclusiones

### Cumplimiento de Objetivos

- ✅ / ❌ Objetivo 1: [Descripción]
- ✅ / ❌ Objetivo 2: [Descripción]
- ✅ / ❌ Objetivo 3: [Descripción]

### Interpretación de Resultados

[Interpretar los resultados en el contexto de la Primera Ley de la Termodinámica]

### Validación de Hipótesis

[¿Se comprobó la hipótesis inicial?]

---

## Mejoras Sugeridas

### Para el Hardware

1. [Sugerencia 1]
2. [Sugerencia 2]

### Para el Software

1. [Sugerencia 1]
2. [Sugerencia 2]

### Para el Procedimiento

1. [Sugerencia 1]
2. [Sugerencia 2]

---

## Próximos Pasos

- [ ] Repetir experimento con [condición modificada]
- [ ] Implementar [mejora sugerida]
- [ ] Analizar [aspecto específico]
- [ ] Documentar [hallazgo particular]

---

## Referencias

1. [Libro/Paper relevante]
2. [Fórmulas utilizadas]
3. [Documentación de componentes]

---

## Anexos

### Datos Crudos

- Archivos CSV: `datos/[lista de archivos]`
- Archivos de gráficas: `docs/graficas/[lista]`

### Código Utilizado

- Versión Arduino: [commit hash o tag]
- Versión Python: [commit hash o tag]
- Scripts de análisis personalizados: [si aplica]

### Fotografías del Setup

![Setup Experimental](ruta/a/foto1.jpg)
![Detalle del Sensor](ruta/a/foto2.jpg)

---

## Metadata del Experimento

```yaml
experimento_id: EXP-001
fecha: 2024-09-30
duracion_total: 45 min
numero_pruebas: 5
pruebas_exitosas: 5
pruebas_fallidas: 0
version_sistema: v1.0
```

---

**Documentado por:** [Nombre]  
**Revisado por:** [Nombre] (si aplica)  
**Fecha de documentación:** YYYY-MM-DD

---

## Checklist de Documentación

- [ ] Información general completada
- [ ] Configuración del sistema documentada
- [ ] Todos los experimentos listados con archivos CSV
- [ ] Observaciones registradas
- [ ] Cálculos termodinámicos realizados
- [ ] Gráficas incluidas
- [ ] Conclusiones escritas
- [ ] Archivos respaldados
- [ ] Commit a GitHub realizado

---

**Repositorio:** https://github.com/obieuan/laboratorioTermodinamica  
**Template Version:** 1.0