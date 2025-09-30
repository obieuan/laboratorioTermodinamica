# 📘 Primera Ley de la Termodinámica

## Sistema de Caracterización con Actuador Lineal

Este proyecto permite la caracterización experimental de la **Primera Ley de la Termodinámica** (ΔU = Q - W) mediante compresión y expansión controlada de gases.

---

## 🎯 Objetivo

Demostrar y caracterizar la Primera Ley de la Termodinámica mediante:
- Compresión adiabática de aire (extensión del actuador)
- Expansión adiabática de aire (retracción del actuador)
- Medición precisa de presión durante el proceso
- Cálculo del trabajo termodinámico realizado
- Validación de ΔU = Q - W

---

## 🔧 Componentes Específicos

### Hardware
- Arduino Mega 2560
- BTS7960 43A (H-Bridge)
- Actuador lineal DC 12/24V
- MPX5700AP (sensor de presión)
- Jeringa calibrada
- Válvulas neumáticas
- Capacitores de desacoplo (0.1µF + 10µF)

### Software
- Código Arduino (`arduino/control_actuador/`)
- Interfaz Python (`python/interfaz_control.py`)
- Scripts de análisis (`ejemplos/analisis_basico.py`)

---

## 📂 Estructura del Proyecto

```
primeraley/
│
├── README_PRIMERALEY.md          # Este archivo
│
├── arduino/
│   └── control_actuador/
│       └── control_actuador.ino  # Control del actuador y sensores
│
├── python/
│   └── interfaz_control.py       # GUI para control y registro
│
├── ejemplos/
│   └── analisis_basico.py        # Análisis de datos experimentales
│
├── datos/
│   ├── README.md
│   ├── .gitkeep
│   └── ejemplo_extension.csv     # Datos de ejemplo
│
└── docs/
    ├── datasheets/               # PDFs de componentes
    ├── diagramas/                # Esquemas del circuito
    └── experimentos/             # Documentación de experimentos
```

---

## 🚀 Inicio Rápido

### 1. Instalación

```bash
# Desde el directorio raíz del repositorio
cd termodinamica/primeraley

# Instalar dependencias
pip install -r ../requirements.txt
```

### 2. Cargar Arduino

1. Abrir `arduino/control_actuador/control_actuador.ino`
2. Seleccionar Arduino Mega 2560
3. Compilar y cargar

### 3. Ejecutar Interfaz

```bash
python python/interfaz_control.py
```

### 4. Realizar Experimento

1. Conectar al puerto COM del Arduino
2. Configurar tiempo de movimiento (ej: 10000 ms)
3. Presionar "EXTENDER" o "RETRAER"
4. Los datos se guardan automáticamente en `datos/`

---

## 📊 Fundamento Teórico

### Primera Ley de la Termodinámica

```
ΔU = Q - W
```

Donde:
- **ΔU**: Cambio en energía interna
- **Q**: Calor transferido al sistema
- **W**: Trabajo realizado por el sistema

### Proceso Adiabático

En un proceso adiabático (Q = 0):
```
ΔU = -W
PV^γ = constante
```

Donde γ (gamma) = Cp/Cv ≈ 1.4 para aire

### Trabajo Termodinámico

```
W = ∫ P dV
```

Calculado mediante integración numérica de los datos de presión vs volumen.

---

## 📈 Tipos de Experimentos

### 1. Compresión Adiabática (Extensión)

- **Archivo**: `presion_extension_YYYYMMDD_HHMMSS.csv`
- **Proceso**: Actuador extiende → pistón empuja → aire se comprime
- **Resultado esperado**: Aumento de presión
- **Trabajo**: W < 0 (el sistema hace trabajo sobre el gas)

### 2. Expansión Adiabática (Retracción)

- **Archivo**: `presion_retraccion_YYYYMMDD_HHMMSS.csv`
- **Proceso**: Actuador retrae → pistón jala → aire se expande
- **Resultado esperado**: Disminución de presión
- **Trabajo**: W > 0 (el gas hace trabajo sobre el entorno)

