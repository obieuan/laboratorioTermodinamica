# Laboratorio de Termodinámica - Experimentación y Caracterización

Sistema automatizado para la experimentación y caracterización de las Leyes de la Termodinámica mediante experimentos controlados con actuador lineal, sensores de presión y temperatura.

## 🔬 Estructura del Laboratorio

Este repositorio contiene múltiples proyectos experimentales:

- **📘 Primera Ley** (`primeraley/`): Caracterización experimental mediante compresión/expansión de gases
- **📗 Segunda Ley** (`segundaley/`): Experimentos futuros sobre entropía y procesos irreversibles
- Más leyes y experimentos por venir...

---

# 📘 PRIMERA LEY DE LA TERMODINÁMICA

El proyecto de la Primera Ley se encuentra en la carpeta `primeraley/` y está completamente funcional.

## 📋 Descripción del Proyecto - Primera Ley

Este sistema permite realizar experimentos controlados de compresión y expansión de gases para validar la Primera Ley de la Termodinámica. El actuador lineal controlado por Arduino comprime o expande aire dentro de una jeringa, mientras sensores neumáticos registran presión y temperatura en tiempo real.

### Principio de Operación

1. **Extensión del actuador** → El pistón empuja la jeringa → Compresión del aire
2. **Retracción del actuador** → El pistón jala la jeringa → Expansión del aire
3. Los sensores conectados mediante válvulas neumáticas registran:
   - Presión absoluta (MPX5700AP)
   - Temperatura del gas (sensor por implementar)

## 🔧 Componentes del Sistema

### Hardware Principal

| Componente | Especificaciones | Función |
|------------|------------------|---------|
| **Arduino Mega 2560** | Microcontrolador principal | Control y adquisición de datos |
| **BTS7960 43A** | H-Bridge doble canal | Control bidireccional del actuador |
| **Actuador Lineal DC** | 12/24V, carrera variable | Compresión/expansión mecánica |
| **MPX5700AP** | Sensor de presión absoluta 15-700 kPa | Medición de presión del gas |

### Alimentación

- **Fuente de potencia principal**: 12/24V DC (según especificación del actuador)
  - Corriente mínima: Capaz de entregar corriente de arranque del actuador (típicamente 3-5A)
- **Fuente lógica**: 5V DC para Arduino y Vcc del BTS7960

### Componentes Auxiliares

- Capacitores de desacoplo:
  - 0.1 µF (cerámico) - filtrado de alta frecuencia
  - 10 µF (electrolítico) - estabilización de voltaje
- Válvulas neumáticas (conexión entre jeringa y sensores)
- Jeringa de volumen calibrado

## 📊 Características del Sensor MPX5700AP

- **Rango de medición**: 15 - 700 kPa (absoluta)
- **Voltaje de salida**: 0.2V - 4.7V (proporcional a la presión)
- **Alimentación**: 5V DC
- **Precisión**: ±2.5% del valor de fondo de escala
- **Tiempo de respuesta**: 1 ms típico

### Ecuación de Conversión

```
Presión (kPa) = ((Vout - 0.2) × (700 - 0)) / (4.7 - 0.2) + 0
```

## 🔌 Diagrama de Conexiones

### Arduino Mega 2560 ↔ BTS7960

| Arduino | BTS7960 | Función |
|---------|---------|---------|
| Pin 5 | RPWM | PWM para rotación horaria |
| Pin 6 | LPWM | PWM para rotación antihoraria |
| Pin 7 | R_EN | Enable canal derecho |
| Pin 8 | L_EN | Enable canal izquierdo |
| GND | GND | Tierra común |
| 5V | VCC | Alimentación lógica |

### BTS7960 ↔ Actuador Lineal

| BTS7960 | Actuador |
|---------|----------|
| M+ | Terminal + |
| M- | Terminal - |

### Arduino ↔ MPX5700AP

| Arduino | MPX5700AP | Notas |
|---------|-----------|-------|
| A0 | Vout | Señal analógica de presión |
| 5V | Vcc | Alimentación (con capacitores) |
| GND | GND | Tierra común |

