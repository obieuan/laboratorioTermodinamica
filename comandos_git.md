# 🚀 Comandos para Subir el Proyecto a GitHub

## Inicialización del Repositorio (Primera Vez)

Si aún no has inicializado el repositorio:

```bash
# 1. Navegar a la carpeta del proyecto
cd /ruta/a/tu/proyecto

# 2. Inicializar git
git init

# 3. Conectar con el repositorio de GitHub
git remote add origin https://github.com/obieuan/laboratorioTermodinamica.git

# 4. Verificar la conexión
git remote -v
```

## Estructura de Archivos a Crear

Asegúrate de tener esta estructura antes de hacer commit:

```
laboratorioTermodinamica/
│
├── termodinamica/
│   │
│   ├── primeraley/              # Proyecto Primera Ley
│   │   ├── README_PRIMERALEY.md
│   │   ├── arduino/
│   │   │   └── control_actuador/
│   │   │       └── control_actuador.ino
│   │   ├── python/
│   │   │   └── interfaz_control.py
│   │   ├── ejemplos/
│   │   │   └── analisis_basico.py
│   │   ├── datos/
│   │   │   ├── .gitkeep
│   │   │   ├── README.md
│   │   │   └── ejemplo_extension.csv
│   │   └── docs/
│   │       ├── datasheets/
│   │       ├── diagramas/
│   │       └── experimentos/
│   │
│   ├── segundaley/              # Proyecto Segunda Ley (futuro)
│   │   └── README_SEGUNDALEY.md
│   │
│   ├── venv/                    # gitignored
│   └── requirements.txt
│
├── README.md
├── LICENSE
├── .gitignore
├── SETUP.md
├── COMANDOS_GIT.md
├── TEMPLATE_EXPERIMENTO.md
└── init_project.py
```

## Subir Todo el Proyecto por Primera Vez

```bash
# 1. Verificar qué archivos se van a subir
git status

# 2. Agregar todos los archivos
git add .

# 3. Hacer el primer commit
git commit -m "Initial commit: Sistema completo de control y análisis termodinámico"

# 4. Configurar la rama principal (si es necesario)
git branch -M main

# 5. Subir al repositorio
git push -u origin main
```

## Comandos para Actualizaciones Futuras

### Agregar cambios específicos

```bash
# Ver estado de los archivos
git status

# Agregar archivo específico
git add python/interfaz_control.py

# Agregar todos los archivos de una carpeta
git add arduino/

# Ver qué cambios hay antes de hacer commit
git diff

# Hacer commit con mensaje descriptivo
git commit -m "Actualizar interfaz: agregar botón de emergencia"

# Subir cambios
git push
```

### Agregar todos los cambios

```bash
# Agregar todos los archivos modificados
git add -A

# Commit
git commit -m "Descripción de los cambios realizados"

# Push
git push
```

## Comandos Útiles para el Día a Día

### Ver historial

```bash
# Ver commits recientes
git log --oneline

# Ver últimos 5 commits
git log --oneline -5

# Ver cambios detallados de un commit
git show [hash-del-commit]
```

### Deshacer cambios

```bash
# Descartar cambios en un archivo (ANTES de hacer commit)
git checkout -- archivo.py

# Descartar TODOS los cambios locales (CUIDADO)
git reset --hard

# Revertir el último commit (crea un nuevo commit)
git revert HEAD
```

### Trabajar con ramas

```bash
# Crear nueva rama para experimentar
git checkout -b experimento-temperatura

# Ver todas las ramas
git branch -a

# Cambiar de rama
git checkout main

# Fusionar rama experimental con main
git checkout main
git merge experimento-temperatura

# Eliminar rama después de fusionar
git branch -d experimento-temperatura
```

### Sincronizar con GitHub

```bash
# Descargar cambios del repositorio (si trabajas desde varias computadoras)
git pull

# Forzar descarga (sobrescribe cambios locales)
git fetch --all
git reset --hard origin/main
```

## Workflow Recomendado para Experimentos

