"""
Script de análisis básico para datos de experimentos termodinámicos
Autor: obieuan
Repositorio: https://github.com/obieuan/laboratorioTermodinamica
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import glob


class AnalizadorTermodinamico:
    """Clase para analizar datos de experimentos de compresión/expansión"""
    
    def __init__(self, archivo_csv):
        """
        Inicializa el analizador con un archivo CSV
        
        Args:
            archivo_csv (str): Ruta al archivo CSV del experimento
        """
        self.archivo = archivo_csv
        self.df = self.cargar_datos()
        self.tipo_experimento = self.detectar_tipo()
        
    def cargar_datos(self):
        """Carga los datos del CSV, saltando las filas de metadata"""
        try:
            # Leer CSV saltando las primeras 2 filas de metadata
            df = pd.read_csv(self.archivo, skiprows=2)
            
            # Convertir timestamp a datetime si es posible
            try:
                df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            except:
                print("No se pudo convertir timestamp a datetime")
            
            return df
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            return None
    
    def detectar_tipo(self):
        """Detecta si el experimento fue de extensión o retracción"""
        nombre = Path(self.archivo).name
        if 'extension' in nombre.lower():
            return 'Extensión (Compresión)'
        elif 'retraccion' in nombre.lower():
            return 'Retracción (Expansión)'
        else:
            return 'Desconocido'
    
    def estadisticas_basicas(self):
        """Calcula estadísticas básicas del experimento"""
        if self.df is None or self.df.empty:
            return None
        
        presion = self.df['Presion (kPa)']
        
        stats = {
            'Tipo': self.tipo_experimento,
            'Presión Inicial (kPa)': presion.iloc[0],
            'Presión Final (kPa)': presion.iloc[-1],
            'Presión Máxima (kPa)': presion.max(),
            'Presión Mínima (kPa)': presion.min(),
            'Presión Promedio (kPa)': presion.mean(),
            'Cambio de Presión (kPa)': presion.iloc[-1] - presion.iloc[0],
            'Desviación Estándar (kPa)': presion.std(),
            'Número de Muestras': len(presion)
        }
        
        return stats
    
    def graficar_presion_vs_tiempo(self, guardar=False):
        """
        Grafica presión vs tiempo
        
        Args:
            guardar (bool): Si True, guarda la figura como PNG
        """
        if self.df is None or self.df.empty:
            print("No hay datos para graficar")
            return
        
        plt.figure(figsize=(12, 6))
        plt.plot(range(len(self.df)), self.df['Presion (kPa)'], 
                linewidth=2, color='#2E86AB', marker='o', markersize=4)
        
        plt.xlabel('Muestra #', fontsize=12)
        plt.ylabel('Presión (kPa)', fontsize=12)
        plt.title(f'Experimento: {self.tipo_experimento}\n{Path(self.archivo).name}', 
                 fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # Añadir líneas de referencia
        plt.axhline(y=self.df['Presion (kPa)'].mean(), 
                   color='red', linestyle='--', 
                   label=f'Promedio: {self.df["Presion (kPa)"].mean():.2f} kPa', 
                   alpha=0.7)
        
        plt.legend()
        plt.tight_layout()
        
        if guardar:
            nombre_salida = Path(self.archivo).stem + '_grafica.png'
            plt.savefig(nombre_salida, dpi=300, bbox_inches='tight')
            print(f"Gráfica guardada: {nombre_salida}")
        
        plt.show()
    
    def estimar_trabajo(self, volumen_inicial, volumen_final):
        """
        Estima el trabajo termodinámico usando integración numérica
        W = ∫P dV
        
        Args:
            volumen_inicial (float): Volumen inicial en litros
            volumen_final (float): Volumen final en litros
            
        Returns:
            float: Trabajo estimado en Joules
        """
        if self.df is None or self.df.empty:
            return None
        
        # Convertir presión de kPa a Pa
        presion_pa = self.df['Presion (kPa)'] * 1000
        
        # Crear array de volumen linealmente espaciado
        volumen_m3 = np.linspace(volumen_inicial/1000, volumen_final/1000, len(presion_pa))
        
        # Integración trapezoidal
        trabajo_j = np.trapz(presion_pa, volumen_m3)
        
        return abs(trabajo_j)
    
    def analisis_completo(self):
        """Realiza un análisis completo y muestra todos los resultados"""
        print("=" * 60)
        print("ANÁLISIS DE EXPERIMENTO TERMODINÁMICO")
        print("=" * 60)
        print(f"\nArchivo: {Path(self.archivo).name}")
        print(f"Tipo: {self.tipo_experimento}")
        print("\n" + "-" * 60)
        print("ESTADÍSTICAS BÁSICAS")
        print("-" * 60)
        
        stats = self.estadisticas_basicas()
        if stats:
            for key, value in stats.items():
                if isinstance(value, float):
                    print(f"{key:.<40} {value:.2f}")
                else:
                    print(f"{key:.<40} {value}")
        
        print("\n" + "=" * 60)


def comparar_experimentos(archivo_extension, archivo_retraccion):
    """
    Compara dos experimentos (extensión vs retracción) en una sola gráfica
    
    Args:
        archivo_extension (str): Ruta al CSV de extensión
        archivo_retraccion (str): Ruta al CSV de retracción
    """
    # Cargar ambos experimentos
    ext = AnalizadorTermodinamico(archivo_extension)
    ret = AnalizadorTermodinamico(archivo_retraccion)
    
    if ext.df is None or ret.df is None:
        print("Error al cargar uno o ambos archivos")
        return
    
    # Crear gráfica comparativa
    plt.figure(figsize=(14, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(range(len(ext.df)), ext.df['Presion (kPa)'], 
            linewidth=2, color='#A23B72', marker='o', markersize=3, label='Extensión')
    plt.xlabel('Muestra #', fontsize=11)
    plt.ylabel('Presión (kPa)', fontsize=11)
    plt.title('Extensión (Compresión)', fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(range(len(ret.df)), ret.df['Presion (kPa)'], 
            linewidth=2, color='#18A558', marker='o', markersize=3, label='Retracción')
    plt.xlabel('Muestra #', fontsize=11)
    plt.ylabel('Presión (kPa)', fontsize=11)
    plt.title('Retracción (Expansión)', fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.suptitle('Comparación de Experimentos', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()


def analizar_directorio(ruta_datos='datos/'):
    """
    Analiza todos los archivos CSV en un directorio
    
    Args:
        ruta_datos (str): Ruta al directorio con los CSVs
    """
    archivos = glob.glob(f"{ruta_datos}/*.csv")
    
    if not archivos:
        print(f"No se encontraron archivos CSV en {ruta_datos}")
        return
    
    print(f"\nSe encontraron {len(archivos)} archivos CSV\n")
    
    for archivo in archivos:
        analizador = AnalizadorTermodinamico(archivo)
        stats = analizador.estadisticas_basicas()
        
        if stats:
            print(f"\n📊 {Path(archivo).name}")
            print(f"   Tipo: {stats['Tipo']}")
            print(f"   ΔP: {stats['Cambio de Presión (kPa)']:.2f} kPa")
            print(f"   P_max: {stats['Presión Máxima (kPa)']:.2f} kPa")


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     Análisis de Experimentos Termodinámicos                  ║
    ║     Laboratorio de Termodinámica                             ║
    ║     https://github.com/obieuan/laboratorioTermodinamica      ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # EJEMPLO 1: Analizar un solo experimento
    print("\n📌 EJEMPLO 1: Análisis Individual")
    print("-" * 60)
    
    # Cambia esta ruta por tu archivo CSV
    archivo_ejemplo = "datos/presion_extension_20240930_143052.csv"
    
    # Verificar si existe el archivo
    if Path(archivo_ejemplo).exists():
        analizador = AnalizadorTermodinamico(archivo_ejemplo)
        analizador.analisis_completo()
        analizador.graficar_presion_vs_tiempo(guardar=True)
        
        # Calcular trabajo (ejemplo con jeringa de 60 ml)
        trabajo = analizador.estimar_trabajo(volumen_inicial=60, volumen_final=30)
        if trabajo:
            print(f"\n🔧 Trabajo estimado: {trabajo:.2f} J")
    else:
        print(f"⚠️  Archivo no encontrado: {archivo_ejemplo}")
        print("    Coloca un archivo CSV de ejemplo en la carpeta 'datos/'")
    
    
    # EJEMPLO 2: Analizar todos los archivos en el directorio
    print("\n\n📌 EJEMPLO 2: Análisis de Directorio")
    print("-" * 60)
    analizar_directorio('datos/')
    
    
    # EJEMPLO 3: Comparar dos experimentos
    print("\n\n📌 EJEMPLO 3: Comparación de Experimentos")
    print("-" * 60)
    
    archivo_ext = "datos/presion_extension_20240930_143052.csv"
    archivo_ret = "datos/presion_retraccion_20240930_150230.csv"
    
    if Path(archivo_ext).exists() and Path(archivo_ret).exists():
        comparar_experimentos(archivo_ext, archivo_ret)
    else:
        print("⚠️  Se necesitan ambos archivos (extensión y retracción) para comparar")
    
    
    print("\n" + "=" * 60)
    print("✅ Análisis completado")
    print("=" * 60)
