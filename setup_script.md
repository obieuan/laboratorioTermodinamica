# 🚀 Guía de Instalación Rápida

## Estructura del Laboratorio

Este repositorio contiene múltiples proyectos experimentales:
- **Primera Ley** (`primeraley/`): Sistema de compresión/expansión con actuador lineal
- **Segunda Ley** (`segundaley/`): En desarrollo

Esta guía se enfoca en la instalación del proyecto de **Primera Ley**.

## Requisitos Previos

- Python 3.8 o superior
- Arduino IDE 1.8.x o 2.x
- Git

## Instalación Paso a Paso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/obieuan/laboratorioTermodinamica.git
cd laboratorioTermodinamica/termodinamica
```

### 2. Crear Estructura de Directorios (Primera Ley)

```bash
# Navegar al proyecto de Primera Ley
cd primeraley

# En Linux/macOS
mkdir -p datos docs/datasheets docs/diagramas docs/experimentos ejemplos

# En Windows (PowerShell)
New-Item -ItemType Directory -Force -Path datos, docs/datasheets, docs/diagramas, docs/experimentos, ejemplos
```

### 3. Instalar Dependencias de Python

#### Opción A: Usando pip

```bash
pip install -r requirements.txt
```

#### Opción B: Instalación manual

```bash
pip install pyserial pandas matplotlib numpy
```

#### Opción C: Usando entorno virtual (recomendado)

```bash
# Desde el directorio termodinamica/
python -m venv venv

# Activar entorno virtual
# En Linux/macOS:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Configurar Arduino

1. Abrir Arduino IDE
2. Ir a `Archivo > Preferencias`
3. En "Gestor de URLs Adicionales de Tarjetas", agregar si es necesario
4. Ir a `Herramientas > Placa > Gestor de tarjetas`
5. Instalar "Arduino AVR Boards" si no está instalado
6. Seleccionar `Herramientas > Placa > Arduino Mega 2560`

### 5. Cargar el Código en Arduino

```bash
# Navegar al directorio del código Arduino
cd primeraley/arduino/control_actuador
# Abrir control_actuador.ino en Arduino IDE
```

En Arduino IDE:
1. Seleccionar puerto: `Herramientas > Puerto > [Tu puerto COM]`
2. Compilar: `Sketch > Verificar/Compilar` (Ctrl+R)
3. Cargar: `Sketch > Subir` (Ctrl+U)

### 6. Probar la Instalación

#### Verificar comunicación con Arduino

```bash
# Ejecutar la interfaz de control
cd python
python interfaz_control.py
```

#### Verificar scripts de análisis

```bash
cd primeraley/ejemplos
python analisis_basico.py
```

## Verificación de Instalación

### Checklist de Hardware

- [ ] Arduino Mega 2560 conectado via USB
- [ ] BTS7960 conectado correctamente
- [ ] Actuador lineal conectado al BTS7960
- [ ] Sensor MPX5700AP conectado a A0
- [ ] Fuente de alimentación de potencia conectada
- [ ] LEDs del BTS7960 encendidos

### Checklist de Software

- [ ] Python 3.8+ instalado (`python --version`)
- [ ] Dependencias instaladas (`pip list`)
- [ ] Arduino IDE funcional
- [ ] Código cargado en Arduino sin errores
- [ ] Puerto COM detectado en la interfaz

### Test Básico

1. **Abrir Monitor Serial** en Arduino IDE (9600 baud)
2. Enviar comando `T:5000` → Debe responder: "Tiempo actualizado a: 5000 ms"
3. Enviar comando `E` → Debe iniciar extensión y mostrar lecturas de presión
4. Esperar 5 segundos → Debe mostrar "Extension completada."

## Solución de Problemas Comunes

### Error: "No module named 'serial'"

```bash
pip install pyserial
```

### Error: "Puerto COM no disponible"

**Windows:**
1. Abrir Administrador de Dispositivos
2. Verificar en "Puertos (COM y LPT)"
3. Reinstalar driver CH340 si es necesario

**Linux:**
```bash
# Agregar usuario al grupo dialout
sudo usermod -a -G dialout $USER
# Cerrar sesión y volver a entrar
```

**macOS:**
```bash
# Listar puertos disponibles
ls /dev/tty.*
```

### Error: "Permission denied" en Linux

```bash
sudo chmod 666 /dev/ttyUSB0  # Cambiar por tu puerto
# O de forma permanente:
sudo usermod -a -G dialout $USER
```

### Error: Lecturas de presión en 0 o constantes

1. Verificar alimentación de 5V en el sensor
2. Verificar conexión en pin A0
3. Verificar capacitores de desacoplo
4. Probar con multímetro: debe leer ~2.5V en reposo

### Interfaz no se conecta

1. Cerrar Arduino IDE (liberar puerto)
2. Verificar que el Arduino esté alimentado
3. Probar con otro cable USB
4. Reiniciar Arduino (botón reset)

## Estructura Final del Proyecto

Después de la instalación, deberías tener:

```
laboratorioTermodinamica/
├── termodinamica/
│   │
│   ├── primeraley/              # ✅ PROYECTO ACTIVO
│   │   ├── README_PRIMERALEY.md
│   │   ├── arduino/
│   │   │   └── control_actuador/
│   │   │       └── control_actuador.ino ✅
│   │   ├── python/
│   │   │   └── interfaz_control.py      ✅
│   │   ├── ejemplos/
│   │   │   └── analisis_basico.py       ✅
│   │   ├── datos/                       📁
│   │   │   ├── .gitkeep
│   │   │   └── ejemplo_extension.csv
│   │   └── docs/
│   │       ├── datasheets/              📁
│   │       ├── diagramas/               📁
│   │       └── experimentos/            📁
│   │
│   ├── segundaley/              # 🚧 EN DESARROLLO
│   │   └── README_SEGUNDALEY.md
│   │
│   ├── venv/                    # Entorno virtual
│   └── requirements.txt         ✅
│
├── README.md                    ✅
├── LICENSE                      ✅
├── .gitignore                   ✅
└── SETUP.md                     ✅
```

## Siguientes Pasos

1. ✅ Verificar todas las conexiones hardware
2. ✅ Realizar experimento de prueba corto (2-3 segundos)
3. ✅ Revisar datos generados en `primeraley/datos/`
4. ✅ Analizar con `analisis_basico.py`
5. 📊 Comenzar experimentos reales
6. 📝 Documentar experimentos en `docs/experimentos/`

## Comandos Útiles de Git

```bash
# Ver estado del repositorio
git status

# Agregar cambios
git add .

# Commit con mensaje
git commit -m "Descripción de cambios"

# Subir a GitHub
git push origin main

# Ver historial
git log --oneline

# Crear rama para experimentos
git checkout -b experimentos
```

## Recursos Adicionales

- [Documentación de pyserial](https://pyserial.readthedocs.io/)
- [Arduino Reference](https://www.arduino.cc/reference/en/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

**¿Encontraste un problema?** Abre un issue en: https://github.com/obieuan/laboratorioTermodinamica/issues

**¿Todo funcionó?** ¡Perfecto! Comienza a experimentar con la Primera Ley de la Termodinámica 🚀