### Opción 1: Commits frecuentes (recomendado para principiantes)

```bash
# Después de cada experimento exitoso
git add datos/presion_extension_*.csv
git commit -m "Experimento: compresión a 8 segundos"
git push
```

### Opción 2: Ramas para series de experimentos

```bash
# Crear rama para una serie de experimentos
git checkout -b serie-experimentos-octubre

# Realizar experimentos y commits
git add datos/
git commit -m "Serie 1: 5 experimentos de compresión"

# Cuando termines la serie, fusionar con main
git checkout main
git merge serie-experimentos-octubre
git push
```

## Comandos para Colaboración

### Si otra persona trabaja en el proyecto

```bash
# Antes de empezar a trabajar, actualizar
git pull

# Después de terminar, subir cambios
git add .
git commit -m "Descripción"
git push

# Si hay conflictos al hacer pull
git pull
# Resolver conflictos manualmente
git add .
git commit -m "Resolver conflictos"
git push
```

## Comandos para Issues y Releases

### Crear release (versión estable)

```bash
# Crear tag para versión
git tag -a v1.0.0 -m "Primera versión estable del sistema"

# Subir el tag
git push origin v1.0.0

# Ver todos los tags
git tag
```

### Referenciar issues en commits

```bash
# Si tienes un issue #5 abierto
git commit -m "Corregir error de lectura de presión (fixes #5)"
```

## Consejos y Mejores Prácticas

### ✅ HACER

- Commits con mensajes descriptivos
- Push frecuente para no perder trabajo
- Usar ramas para cambios experimentales
- Revisar `git status` antes de commit
- Probar el código antes de hacer push

### ❌ EVITAR

- Commits con mensaje "update" o "fix"
- Subir archivos muy grandes (>100MB)
- Hacer commit de datos sensibles o contraseñas
- Subir carpetas de dependencias (venv/, node_modules/)
- Forzar push (`git push -f`) en rama main

## Mensajes de Commit Recomendados

Usa prefijos para organizar:

```bash
git commit -m "feat: agregar sensor de temperatura al sistema"
git commit -m "fix: corregir cálculo de presión en rango alto"
git commit -m "docs: actualizar README con nuevos ejemplos"
git commit -m "refactor: optimizar lectura serial"
git commit -m "test: agregar pruebas unitarias para analizador"
```

## Solución de Problemas Comunes

### Error: "remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/obieuan/laboratorioTermodinamica.git
```

### Error: "refusing to merge unrelated histories"

```bash
git pull origin main --allow-unrelated-histories
```

### Error: "Your branch is ahead of 'origin/main'"

```bash
# Significa que tienes commits locales sin subir
git push
```

### Olvidaste hacer .gitignore antes del primer commit

```bash
# Crear .gitignore con el contenido correcto
# Luego ejecutar:
git rm -r --cached .
git add .
git commit -m "Aplicar .gitignore correctamente"
git push
```

## Verificar que Todo Esté Bien

Después de hacer push, verifica en GitHub:

1. Ve a: https://github.com/obieuan/laboratorioTermodinamica
2. Verifica que aparezcan todos los archivos
3. Comprueba que el README se vea correctamente
4. Verifica que los archivos en `datos/` estén ignorados (excepto ejemplos)

## Comandos para Limpiar el Repositorio

```bash
# Ver tamaño del repositorio
du -sh .git

# Limpiar archivos sin seguimiento
git clean -fd

# Optimizar el repositorio
git gc --aggressive --prune=now
```

---

## 🎯 Quick Reference (Comandos Más Usados)

```bash
git status              # Ver estado actual
git add .               # Agregar todos los cambios
git commit -m "mensaje" # Hacer commit
git push                # Subir a GitHub
git pull                # Descargar de GitHub
git log --oneline       # Ver historial
git branch              # Ver ramas
```

---

**¿Dudas?** Consulta la [documentación oficial de Git](https://git-scm.com/doc) o abre un issue en el repositorio.

**Repositorio:** https://github.com/obieuan/laboratorioTermodinamica