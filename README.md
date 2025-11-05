# Flood Damage Calculation Library with JRC Data

A comprehensive Python library for calculating economic damages caused by floods, based on global damage functions from the **Joint Research Centre (JRC)** of the European Commission.

## 🌟 Key Features

### ✅ JRC Global Damage Functions
- **270 damage functions** processed from JRC (2017)
- **7 geographic regions**: Europe, North America, Central & South America, Asia, Africa, Oceania, Global
- **6 building types**: Residential, Commercial, Industrial, Transport, Infrastructure, Agriculture
- **9 flood depths**: 0.0 to 6.0 meters

### ✅ Maximum Damage Values by Country
- **248 countries** with specific data
- Values differentiated by building type
- Economic data in EUR (2010 base)
- Automatic adjustments by economic context

### ✅ Uncertainty Analysis
- JRC standard deviations
- Confidence intervals (68% and 95%)
- Sensitivity analysis

### ✅ Advanced Features
- Automatic region inference from coordinates
- Batch calculations for multiple locations
- ISO country code support
- Complete input data validation

## 📦 Installation

```bash
# Clone the repository
git clone <repository-url>
cd flood_damage_library

# Install dependencies
pip install -r requirements.txt

# Process JRC data (required)
python process_jrc_excel.py
```

## 🚀 Quick Start

### Basic Calculation

```python
from flood_damage_library import JRCFloodDamageCalculator

# Initialize calculator
calculator = JRCFloodDamageCalculator(data_directory="./processed_jrc_data")

# Option 1: Simple calculation with country code (coordinates optional!)
result = calculator.calculate_damage_by_country(
    flood_depth=1.5,       # 1.5 meters
    country_code='DE',     # Germany
    building_type='residential',
    area_m2=120           # 120 m²
)

# Option 2: With coordinates (for automatic country inference)
result = calculator.calculate_jrc_damage(
    latitude=52.5200,      # Berlin coordinates
    longitude=13.4050,
    flood_depth=1.5,
    building_type='residential',
    area_m2=120
)

print(f"Economic damage: €{result['damage_assessment']['economic_damage_eur']:,.2f}")
print(f"Damage ratio: {result['damage_assessment']['damage_ratio']:.1%}")
```

### Batch Analysis

```python
# Multiple locations
locations = [
    {
        'latitude': 52.5200, 'longitude': 13.4050, 'flood_depth': 1.5,
        'country_code': 'DE', 'building_type': 'residential', 'area_m2': 100
    },
    {
        'latitude': 48.8566, 'longitude': 2.3522, 'flood_depth': 2.0,
        'country_code': 'FR', 'building_type': 'commercial', 'area_m2': 150
    }
]

results = calculator.calculate_damage_batch_jrc(locations)

total_damage = sum(r['damage_assessment']['economic_damage_eur'] 
                  for r in results if 'error' not in r)
print(f"Total damage: €{total_damage:,.2f}")
```

### Batch Analysis by Country (No Coordinates Required)

```python
# Portfolio analysis using only country codes
scenarios = [
    {
        'flood_depth': 1.5, 'country_code': 'DE', 
        'building_type': 'residential', 'area_m2': 120
    },
    {
        'flood_depth': 2.0, 'country_code': 'FR', 
        'building_type': 'commercial', 'area_m2': 500
    },
    {
        'flood_depth': 1.8, 'country_code': 'IT', 
        'building_type': 'industrial', 'area_m2': 1000
    }
]

# Process batch by country (no coordinates needed)
results = calculator.calculate_damage_batch_by_country(scenarios)

for result in results:
    if 'error' not in result:
        scenario = result['input_scenario']
        damage = result['damage_assessment']['economic_damage_eur']
        print(f"{scenario['country_code']} {scenario['building_type']}: €{damage:,.0f}")
```

## 📊 Data Structure

### Calculation Result

