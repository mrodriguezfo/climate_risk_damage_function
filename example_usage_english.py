"""
Example usage of the Flood Damage Library with real JRC data.
Demonstrates how to use the global damage functions from the Joint Research Centre.
"""

from flood_damage_library import JRCFloodDamageCalculator
import pandas as pd
import os

def main():
    """Main example using JRC data."""
    
    print("🌊 Flood Damage Calculation Library - JRC Data")
    print("=" * 70)
    
    # Check if JRC processed data exists
    jrc_data_dir = "./processed_jrc_data"
    if not os.path.exists(jrc_data_dir):
        print("❌ JRC data not found.")
        print("💡 Run first: python process_jrc_excel.py")
        return
    
    try:
        # Initialize JRC calculator
        print("🔧 Initializing JRC calculator...")
        calculator = JRCFloodDamageCalculator(data_directory=jrc_data_dir)
        
        print(f"\n📊 JRC Database Information:")
        print(f"  - Available regions: {calculator.get_available_regions()}")
        print(f"  - Building types: {calculator.get_available_building_types()}")
        print(f"  - Countries with residential data: {len(calculator.get_countries_with_data('residential'))}")
        
        # Example 1: Damage calculation for Germany (Europe)
        print(f"\n📍 Example 1: Damage in Germany (Europe)")
        print("-" * 50)
        
        result_de = calculator.calculate_jrc_damage(
            latitude=52.5200,  # Berlin
            longitude=13.4050,
            flood_depth=1.5,
            country_code='DE',
            building_type='residential',
            area_m2=120
        )
        
        print_result_summary(result_de, "Berlin, Germany")
        
        # Example 2: Damage calculation for United States (North America)
        print(f"\n📍 Example 2: Damage in United States (North America)")
        print("-" * 50)
        
        result_us = calculator.calculate_jrc_damage(
            latitude=40.7128,  # New York
            longitude=-74.0060,
            flood_depth=2.0,
            country_code='US',
            building_type='commercial',
            area_m2=200
        )
        
        print_result_summary(result_us, "New York, United States")
        
        # Example 3: Damage calculation for Japan (Asia)
        print(f"\n📍 Example 3: Damage in Japan (Asia)")
        print("-" * 50)
        
        result_jp = calculator.calculate_jrc_damage(
            latitude=35.6762,  # Tokyo
            longitude=139.6503,
            flood_depth=1.0,
            country_code='JP',
            building_type='industrial',
            area_m2=500
        )
        
        print_result_summary(result_jp, "Tokyo, Japan")
        
        # Example 4: Batch calculation for multiple locations
        print(f"\n📍 Example 4: Batch analysis (multiple locations)")
        print("-" * 50)
        
        locations = [
            {
                'latitude': 52.5200, 'longitude': 13.4050, 'flood_depth': 1.5,
                'country_code': 'DE', 'building_type': 'residential', 'area_m2': 100,
                'name': 'Berlin'
            },
            {
                'latitude': 48.8566, 'longitude': 2.3522, 'flood_depth': 2.0,
                'country_code': 'FR', 'building_type': 'commercial', 'area_m2': 150,
                'name': 'Paris'
            },
            {
                'latitude': 41.9028, 'longitude': 12.4964, 'flood_depth': 1.2,
                'country_code': 'IT', 'building_type': 'residential', 'area_m2': 80,
                'name': 'Rome'
            },
            {
                'latitude': 40.4168, 'longitude': -3.7038, 'flood_depth': 1.8,
                'country_code': 'ES', 'building_type': 'industrial', 'area_m2': 300,
                'name': 'Madrid'
            }
        ]
        
        batch_results = calculator.calculate_damage_batch_jrc(locations)
        
        print("Batch analysis results:")
        total_damage = 0
        
        for i, result in enumerate(batch_results):
            if 'error' not in result:
                location_name = locations[i].get('name', f'Location {i+1}')
                damage = result['damage_assessment']['economic_damage_eur']
                region = result['location']['region']
                building_type = result['property_characteristics']['building_type']
                
                print(f"  {location_name}: €{damage:,.2f} ({building_type}, {region})")
                total_damage += damage
            else:
                print(f"  Location {i+1}: Error - {result['error']}")
        
        print(f"\n💰 Total estimated damage: €{total_damage:,.2f}")
        
        # Example 5: Regional comparison
        print(f"\n📊 Example 5: Regional comparison")
        print("-" * 50)
        
        compare_regions(calculator)
        
        # Example 6: Uncertainty analysis
        print(f"\n📈 Example 6: Detailed uncertainty analysis")
        print("-" * 50)
        
        analyze_uncertainty(result_de)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure JRC data is processed correctly.")

