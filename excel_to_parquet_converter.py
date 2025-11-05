"""
Convertidor de archivos Excel a Parquet para la librería de daños por inundación.
Útil para convertir tus datos de Excel al formato requerido por la librería.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

def convert_excel_to_parquet(excel_file, output_dir="./data"):
    """
    Convierte un archivo Excel con funciones de daño a archivos parquet.
    
    Args:
        excel_file: Ruta al archivo Excel
        output_dir: Directorio donde guardar los archivos parquet
    """
    try:
        print(f"📖 Leyendo archivo Excel: {excel_file}")
        
        # Leer el archivo Excel
        xl = pd.ExcelFile(excel_file, engine='openpyxl')
        
        print(f"📋 Hojas encontradas: {xl.sheet_names}")
        
        # Crear directorio de salida
        os.makedirs(output_dir, exist_ok=True)
        
        # Procesar cada hoja
        for sheet_name in xl.sheet_names:
            print(f"\n🔄 Procesando hoja: {sheet_name}")
            
            df = pd.read_excel(excel_file, sheet_name=sheet_name, engine='openpyxl')
            
            print(f"  - Dimensiones: {df.shape}")
            print(f"  - Columnas: {list(df.columns)}")
            
            # Determinar el tipo de datos basándose en las columnas
            output_file = None
            
            # Detectar funciones de daño
            if any(col.lower() in ['depth', 'profundidad', 'damage', 'daño'] for col in df.columns):
                output_file = os.path.join(output_dir, "damage_functions.parquet")
                df = process_damage_functions(df)
            
            # Detectar datos de uso de suelo
            elif any(col.lower() in ['land_use', 'uso_suelo', 'latitude', 'latitud'] for col in df.columns):
                output_file = os.path.join(output_dir, "land_use.parquet")
                df = process_land_use_data(df)
            
            # Detectar datos de edificaciones
            elif any(col.lower() in ['building', 'edificio', 'value', 'valor'] for col in df.columns):
                output_file = os.path.join(output_dir, "building_types.parquet")
                df = process_building_data(df)
            
            # Archivo genérico
            else:
                output_file = os.path.join(output_dir, f"{sheet_name.lower().replace(' ', '_')}.parquet")
            
            if output_file:
                df.to_parquet(output_file, index=False)
                print(f"  ✅ Guardado como: {output_file}")
            
        print(f"\n🎉 Conversión completada. Archivos guardados en: {output_dir}")
        
    except Exception as e:
        print(f"❌ Error al procesar el archivo Excel: {e}")
        print(f"💡 Asegúrate de que el archivo no esté corrupto y sea un Excel válido (.xlsx)")

def process_damage_functions(df):
    """
    Procesa y normaliza datos de funciones de daño.
    
    Args:
        df: DataFrame con datos de funciones de daño
        
    Returns:
        DataFrame normalizado
    """
    print("  🔧 Procesando como funciones de daño...")
    
    # Mapear nombres de columnas comunes
    column_mapping = {
        'profundidad': 'depth',
        'depth_m': 'depth',
        'daño': 'damage_ratio',
        'damage': 'damage_ratio',
        'ratio': 'damage_ratio',
        'uso_suelo': 'land_use_type',
        'land_use': 'land_use_type',
        'tipo_edificio': 'building_type',
        'building': 'building_type'
    }
    
    # Renombrar columnas
    df_renamed = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
    
    # Asegurar columnas requeridas
    required_columns = ['land_use_type', 'building_type', 'depth', 'damage_ratio']
    
    for col in required_columns:
        if col not in df_renamed.columns:
            if col == 'land_use_type':
                df_renamed[col] = 'residential'  # Valor por defecto
            elif col == 'building_type':
                df_renamed[col] = 'single_family'  # Valor por defecto
            else:
                print(f"  ⚠️  Columna requerida '{col}' no encontrada")
    
    return df_renamed[required_columns] if all(col in df_renamed.columns for col in required_columns) else df_renamed

def process_land_use_data(df):
    """
    Procesa y normaliza datos de uso de suelo.
    
    Args:
        df: DataFrame con datos de uso de suelo
        
    Returns:
        DataFrame normalizado
    """
    print("  🔧 Procesando como datos de uso de suelo...")
    
    column_mapping = {
        'latitud': 'latitude',
        'lat': 'latitude',
        'longitud': 'longitude',
        'lon': 'longitude',
        'lng': 'longitude',
        'uso_suelo': 'land_use_type',
        'land_use': 'land_use_type'
    }
    
    df_renamed = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
    
    required_columns = ['latitude', 'longitude', 'land_use_type']
    
    return df_renamed[required_columns] if all(col in df_renamed.columns for col in required_columns) else df_renamed

def process_building_data(df):
    """
    Procesa y normaliza datos de edificaciones.
    
    Args:
        df: DataFrame con datos de edificaciones
        
    Returns:
        DataFrame normalizado
    """
    print("  🔧 Procesando como datos de edificaciones...")
    
    column_mapping = {
        'latitud': 'latitude',
        'lat': 'latitude',
        'longitud': 'longitude',
        'lon': 'longitude',
        'lng': 'longitude',
        'tipo_edificio': 'building_type',
        'building': 'building_type',
        'valor_m2': 'value_per_m2',
        'value': 'value_per_m2',
        'precio': 'value_per_m2'
    }
    
    df_renamed = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
    
    required_columns = ['latitude', 'longitude', 'building_type', 'value_per_m2']
    
    return df_renamed[required_columns] if all(col in df_renamed.columns for col in required_columns) else df_renamed

def create_template_excel():
    """
    Crea un archivo Excel de plantilla con la estructura esperada.
    """
    output_file = "damage_function_template.xlsx"
    
    print(f"📝 Creando plantilla Excel: {output_file}")
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        
        # Hoja de funciones de daño
        damage_functions = pd.DataFrame({
            'land_use_type': ['residential', 'residential', 'commercial', 'commercial', 'industrial', 'industrial'],
            'building_type': ['single_family', 'multi_family', 'office', 'retail', 'warehouse', 'factory'],
            'depth': [0.0, 1.0, 0.0, 1.0, 0.0, 1.0],
            'damage_ratio': [0.0, 0.35, 0.0, 0.40, 0.0, 0.25]
        })
        damage_functions.to_excel(writer, sheet_name='Damage_Functions', index=False)
        
        # Hoja de uso de suelo
        land_use = pd.DataFrame({
            'latitude': [40.7128, 40.7589, 40.6892],
            'longitude': [-74.0060, -73.9851, -74.0445],
            'land_use_type': ['residential', 'commercial', 'industrial']
        })
        land_use.to_excel(writer, sheet_name='Land_Use', index=False)
        
        # Hoja de edificaciones
        buildings = pd.DataFrame({
            'latitude': [40.7128, 40.7589, 40.6892],
            'longitude': [-74.0060, -73.9851, -74.0445],
            'building_type': ['single_family', 'office', 'warehouse'],
            'value_per_m2': [1000, 1500, 800]
        })
        buildings.to_excel(writer, sheet_name='Building_Types', index=False)
    
    print(f"✅ Plantilla creada: {output_file}")
    print(f"💡 Puedes usar esta plantilla como referencia para estructurar tus datos")

def main():
    """Función principal del convertidor."""
    print("🔄 Convertidor de Excel a Parquet")
    print("Para la Librería de Cálculo de Daños por Inundación")
    print("=" * 60)
    
    import sys
    
    if len(sys.argv) > 1:
        excel_file = sys.argv[1]
        
        if not os.path.exists(excel_file):
            print(f"❌ Archivo no encontrado: {excel_file}")
            return
        
        convert_excel_to_parquet(excel_file)
        
    else:
        print("📋 Opciones:")
        print("  1. Convertir archivo Excel existente:")
        print("     python excel_to_parquet_converter.py tu_archivo.xlsx")
        print("  2. Crear plantilla de ejemplo:")
        print("     python excel_to_parquet_converter.py --template")
        
        if len(sys.argv) > 1 and sys.argv[1] == '--template':
            create_template_excel()
        else:
            # Buscar archivo Excel en el directorio actual
            excel_files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.xls'))]
            
            if excel_files:
                print(f"\n📁 Archivos Excel encontrados:")
                for i, file in enumerate(excel_files, 1):
                    print(f"  {i}. {file}")
                
                try:
                    choice = input(f"\nSelecciona un archivo (1-{len(excel_files)}) o presiona Enter para crear plantilla: ")
                    
                    if choice.strip():
                        idx = int(choice) - 1
                        if 0 <= idx < len(excel_files):
                            convert_excel_to_parquet(excel_files[idx])
                        else:
                            print("❌ Selección inválida")
                    else:
                        create_template_excel()
                        
                except (ValueError, KeyboardInterrupt):
                    print("\n👋 Operación cancelada")
            else:
                print("\n❌ No se encontraron archivos Excel en el directorio actual")
                create_template_excel()

if __name__ == "__main__":
    main()