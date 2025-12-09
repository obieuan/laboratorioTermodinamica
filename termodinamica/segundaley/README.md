# 📗 Segunda Ley de la Termodinámica

## 🚀 Intercambiador de Calor de Placas - Sistema de Caracterización Térmica

Este proyecto implementa un sistema experimental para el estudio de la **Segunda Ley de la Termodinámica** mediante un intercambiador de calor de placas. El sistema permite caracterizar transferencia de calor, calcular cambios de entropía y analizar la eficiencia térmica en tiempo real.

---

## 🎯 Objetivos

1. **Caracterización de Intercambiador**: Medir efectividad y eficiencia del intercambiador de calor de placas
2. **Análisis de Entropía**: Calcular generación de entropía en ambos circuitos (caliente y frío)
3. **Procesos Irreversibles**: Cuantificar irreversibilidades en transferencia de calor
4. **Balance Térmico**: Validar conservación de energía y aumento de entropía
5. **Eficiencia NTU-ε**: Determinar número de unidades de transferencia y efectividad

---

## 📋 Fundamento Teórico

### Intercambiador de Calor

Un intercambiador de calor de placas permite transferencia térmica entre dos fluidos sin mezclarlos directamente.

**Balance de Energía:**
```
Q̇_caliente = ṁ_h · cp · (T_h,in - T_h,out)
Q̇_frío = ṁ_c · cp · (T_c,out - T_c,in)
```

**Efectividad (ε):**
```
ε = Q̇_real / Q̇_max
```

Donde:
```
Q̇_max = (ṁ·cp)_min · (T_h,in - T_c,in)
```

### Segunda Ley y Entropía

**Cambio de entropía para cada fluido:**
```
ΔS_caliente = ṁ_h · cp · ln(T_h,out / T_h,in)  [negativo, pierde calor]
ΔS_frío = ṁ_c · cp · ln(T_c,out / T_c,in)      [positivo, gana calor]
```

**Generación de entropía (irreversibilidad):**
```
Ṡ_gen = ΔṠ_total = ΔṠ_caliente + ΔṠ_frío > 0
```

Para procesos reversibles ideales:
```
Ṡ_gen = 0  (imposible en sistemas reales)
```

### Número de Unidades de Transferencia (NTU)

```
NTU = UA / (ṁ·cp)_min
```

Donde:
- U: Coeficiente global de transferencia de calor
- A: Área de transferencia
- (ṁ·cp)_min: Menor capacidad térmica

**Relación NTU-ε** (contraflujo):
```
ε = [1 - exp(-NTU·(1-C))] / [1 - C·exp(-NTU·(1-C))]

C = (ṁ·cp)_min / (ṁ·cp)_max
```

---

## 🔧 Descripción del Sistema

### Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                    SISTEMA COMPLETO                          │
└─────────────────────────────────────────────────────────────┘

CIRCUITO CALIENTE (Lado Primario):
┌──────────┐      ┌───────┐      ┌─────────────────┐      ┌──────────┐
│ CUBETA 1 │──────│ BOMBA │──────│  INTERCAMBIADOR │──────│ CUBETA 2 │
│  (Agua   │  Q1  │   1   │      │   DE CALOR DE   │      │ (Agua    │
│ Caliente)│      │       │      │     PLACAS      │      │ Templada)│
│  T1      │      │       │      │                 │      │  T2      │
└──────────┘      └───────┘      │    ║ ║ ║ ║     │      └──────────┘
                                 │                 │
CIRCUITO FRÍO (Lado Secundario): │                 │
┌──────────┐      ┌───────┐      │                 │
│ CUBETA 3 │──┐   │ BOMBA │──────│                 │
│  (Agua   │  │   │   2   │      │                 │
│  Fría)   │  │   │       │      │                 │
│  T3      │  │   └───────┘      └─────────────────┘
└──────────┘  │        Q2
              │
              └────────────────────┘
              (Recirculación)

