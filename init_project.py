#!/usr/bin/env python3
"""
Script de inicialización del proyecto Laboratorio de Termodinámica
Crea la estructura de directorios y archivos necesarios
Autor: obieuan
Repositorio: https://github.com/obieuan/laboratorioTermodinamica
"""

import os
import sys
from pathlib import Path


def crear_directorios():
    """Crea la estructura de directorios del proyecto"""
    directorios = [
        'termodinamica/primeraley/arduino/control_actuador',
        'termodinamica/primeraley/python',
        'termodinamica/primeraley/ejemplos',
        'termodinamica/primeraley/datos',
        'termodinamica/primeraley/docs/datasheets',
        'termodinamica/primeraley/docs/diagramas',
        'termodinamica/primeraley/docs/experimentos',
        'termodinamica/segundaley/docs',
        'termodinamica/segundaley/datos'
    ]
    
    print("📁 Creando estructura de directorios...")
    for directorio in directorios:
        Path(directorio).mkdir(parents=True, exist_ok=True)
        print(f"   ✓ {directorio}/")
    
    # Crear archivos .gitkeep en directorios de datos
    for proyecto in ['primeraley', 'segundaley']:
        gitkeep_path = Path(f'termodinamica/{proyecto}/datos/.gitkeep')
        gitkeep_path.touch()
        print(f"   ✓ termodinamica/{proyecto}/datos/.gitkeep")


