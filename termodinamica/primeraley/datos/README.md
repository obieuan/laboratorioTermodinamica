# Directorio de Datos - Primera Ley

Este directorio contiene los archivos CSV generados por los experimentos de Primera Ley.

## Nomenclatura de Archivos

- `presion_extension_YYYYMMDD_HHMMSS.csv`: Experimentos de extensión (compresión)
- `presion_retraccion_YYYYMMDD_HHMMSS.csv`: Experimentos de retracción (expansión)

## Estructura de CSV

Cada archivo contiene:
1. Metadata (2 primeras filas)
2. Headers de datos
3. Timestamp y mediciones de presión

## Nota

Estos archivos están ignorados en `.gitignore` para no llenar el repositorio.
Solo archivos de ejemplo (`ejemplo_*.csv`) se suben a GitHub.