LEYENDA:
T1 = Temperatura entrada circuito caliente (Sensor 1, Pin 11)
T2 = Temperatura salida circuito caliente (Sensor 2, Pin 12)
T3 = Temperatura circuito frío (Sensor 3, Pin 4)
Q1 = Caudal circuito caliente (Caudalímetro 1, Pin 2)
Q2 = Caudal circuito frío (Caudalímetro 2, Pin 3)
```

### Componentes del Sistema

#### Cubeta 1 - Reservorio Caliente
- **Función**: Almacén de agua caliente
- **Sensor**: DS18B20 #1 (Pin 11) - Temperatura inicial T_h,in
- **Actuador**: Bomba 1 + BTS7960
- **Caudalímetro**: YF-S201 #1 (Pin 2) - Flujo circuito caliente

#### Cubeta 2 - Reservorio de Salida Caliente
- **Función**: Recepción de agua enfriada del intercambiador
- **Sensor**: DS18B20 #2 (Pin 12) - Temperatura salida T_h,out
- **Nota**: No tiene bomba, recibe por gravedad/presión

#### Cubeta 3 - Reservorio Frío
- **Función**: Almacén de agua fría en recirculación
- **Sensor**: DS18B20 #3 (Pin 4) - Temperatura circuito frío T_c
- **Actuador**: Bomba 2 + BTS7960
- **Caudalímetro**: YF-S201 #2 (Pin 3) - Flujo circuito frío
- **Nota**: Sistema cerrado de recirculación

#### Intercambiador de Calor de Placas
- **Tipo**: Placas paralelas (contraflujo o flujo cruzado)
- **Función**: Transferir calor de circuito caliente a circuito frío
- **Entrada caliente**: Desde Cubeta 1 (T_h,in)
- **Salida caliente**: Hacia Cubeta 2 (T_h,out)
- **Circuito frío**: Desde/hacia Cubeta 3 (T_c)

---

## 🔧 Hardware Implementado

### Sistema de Control Principal

- **Microcontrolador**: Arduino Nano (ATmega328P)
- **Frecuencia de muestreo**: 10 Hz (100ms entre lecturas)
- **Baudrate**: 115200 bps
- **Alimentación**: 5V USB + 12V para bombas

### Sensores de Temperatura (3x DS18B20)

| Sensor | Ubicación | Pin | Medición | Rango |
|--------|-----------|-----|----------|-------|
| DS18B20 #1 | Cubeta 1 | 11 | T_h,in (entrada caliente) | -55°C a +125°C |
| DS18B20 #2 | Cubeta 2 | 12 | T_h,out (salida caliente) | -55°C a +125°C |
| DS18B20 #3 | Cubeta 3 | 4 | T_c (circuito frío) | -55°C a +125°C |

**Especificaciones**:
- Precisión: ±0.5°C
- Resolución configurada: 9 bits (93.75 ms)
- Protocolo: 1-Wire
- Alimentación: 3.0V - 5.5V

### Caudalímetros (2x YF-S201)

| Caudalímetro | Circuito | Pin | Medición | Rango |
|--------------|----------|-----|----------|-------|
| YF-S201 #1 | Caliente | 2 (INT0) | ṁ_h (flujo lado caliente) | 1-30 L/min |
| YF-S201 #2 | Frío | 3 (INT1) | ṁ_c (flujo lado frío) | 1-30 L/min |

**Especificaciones**:
- Factor K: 7.11 pulsos/L
- Salida: Pulsos digitales (Hall effect)
- Precisión: ±3%
- Presión máxima: 1.75 MPa

### Sistema de Bombeo (2x BTS7960)

#### Bomba 1 - Circuito Caliente
- **Driver**: BTS7960 Módulo 1
- **Control**:
  - R_EN: Pin 7 (Enable derecho)
  - L_EN: Pin 8 (Enable izquierdo)
  - RPWM: Pin 5 (PWM sentido horario)
- **Velocidad configurada**: 200/255 (~78%)
- **Función**: Impulsar agua caliente hacia intercambiador

#### Bomba 2 - Circuito Frío
- **Driver**: BTS7960 Módulo 2
- **Control**:
  - R_EN: Pin 9
  - L_EN: Pin 10
  - RPWM: Pin 6 (PWM)
- **Velocidad configurada**: 180/255 (~71%)
- **Función**: Recircular agua fría a través del intercambiador

**Especificaciones BTS7960**:
- Corriente máxima: 43A
- Voltaje: 5.5V - 27V
- Control PWM: 0-255
- Protección térmica integrada

---

## 💻 Software Desarrollado

### Firmware Arduino

**Archivo**: `arduino/control_sistema.ino`

**Funciones Principales**:
```cpp
// Lectura continua de temperaturas
void leerTemperaturas() {
  T1 = sensor1.getTempCByIndex(0);  // Entrada caliente
  T2 = sensor2.getTempCByIndex(0);  // Salida caliente
  T3 = sensor3.getTempCByIndex(0);  // Circuito frío
}

