"""
Script para analizar esquemas de archivos parquet existentes.
Útil para entender la estructura de tus datos antes de usar la librería.
"""

import pandas as pd
import pyarrow.parquet as pq
import os
from pathlib import Path

def analyze_parquet_file(file_path):
    """
    Analiza un archivo parquet y muestra información detallada.
    
    Args:
        file_path: Ruta al archivo parquet
    """
    try:
        print(f"\n📘 Analizando: {file_path}")
        print("=" * 60)
        
        # Leer con pandas para análisis básico
        df = pd.read_parquet(file_path)
        
        print(f"📊 Información básica:")
        print(f"  - Filas: {len(df):,}")
        print(f"  - Columnas: {len(df.columns)}")
        print(f"  - Tamaño en memoria: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        print(f"\n📋 Columnas y tipos de datos:")
        for col in df.columns:
            dtype = df[col].dtype
            null_count = df[col].isnull().sum()
            null_pct = (null_count / len(df)) * 100
            
            if dtype == 'object':
                unique_count = df[col].nunique()
                print(f"  - {col}: {dtype} ({unique_count:,} valores únicos, {null_pct:.1f}% nulos)")
                if unique_count <= 10:
                    print(f"    Valores: {list(df[col].unique())}")
            else:
                min_val = df[col].min()
                max_val = df[col].max()
                print(f"  - {col}: {dtype} (rango: {min_val} - {max_val}, {null_pct:.1f}% nulos)")
        
        print(f"\n📈 Primeras 5 filas:")
        print(df.head().to_string())
        
        # Análisis con pyarrow para información más detallada
        print(f"\n🔍 Esquema PyArrow:")
        parquet_file = pq.ParquetFile(file_path)
        schema = parquet_file.schema
        print(schema)
        
        print(f"\n📦 Metadatos del archivo:")
        metadata = parquet_file.metadata
        print(f"  - Versión: {metadata.version}")
        print(f"  - Filas totales: {metadata.num_rows:,}")
        print(f"  - Grupos de filas: {metadata.num_row_groups}")
        print(f"  - Tamaño serializado: {metadata.serialized_size:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al analizar {file_path}: {e}")
        return False

def analyze_directory(directory_path):
    """
    Analiza todos los archivos parquet en un directorio.
    
    Args:
        directory_path: Ruta al directorio
    """
    directory = Path(directory_path)
    
    if not directory.exists():
        print(f"❌ El directorio {directory_path} no existe")
        return
    
    parquet_files = list(directory.glob("*.parquet"))
    
    if not parquet_files:
        print(f"❌ No se encontraron archivos .parquet en {directory_path}")
        return
    
    print(f"🔍 Encontrados {len(parquet_files)} archivos parquet en {directory_path}")
    
    successful_analyses = 0
    for file_path in parquet_files:
        if analyze_parquet_file(file_path):
            successful_analyses += 1
    
    print(f"\n✅ Análisis completado: {successful_analyses}/{len(parquet_files)} archivos procesados exitosamente")

def suggest_library_usage(directory_path):
    """
    Sugiere cómo usar la librería basándose en los archivos encontrados.
    
    Args:
        directory_path: Ruta al directorio con archivos parquet
    """
    directory = Path(directory_path)
    parquet_files = list(directory.glob("*.parquet"))
    
    if not parquet_files:
        return
    
    print(f"\n💡 Sugerencias para usar la librería:")
    print("=" * 50)
    
    file_names = [f.name for f in parquet_files]
    
    # Verificar archivos esperados
    expected_files = {
        'damage_functions.parquet': 'Funciones de daño por tipo de uso y edificación',
        'land_use.parquet': 'Información de uso de suelo por ubicación',
        'building_types.parquet': 'Tipos de edificación y valores por ubicación'
    }
    
    print("📋 Archivos esperados por la librería:")
    for expected_file, description in expected_files.items():
        if expected_file in file_names:
            print(f"  ✅ {expected_file}: {description}")
        else:
            print(f"  ❌ {expected_file}: {description} (NO ENCONTRADO)")
    
    print(f"\n📝 Archivos adicionales encontrados:")
    additional_files = set(file_names) - set(expected_files.keys())
    for file_name in additional_files:
        print(f"  📄 {file_name}")
    
    print(f"\n🚀 Código de ejemplo para usar la librería:")
    print(f"""
from flood_damage_library import FloodDamageCalculator

# Inicializar con tu directorio de datos
calculator = FloodDamageCalculator(data_directory="{directory_path}")

# Calcular daño para una ubicación
result = calculator.calculate_damage(
    latitude=TU_LATITUD,      # Reemplaza con coordenadas reales
    longitude=TU_LONGITUD,    # Reemplaza con coordenadas reales
    flood_depth=1.5           # Profundidad en metros
)

print(f"Daño estimado: ${{result['damage_assessment']['economic_damage']:,.2f}}")
""")

def main():
    """Función principal del script."""
    print("🌊 Analizador de Esquemas de Archivos Parquet")
    print("Para la Librería de Cálculo de Daños por Inundación")
    print("=" * 60)
    
    # Analizar directorio actual por defecto
    default_dir = "./data"
    
    # Permitir al usuario especificar un directorio diferente
    import sys
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = default_dir
    
    print(f"📁 Analizando directorio: {target_dir}")
    
    analyze_directory(target_dir)
    suggest_library_usage(target_dir)
    
    print(f"\n📚 Para más información, consulta:")
    print(f"  - README.md: Documentación completa")
    print(f"  - example_usage.py: Ejemplos de uso")
    print(f"  - tests/: Tests unitarios")

if __name__ == "__main__":
    main()