---

## 🔬 Procedimiento Experimental

### Setup Inicial

1. **Verificar conexiones hardware**
2. **Calibrar presión inicial** (debe leer ~101.3 kPa)
3. **Verificar sellado** del sistema neumático
4. **Configurar tiempo** apropiado (5000-10000 ms recomendado)

### Ejecución

1. Iniciar interfaz de control
2. Conectar al Arduino
3. Configurar parámetros
4. Ejecutar experimento (Extender o Retraer)
5. Esperar finalización automática
6. Revisar archivo CSV generado

### Análisis

```bash
cd ejemplos
python analisis_basico.py
```

El script genera:
- Estadísticas básicas (P inicial, final, máx, mín, promedio)
- Gráficas P vs tiempo
- Cálculo de trabajo termodinámico
- Comparación entre experimentos

---

## 📐 Ecuaciones Utilizadas

### Conversión de Sensor

```python
V_out = sensorValue * (5.0 / 1023.0)
P_kPa = ((V_out - 0.2) * (700 - 0)) / (4.7 - 0.2) + 0
```

### Trabajo Termodinámico

```python
# Integración trapezoidal
W = ∫ P dV ≈ Σ ((P[i] + P[i+1])/2) * ΔV
```

### Cambio de Energía Interna (adiabático)

```python
ΔU = -W = -∫ P dV
```

---

## 📊 Resultados Esperados

### Compresión

- **P inicial**: ~101.3 kPa (presión atmosférica)
- **P final**: 150-250 kPa (depende del volumen)
- **ΔP**: +50 a +150 kPa
- **Trabajo**: Negativo (se comprime el gas)

### Expansión

- **P inicial**: Depende del experimento previo
- **P final**: ~101.3 kPa
- **ΔP**: -50 a -150 kPa
- **Trabajo**: Positivo (el gas se expande)

---

## 🐛 Troubleshooting

### Presión no cambia

- Verificar sellado del sistema
- Revisar conexión del sensor (pin A0)
- Verificar alimentación del sensor (5V)

### Actuador no se mueve

- Verificar alimentación de potencia (12/24V)
- Revisar conexiones BTS7960
- Verificar que R_EN y L_EN estén en HIGH

### CSV vacío

- Verificar que Arduino envíe "completada"
- Revisar comunicación serial
- Aumentar tiempo de operación

---

## 📚 Referencias

1. Cengel, Y. A., & Boles, M. A. (2015). *Thermodynamics: An Engineering Approach*
2. [MPX5700AP Datasheet](https://www.nxp.com/docs/en/data-sheet/MPX5700.pdf)
3. [Arduino Mega 2560 Reference](https://docs.arduino.cc/hardware/mega-2560)

---

## 🎓 Para Estudiantes

### Preguntas de Análisis

1. ¿Cómo se relaciona el cambio de presión con el trabajo realizado?
2. ¿Por qué asumimos el proceso como adiabático?
3. ¿Qué efecto tiene la velocidad del actuador en los resultados?
4. ¿Cómo se compara γ experimental vs teórico?
5. ¿Qué fuentes de error existen en el experimento?

### Ejercicios Propuestos

1. Calcular el trabajo para diferentes volúmenes iniciales
2. Determinar γ experimental y comparar con el teórico
3. Graficar diagrama P-V completo (compresión + expansión)
4. Estimar la temperatura final usando la ley de gases ideales
5. Calcular la eficiencia del proceso

---

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/obieuan/laboratorioTermodinamica/issues)
- **Documentación general**: Ver README.md principal
- **Setup**: Ver SETUP.md en el directorio raíz

---

**Proyecto**: Primera Ley de la Termodinámica  
**Repositorio**: https://github.com/obieuan/laboratorioTermodinamica  
**Autor**: @obieuan