// Cálculo de caudales mediante interrupciones
void CalcularCaudalesYVolumenes(float dt_s) {
  caudal1 = frecuencia1 / factor_K;  // L/min circuito caliente
  caudal2 = frecuencia2 / factor_K;  // L/min circuito frío
}

// Control de bombas
void controlarBombas() {
  analogWrite(RPWM1, SPEED1);  // Bomba circuito caliente
  analogWrite(RPWM2, SPEED2);  // Bomba circuito frío
}
```

**Características**:
- ✅ Adquisición sincronizada de 3 temperaturas
- ✅ Medición dual de caudal con interrupciones
- ✅ Control PWM independiente de bombas
- ✅ Cálculo de volúmenes acumulados
- ✅ Comando 'r' para reset
- ✅ Salida estructurada cada 100ms

**Librerías**:
- `OneWire.h` - Protocolo 1-Wire
- `DallasTemperature.h` - Driver DS18B20

### Interfaz de Monitoreo Python

**Archivo**: `python/interfaz_monitor.py`

**Características**:
- ✅ **Panel de Temperaturas**:
  - T1: Entrada circuito caliente
  - T2: Salida circuito caliente  
  - T3: Circuito frío
  - Visualización con displays de 20pt

- ✅ **Panel de Caudales**:
  - Caudal instantáneo (L/min)
  - Volumen acumulado (L)
  - Ambos circuitos simultáneamente

- ✅ **Panel de Bombas**:
  - Estado en tiempo real
  - Botón de reset de volúmenes

- ✅ **Gráficas Dinámicas**:
  - Temperaturas vs Tiempo (T1, T2, T3)
  - Caudales vs Tiempo (Q1, Q2)
  - Historial de 50 puntos (~5 segundos)

**Tecnologías**:
- `tkinter` - Interfaz gráfica
- `pyserial` - Comunicación serial
- `matplotlib` - Visualización

---

## 🔬 Experimentos y Análisis

### 1. Caracterización del Intercambiador

**Objetivo**: Determinar coeficiente UA y efectividad

**Procedimiento**:
1. Establecer flujo estable en ambos circuitos
2. Registrar T1, T2, T3, Q1, Q2 cada 100ms
3. Esperar estado estacionario
4. Calcular calor transferido

**Cálculos**:
```python
# Calor cedido por circuito caliente
Q_hot = m_dot_hot * cp * (T1 - T2)  # W

# Calor ganado por circuito frío
Q_cold = m_dot_cold * cp * (T3_out - T3_in)  # W

# Efectividad
Q_max = (m_dot*cp)_min * (T1 - T3)
epsilon = Q_real / Q_max

# Coeficiente UA
UA = -ln(1-epsilon) * (m_dot*cp)_min  # W/K
```

### 2. Análisis de Entropía

**Objetivo**: Cuantificar generación de entropía

**Cálculo de cambios de entropía**:
```python
# Propiedades del agua
cp = 4186  # J/(kg·K)
rho = 1000  # kg/m³

# Flujos másicos
m_dot_hot = Q1 * rho / 60  # kg/s
m_dot_cold = Q2 * rho / 60  # kg/s

# Cambio de entropía - circuito caliente (pierde calor)
Delta_S_hot = m_dot_hot * cp * ln(T2/T1)  # W/K (negativo)

# Cambio de entropía - circuito frío (gana calor)
# Nota: T3 es temperatura promedio del sistema recirculante
Delta_S_cold = m_dot_cold * cp * ln(T3_salida/T3_entrada)  # W/K (positivo)

