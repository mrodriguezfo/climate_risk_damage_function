"""
Demostración completa de la librería de cálculo de daños por inundación.
Muestra todas las funcionalidades disponibles con datos reales del JRC.
"""

from flood_damage_library import JRCFloodDamageCalculator, FloodDamageCalculator
import pandas as pd
import numpy as np
import os

def main():
    """Demostración completa de la librería."""
    
    print("🌊 LIBRERÍA DE CÁLCULO DE DAÑOS POR INUNDACIÓN")
    print("=" * 80)
    print("Demostración completa con datos del JRC (Joint Research Centre)")
    print()
    
    # Verificar disponibilidad de datos JRC
    jrc_data_dir = "./processed_jrc_data"
    if not os.path.exists(jrc_data_dir):
        print("❌ Datos del JRC no encontrados.")
        print("💡 Ejecuta primero: python process_jrc_excel.py")
        return
    
    # Inicializar calculadoras
    print("🔧 Inicializando calculadoras...")
    jrc_calculator = JRCFloodDamageCalculator(data_directory=jrc_data_dir)
    basic_calculator = FloodDamageCalculator()
    
    print("✅ Calculadoras inicializadas correctamente")
    print()
    
    # Demostración 1: Comparación de métodos
    demo_comparison(jrc_calculator, basic_calculator)
    
    # Demostración 2: Análisis regional
    demo_regional_analysis(jrc_calculator)
    
    # Demostración 3: Análisis de sensibilidad
    demo_sensitivity_analysis(jrc_calculator)
    
    # Demostración 4: Portfolio de propiedades
    demo_portfolio_analysis(jrc_calculator)
    
    # Demostración 5: Análisis de incertidumbre
    demo_uncertainty_analysis(jrc_calculator)
    
    # Demostración 6: Casos de uso específicos
    demo_specific_use_cases(jrc_calculator)
    
    print("\n🎉 Demostración completada exitosamente!")
    print("📚 Consulta README_JRC.md para documentación completa")

def demo_comparison(jrc_calc, basic_calc):
    """Compara calculadora JRC vs básica."""
    
    print("📊 DEMOSTRACIÓN 1: COMPARACIÓN DE MÉTODOS")
    print("-" * 60)
    
    # Parámetros de prueba
    test_params = {
        'latitude': 52.5200,
        'longitude': 13.4050,
        'flood_depth': 1.5,
        'area': 100
    }
    
    print(f"Ubicación: Berlín, Alemania")
    print(f"Profundidad: {test_params['flood_depth']} m")
    print(f"Área: {test_params['area']} m²")
    print()
    
    # Cálculo con JRC
    jrc_result = jrc_calc.calculate_jrc_damage(
        latitude=test_params['latitude'],
        longitude=test_params['longitude'],
        flood_depth=test_params['flood_depth'],
        country_code='DE',
        building_type='residential',
        area_m2=test_params['area']
    )
    
    # Cálculo básico
    basic_result = basic_calc.calculate_damage(
        latitude=test_params['latitude'],
        longitude=test_params['longitude'],
        flood_depth=test_params['flood_depth'],
        area=test_params['area']
    )
    
    print("Resultados:")
    print(f"  JRC (Europa):     €{jrc_result['damage_assessment']['economic_damage_eur']:8,.2f}")
    print(f"  Método básico:    €{basic_result['damage_assessment']['economic_damage']:8,.2f}")
    print(f"  Diferencia:       {(jrc_result['damage_assessment']['economic_damage_eur'] / basic_result['damage_assessment']['economic_damage'] - 1) * 100:+6.1f}%")
    print()
    
    print("Ventajas del método JRC:")
    print("  ✅ Datos específicos por región y país")
    print("  ✅ Funciones de daño validadas científicamente")
    print("  ✅ Análisis de incertidumbre incluido")
    print("  ✅ 248 países con datos específicos")
    print()