**Importante**: Colocar capacitores de desacoplo (0.1µF y 10µF) entre Vcc y GND del sensor, lo más cerca posible del chip.

## 🖥️ Software

### Requisitos Python

```bash
pip install pyserial tkinter
```

### Estructura de Archivos

```
proyecto-termodinamica/
│
├── arduino/
│   └── control_actuador.ino       # Código para Arduino
│
├── python/
│   └── interfaz_control.py        # Interfaz gráfica de control
│
├── docs/
│   ├── datasheets/
│   │   ├── MPX5700AP.pdf
│   │   └── BTS7960.pdf
│   └── diagramas/
│       └── esquematico.png
│
├── datos/                          # Directorio para CSVs generados
│
└── README.md
```

## 🚀 Uso del Sistema - Primera Ley

### 1. Configuración Inicial

1. **Navegar al proyecto**:
   ```bash
   cd termodinamica/primeraley
   ```

2. **Cargar código en Arduino**:
   ```bash
   # Abrir arduino/control_actuador.ino en Arduino IDE
   # Seleccionar placa: Arduino Mega 2560
   # Seleccionar puerto COM correcto
   # Cargar código
   ```

2. **Verificar conexiones**:
   - Alimentación de potencia conectada y estable
   - BTS7960 con LEDs indicadores encendidos
   - Sensor MPX5700AP alimentado (verificar con multímetro: ~2.5V en Vout en reposo)

### 2. Ejecutar Interfaz de Control

```bash
python python/interfaz_control.py
```

### 3. Operación

1. **Conectar**: Seleccionar puerto COM del Arduino y presionar "Conectar"
2. **Configurar tiempo**: Ingresar duración del movimiento en ms (1000-60000)
3. **Actualizar tiempo**: Enviar configuración al Arduino
4. **Ejecutar experimento**:
   - Presionar **EXTENDER** → Compresión de aire
   - Presionar **RETRAER** → Expansión de aire
5. **Datos**: Automáticamente se genera un CSV con timestamp y mediciones

### 4. Archivos de Datos Generados

Formato: `presion_[tipo]_[fecha]_[hora].csv`

Ejemplo:
- `presion_extension_20240930_143052.csv`
- `presion_retraccion_20240930_150230.csv`

Estructura del CSV:
```csv
Timestamp,Presion (kPa),Tipo
,,extension
Timestamp,Presion (kPa)
2024-09-30 14:30:52.123,125.5
2024-09-30 14:30:52.623,130.2
...
```

## 📈 Análisis de Datos

Los archivos CSV pueden ser procesados con:
- **Python**: pandas, matplotlib, numpy
- **MATLAB**: readtable, plot
- **Excel**: Importación directa

### Ejemplo de Análisis en Python

```python
import pandas as pd
import matplotlib.pyplot as plt

# Leer datos (saltar las primeras 2 filas de metadata)
df = pd.read_csv('presion_extension_20240930_143052.csv', skiprows=2)

# Graficar
plt.plot(df['Timestamp'], df['Presion (kPa)'])
plt.xlabel('Tiempo')
plt.ylabel('Presión (kPa)')
plt.title('Compresión de Gas - Primera Ley de Termodinámica')
plt.show()
```

## 🛡️ Seguridad y Precauciones

### ⚠️ Advertencias

- **NO exceder la presión máxima** del sensor (700 kPa) o de la jeringa
- **Verificar corriente** de la fuente antes de conectar el actuador
- **No invertir polaridad** del sensor MPX5700AP
- **Supervisar temperatura** del BTS7960 durante operación prolongada

### Recomendaciones

1. Realizar pruebas iniciales con tiempos cortos (2-3 segundos)
2. Verificar que las válvulas neumáticas estén correctamente selladas
3. Monitorear el sistema durante los primeros experimentos
4. Mantener el área de trabajo libre de obstrucciones

## 🔄 Comandos del Sistema

### Comandos Seriales (9600 baud)

| Comando | Función | Respuesta |
|---------|---------|-----------|
| `E` o `e` | Extender actuador | "Extendiendo motor..." |
| `R` o `r` | Retraer actuador | "Retrayendo motor..." |
| `T:valor` | Configurar tiempo (ms) | "Tiempo actualizado a: [valor] ms" |

