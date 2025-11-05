"""
Ejemplo de uso de la librería con datos reales del JRC.
Demuestra cómo usar las funciones de daño globales del Joint Research Centre.
"""

from flood_damage_library import JRCFloodDamageCalculator
import pandas as pd
import os

def main():
    """Ejemplo principal usando datos del JRC."""
    
    print("🌊 Librería de Cálculo de Daños por Inundación - Datos JRC")
    print("=" * 70)
    
    # Verificar si existen los datos procesados del JRC
    jrc_data_dir = "./processed_jrc_data"
    if not os.path.exists(jrc_data_dir):
        print("❌ Datos del JRC no encontrados.")
        print("💡 Ejecuta primero: python process_jrc_excel.py")
        return
    
    try:
        # Inicializar calculadora JRC
        print("🔧 Inicializando calculadora JRC...")
        calculator = JRCFloodDamageCalculator(data_directory=jrc_data_dir)
        
        print(f"\n📊 Información de la base de datos JRC:")
        print(f"  - Regiones disponibles: {calculator.get_available_regions()}")
        print(f"  - Tipos de edificación: {calculator.get_available_building_types()}")
        print(f"  - Países con datos residenciales: {len(calculator.get_countries_with_data('residential'))}")
        
        # Ejemplo 1: Cálculo para una ubicación en Europa (Alemania)
        print(f"\n📍 Ejemplo 1: Daño en Alemania (Europa)")
        print("-" * 50)
        
        result_de = calculator.calculate_jrc_damage(
            latitude=52.5200,  # Berlín
            longitude=13.4050,
            flood_depth=1.5,
            country_code='DE',
            building_type='residential',
            area_m2=120
        )
        
        print_result_summary(result_de, "Berlín, Alemania")
        
        # Ejemplo 2: Cálculo para una ubicación en América del Norte (Estados Unidos)
        print(f"\n📍 Ejemplo 2: Daño en Estados Unidos (América del Norte)")
        print("-" * 50)
        
        result_us = calculator.calculate_jrc_damage(
            latitude=40.7128,  # Nueva York
            longitude=-74.0060,
            flood_depth=2.0,
            country_code='US',
            building_type='commercial',
            area_m2=200
        )
        
        print_result_summary(result_us, "Nueva York, Estados Unidos")
        
        # Ejemplo 3: Cálculo para una ubicación en Asia (Japón)
        print(f"\n📍 Ejemplo 3: Daño en Japón (Asia)")
        print("-" * 50)
        
        result_jp = calculator.calculate_jrc_damage(
            latitude=35.6762,  # Tokio
            longitude=139.6503,
            flood_depth=1.0,
            country_code='JP',
            building_type='industrial',
            area_m2=500
        )
        
        print_result_summary(result_jp, "Tokio, Japón")
        
        # Ejemplo 4: Cálculo por lotes para múltiples ubicaciones
        print(f"\n📍 Ejemplo 4: Análisis por lotes (múltiples ubicaciones)")
        print("-" * 50)
        
        locations = [
            {
                'latitude': 52.5200, 'longitude': 13.4050, 'flood_depth': 1.5,
                'country_code': 'DE', 'building_type': 'residential', 'area_m2': 100,
                'name': 'Berlín'
            },
            {
                'latitude': 48.8566, 'longitude': 2.3522, 'flood_depth': 2.0,
                'country_code': 'FR', 'building_type': 'commercial', 'area_m2': 150,
                'name': 'París'
            },
            {
                'latitude': 41.9028, 'longitude': 12.4964, 'flood_depth': 1.2,
                'country_code': 'IT', 'building_type': 'residential', 'area_m2': 80,
                'name': 'Roma'
            },
            {
                'latitude': 40.4168, 'longitude': -3.7038, 'flood_depth': 1.8,
                'country_code': 'ES', 'building_type': 'industrial', 'area_m2': 300,
                'name': 'Madrid'
            }
        ]
        
        batch_results = calculator.calculate_damage_batch_jrc(locations)
        
        print("Resultados del análisis por lotes:")
        total_damage = 0
        
        for i, result in enumerate(batch_results):
            if 'error' not in result:
                location_name = locations[i].get('name', f'Ubicación {i+1}')
                damage = result['damage_assessment']['economic_damage_eur']
                region = result['location']['region']
                building_type = result['property_characteristics']['building_type']
                
                print(f"  {location_name}: €{damage:,.2f} ({building_type}, {region})")
                total_damage += damage
            else:
                print(f"  Ubicación {i+1}: Error - {result['error']}")
        
        print(f"\n💰 Daño total estimado: €{total_damage:,.2f}")
        
        # Ejemplo 5: Comparación entre regiones
        print(f"\n📊 Ejemplo 5: Comparación entre regiones")
        print("-" * 50)
        
        compare_regions(calculator)
        
        # Ejemplo 6: Análisis de incertidumbre
        print(f"\n📈 Ejemplo 6: Análisis de incertidumbre detallado")
        print("-" * 50)
        
        analyze_uncertainty(result_de)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Asegúrate de que los datos del JRC estén procesados correctamente.")