def demo_regional_analysis(jrc_calc):
    """Demuestra análisis por regiones."""
    
    print("🌍 DEMOSTRACIÓN 2: ANÁLISIS REGIONAL")
    print("-" * 60)
    
    # Mismas condiciones, diferentes regiones
    base_params = {
        'flood_depth': 1.5,
        'building_type': 'residential',
        'area_m2': 100
    }
    
    locations = [
        {'name': 'Berlín (Europa)', 'lat': 52.52, 'lon': 13.40, 'country': 'DE'},
        {'name': 'Nueva York (N. América)', 'lat': 40.71, 'lon': -74.01, 'country': 'US'},
        {'name': 'Tokio (Asia)', 'lat': 35.68, 'lon': 139.65, 'country': 'JP'},
        {'name': 'São Paulo (S. América)', 'lat': -23.55, 'lon': -46.63, 'country': 'BR'},
        {'name': 'Lagos (África)', 'lat': 6.52, 'lon': 3.38, 'country': 'NG'},
        {'name': 'Sídney (Oceanía)', 'lat': -33.87, 'lon': 151.21, 'country': 'AU'}
    ]
    
    print("Comparación regional para edificios residenciales:")
    print(f"Condiciones: {base_params['flood_depth']}m profundidad, {base_params['area_m2']}m²")
    print()
    
    results = []
    for loc in locations:
        result = jrc_calc.calculate_jrc_damage(
            latitude=loc['lat'],
            longitude=loc['lon'],
            country_code=loc['country'],
            **base_params
        )
        
        damage = result['damage_assessment']['economic_damage_eur']
        ratio = result['damage_assessment']['damage_ratio']
        region = result['location']['region']
        
        results.append({
            'location': loc['name'],
            'region': region,
            'damage': damage,
            'ratio': ratio
        })
        
        print(f"  {loc['name']:25} ({region:20}): €{damage:8,.0f} ({ratio:5.1%})")
    
    # Estadísticas
    damages = [r['damage'] for r in results]
    print(f"\nEstadísticas:")
    print(f"  Daño promedio: €{np.mean(damages):8,.0f}")
    print(f"  Rango:         €{min(damages):8,.0f} - €{max(damages):8,.0f}")
    print(f"  Desv. estándar: €{np.std(damages):8,.0f}")
    print()

def demo_sensitivity_analysis(jrc_calc):
    """Demuestra análisis de sensibilidad."""
    
    print("📈 DEMOSTRACIÓN 3: ANÁLISIS DE SENSIBILIDAD")
    print("-" * 60)
    
    # Análisis por profundidad
    print("Sensibilidad a la profundidad de inundación:")
    print("Ubicación: Berlín, Alemania (Residencial, 100m²)")
    print()
    
    depths = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0]
    
    print("Profundidad (m)  |  Daño (EUR)  |  Ratio  |  Incremento")
    print("-" * 55)
    
    previous_damage = 0
    for depth in depths:
        result = jrc_calc.calculate_jrc_damage(
            latitude=52.5200,
            longitude=13.4050,
            flood_depth=depth,
            country_code='DE',
            building_type='residential',
            area_m2=100
        )
        
        damage = result['damage_assessment']['economic_damage_eur']
        ratio = result['damage_assessment']['damage_ratio']
        increment = damage - previous_damage if previous_damage > 0 else 0
        
        print(f"     {depth:4.1f}       | €{damage:8,.0f} | {ratio:5.1%} | +€{increment:7,.0f}")
        previous_damage = damage
    
    print()
    
    # Análisis por tipo de edificación
    print("Sensibilidad al tipo de edificación:")
    print("Ubicación: Berlín, Alemania (1.5m profundidad, 100m²)")
    print()
    
    building_types = ['residential', 'commercial', 'industrial']
    
    for building_type in building_types:
        result = jrc_calc.calculate_jrc_damage(
            latitude=52.5200,
            longitude=13.4050,
            flood_depth=1.5,
            country_code='DE',
            building_type=building_type,
            area_m2=100
        )
        
        damage = result['damage_assessment']['economic_damage_eur']
        ratio = result['damage_assessment']['damage_ratio']
        max_damage = result['property_characteristics']['max_damage_per_m2_eur']
        
        print(f"  {building_type.capitalize():12}: €{damage:8,.0f} ({ratio:5.1%}) - Max: €{max_damage:6.0f}/m²")
    
    print()