def print_result_summary(result, location_name):
    """Print a summary of the results."""
    
    if 'error' in result:
        print(f"❌ Error in {location_name}: {result['error']}")
        return
    
    location = result['location']
    flood_params = result['flood_parameters']
    property_chars = result['property_characteristics']
    damage_assessment = result['damage_assessment']
    jrc_data = result['jrc_data']
    uncertainty = result['uncertainty_analysis']
    
    print(f"🏠 Location: {location_name}")
    print(f"🌍 Country: {location['country_name']} ({location['country_code']})")
    print(f"🗺️  JRC Region: {location['region']}")
    print(f"🌊 Depth: {flood_params['depth_m']} m")
    print(f"🏢 Type: {property_chars['building_type']}")
    print(f"📐 Area: {property_chars['area_m2']} m²")
    print(f"💶 Max value: €{property_chars['max_damage_per_m2_eur']:.2f}/m²")
    print(f"💰 Total value: €{property_chars['total_value_eur']:,.2f}")
    print(f"📊 Damage ratio: {damage_assessment['damage_ratio']:.1%}")
    print(f"💸 Economic damage: €{damage_assessment['economic_damage_eur']:,.2f}")
    
    # Show confidence interval
    ci_95 = uncertainty['confidence_interval_95']
    print(f"📈 95% CI: €{ci_95['lower_eur']:,.0f} - €{ci_95['upper_eur']:,.0f}")

def compare_regions(calculator):
    """Compare damages between different regions for the same conditions."""
    
    # Standard conditions
    latitude, longitude = 50.0, 10.0  # Generic coordinates
    flood_depth = 1.5
    building_type = 'residential'
    area_m2 = 100
    
    regions = ['EUROPE', 'North AMERICA', 'ASIA', 'GLOBAL']
    
    print("Regional comparison for the same conditions:")
    print(f"  Depth: {flood_depth} m, Type: {building_type}, Area: {area_m2} m²")
    print()
    
    for region in regions:
        try:
            # Use a representative country for each region
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
    """Analyze the uncertainty of a result."""
    
    if 'uncertainty_analysis' not in result:
        print("No uncertainty data available.")
        return
    
    uncertainty = result['uncertainty_analysis']
    damage = result['damage_assessment']['economic_damage_eur']
    
    print("Detailed uncertainty analysis:")
    print(f"  Estimated damage: €{damage:,.2f}")
    print(f"  Standard deviation: {uncertainty['standard_deviation_ratio']:.1%}")
    print(f"  Damage std deviation: €{uncertainty['damage_standard_deviation_eur']:,.2f}")
    
    # Confidence intervals
    ci_68 = uncertainty['confidence_interval_68']
    ci_95 = uncertainty['confidence_interval_95']
    
    print(f"\n  Confidence intervals:")
    print(f"    68% (±1σ): €{ci_68['lower_eur']:,.0f} - €{ci_68['upper_eur']:,.0f}")
    print(f"    95% (±2σ): €{ci_95['lower_eur']:,.0f} - €{ci_95['upper_eur']:,.0f}")
    
    # Uncertainty range
    range_68 = ci_68['upper_eur'] - ci_68['lower_eur']
    range_95 = ci_95['upper_eur'] - ci_95['lower_eur']
    
    print(f"\n  Uncertainty ranges:")
    print(f"    68%: ±€{range_68/2:,.0f} ({range_68/damage:.1%} of estimated damage)")
    print(f"    95%: ±€{range_95/2:,.0f} ({range_95/damage:.1%} of estimated damage)")

if __name__ == "__main__":
    main()