def crear_readme_datos():
    """Crea un README en el directorio de datos de Primera Ley"""
    readme_content = """# Directorio de Datos - Primera Ley

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
"""
    
    readme_path = Path('termodinamica/primeraley/datos/README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"\n📄 Creado: termodinamica/primeraley/datos/README.md")
    
    # README para Segunda Ley
    readme_segundaley = """# Directorio de Datos - Segunda Ley

Este directorio contendrá los datos de experimentos de Segunda Ley (en desarrollo).
"""
    readme_path2 = Path('termodinamica/segundaley/datos/README.md')
    with open(readme_path2, 'w', encoding='utf-8') as f:
        f.write(readme_segundaley)
    print(f"📄 Creado: termodinamica/segundaley/datos/README.md")


def crear_ejemplo_csv():
    """Crea un archivo CSV de ejemplo"""
    csv_ejemplo = """Timestamp,Presion (kPa),Tipo
,,extension
Timestamp,Presion (kPa)
2024-09-30 14:30:52.123,101.3
2024-09-30 14:30:52.623,108.5
2024-09-30 14:30:53.123,115.2
2024-09-30 14:30:53.623,122.8
2024-09-30 14:30:54.123,130.4
2024-09-30 14:30:54.623,138.6
2024-09-30 14:30:55.123,146.2
2024-09-30 14:30:55.623,153.8
2024-09-30 14:30:56.123,161.5
2024-09-30 14:30:56.623,168.9
"""
    
    csv_path = Path('termodinamica/primeraley/datos/ejemplo_extension.csv')
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write(csv_ejemplo)
    print(f"📄 Creado: termodinamica/primeraley/datos/ejemplo_extension.csv")


def crear_requirements():
    """Crea archivo requirements.txt"""
    requirements = """pyserial==3.5
pandas==2.0.3
matplotlib==3.7.2
numpy==1.24.3
"""
    req_path = Path('termodinamica/requirements.txt')
    with open(req_path, 'w', encoding='utf-8') as f:
        f.write(requirements)
    print(f"📄 Creado: termodinamica/requirements.txt")


def verificar_dependencias():
    """Verifica que las dependencias de Python estén instaladas"""
    print("\n🔍 Verificando dependencias de Python...")
    
    dependencias = {
        'serial': 'pyserial',
        'pandas': 'pandas',
        'matplotlib': 'matplotlib',
        'numpy': 'numpy'
    }
    
    faltantes = []
    
    for modulo, paquete in dependencias.items():
        try:
            __import__(modulo)
            print(f"   ✓ {paquete}")
        except ImportError:
            print(f"   ✗ {paquete} - NO INSTALADO")
            faltantes.append(paquete)
    
    if faltantes:
        print(f"\n⚠️  Faltan {len(faltantes)} dependencia(s)")
        print(f"   Ejecuta: pip install {' '.join(faltantes)}")
        return False
    else:
        print("\n✅ Todas las dependencias están instaladas")
        return True


def verificar_git():
    """Verifica si el repositorio está conectado a GitHub"""
    print("\n🔗 Verificando conexión con GitHub...")
    
    git_config = Path('.git/config')
    
    if not git_config.exists():
        print("   ⚠️  No es un repositorio git")
        print("   Ejecuta: git init")
        return False
    
    with open(git_config, 'r') as f:
        contenido = f.read()
        if 'github.com' in contenido and 'obieuan/laboratorioTermodinamica' in contenido:
            print("   ✓ Conectado a: github.com/obieuan/laboratorioTermodinamica")
            return True
        else:
            print("   ⚠️  Repositorio git local, no conectado a GitHub")
            print("   Ejecuta: git remote add origin https://github.com/obieuan/laboratorioTermodinamica.git")
            return False


def mostrar_siguiente_pasos():
    """Muestra los siguientes pasos a seguir"""
    print("\n" + "="*70)
    print("✅ INICIALIZACIÓN COMPLETADA")
    print("="*70)
    
    print("\n📝 SIGUIENTES PASOS:\n")
    
    print("1. Instalar dependencias (si no están instaladas):")
    print("   cd termodinamica")
    print("   pip install -r requirements.txt\n")
    
    print("2. Cargar código en Arduino (Primera Ley):")
    print("   - Abrir primeraley/arduino/control_actuador/control_actuador.ino")
    print("   - Seleccionar Arduino Mega 2560")
    print("   - Compilar y cargar\n")
    
    print("3. Conectar hardware:")
    print("   - Arduino Mega 2560 → USB")
    print("   - BTS7960 → Pines 5,6,7,8")
    print("   - MPX5700AP → Pin A0")
    print("   - Alimentación de potencia\n")
    
    print("4. Probar el sistema (Primera Ley):")
    print("   cd termodinamica/primeraley")
    print("   python python/interfaz_control.py\n")
    
    print("5. Analizar datos de ejemplo:")
    print("   cd termodinamica/primeraley")
    print("   python ejemplos/analisis_basico.py\n")
    
    print("="*70)
    print("📚 Documentación:")
    print("   - General: README.md (raíz)")
    print("   - Primera Ley: primeraley/README_PRIMERALEY.md")
    print("   - Segunda Ley: segundaley/README_SEGUNDALEY.md")
    print("🐛 Problemas: https://github.com/obieuan/laboratorioTermodinamica/issues")
    print("="*70)


def main():
    """Función principal"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║     Inicialización del Proyecto                                     ║
║     Laboratorio de Termodinámica                                    ║
║     https://github.com/obieuan/laboratorioTermodinamica             ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Crear estructura de directorios
        crear_directorios()
        
        # Crear archivos README en datos
        crear_readme_datos()
        
        # Crear CSV de ejemplo
        crear_ejemplo_csv()
        
        # Crear requirements.txt
        crear_requirements()
        
        # Verificar dependencias
        deps_ok = verificar_dependencias()
        
        # Verificar conexión con GitHub
        git_ok = verificar_git()
        
        # Mostrar siguiente pasos
        mostrar_siguiente_pasos()
        
        # Mensaje final
        if deps_ok and git_ok:
            print("\n🎉 ¡Todo listo para comenzar con la Primera Ley!")
        else:
            print("\n⚠️  Revisa las advertencias anteriores antes de continuar")
        
        print("\n💡 TIP: La carpeta 'venv' se creará al hacer 'python -m venv venv'")
        print("    desde el directorio 'termodinamica/'")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error durante la inicialización: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())