# Generación total de entropía (siempre positiva)
S_gen = Delta_S_hot + Delta_S_cold  # W/K > 0
```

**Interpretación**:
- `S_gen > 0`: Confirma Segunda Ley (proceso irreversible)
- `S_gen → 0`: Mayor reversibilidad (mejor diseño)
- Mayor `S_gen`: Mayor irreversibilidad (pérdidas)

### 3. Balance de Energía

**Objetivo**: Validar Primera Ley

**Verificación**:
```python
# Calor cedido = Calor ganado (idealmente)
Q_hot = m_dot_hot * cp * (T1 - T2)
Q_cold = m_dot_cold * cp * (T3_out - T3_in)

# Pérdidas al ambiente
Q_loss = Q_hot - Q_cold

# Eficiencia de transferencia
eta = Q_cold / Q_hot * 100  # %
```

### 4. Análisis NTU-ε

**Objetivo**: Caracterizar desempeño del intercambiador

**Método**:
```python
# Capacidades térmicas
C_hot = m_dot_hot * cp
C_cold = m_dot_cold * cp
C_min = min(C_hot, C_cold)
C_max = max(C_hot, C_cold)
C_ratio = C_min / C_max

# Efectividad medida
epsilon_measured = Q_actual / (C_min * (T1 - T3))

# Cálculo de NTU
# Para contraflujo:
if C_ratio < 1:
    NTU = ln((1-epsilon*C_ratio)/(1-epsilon)) / (1-C_ratio)
else:
    NTU = epsilon / (1-epsilon)

# Coeficiente UA
UA = NTU * C_min  # W/K
```

### 5. Estudio de Régimen de Flujo

**Objetivo**: Caracterizar flujo (laminar vs turbulento)

**Número de Reynolds**:
```python
# Geometría de tubería
D = 0.015  # m (diámetro típico)
mu = 0.001  # Pa·s (viscosidad agua a 20°C)

# Velocidad
v = Q / (pi * (D/2)**2)  # m/s

# Reynolds
Re = rho * v * D / mu

# Clasificación
if Re < 2300:
    regimen = "Laminar"
elif Re < 4000:
    regimen = "Transición"
else:
    regimen = "Turbulento"
```

---

## 📂 Estructura del Proyecto

```
segundaley/
│
├── README_SEGUNDALEY.md          # Este archivo
│
├── arduino/
│   └── control_sistema/
│       └── control_sistema.ino   # ✅ Firmware completo
│
├── python/
│   ├── interfaz_monitor.py       # ✅ Sistema de monitoreo
│   ├── analisis_entropia.py      # 🔄 Script de análisis
│   └── exportar_datos.py         # 📋 Por desarrollar
│
├── ejemplos/
│   ├── caracterizacion_UA.py     # 📊 Por desarrollar
│   ├── analisis_NTU.py           # 📊 Por desarrollar
│   └── balance_termico.py        # 📊 Por desarrollar
│
├── datos/
│   ├── README.md
│   ├── raw/                      # Datos crudos (.csv)
│   ├── procesados/               # Datos analizados
│   └── experimentos/
│       ├── 2024-12-05_test01/
│       └── plantilla_experimento.md
│
├── docs/
│   ├── diagramas/
│   │   ├── sistema_completo.png  # 📋 Por crear
│   │   ├── circuito_caliente.png
│   │   ├── circuito_frio.png
│   │   └── conexiones_arduino.png
│   ├── datasheets/
│   │   ├── DS18B20.pdf
│   │   ├── YF-S201.pdf
│   │   └── BTS7960.pdf
│   ├── manual_usuario.md         # 📖 Por escribir
│   ├── procedimientos/
│   │   ├── calibracion.md
│   │   ├── experimento_base.md
│   │   └── analisis_datos.md
│   └── teoria/
│       ├── intercambiadores.md
│       ├── segunda_ley.md
│       └── NTU_epsilon.md
│
└── imagenes/
    ├── sistema_montado.jpg       # 📸 Por agregar
    ├── interfaz_funcionando.png
    └── resultados_ejemplo.png