```python
{
    'location': {
        'latitude': 52.5200,
        'longitude': 13.4050,
        'country_code': 'DE',
        'country_name': 'GERMANY',
        'region': 'EUROPE'
    },
    'flood_parameters': {
        'depth_m': 1.5
    },
    'property_characteristics': {
        'building_type': 'residential',
        'area_m2': 120,
        'max_damage_per_m2_eur': 783.04,
        'total_value_eur': 93964.87,
        'currency': 'EUR',
        'base_year': 2010
    },
    'damage_assessment': {
        'damage_ratio': 0.50,
        'economic_damage_eur': 46982.44,
        'currency': 'EUR'
    },
    'uncertainty_analysis': {
        'standard_deviation_ratio': 0.20,
        'confidence_interval_95': {
            'lower_eur': 28565.46,
            'upper_eur': 65399.42
        }
    }
}
```

## 🌍 Supported Regions and Types

### JRC Regions
- **EUROPE**: Europe
- **North AMERICA**: North America
- **Centr&South_AMERICA**: Central and South America
- **ASIA**: Asia
- **AFRICA**: Africa
- **OCEANIA**: Oceania
- **GLOBAL**: Global function (average)

### Building Types
- **residential**: Residential buildings
- **commercial**: Commercial buildings
- **industrial**: Industrial buildings

### Countries with Data
248 countries included with specific maximum damage values.

## 🔧 Complete API

### JRCFloodDamageCalculator

#### Main Methods

```python
# Individual calculation (flexible - with or without coordinates)
calculate_jrc_damage(latitude=None, longitude=None, flood_depth=None, 
                    country_code=None, building_type='residential', 
                    area_m2=None, region=None)

# Simplified country-based calculation (no coordinates needed)
calculate_damage_by_country(flood_depth, country_code, 
                           building_type='residential', area_m2=None, region=None)

# Batch calculation (with coordinates)
calculate_damage_batch_jrc(locations)

# Batch calculation by country (no coordinates needed)
calculate_damage_batch_by_country(scenarios)

# Available information
get_available_regions()
get_available_building_types()
get_countries_with_data(building_type='residential')
```

#### Parameters

- **flood_depth** (float): Depth in meters (≥ 0) - **Required**
- **country_code** (str): ISO country code (e.g., 'US', 'DE', 'BR') - **Required if no coordinates**
- **latitude** (float, optional): Latitude (-90 to 90) - Only needed if country_code not provided
- **longitude** (float, optional): Longitude (-180 to 180) - Only needed if country_code not provided
- **building_type** (str): 'residential', 'commercial', 'industrial', 'agriculture', 'infrastructure', 'transport' - Default: 'residential'
- **area_m2** (float, optional): Area in square meters - Default: 100
- **region** (str, optional): Specific JRC region - Auto-inferred from country if not provided

**Note**: Either provide `country_code` OR both `latitude` and `longitude`. Coordinates are only used for automatic country inference.

## 📋 Data Validation

The library includes automatic validation for:

- ✅ Valid geographic coordinates
- ✅ Non-negative flood depths
- ✅ Supported building types
- ✅ Valid country codes
- ✅ Positive areas

## 🧪 Tests

```bash
# Run all tests
python -m pytest tests/ -v

# JRC-specific tests
python -m pytest tests/test_jrc_calculator.py -v

# Tests with coverage
python -m pytest tests/ --cov=flood_damage_library --cov-report=html
```

## 📚 Data Source

Data comes from:

**"Global flood depth-damage functions database"**
- Joint Research Centre (JRC), European Commission
- April 2017
- File: `copy_of_global_flood_depth-damage_functions__30102017.xlsx`

### Data Processing

```bash
# Process JRC Excel file
python process_jrc_excel.py

# Generated files:
# - processed_jrc_data/damage_functions_jrc.parquet
# - processed_jrc_data/max_damage_residential_jrc.parquet
# - processed_jrc_data/max_damage_commercial_jrc.parquet
# - processed_jrc_data/max_damage_industrial_jrc.parquet
# - processed_jrc_data/iso_table_jrc.parquet
```

## 🎯 Use Cases