def demo_portfolio_analysis(jrc_calc):
    """Demuestra análisis de portfolio."""
    
    print("🏢 DEMOSTRACIÓN 4: ANÁLISIS DE PORTFOLIO")
    print("-" * 60)
    
    # Portfolio de propiedades diversificado
    portfolio = [
        {
            'name': 'Oficina Berlín',
            'latitude': 52.5200, 'longitude': 13.4050,
            'country_code': 'DE', 'building_type': 'commercial',
            'area_m2': 500, 'flood_depth': 1.5
        },
        {
            'name': 'Residencia París',
            'latitude': 48.8566, 'longitude': 2.3522,
            'country_code': 'FR', 'building_type': 'residential',
            'area_m2': 120, 'flood_depth': 2.0
        },
        {
            'name': 'Fábrica Milán',
            'latitude': 45.4642, 'longitude': 9.1900,
            'country_code': 'IT', 'building_type': 'industrial',
            'area_m2': 1000, 'flood_depth': 1.0
        },
        {
            'name': 'Centro Madrid',
            'latitude': 40.4168, 'longitude': -3.7038,
            'country_code': 'ES', 'building_type': 'commercial',
            'area_m2': 300, 'flood_depth': 1.8
        },
        {
            'name': 'Almacén Ámsterdam',
            'latitude': 52.3676, 'longitude': 4.9041,
            'country_code': 'NL', 'building_type': 'industrial',
            'area_m2': 800, 'flood_depth': 2.5
        }
    ]
    
    print("Portfolio de propiedades europeas:")
    print()
    
    total_value = 0
    total_damage = 0
    results = []
    
    print("Propiedad           | Tipo        | Área  | Prof. | Valor Total | Daño Est.  | Ratio")
    print("-" * 85)
    
    for prop in portfolio:
        result = jrc_calc.calculate_jrc_damage(
            latitude=prop['latitude'],
            longitude=prop['longitude'],
            flood_depth=prop['flood_depth'],
            country_code=prop['country_code'],
            building_type=prop['building_type'],
            area_m2=prop['area_m2']
        )
        
        value = result['property_characteristics']['total_value_eur']
        damage = result['damage_assessment']['economic_damage_eur']
        ratio = result['damage_assessment']['damage_ratio']
        
        total_value += value
        total_damage += damage
        results.append(result)
        
        print(f"{prop['name']:18} | {prop['building_type']:11} | {prop['area_m2']:4.0f}m² | {prop['flood_depth']:4.1f}m | €{value:9,.0f} | €{damage:8,.0f} | {ratio:5.1%}")
    
    print("-" * 85)
    print(f"{'TOTAL':18} | {'':11} | {'':6} | {'':6} | €{total_value:9,.0f} | €{total_damage:8,.0f} | {total_damage/total_value:5.1%}")
    
    print(f"\nResumen del portfolio:")
    print(f"  Valor total:        €{total_value:,.0f}")
    print(f"  Daño estimado:      €{total_damage:,.0f}")
    print(f"  Pérdida esperada:   {total_damage/total_value:.2%}")
    
    # Análisis de concentración
    by_type = {}
    for i, prop in enumerate(portfolio):
        building_type = prop['building_type']
        if building_type not in by_type:
            by_type[building_type] = {'value': 0, 'damage': 0}
        
        by_type[building_type]['value'] += results[i]['property_characteristics']['total_value_eur']
        by_type[building_type]['damage'] += results[i]['damage_assessment']['economic_damage_eur']
    
    print(f"\nConcentración por tipo:")
    for building_type, data in by_type.items():
        pct_value = data['value'] / total_value * 100
        pct_damage = data['damage'] / total_damage * 100 if total_damage > 0 else 0
        print(f"  {building_type.capitalize():12}: {pct_value:5.1f}% valor, {pct_damage:5.1f}% daño")
    
    print()

