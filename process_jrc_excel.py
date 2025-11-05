"""
Procesador del archivo Excel de funciones de daño del JRC (Joint Research Centre).
Extrae y estructura los datos para uso en la librería de cálculo de daños.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

def process_jrc_excel(excel_file, output_dir="./processed_data"):
    """
    Procesa el archivo Excel del JRC y genera archivos parquet estructurados.
    
    Args:
        excel_file: Ruta al archivo Excel del JRC
        output_dir: Directorio donde guardar los archivos procesados
    """
    print("🔄 Procesando archivo Excel del JRC...")
    print("=" * 60)
    
    # Crear directorio de salida
    os.makedirs(output_dir, exist_ok=True)
    
    # Procesar cada hoja relevante
    process_damage_functions(excel_file, output_dir)
    process_max_damage_residential(excel_file, output_dir)
    process_max_damage_commercial(excel_file, output_dir)
    process_max_damage_industrial(excel_file, output_dir)
    process_iso_table(excel_file, output_dir)
    
    print(f"\n✅ Procesamiento completado. Archivos guardados en: {output_dir}")

def process_damage_functions(excel_file, output_dir):
    """Procesa la hoja de funciones de daño."""
    print("\n📊 Procesando funciones de daño...")
    
    try:
        # Leer la hoja de funciones de daño
        df = pd.read_excel(excel_file, sheet_name='Damage functions', engine='openpyxl')
        
        # Limpiar y estructurar los datos
        # Las primeras filas contienen headers
        # Fila 0: Damage class, Flood depth, Damage function, ..., Standard deviation
        # Fila 1: NaN, NaN, EUROPE, North AMERICA, etc.
        
        # Extraer headers de regiones
        regions = ['EUROPE', 'North AMERICA', 'Centr&South\nAMERICA', 'ASIA', 'AFRICA', 'OCEANIA', 'GLOBAL']
        
        # Encontrar las columnas de funciones de daño y desviaciones estándar
        damage_func_cols = []
        std_dev_cols = []
        
        for i, col in enumerate(df.columns):
            if i >= 2 and i <= 8:  # Columnas de funciones de daño
                damage_func_cols.append(col)
            elif i >= 9 and i <= 15:  # Columnas de desviación estándar
                std_dev_cols.append(col)
        
        # Procesar datos línea por línea
        processed_data = []
        current_damage_class = None
        
        for idx, row in df.iterrows():
            if idx < 2:  # Saltar headers
                continue
            
            # Obtener clase de daño (puede estar en la primera columna o ser continuación)
            if not pd.isna(row.iloc[0]):
                current_damage_class = row.iloc[0]
            
            flood_depth = row.iloc[1]
            
            # Saltar filas sin profundidad válida
            if pd.isna(flood_depth):
                continue
            
            # Convertir profundidad a numérico
            try:
                depth_value = float(flood_depth)
            except:
                continue
            
            # Procesar cada región
            for i, region in enumerate(regions):
                if i < len(damage_func_cols):
                    damage_value = row.iloc[2 + i]
                    std_dev_value = row.iloc[9 + i] if i < len(std_dev_cols) else None
                    
                    # Convertir a numérico
                    try:
                        damage_ratio = float(damage_value) if not pd.isna(damage_value) and damage_value != '-' else None
                        std_deviation = float(std_dev_value) if not pd.isna(std_dev_value) and std_dev_value != '-' else None
                    except:
                        damage_ratio = None
                        std_deviation = None
                    
                    if damage_ratio is not None and current_damage_class is not None:
                        processed_data.append({
                            'damage_class': current_damage_class,
                            'building_type': current_damage_class.lower().replace(' ', '_').replace('-', '_'),
                            'depth_m': depth_value,
                            'region': region.replace('\n', '_'),
                            'damage_ratio': damage_ratio,
                            'standard_deviation': std_deviation
                        })
        
        # Crear DataFrame y guardar
        df_processed = pd.DataFrame(processed_data)
        output_file = os.path.join(output_dir, 'damage_functions_jrc.parquet')
        df_processed.to_parquet(output_file, index=False)
        
        print(f"  ✅ Funciones de daño procesadas: {len(df_processed)} registros")
        print(f"  📁 Guardado en: {output_file}")
        
        # Mostrar resumen
        print(f"  📋 Clases de daño: {df_processed['damage_class'].unique()}")
        print(f"  🌍 Regiones: {df_processed['region'].unique()}")
        
    except Exception as e:
        print(f"  ❌ Error procesando funciones de daño: {e}")

def process_max_damage_residential(excel_file, output_dir):
    """Procesa valores máximos de daño residencial."""
    print("\n🏠 Procesando daños máximos residenciales...")
    
    try:
        df = pd.read_excel(excel_file, sheet_name='MaxDamage-Residential', engine='openpyxl')
        
        # Limpiar datos
        # Fila 0: Country, Building based, ..., Object based
        # Fila 1: NaN, Max Damage Structure, Max Damage Content, Total, Total, Total
        # Fila 2: NaN, (€/m2, 2010), (€/m2, 2010), (€/m2, 2010), (€/m2, 2010), (€/object, 2010)
        
        processed_data = []
        
        for idx, row in df.iterrows():
            if idx < 2:  # Saltar headers
                continue
                
            country = row.iloc[0]
            if pd.isna(country):
                continue
            
            # Extraer valores
            try:
                max_damage_structure = float(row.iloc[1]) if not pd.isna(row.iloc[1]) else None
                max_damage_content = float(row.iloc[2]) if not pd.isna(row.iloc[2]) else None
                total_building = float(row.iloc[3]) if not pd.isna(row.iloc[3]) else None
                total_landuse = float(row.iloc[4]) if not pd.isna(row.iloc[4]) else None
                total_object = float(row.iloc[5]) if not pd.isna(row.iloc[5]) else None
                
                processed_data.append({
                    'country': country,
                    'building_type': 'residential',
                    'max_damage_structure_eur_m2': max_damage_structure,
                    'max_damage_content_eur_m2': max_damage_content,
                    'total_building_eur_m2': total_building,
                    'total_landuse_eur_m2': total_landuse,
                    'total_object_eur': total_object,
                    'currency': 'EUR',
                    'base_year': 2010
                })
                
            except Exception as e:
                print(f"    ⚠️ Error procesando país {country}: {e}")
                continue
        
        # Guardar
        df_processed = pd.DataFrame(processed_data)
        output_file = os.path.join(output_dir, 'max_damage_residential_jrc.parquet')
        df_processed.to_parquet(output_file, index=False)
        
        print(f"  ✅ Daños máximos residenciales: {len(df_processed)} países")
        print(f"  📁 Guardado en: {output_file}")
        
    except Exception as e:
        print(f"  ❌ Error procesando daños residenciales: {e}")

def process_max_damage_commercial(excel_file, output_dir):
    """Procesa valores máximos de daño comercial."""
    print("\n🏢 Procesando daños máximos comerciales...")
    
    try:
        df = pd.read_excel(excel_file, sheet_name='MaxDamage-Commercial', engine='openpyxl')
        
        processed_data = []
        
        for idx, row in df.iterrows():
            if idx < 2:  # Saltar headers
                continue
                
            country = row.iloc[0]
            if pd.isna(country):
                continue
            
            try:
                max_damage_structure = float(row.iloc[1]) if not pd.isna(row.iloc[1]) else None
                max_damage_content = float(row.iloc[2]) if not pd.isna(row.iloc[2]) else None
                total_building = float(row.iloc[3]) if not pd.isna(row.iloc[3]) else None
                total_landuse = float(row.iloc[4]) if not pd.isna(row.iloc[4]) else None
                total_object = float(row.iloc[5]) if not pd.isna(row.iloc[5]) else None
                
                processed_data.append({
                    'country': country,
                    'building_type': 'commercial',
                    'max_damage_structure_eur_m2': max_damage_structure,
                    'max_damage_content_eur_m2': max_damage_content,
                    'total_building_eur_m2': total_building,
                    'total_landuse_eur_m2': total_landuse,
                    'total_object_eur': total_object,
                    'currency': 'EUR',
                    'base_year': 2010
                })
                
            except Exception as e:
                continue
        
        # Guardar
        df_processed = pd.DataFrame(processed_data)
        output_file = os.path.join(output_dir, 'max_damage_commercial_jrc.parquet')
        df_processed.to_parquet(output_file, index=False)
        
        print(f"  ✅ Daños máximos comerciales: {len(df_processed)} países")
        print(f"  📁 Guardado en: {output_file}")
        
    except Exception as e:
        print(f"  ❌ Error procesando daños comerciales: {e}")

def process_max_damage_industrial(excel_file, output_dir):
    """Procesa valores máximos de daño industrial."""
    print("\n🏭 Procesando daños máximos industriales...")
    
    try:
        df = pd.read_excel(excel_file, sheet_name='MaxDamage-Industrial', engine='openpyxl')
        
        processed_data = []
        
        for idx, row in df.iterrows():
            if idx < 2:  # Saltar headers
                continue
                
            country = row.iloc[0]
            if pd.isna(country):
                continue
            
            try:
                max_damage_structure = float(row.iloc[1]) if not pd.isna(row.iloc[1]) else None
                max_damage_content = float(row.iloc[2]) if not pd.isna(row.iloc[2]) else None
                total_building = float(row.iloc[3]) if not pd.isna(row.iloc[3]) else None
                total_landuse = float(row.iloc[4]) if not pd.isna(row.iloc[4]) else None
                total_object = float(row.iloc[5]) if not pd.isna(row.iloc[5]) else None
                
                processed_data.append({
                    'country': country,
                    'building_type': 'industrial',
                    'max_damage_structure_eur_m2': max_damage_structure,
                    'max_damage_content_eur_m2': max_damage_content,
                    'total_building_eur_m2': total_building,
                    'total_landuse_eur_m2': total_landuse,
                    'total_object_eur': total_object,
                    'currency': 'EUR',
                    'base_year': 2010
                })
                
            except Exception as e:
                continue
        
        # Guardar
        df_processed = pd.DataFrame(processed_data)
        output_file = os.path.join(output_dir, 'max_damage_industrial_jrc.parquet')
        df_processed.to_parquet(output_file, index=False)
        
        print(f"  ✅ Daños máximos industriales: {len(df_processed)} países")
        print(f"  📁 Guardado en: {output_file}")
        
    except Exception as e:
        print(f"  ❌ Error procesando daños industriales: {e}")

def process_iso_table(excel_file, output_dir):
    """Procesa la tabla de códigos ISO."""
    print("\n🌍 Procesando tabla ISO...")
    
    try:
        df = pd.read_excel(excel_file, sheet_name='ISO_Table', engine='openpyxl')
        
        # Limpiar y estructurar
        processed_data = []
        
        for idx, row in df.iterrows():
            country = row['Country']
            iso_a2 = row['A 2']
            iso_a3 = row['A 3']
            iso_number = row['Number']
            
            if not pd.isna(country):
                processed_data.append({
                    'country_name': country,
                    'iso_alpha2': iso_a2,
                    'iso_alpha3': iso_a3,
                    'iso_numeric': int(iso_number) if not pd.isna(iso_number) else None
                })
        
        # Guardar
        df_processed = pd.DataFrame(processed_data)
        output_file = os.path.join(output_dir, 'iso_table_jrc.parquet')
        df_processed.to_parquet(output_file, index=False)
        
        print(f"  ✅ Tabla ISO procesada: {len(df_processed)} países")
        print(f"  📁 Guardado en: {output_file}")
        
    except Exception as e:
        print(f"  ❌ Error procesando tabla ISO: {e}")

def analyze_processed_data(data_dir):
    """Analiza los datos procesados."""
    print(f"\n📊 Analizando datos procesados en {data_dir}...")
    print("=" * 60)
    
    parquet_files = list(Path(data_dir).glob("*.parquet"))
    
    for file_path in parquet_files:
        print(f"\n📘 {file_path.name}")
        print("-" * 40)
        
        try:
            df = pd.read_parquet(file_path)
            print(f"Dimensiones: {df.shape}")
            print(f"Columnas: {list(df.columns)}")
            
            if len(df) > 0:
                print("Primeras 3 filas:")
                print(df.head(3).to_string())
            
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Función principal."""
    excel_file = 'copy_of_global_flood_depth-damage_functions__30102017.xlsx'
    output_dir = './processed_jrc_data'
    
    if not os.path.exists(excel_file):
        print(f"❌ Archivo Excel no encontrado: {excel_file}")
        return
    
    # Procesar Excel
    process_jrc_excel(excel_file, output_dir)
    
    # Analizar resultados
    analyze_processed_data(output_dir)

if __name__ == "__main__":
    main()