### Ejemplo de Uso Manual (Monitor Serial)

```
> E
Extendiendo motor...
Pressure: 101.3 kPa
Pressure: 125.4 kPa
Pressure: 145.2 kPa
Extension completada.

> T:8000
Tiempo actualizado a: 8000 ms

> R
Retrayendo motor...
Pressure: 145.2 kPa
Pressure: 120.1 kPa
Pressure: 101.5 kPa
Retraccion completada.
```

## 🔬 Aplicaciones Experimentales - Primera Ley

Este sistema permite caracterizar:

1. **Primera Ley de la Termodinámica**: ΔU = Q - W
2. **Procesos adiabáticos**: PV^γ = constante
3. **Ley de Boyle-Mariotte**: PV = constante (isotérmico)
4. **Trabajo de compresión**: W = ∫P dV
5. **Relación P-V-T** en gases ideales

---

# 🔄 ESTRUCTURA GENERAL DEL REPOSITORIO

```
termodinamica/
│
├── primeraley/              # ✅ Proyecto Primera Ley (ACTIVO)
│   ├── arduino/
│   ├── python/
│   ├── ejemplos/
│   ├── datos/
│   ├── docs/
│   └── README_PRIMERALEY.md
│
├── segundaley/              # 🚧 Proyecto Segunda Ley (EN DESARROLLO)
│   └── README_SEGUNDALEY.md
│
├── venv/                    # Entorno virtual Python (gitignored)
│
├── README.md               # Este archivo
├── LICENSE
├── .gitignore
└── requirements.txt        # Dependencias comunes
```

## 🐛 Solución de Problemas

### El actuador no se mueve

- Verificar alimentación de potencia (12/24V)
- Revisar conexiones RPWM, LPWM, R_EN, L_EN
- Verificar que los LEDs del BTS7960 estén encendidos

### Lecturas de presión erróneas

- Verificar alimentación del sensor (debe ser 5V estable)
- Revisar capacitores de desacoplo
- Verificar continuidad en conexión A0
- Calibrar con presión atmosférica conocida (~101.3 kPa)

### Pérdida de conexión serial

- Verificar cable USB
- Reiniciar Arduino
- Revisar que no haya otro programa usando el puerto COM

### CSV vacío o incompleto

- Verificar que el Arduino envíe "completada" al terminar
- Revisar que la operación dure el tiempo configurado
- Comprobar permisos de escritura en el directorio

## 📝 Trabajo Futuro

### Primera Ley
- [ ] Integración de sensor de temperatura
- [ ] Cálculo en tiempo real de trabajo termodinámico
- [ ] Gráficas en vivo P-V
- [ ] Control PID de velocidad del actuador
- [ ] Sistema de seguridad con límites de presión programables

### Segunda Ley
- [ ] Diseño del experimento
- [ ] Selección de sensores adicionales
- [ ] Implementación del sistema
- [ ] Análisis de entropía
- [ ] Caracterización de ciclos termodinámicos

### General
- [ ] Dashboard web centralizado
- [ ] Base de datos para experimentos
- [ ] Exportación de datos en formato HDF5
- [ ] Sistema de control remoto

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo `LICENSE` para más detalles.

## 📧 Contacto

Para preguntas, sugerencias o reportar problemas, por favor abre un issue en este repositorio.

**GitHub**: [@obieuan](https://github.com/obieuan)  
**Repositorio**: [laboratorioTermodinamica](https://github.com/obieuan/laboratorioTermodinamica)

## 🙏 Referencias

- [Datasheet MPX5700AP - NXP Semiconductors](https://www.nxp.com/docs/en/data-sheet/MPX5700.pdf)
- [BTS7960 H-Bridge Motor Driver](https://www.handsontec.com/dataspecs/L298N%20Motor%20Driver.pdf)
- [Arduino Mega 2560 Documentation](https://docs.arduino.cc/hardware/mega-2560)

---

**Nota**: Este es un proyecto experimental con fines educativos. Asegúrese de seguir todas las precauciones de seguridad al trabajar con sistemas neumáticos presurizados y equipo eléctrico.