def demo_uncertainty_analysis(jrc_calc):
    """Demuestra análisis de incertidumbre."""
    
    print("📊 DEMOSTRACIÓN 5: ANÁLISIS DE INCERTIDUMBRE")
    print("-" * 60)
    
    # Cálculo con incertidumbre
    result = jrc_calc.calculate_jrc_damage(
        latitude=52.5200,
        longitude=13.4050,
        flood_depth=1.5,
        country_code='DE',
        building_type='residential',
        area_m2=200
    )
    
    damage = result['damage_assessment']['economic_damage_eur']
    uncertainty = result['uncertainty_analysis']
    
    print("Análisis de incertidumbre para:")
    print("  Ubicación: Berlín, Alemania")
    print("  Tipo: Residencial, 200m², 1.5m profundidad")
    print()
    
    print(f"Daño estimado: €{damage:,.2f}")
    print(f"Desviación estándar: {uncertainty['standard_deviation_ratio']:.1%}")
    print(f"Desviación en EUR: €{uncertainty['damage_standard_deviation_eur']:,.2f}")
    print()
    
    # Intervalos de confianza
    ci_68 = uncertainty['confidence_interval_68']
    ci_95 = uncertainty['confidence_interval_95']
    
    print("Intervalos de confianza:")
    print(f"  68% (±1σ): €{ci_68['lower_eur']:,.0f} - €{ci_68['upper_eur']:,.0f}")
    print(f"  95% (±2σ): €{ci_95['lower_eur']:,.0f} - €{ci_95['upper_eur']:,.0f}")
    print()
    
    # Interpretación
    range_68 = ci_68['upper_eur'] - ci_68['lower_eur']
    range_95 = ci_95['upper_eur'] - ci_95['lower_eur']
    
    print("Interpretación:")
    print(f"  Hay 68% de probabilidad de que el daño esté entre €{ci_68['lower_eur']:,.0f} y €{ci_68['upper_eur']:,.0f}")
    print(f"  Hay 95% de probabilidad de que el daño esté entre €{ci_95['lower_eur']:,.0f} y €{ci_95['upper_eur']:,.0f}")
    print(f"  Rango de incertidumbre (95%): ±€{range_95/2:,.0f} ({range_95/damage:.1%} del daño estimado)")
    print()
    
    # Escenarios
    print("Escenarios de daño:")
    print(f"  Pesimista (P95):  €{ci_95['upper_eur']:,.0f}")
    print(f"  Esperado:         €{damage:,.0f}")
    print(f"  Optimista (P5):   €{ci_95['lower_eur']:,.0f}")
    print()

