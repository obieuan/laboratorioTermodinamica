# 📗 Segunda Ley de la Termodinámica

## 🚧 Proyecto en Desarrollo

Este proyecto se enfocará en la caracterización experimental de la **Segunda Ley de la Termodinámica** y conceptos relacionados con entropía, procesos irreversibles y eficiencia termodinámica.

---

## 🎯 Objetivos (Planificados)

1. **Medición de Entropía**: Caracterizar el cambio de entropía en procesos termodinámicos
2. **Procesos Irreversibles**: Demostrar la irreversibilidad de procesos naturales
3. **Eficiencia Termodinámica**: Calcular la eficiencia de ciclos termodinámicos
4. **Máquinas Térmicas**: Análisis experimental de conversión calor-trabajo
5. **Ciclo de Carnot**: Aproximación experimental al ciclo ideal

---

## 📋 Fundamento Teórico

### Segunda Ley de la Termodinámica

**Enunciado de Clausius**:
> Es imposible que un proceso cíclico transfiera calor de un cuerpo frío a uno caliente sin ningún otro efecto.

**Enunciado de Kelvin-Planck**:
> Es imposible que un sistema opere en un ciclo termodinámico y suministre una cantidad neta de trabajo a sus alrededores mientras recibe energía mediante transferencia de calor de un único reservorio térmico.

### Entropía

```
ΔS = ∫ (dQ/T)
```

Para procesos irreversibles:
```
ΔS_universo > 0
```

### Eficiencia de Carnot

```
η_Carnot = 1 - (T_fría / T_caliente)
```

---

## 🔧 Componentes Propuestos

### Hardware Adicional Necesario

- **Sensores de Temperatura**:
  - Termopares tipo K o PT100
  - Sensores DS18B20 (digital)
  - Rango: -50°C a +150°C

- **Sistema de Calentamiento**:
  - Resistencias calefactoras controladas
  - Baño térmico o placa caliente

- **Sistema de Enfriamiento**:
  - Disipadores con ventilación forzada
  - Peltier modules (opcional)

- **Medición de Trabajo**:
  - Sensor de torque o fuerza
  - Encoder rotacional

### Componentes Compartidos con Primera Ley

- Arduino Mega 2560
- Sistema de adquisición de datos
- Válvulas de control
- Estructura mecánica base

---

## 🔬 Experimentos Propuestos

### 1. Expansión Libre (Proceso Irreversible)

**Objetivo**: Demostrar que la entropía aumenta en procesos irreversibles

**Setup**:
- Dos cámaras conectadas por válvula
- Una cámara presurizada, otra al vacío
- Sensores de presión y temperatura en ambas

**Mediciones**:
- Presión antes y después
- Temperatura antes y después
- Calcular ΔS del sistema

### 2. Transferencia de Calor Irreversible

**Objetivo**: Medir el cambio de entropía en transferencia de calor

**Setup**:
- Dos cuerpos a diferentes temperaturas
- Contacto térmico controlado
- Múltiples termopares

**Mediciones**:
- Perfil de temperatura vs tiempo
- Calcular ΔS_total = ΔS_caliente + ΔS_frío

### 3. Ciclo Termodinámico Simplificado

**Objetivo**: Caracterizar eficiencia de un ciclo real

**Setup**:
- Sistema con etapas de compresión/expansión
- Calentamiento/enfriamiento controlado
- Medición de trabajo neto

**Mediciones**:
- Trabajo en cada etapa
- Calor transferido
- Eficiencia real vs ideal

### 4. Máquina Térmica Básica

**Objetivo**: Construir una máquina térmica simple y medir su eficiencia

**Setup**:
- Motor Stirling o similar
- Fuente caliente y fría
- Medición de potencia de salida

**Mediciones**:
- Temperaturas de reservorios
- Trabajo producido
- Calor absorbido/rechazado
- Comparar η_real vs η_Carnot

---

## 📂 Estructura Propuesta

```
segundaley/
│
├── README_SEGUNDALEY.md          # Este archivo
│
├── arduino/
│   └── control_entropia/         # Por definir
│       └── control_entropia.ino
│
├── python/
│   └── interfaz_segundaley.py    # Por definir
│
├── ejemplos/
│   └── analisis_entropia.py      # Por definir
│
├── datos/
│   └── README.md
│
└── docs/
    ├── diseño_experimental/
    ├── datasheets/
    └── experimentos/
```

---

## 🛠️ Estado del Desarrollo

### ✅ Completado
- [ ] Revisión bibliográfica
- [ ] Definición de experimentos
- [ ] Selección de componentes

