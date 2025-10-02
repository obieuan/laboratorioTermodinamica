# 🚀 Guía Rápida - Laboratorio de Termodinámica

## 📁 Estructura del Repositorio

```
laboratorioTermodinamica/
│
├── README.md                    # Documentación principal
├── LICENSE                      # Licencia MIT
├── .gitignore                   # Archivos ignorados
├── SETUP.md                     # Guía de instalación
├── COMANDOS_GIT.md             # Referencia de Git
├── TEMPLATE_EXPERIMENTO.md     # Template para experimentos
├── GUIA_RAPIDA.md              # Este archivo
├── init_project.py             # Script de inicialización
│
└── termodinamica/
    │
    ├── requirements.txt         # Dependencias Python
    ├── venv/                    # Entorno virtual (gitignored)
    │
    ├── primeraley/              # ✅ PROYECTO ACTIVO
    │   ├── README_PRIMERALEY.md
    │   ├── arduino/
    │   │   └── control_actuador/
    │   │       └── control_actuador.ino
    │   ├── python/
    │   │   └── interfaz_control.py
    │   ├── ejemplos/
    │   │   └── analisis_basico.py
    │   ├── datos/
    │   │   ├── .gitkeep
    │   │   ├── README.md
    │   │   └── ejemplo_extension.csv
    │   └── docs/
    │       ├── datasheets/
    │       ├── diagramas/
    │       └── experimentos/
    │
    └── segundaley/              # 🚧 EN DESARROLLO
        ├── README_SEGUNDALEY.md
        ├── datos/
        └── docs/
```

---

## ⚡ Setup en 5 Minutos

### 1. Clonar Repositorio

```bash
git clone https://github.com/obieuan/laboratorioTermodinamica.git
cd laboratorioTermodinamica
```

### 2. Ejecutar Script de Inicialización

```bash
python init_project.py
```

### 3. Instalar Dependencias

```bash
cd termodinamica
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 4. Cargar Arduino

```bash
# Abrir en Arduino IDE:
# termodinamica/primeraley/arduino/control_actuador/control_actuador.ino
# Compilar y cargar al Arduino Mega 2560
```

### 5. Ejecutar Interfaz

```bash
cd primeraley
python python/interfaz_control.py
```

---

## 🎯 Uso Rápido - Primera Ley

### Realizar un Experimento

1. **Conectar** Arduino al puerto USB
2. **Abrir** interfaz: `python python/interfaz_control.py`
3. **Seleccionar** puerto COM y presionar "Conectar"
4. **Configurar** tiempo (ej: 10000 ms)
5. **Presionar** "EXTENDER" o "RETRAER"
6. **Esperar** a que termine (CSV se guarda automáticamente)

### Analizar Datos

```bash
cd primeraley/ejemplos
python analisis_basico.py
```

---

## 📊 Archivos Generados

### CSVs de Experimentos

Ubicación: `termodinamica/primeraley/datos/`

Formato:
- `presion_extension_YYYYMMDD_HHMMSS.csv` - Compresión
- `presion_retraccion_YYYYMMDD_HHMMSS.csv` - Expansión

### Gráficas

Se generan automáticamente al ejecutar `analisis_basico.py`:
- `presion_extension_*_grafica.png`
- Comparaciones entre experimentos

---

## 🔧 Comandos Útiles

### Git

```bash
# Ver estado
git status

# Agregar cambios
git add .

# Commit
git commit -m "Descripción"

# Subir a GitHub
git push

# Ver historial
git log --oneline
```

### Python

```bash
# Activar entorno virtual
# Windows:
termodinamica\venv\Scripts\activate
# Linux/Mac:
source termodinamica/venv/bin/activate

# Instalar dependencia adicional
pip install nombre_paquete

# Congelar dependencias
pip freeze > requirements.txt

# Desactivar entorno
deactivate
```

### Arduino

```bash
# Verificar puerto COM (Windows PowerShell)
Get-WmiObject Win32_SerialPort | Select-Object Name, DeviceID

# Verificar puerto COM (Linux)
ls /dev/tty*

# Verificar puerto COM (Mac)
ls /dev/tty.*
```

---

## 📝 Workflow Típico

### Día de Experimentos

```bash
# 1. Activar entorno
cd laboratorioTermodinamica/termodinamica
source venv/bin/activate  # o venv\Scripts\activate en Windows

# 2. Ir a Primera Ley
cd primeraley

# 3. Ejecutar interfaz
python python/interfaz_control.py

# 4. Realizar experimentos (usar la GUI)

# 5. Analizar datos
python ejemplos/analisis_basico.py

# 6. Guardar en Git
git add datos/
git commit -m "Experimentos del [fecha]: [descripción]"
git push
```

### Documentar Experimento

```bash
# 1. Copiar template
cp TEMPLATE_EXPERIMENTO.md termodinamica/primeraley/docs/experimentos/EXP-001.md

# 2. Editar con tus datos