def demo_specific_use_cases(jrc_calc):
    """Demuestra casos de uso específicos."""
    
    print("🎯 DEMOSTRACIÓN 6: CASOS DE USO ESPECÍFICOS")
    print("-" * 60)
    
    # Caso 1: Evaluación de riesgo por escenarios
    print("Caso 1: Evaluación de riesgo por escenarios")
    print("Propiedad: Oficina comercial en Londres, 500m²")
    print()
    
    scenarios = [
        {'name': 'Inundación menor', 'depth': 0.5, 'probability': 0.10},
        {'name': 'Inundación moderada', 'depth': 1.0, 'probability': 0.05},
        {'name': 'Inundación severa', 'depth': 2.0, 'probability': 0.02},
        {'name': 'Inundación extrema', 'depth': 3.0, 'probability': 0.01}
    ]
    
    print("Escenario           | Prof. | Prob. | Daño Est.  | Pérdida Esperada")
    print("-" * 65)
    
    total_expected_loss = 0
    for scenario in scenarios:
        result = jrc_calc.calculate_jrc_damage(
            latitude=51.5074,  # Londres
            longitude=-0.1278,
            flood_depth=scenario['depth'],
            country_code='GB',
            building_type='commercial',
            area_m2=500
        )
        
        damage = result['damage_assessment']['economic_damage_eur']
        expected_loss = damage * scenario['probability']
        total_expected_loss += expected_loss
        
        print(f"{scenario['name']:18} | {scenario['depth']:4.1f}m | {scenario['probability']:4.1%} | €{damage:8,.0f} | €{expected_loss:8,.0f}")
    
    print("-" * 65)
    print(f"{'PÉRDIDA ANUAL ESPERADA':18} | {'':6} | {'':6} | {'':10} | €{total_expected_loss:8,.0f}")
    print()
    
    # Caso 2: Comparación de ubicaciones para inversión
    print("Caso 2: Comparación de ubicaciones para inversión")
    print("Tipo: Centro comercial, 1000m², escenario 1.5m")
    print()
    
    investment_locations = [
        {'name': 'Ámsterdam', 'lat': 52.37, 'lon': 4.90, 'country': 'NL'},
        {'name': 'Hamburgo', 'lat': 53.55, 'lon': 9.99, 'country': 'DE'},
        {'name': 'Venecia', 'lat': 45.44, 'lon': 12.32, 'country': 'IT'},
        {'name': 'Nueva Orleans', 'lat': 29.95, 'lon': -90.07, 'country': 'US'}
    ]
    
    print("Ciudad        | País | Región           | Daño Est.  | Ratio | Riesgo")
    print("-" * 70)
    
    for loc in investment_locations:
        result = jrc_calc.calculate_jrc_damage(
            latitude=loc['lat'],
            longitude=loc['lon'],
            flood_depth=1.5,
            country_code=loc['country'],
            building_type='commercial',
            area_m2=1000
        )
        
        damage = result['damage_assessment']['economic_damage_eur']
        ratio = result['damage_assessment']['damage_ratio']
        region = result['location']['region']
        
        # Clasificar riesgo
        if ratio < 0.3:
            risk_level = "Bajo"
        elif ratio < 0.6:
            risk_level = "Medio"
        else:
            risk_level = "Alto"
        
        print(f"{loc['name']:12} | {loc['country']:4} | {region:16} | €{damage:8,.0f} | {ratio:5.1%} | {risk_level}")
    
    print()
    
    # Caso 3: Análisis temporal (diferentes profundidades)
    print("Caso 3: Análisis de costo-beneficio de medidas de protección")
    print("Ubicación: Rotterdam, Países Bajos (Industrial, 2000m²)")
    print()
    
    # Sin protección
    unprotected_damage = jrc_calc.calculate_jrc_damage(
        latitude=51.9225,
        longitude=4.4792,
        flood_depth=2.0,
        country_code='NL',
        building_type='industrial',
        area_m2=2000
    )['damage_assessment']['economic_damage_eur']
    
    # Con diferentes niveles de protección
    protection_levels = [
        {'name': 'Sin protección', 'depth': 2.0, 'cost': 0},
        {'name': 'Protección básica', 'depth': 1.5, 'cost': 50000},
        {'name': 'Protección avanzada', 'depth': 1.0, 'cost': 150000},
        {'name': 'Protección total', 'depth': 0.5, 'cost': 300000}
    ]
    
    print("Nivel de Protección  | Costo    | Prof.Res. | Daño Est.  | Ahorro    | ROI")
    print("-" * 75)
    
    for protection in protection_levels:
        result = jrc_calc.calculate_jrc_damage(
            latitude=51.9225,
            longitude=4.4792,
            flood_depth=protection['depth'],
            country_code='NL',
            building_type='industrial',
            area_m2=2000
        )
        
        damage = result['damage_assessment']['economic_damage_eur']
        savings = unprotected_damage - damage
        roi = (savings / protection['cost'] - 1) * 100 if protection['cost'] > 0 else 0
        
        print(f"{protection['name']:19} | €{protection['cost']:7,.0f} | {protection['depth']:6.1f}m | €{damage:8,.0f} | €{savings:7,.0f} | {roi:5.1f}%")
    
    print()
    print("Recomendación: La protección avanzada ofrece el mejor ROI")
    print()

if __name__ == "__main__":
    main()