### 🔄 En Proceso
- [ ] Diseño del circuito
- [ ] Diseño mecánico
- [ ] Selección de sensores de temperatura

### 📋 Por Hacer
- [ ] Adquisición de componentes
- [ ] Prototipo del sistema
- [ ] Código Arduino
- [ ] Interfaz de control Python
- [ ] Scripts de análisis
- [ ] Calibración de sensores
- [ ] Validación experimental
- [ ] Documentación completa

---

## 🎓 Conceptos Clave a Explorar

### Entropía y Desorden

- Interpretación microscópica de la entropía
- Relación entre entropía y estados accesibles
- Principio de aumento de entropía

### Máquinas Térmicas

- Límites fundamentales de eficiencia
- Ciclo de Carnot y su importancia
- Máquinas reales vs ideales

### Procesos Reversibles e Irreversibles

- Condiciones para reversibilidad
- Fuentes de irreversibilidad
- Impacto en la eficiencia

### Refrigeradores y Bombas de Calor

- Coeficiente de rendimiento (COP)
- Límites termodinámicos
- Aplicaciones prácticas

---

## 📊 Resultados Esperados

Una vez completado el proyecto, se espera:

1. **Validación Experimental** de la Segunda Ley
2. **Mediciones Cuantitativas** de cambios de entropía
3. **Caracterización de Eficiencia** de ciclos reales
4. **Comparación** entre procesos reversibles e irreversibles
5. **Datos Experimentales** para análisis estadístico

---

## 🔗 Relación con Primera Ley

Este proyecto complementa el de Primera Ley al:

- Usar el mismo hardware base (Arduino, actuador)
- Extender las mediciones a temperatura
- Combinar análisis de energía y entropía
- Permitir ciclos termodinámicos completos

---

## 📚 Referencias Preliminares

1. Cengel, Y. A., & Boles, M. A. (2015). *Thermodynamics: An Engineering Approach*
2. Atkins, P., & de Paula, J. (2014). *Physical Chemistry: Thermodynamics, Structure, and Change*
3. Bejan, A. (2016). *Advanced Engineering Thermodynamics*
4. Moran, M. J., et al. (2018). *Fundamentals of Engineering Thermodynamics*

---

## 💡 Ideas Adicionales

### Experimentos Avanzados

1. **Efecto Joule-Thomson**: Expansión de gases a través de válvula porosa
2. **Refrigeración Termoeléctrica**: Usando módulos Peltier
3. **Ciclo Otto Simplificado**: Para motores de combustión
4. **Regenerador Térmico**: Recuperación de energía

### Integraciones Posibles

- Dashboard unificado con Primera Ley
- Análisis comparativo de eficiencias
- Simulación vs experimento
- Machine learning para optimización

---

## 🤝 Contribuciones

Si tienes ideas para este proyecto o quieres contribuir:

1. Abre un **Issue** con tu propuesta
2. Comparte **referencias** relevantes
3. Sugiere **componentes** específicos
4. Propón **experimentos** adicionales

---

## 📅 Timeline Estimado

**Fase 1 - Diseño (2-3 meses)**
- Investigación y diseño experimental
- Selección de componentes
- Simulaciones preliminares

**Fase 2 - Construcción (2-3 meses)**
- Adquisición de hardware
- Ensamblaje del sistema
- Pruebas iniciales

**Fase 3 - Software (1-2 meses)**
- Desarrollo de código Arduino
- Interfaz de control
- Scripts de análisis

**Fase 4 - Validación (1-2 meses)**
- Calibración
- Experimentos de prueba
- Análisis de resultados

**Fase 5 - Documentación (1 mes)**
- Guías de usuario
- Publicación de resultados
- Videos demostrativos

---

## 📞 Contacto y Colaboración

¿Interesado en colaborar en este proyecto?

- **Issues**: [GitHub Issues](https://github.com/obieuan/laboratorioTermodinamica/issues)
- **Discusiones**: Abre una discusión en el repositorio
- **Pull Requests**: Siempre bienvenidos

---

## 🔜 Próximos Pasos Inmediatos

1. [ ] Definir lista final de componentes
2. [ ] Crear presupuesto del proyecto
3. [ ] Diseñar esquemático del circuito
4. [ ] Modelar sistema en CAD
5. [ ] Realizar simulaciones térmicas

---

**Estado**: 🚧 En Planificación  
**Inicio Estimado**: Por definir  
**Repositorio**: https://github.com/obieuan/laboratorioTermodinamica  
**Autor**: @obieuan

---

**Nota**: Este documento se actualizará conforme avance el desarrollo del proyecto. Mantente al tanto del repositorio para las últimas novedades.