```

---

## 🛠️ Estado del Desarrollo

### ✅ Completado (Hardware & Software Base)

- [x] **Sistema físico ensamblado**
  - [x] 3 cubetas instaladas
  - [x] Intercambiador de calor de placas
  - [x] 2 circuitos hidráulicos independientes
  - [x] Sensores de temperatura instalados
  - [x] Caudalímetros integrados
  
- [x] **Control electrónico**
  - [x] Arduino Nano programado
  - [x] Drivers BTS7960 configurados
  - [x] Sistema de adquisición funcional
  
- [x] **Software de monitoreo**
  - [x] Firmware Arduino completo
  - [x] Interfaz Python con gráficas
  - [x] Comunicación serial estable

### 🔄 En Proceso

- [ ] **Calibración del sistema**
  - [ ] Calibración de sensores de temperatura
  - [ ] Verificación de caudalímetros
  - [ ] Ajuste de velocidades de bombas
  
- [ ] **Validación experimental**
  - [ ] Pruebas de estabilidad térmica
  - [ ] Verificación de balance de energía
  - [ ] Medición de tiempos de respuesta

- [ ] **Desarrollo de análisis**
  - [ ] Script de cálculo de entropía
  - [ ] Algoritmo NTU-ε
  - [ ] Exportación de datos

### 📋 Por Hacer

#### Software
- [ ] Sistema de logging automático (CSV)
- [ ] Análisis automático de entropía
- [ ] Cálculo de UA en tiempo real
- [ ] Detección automática de estado estacionario
- [ ] Exportación a Excel con gráficas
- [ ] Sistema de alertas (temperaturas límite)
- [ ] Control manual de velocidades desde Python

#### Experimentos
- [ ] Protocolo de caracterización completo
- [ ] Matriz de experimentos (diferentes caudales)
- [ ] Estudio de efectividad vs caudal
- [ ] Análisis de irreversibilidades
- [ ] Comparación con modelos teóricos

#### Documentación
- [ ] Manual de operación detallado
- [ ] Guía de análisis de datos
- [ ] Procedimientos de calibración
- [ ] Videos tutoriales
- [ ] Publicación de resultados

---

## 🚀 Inicio Rápido

### Preparación del Sistema

#### 1. Llenado de Cubetas

```
Cubeta 1 (Caliente): Llenar con agua caliente (60-80°C)
Cubeta 2 (Salida):   Inicialmente vacía
Cubeta 3 (Fría):     Llenar con agua fría (15-25°C)
```

#### 2. Verificación de Conexiones

**Sensores de Temperatura:**
```
Pin 11 → Sensor 1 (Cubeta 1 - entrada caliente)
Pin 12 → Sensor 2 (Cubeta 2 - salida caliente)
Pin 4  → Sensor 3 (Cubeta 3 - circuito frío)
```

**Caudalímetros:**
```
Pin 2 → Caudalímetro 1 (circuito caliente)
Pin 3 → Caudalímetro 2 (circuito frío)
```

**Bombas:**
```
Bomba 1 (Pins 5,7,8) → Cubeta 1 → Intercambiador → Cubeta 2
Bomba 2 (Pins 6,9,10) → Cubeta 3 → Intercambiador → Cubeta 3
```

#### 3. Carga de Software

**Arduino:**
```bash
# Abrir Arduino IDE
# Archivo: arduino/control_sistema/control_sistema.ino
# Board: Arduino Nano
# Processor: ATmega328P (Old Bootloader)
# Upload
```

**Python:**
```bash
# Instalar dependencias
pip install pyserial matplotlib

# Ejecutar interfaz
python python/interfaz_monitor.py
```

### Operación Básica

1. **Inicio del Sistema**
   - Conectar Arduino por USB
   - Abrir interfaz Python
   - Seleccionar puerto COM correcto
   - Click en "Conectar"

2. **Verificación Inicial**
   - Confirmar lectura de 3 temperaturas
   - Verificar que bombas no estén activas inicialmente
   - Comprobar comunicación serial

3. **Activación**
   - Bombas se activan automáticamente al conectar
   - Observar flujo de agua en ambos circuitos
   - Verificar lecturas de caudal

4. **Monitoreo**
   - Observar temperaturas en tiempo real
   - Verificar gráficas de tendencias
   - Registrar datos para análisis

5. **Apagado**
   - Click en "Desconectar" (detiene bombas)
   - Esperar a que flujo cese completamente
   - Desconectar alimentación

---

## 📊 Datos Esperados y Mediciones Típicas

### Condiciones Iniciales Típicas

```
T1 (entrada caliente): 60-80°C
T2 (salida caliente):  40-60°C (menor que T1)
T3 (circuito frío):    15-25°C (aumenta lentamente)