# 3. Agregar a Git
git add termodinamica/primeraley/docs/experimentos/EXP-001.md
git commit -m "docs: Experimento EXP-001 completado"
git push
```

---

## 🐛 Solución Rápida de Problemas

### Arduino no se conecta

```bash
# Verificar puerto
# Windows: Administrador de Dispositivos
# Linux: ls /dev/ttyUSB* o /dev/ttyACM*
# Mac: ls /dev/tty.*

# Cerrar Arduino IDE si está abierto
# Desconectar y reconectar USB
# Reiniciar Arduino (botón reset)
```

### Error "module not found"

```bash
# Activar entorno virtual
cd termodinamica
source venv/bin/activate  # o venv\Scripts\activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### CSV vacío o sin datos

- Verificar que Arduino envíe "completada" al terminar
- Aumentar tiempo de operación
- Revisar conexión serial en Monitor Serial (9600 baud)

### Lecturas de presión incorrectas

- Verificar alimentación del sensor (5V)
- Verificar conexión en pin A0
- Revisar capacitores de desacoplo
- Calibrar con presión atmosférica (~101.3 kPa)

---

## 📚 Documentación Completa

| Documento | Descripción |
|-----------|-------------|
| `README.md` | Visión general del laboratorio |
| `SETUP.md` | Instalación paso a paso |
| `COMANDOS_GIT.md` | Referencia completa de Git |
| `primeraley/README_PRIMERALEY.md` | Documentación Primera Ley |
| `segundaley/README_SEGUNDALEY.md` | Plan Segunda Ley |
| `TEMPLATE_EXPERIMENTO.md` | Template para documentar |

---

## 🔗 Enlaces Rápidos

- **Repositorio**: https://github.com/obieuan/laboratorioTermodinamica
- **Issues**: https://github.com/obieuan/laboratorioTermodinamica/issues
- **Arduino Mega 2560**: https://docs.arduino.cc/hardware/mega-2560
- **MPX5700AP Datasheet**: https://www.nxp.com/docs/en/data-sheet/MPX5700.pdf

---

## 💡 Tips Profesionales

### Nomenclatura de Commits

```bash
git commit -m "feat: nueva función de análisis"
git commit -m "fix: corregir lectura de presión"
git commit -m "docs: actualizar README"
git commit -m "exp: serie de 5 experimentos"
```

### Backup de Datos

```bash
# Comprimir datos antes de experimentos importantes
cd termodinamica/primeraley
tar -czf backup_datos_$(date +%Y%m%d).tar.gz datos/

# O en Windows (PowerShell)
Compress-Archive -Path datos -DestinationPath "backup_datos_$(Get-Date -Format 'yyyyMMdd').zip"
```

### Análisis Batch

```python
# En ejemplos/analisis_basico.py
# Analizar todos los CSVs de un directorio
analizar_directorio('datos/')
```

---

## 🎓 Para Estudiantes

### Checklist Antes de Experimentar

- [ ] Hardware conectado correctamente
- [ ] Arduino cargado con código actualizado
- [ ] Presión inicial ~101.3 kPa
- [ ] Sistema sellado sin fugas
- [ ] Entorno virtual activado
- [ ] Git actualizado (`git pull`)

### Checklist Después de Experimentar

- [ ] Datos guardados en CSV
- [ ] Gráficas generadas
- [ ] Experimento documentado
- [ ] Cambios committeados
- [ ] Backup realizado (opcional)

---

## 🚀 Próximos Pasos

### Corto Plazo (Primera Ley)
1. Realizar experimentos de calibración
2. Documentar primer experimento completo
3. Crear colección de datos de referencia

### Mediano Plazo (Primera Ley)
1. Agregar sensor de temperatura
2. Implementar gráficas en tiempo real
3. Optimizar análisis de datos

### Largo Plazo
1. Iniciar proyecto Segunda Ley
2. Dashboard web unificado
3. Publicación de resultados

---

## ❓ FAQ Rápido

**P: ¿Cuánto tiempo dura un experimento típico?**  
R: 5-10 segundos de movimiento + ~30 segundos de setup = ~1 minuto total

**P: ¿Cuántos experimentos puedo hacer por día?**  
R: Sin límite técnico. Recomendado: 10-20 para evitar fatiga del equipo

**P: ¿Los datos se guardan automáticamente?**  
R: Sí, cada experimento genera un CSV automáticamente en `datos/`

**P: ¿Puedo modificar el código Arduino?**  
R: Sí, pero haz un commit antes: `git commit -m "backup antes de modificar"`

**P: ¿Cómo contribuyo al proyecto?**  
R: Fork → Cambios → Pull Request. Ver COMANDOS_GIT.md

---

## 📞 Soporte

- 🐛 **Bugs/Problemas**: Abre un Issue en GitHub
- 💬 **Preguntas**: Usa GitHub Discussions
- 📧 **Contacto**: @obieuan en GitHub

---

**Última actualización**: 2024-10-02  
**Versión**: 1.0  
**Repositorio**: https://github.com/obieuan/laboratorioTermodinamica# 🚀 Guía Rápida - Laboratorio de