def print_result_summary(result, location_name):
    """Imprime un resumen de los resultados."""
    
    if 'error' in result:
        print(f"❌ Error en {location_name}: {result['error']}")
        return
    
    location = result['location']
    flood_params = result['flood_parameters']
    property_chars = result['property_characteristics']
    damage_assessment = result['damage_assessment']
    jrc_data = result['jrc_data']
    uncertainty = result['uncertainty_analysis']
    
    print(f"🏠 Ubicación: {location_name}")
    print(f"🌍 País: {location['country_name']} ({location['country_code']})")
    print(f"🗺️  Región JRC: {location['region']}")
    print(f"🌊 Profundidad: {flood_params['depth_m']} m")
    print(f"🏢 Tipo: {property_chars['building_type']}")
    print(f"📐 Área: {property_chars['area_m2']} m²")
    print(f"💶 Valor máximo: €{property_chars['max_damage_per_m2_eur']:.2f}/m²")
    print(f"💰 Valor total: €{property_chars['total_value_eur']:,.2f}")
    print(f"📊 Ratio de daño: {damage_assessment['damage_ratio']:.1%}")
    print(f"💸 Daño económico: €{damage_assessment['economic_damage_eur']:,.2f}")
    
    # Mostrar intervalo de confianza
    ci_95 = uncertainty['confidence_interval_95']
    print(f"📈 IC 95%: €{ci_95['lower_eur']:,.0f} - €{ci_95['upper_eur']:,.0f}")

def compare_regions(calculator):
    """Compara daños entre diferentes regiones para las mismas condiciones."""
    
    # Condiciones estándar
    latitude, longitude = 50.0, 10.0  # Coordenadas genéricas
    flood_depth = 1.5
    building_type = 'residential'
    area_m2 = 100
    
    regions = ['EUROPE', 'North AMERICA', 'ASIA', 'GLOBAL']
    
    print("Comparación de daños para las mismas condiciones:")
    print(f"  Profundidad: {flood_depth} m, Tipo: {building_type}, Área: {area_m2} m²")
    print()
    
    for region in regions:
        try:
            # Usar un país representativo de cada región
            country_mapping = {
                'EUROPE': 'DE',
                'North AMERICA': 'US', 
                'ASIA': 'JP',
                'GLOBAL': 'US'
            }
            
            result = calculator.calculate_jrc_damage(
                latitude=latitude,
                longitude=longitude,
                flood_depth=flood_depth,
                country_code=country_mapping[region],
                building_type=building_type,
                area_m2=area_m2,
                region=region
            )
            
            damage = result['damage_assessment']['economic_damage_eur']
            ratio = result['damage_assessment']['damage_ratio']
            
            print(f"  {region:20}: €{damage:8,.0f} (ratio: {ratio:.1%})")
            
        except Exception as e:
            print(f"  {region:20}: Error - {str(e)[:50]}")

def analyze_uncertainty(result):
    """Analiza la incertidumbre de un resultado."""
    
    if 'uncertainty_analysis' not in result:
        print("No hay datos de incertidumbre disponibles.")
        return
    
    uncertainty = result['uncertainty_analysis']
    damage = result['damage_assessment']['economic_damage_eur']
    
    print("Análisis detallado de incertidumbre:")
    print(f"  Daño estimado: €{damage:,.2f}")
    print(f"  Desviación estándar: {uncertainty['standard_deviation_ratio']:.1%}")
    print(f"  Desviación en €: €{uncertainty['damage_standard_deviation_eur']:,.2f}")
    
    # Intervalos de confianza
    ci_68 = uncertainty['confidence_interval_68']
    ci_95 = uncertainty['confidence_interval_95']
    
    print(f"\n  Intervalos de confianza:")
    print(f"    68% (±1σ): €{ci_68['lower_eur']:,.0f} - €{ci_68['upper_eur']:,.0f}")
    print(f"    95% (±2σ): €{ci_95['lower_eur']:,.0f} - €{ci_95['upper_eur']:,.0f}")
    
    # Rango de incertidumbre
    range_68 = ci_68['upper_eur'] - ci_68['lower_eur']
    range_95 = ci_95['upper_eur'] - ci_95['lower_eur']
    
    print(f"\n  Rangos de incertidumbre:")
    print(f"    68%: ±€{range_68/2:,.0f} ({range_68/damage:.1%} del daño estimado)")
    print(f"    95%: ±€{range_95/2:,.0f} ({range_95/damage:.1%} del daño estimado)")

if __name__ == "__main__":
    main()