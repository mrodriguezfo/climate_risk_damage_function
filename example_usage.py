"""
Ejemplo de uso de la librería de cálculo de daños por inundación.
"""

from flood_damage_library import FloodDamageCalculator, DataManager
import pandas as pd
import os

def main():
    """Ejemplo principal de uso de la librería."""
    
    # Inicializar la calculadora
    # Si tienes archivos parquet, especifica el directorio donde están
    calculator = FloodDamageCalculator(data_directory="./data")
    
    print("🌊 Librería de Cálculo de Daños por Inundación")
    print("=" * 50)
    
    # Ejemplo 1: Cálculo individual
    print("\n📍 Ejemplo 1: Cálculo de daño individual")
    
    try:
        result = calculator.calculate_damage(
            latitude=40.7128,           # Nueva York (ejemplo)
            longitude=-74.0060,
            flood_depth=1.5,            # 1.5 metros de profundidad
            land_use_type="residential", # Opcional: se puede inferir
            building_type="single_family", # Opcional: se puede inferir
            area=150,                   # 150 m² de área
            value_per_m2=1200          # $1200 por m²
        )
        
        print(f"Ubicación: {result['location']['latitude']}, {result['location']['longitude']}")
        print(f"Profundidad de inundación: {result['flood_parameters']['depth_m']} m")
        print(f"Tipo de uso: {result['property_characteristics']['land_use_type']}")
        print(f"Tipo de edificación: {result['property_characteristics']['building_type']}")
        print(f"Área afectada: {result['property_characteristics']['area_m2']} m²")
        print(f"Valor total de la propiedad: ${result['property_characteristics']['total_value']:,.2f}")
        print(f"Ratio de daño: {result['damage_assessment']['damage_ratio']:.2%}")
        print(f"Daño económico estimado: ${result['damage_assessment']['economic_damage']:,.2f}")
        
    except Exception as e:
        print(f"Error en el cálculo: {e}")
    
    # Ejemplo 2: Cálculo por lotes
    print("\n📍 Ejemplo 2: Cálculo por lotes (múltiples ubicaciones)")
    
    locations = [
        {
            'latitude': 40.7128,
            'longitude': -74.0060,
            'flood_depth': 0.8,
            'land_use_type': 'residential'
        },
        {
            'latitude': 40.7589,
            'longitude': -73.9851,
            'flood_depth': 2.1,
            'land_use_type': 'commercial',
            'area': 300
        },
        {
            'latitude': 40.6892,
            'longitude': -74.0445,
            'flood_depth': 1.2,
            'land_use_type': 'industrial',
            'value_per_m2': 800
        }
    ]
    
    try:
        batch_results = calculator.calculate_damage_batch(locations)
        
        print(f"Procesadas {len(batch_results)} ubicaciones:")
        
        for i, result in enumerate(batch_results):
            if 'error' not in result:
                print(f"  Ubicación {i+1}: ${result['damage_assessment']['economic_damage']:,.2f} de daño")
            else:
                print(f"  Ubicación {i+1}: Error - {result['error']}")
        
        # Estadísticas resumen
        stats = calculator.get_damage_summary_statistics(batch_results)
        if 'error' not in stats:
            print(f"\n📊 Estadísticas resumen:")
            print(f"  Daño total: ${stats['economic_damage']['total']:,.2f}")
            print(f"  Daño promedio: ${stats['economic_damage']['mean']:,.2f}")
            print(f"  Ratio de daño promedio: {stats['damage_ratios']['mean']:.2%}")
        
    except Exception as e:
        print(f"Error en el cálculo por lotes: {e}")
    
    # Ejemplo 3: Información sobre datos disponibles
    print("\n📊 Ejemplo 3: Información sobre datos disponibles")
    
    try:
        data_info = calculator.data_manager.list_available_data()
        print("Datos cargados:")
        for key, value in data_info.items():
            print(f"  {key}: {value}")
            
    except Exception as e:
        print(f"Error al obtener información de datos: {e}")

def create_sample_parquet_files():
    """
    Crea archivos parquet de ejemplo para demostrar la funcionalidad.
    Ejecuta esta función si no tienes archivos parquet existentes.
    """
    import os
    
    # Crear directorio de datos
    os.makedirs("./data", exist_ok=True)
    
    # Crear archivo de funciones de daño de ejemplo
    damage_functions_data = []
    
    # Funciones para diferentes combinaciones
    land_uses = ['residential', 'commercial', 'industrial']
    building_types = ['single_family', 'multi_family', 'office', 'retail', 'warehouse']
    
    for land_use in land_uses:
        for building_type in building_types:
            if land_use == 'residential':
                depths = [0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
                base_ratios = [0, 0.15, 0.35, 0.50, 0.65, 0.80, 0.90, 0.95]
            elif land_use == 'commercial':
                depths = [0, 0.3, 0.6, 1.0, 1.5, 2.0, 3.0, 4.0]
                base_ratios = [0, 0.20, 0.40, 0.60, 0.75, 0.85, 0.92, 0.97]
            else:  # industrial
                depths = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
                base_ratios = [0, 0.10, 0.25, 0.40, 0.55, 0.70, 0.80, 0.90]
            
            # Ajustar ratios según tipo de edificación
            multiplier = 1.0
            if building_type == 'multi_family':
                multiplier = 1.1
            elif building_type == 'office':
                multiplier = 1.2
            elif building_type == 'warehouse':
                multiplier = 0.8
            
            for depth, ratio in zip(depths, base_ratios):
                damage_functions_data.append({
                    'land_use_type': land_use,
                    'building_type': building_type,
                    'depth': depth,
                    'damage_ratio': min(ratio * multiplier, 1.0)
                })
    
    df_damage = pd.DataFrame(damage_functions_data)
    df_damage.to_parquet("./data/damage_functions.parquet", index=False)
    
    # Crear archivo de uso de suelo de ejemplo
    land_use_data = []
    for i in range(1000):
        land_use_data.append({
            'latitude': 40.7 + (i % 100) * 0.001,
            'longitude': -74.0 + (i // 100) * 0.001,
            'land_use_type': land_uses[i % len(land_uses)]
        })
    
    df_land_use = pd.DataFrame(land_use_data)
    df_land_use.to_parquet("./data/land_use.parquet", index=False)
    
    # Crear archivo de tipos de edificación de ejemplo
    building_data = []
    for i in range(1000):
        building_data.append({
            'latitude': 40.7 + (i % 100) * 0.001,
            'longitude': -74.0 + (i // 100) * 0.001,
            'building_type': building_types[i % len(building_types)],
            'value_per_m2': 800 + (i % 800)  # Valores entre $800-1600 por m²
        })
    
    df_buildings = pd.DataFrame(building_data)
    df_buildings.to_parquet("./data/building_types.parquet", index=False)
    
    print("✅ Archivos parquet de ejemplo creados en ./data/")
    print("  - damage_functions.parquet")
    print("  - land_use.parquet") 
    print("  - building_types.parquet")

if __name__ == "__main__":
    # Crear archivos de ejemplo si no existen
    if not os.path.exists("./data"):
        print("📁 Creando archivos de datos de ejemplo...")
        create_sample_parquet_files()
        print()
    
    # Ejecutar ejemplos
    main()