### 1. Flood Risk Assessment
```python
# Evaluate multiple depth scenarios
scenarios = [0.5, 1.0, 1.5, 2.0, 3.0]
for depth in scenarios:
    result = calculator.calculate_jrc_damage(
        latitude=40.7128, longitude=-74.0060,  # New York
        flood_depth=depth,
        country_code='US',
        building_type='commercial',
        area_m2=500
    )
    print(f"Depth {depth}m: €{result['damage_assessment']['economic_damage_eur']:,.0f}")
```

### 2. Property Portfolio Analysis
```python
# Property portfolio
portfolio = [
    {'lat': 52.52, 'lon': 13.40, 'country': 'DE', 'type': 'residential', 'area': 120},
    {'lat': 48.86, 'lon': 2.35, 'country': 'FR', 'type': 'commercial', 'area': 200},
    {'lat': 41.90, 'lon': 12.50, 'country': 'IT', 'type': 'industrial', 'area': 800}
]

total_risk = 0
for prop in portfolio:
    result = calculator.calculate_jrc_damage(
        latitude=prop['lat'], longitude=prop['lon'],
        flood_depth=2.0,  # 2m scenario
        country_code=prop['country'],
        building_type=prop['type'],
        area_m2=prop['area']
    )
    total_risk += result['damage_assessment']['economic_damage_eur']

print(f"Total portfolio risk: €{total_risk:,.2f}")
```

## 🔍 Uncertainty Analysis

```python
# Detailed uncertainty analysis
result = calculator.calculate_jrc_damage(
    latitude=52.5200, longitude=13.4050,
    flood_depth=1.5, country_code='DE',
    building_type='residential', area_m2=100
)

uncertainty = result['uncertainty_analysis']
damage = result['damage_assessment']['economic_damage_eur']

print(f"Estimated damage: €{damage:,.2f}")
print(f"Standard deviation: {uncertainty['standard_deviation_ratio']:.1%}")

ci_95 = uncertainty['confidence_interval_95']
print(f"95% CI: €{ci_95['lower_eur']:,.0f} - €{ci_95['upper_eur']:,.0f}")
```

## 🚨 Limitations and Considerations

### Data Limitations
- JRC data is from 2017 and may not reflect current conditions
- Values are in EUR 2010 and may require inflation adjustments
- Some regions have limited data (especially Africa and Oceania)

### Usage Considerations
- Results are estimates based on average functions
- Validation with local data is recommended when possible
- Uncertainty can be significant (±20-40% typically)

### Recommendations
- Use multiple scenarios for sensitivity analysis
- Consider local factors not captured in global functions
- Update economic values according to local inflation

## 📁 Repository Structure

```
climate_risk_damage_function/
├── flood_damage_library/           # Main library package
│   ├── __init__.py
│   ├── core/                       # Core calculation modules
│   │   ├── __init__.py
│   │   ├── jrc_damage_calculator.py    # Main JRC calculator
│   │   ├── damage_calculator.py        # Base calculator
│   │   ├── data_manager.py             # Data management
│   │   └── enhanced_damage_calculator.py
│   └── utils/                      # Utility modules
│       ├── __init__.py
│       ├── exceptions.py           # Custom exceptions
│       └── validators.py           # Input validation
├── processed_jrc_data/             # JRC data (8 parquet files)
│   ├── damage_functions_jrc.parquet     # 270 damage functions
│   ├── iso_table_jrc.parquet           # Country codes
│   ├── max_damage_residential_jrc.parquet
│   ├── max_damage_commercial_jrc.parquet
│   ├── max_damage_industrial_jrc.parquet
│   ├── max_damage_agriculture_jrc.parquet
│   ├── max_damage_infrastructure_jrc.parquet
│   └── max_damage_transport_jrc.parquet
├── flood_damage_tutorial.ipynb    # Interactive tutorial
├── requirements.txt               # Dependencies
├── setup.py                      # Package installation
└── README.md                     # Documentation
```

## 📄 License

This project is under MIT license. See `LICENSE` file for details.

## 🙏 Acknowledgments

- **Joint Research Centre (JRC)** of the European Commission for providing the global database
- Flood risk assessment scientific community
- Project contributors

---

**Version**: 2.0.0  
**Last updated**: November 2024  
**Compatibility**: Python 3.8+