Q1 (caudal caliente):  2-8 L/min
Q2 (caudal frío):      2-8 L/min

ΔT_hot = T1 - T2:      10-30°C (enfriamiento del agua caliente)
ΔT_cold:               Depende del tiempo de recirculación
```

### Resultados Esperados

**Efectividad del Intercambiador:**
```
ε = 0.4 - 0.8  (40% - 80%)
Típicamente 50-60% para intercambiadores de placas simples
```

**Generación de Entropía:**
```
Ṡ_gen > 0  (siempre, por Segunda Ley)
Menor Ṡ_gen indica mejor diseño/operación
```

**Balance de Energía:**
```
|Q_hot - Q_cold| / Q_hot < 10%  (pérdidas aceptables)
```

---

## 🎓 Conceptos Clave Demostrados

### 1. Segunda Ley de la Termodinámica

✅ **Dirección de transferencia de calor**:
- El calor fluye naturalmente de T1 (caliente) a T3 (frío)
- No se requiere trabajo neto para esta transferencia

✅ **Generación de entropía**:
- ΔS_universo = ΔS_hot + ΔS_cold > 0
- Proceso irreversible

### 2. Intercambiadores de Calor

✅ **Efectividad**:
- Medida de qué tan bien el intercambiador transfiere calor
- ε = 1 sería ideal (imposible)

✅ **Método NTU**:
- Caracterización independiente del fluido
- Permite diseño y escalamiento

### 3. Balance de Energía (Primera Ley)

✅ **Conservación**:
- Energía que sale del circuito caliente ≈ energía que entra al frío
- Diferencia = pérdidas al ambiente

### 4. Irreversibilidades

✅ **Fuentes de irreversibilidad**:
- Diferencia finita de temperatura (ΔT)
- Fricción en tuberías
- Mezcla turbulenta
- Pérdidas al ambiente

---

## 📈 Desarrollos Futuros

### Corto Plazo (1-2 meses)

1. **Sistema de Registro de Datos**
   ```python
   # Características deseadas:
   - Timestamp de cada medición
   - Guardado automático en CSV
   - Metadatos del experimento
   - Organización por fecha/hora
   ```

2. **Análisis Automático**
   ```python
   # Scripts a desarrollar:
   - Cálculo de entropía en tiempo real
   - Detección de estado estacionario
   - Cálculo de efectividad
   - Balance de energía
   - Generación de reportes PDF
   ```

3. **Mejoras de Interfaz**
   - Control individual de bombas
   - Ajuste de velocidades con sliders
   - Alarmas configurables
   - Vista de estado estacionario

### Medio Plazo (3-6 meses)

1. **Caracterización Completa**
   - Matriz de experimentos (diferentes caudales)
   - Curva efectividad vs NTU
   - Mapeo de UA vs condiciones
   - Análisis estadístico

2. **Optimización**
   - Caudales óptimos para máxima efectividad
   - Minimización de generación de entropía
   - Máxima eficiencia energética

3. **Integración con Primera Ley**
   - Dashboard unificado
   - Análisis combinado energía-entropía
   - Validación cruzada

### Largo Plazo (6-12 meses)

1. **Sistema Avanzado**
   - Control PID de temperaturas
   - Calentadores/enfriadores activos
   - Operación en ciclos automáticos

2. **Machine Learning**
   - Predicción de comportamiento
   - Optimización automática
   - Detección de anomalías

---

## 🔧 Troubleshooting

### Problema: No se detecta flujo en caudalímetros

**Posibles causas:**
- Aire en las líneas
- Bomba no funcionando
- Caudalímetro mal orientado
- Caudal muy bajo

**Solución:**
1. Verificar que bombas estén encendidas
2. Purgar aire de las líneas
3. Verificar conexión eléctrica de caudalímetro
4. Aumentar velocidad de bomba

### Problema: Temperatura no cambia

**Posibles causas:**
- Sensor mal conectado
- Sensor no sumergido
- Flujo detenido

**Solución:**
1. Verificar conexión 1-Wire
2. Asegurar que sensor esté en contacto con agua
3. Verificar flujo con caudalímetro

### Problema: Balance de energía no cierra

**Posibles causas:**
- Pérdidas al ambiente significativas
- Diferencia en caudales
- Sistema no en estado estacionario

**Solución:**
1. Aislar térmicamente tuberías
2. Equilibrar caudales de ambos circuitos
3. Esperar más tiempo para estabilización

---

## 📚 Referencias

### Libros
1. Cengel, Y. A., & Boles, M. A. (2015). *Thermodynamics: An Engineering Approach* (8th ed.)
2. Incropera, F. P., et al. (2011). *Fundamentals of Heat and Mass Transfer* (7th ed.)
3. Bejan, A. (2016). *Advanced Engineering Thermodynamics* (4th ed.)
4. Shah, R. K., & Sekulic, D. P. (2003). *Fundamentals of Heat Exchanger Design*

### Papers Relevantes
- Kays, W. M., & London, A. L. (1984). *Compact Heat Exchangers*
- Bejan, A. (1996). "Entropy Generation Minimization"

### Recursos Online
- Arduino Reference: https://www.arduino.cc/reference/en/
- DS18B20 Datasheet: Maxim Integrated
- Heat Exchanger Design: Engineering Toolbox

---

## 🤝 Contribuciones

Este es un proyecto educativo abierto. Contribuciones bienvenidas:

### Cómo Contribuir

1. **Reportar Issues**
   - Bugs en el código
   - Problemas de hardware
   - Sugerencias de mejora

2. **Compartir Datos**
   - Resultados experimentales
   - Calibraciones
   - Validaciones

3. **Mejorar Documentación**
   - Correcciones
   - Ejemplos adicionales
   - Traducciones

4. **Código**
   - Scripts de análisis
   - Mejoras de interfaz
   - Nuevas funcionalidades

---

## 📞 Contacto

- **Autor**: Dr. Gabriel Euan[@obieuan]
- **Institución**: Universidad Modelo
- **Repositorio**: [laboratorioTermodinamica](https://github.com/obieuan/laboratorioTermodinamica)
- **Email**: A través de GitHub Issues

---

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo LICENSE para detalles.

Uso educativo libre. Se agradece citar este trabajo si se utiliza en publicaciones académicas.

---

## 🏆 Logros del Proyecto

- ✅ **Sistema integrado funcional** (Diciembre 2025)
- ✅ **Monitoreo en tiempo real** de 3 temperaturas + 2 caudales
- ✅ **Interfaz gráfica completa** con visualización dinámica
- ✅ **Control automático** de 2 circuitos independientes
- ✅ **Base para caracterización** de Segunda Ley

---

## 🎯 Objetivos de Aprendizaje

Al completar este proyecto, los estudiantes podrán:

1. ✅ **Aplicar la Segunda Ley** en un sistema real
2. ✅ **Calcular cambios de entropía** en procesos de transferencia de calor
3. ✅ **Caracterizar intercambiadores** usando método NTU-ε
4. ✅ **Cuantificar irreversibilidades** en sistemas térmicos
5. ✅ **Validar balances** de energía y entropía experimentalmente
6. ✅ **Analizar eficiencia** termodinámica de equipos reales

---

**Estado**: 🟢 Sistema Funcional - Fase de Caracterización  
**Última Actualización**: Diciembre 5, 2025  
**Versión**: 1.0-beta  
**Curso**: Termodinámica / Laboratorio de Ingeniería Térmica

---

*"La entropía del universo tiende a un máximo" - Rudolf Clausius*

*Este proyecto demuestra experimentalmente los principios fundamentales que rigen toda transferencia de energía en el universo.*