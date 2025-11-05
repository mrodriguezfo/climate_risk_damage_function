# Coordinates Are Optional! 🌍

## Summary

**Good news!** Latitude and longitude coordinates are **NOT required** for flood damage calculations. They are only used for automatic country inference when you don't provide a country code.

## How It Works

### What coordinates are used for:
1. **Country inference**: If you don't provide `country_code`, the library uses basic geographic rules to guess the country
2. **Validation**: Ensures coordinates are in valid ranges if provided
3. **Result metadata**: Includes coordinates in the output for reference

### What coordinates are NOT used for:
- **Damage calculation**: The actual mathematical calculation doesn't use coordinates
- **Region determination**: Regions are determined from country codes, not coordinates
- **Maximum damage values**: These come from country-specific data, not geographic location

## Usage Options

### Option 1: With Coordinates (Traditional)
```python
from flood_damage_library import JRCFloodDamageCalculator

calculator = JRCFloodDamageCalculator()

# Coordinates will be used to infer country (DE = Germany)
result = calculator.calculate_jrc_damage(
    latitude=52.5200,      # Berlin coordinates
    longitude=13.4050,
    flood_depth=1.5,
    building_type='residential',
    area_m2=120
)
```

### Option 2: With Country Code Only (No Coordinates)
```python
# Skip coordinates entirely - much simpler!
result = calculator.calculate_jrc_damage(
    flood_depth=1.5,
    country_code='DE',     # Directly specify Germany
    building_type='residential',
    area_m2=120
)
```

### Option 3: Using the Simplified Method
```python
# Even cleaner API for country-based calculations
result = calculator.calculate_damage_by_country(
    flood_depth=1.5,
    country_code='DE',
    building_type='residential',
    area_m2=120
)
```

## Required vs Optional Parameters

### Always Required:
- `flood_depth` - The depth of flooding in meters
- Either `country_code` OR coordinates (`latitude` + `longitude`)

### Optional:
- `building_type` - Defaults to 'residential'
- `area_m2` - Defaults to 100 square meters
- `region` - Automatically inferred from country if not provided
- `latitude` + `longitude` - Only needed if country_code not provided

## Examples by Use Case

### 1. You Know the Country
```python
# Best approach - direct and simple
result = calculator.calculate_damage_by_country(
    flood_depth=2.0,
    country_code='US',
    building_type='commercial',
    area_m2=500
)
```

### 2. You Have GPS Coordinates but No Country
```python
# Let the library infer the country
result = calculator.calculate_jrc_damage(
    latitude=40.7128,      # New York
    longitude=-74.0060,
    flood_depth=2.0,
    building_type='commercial',
    area_m2=500
)
```

### 3. You Want to Specify Everything
```python
# Full control - provide both coordinates and country
result = calculator.calculate_jrc_damage(
    latitude=40.7128,
    longitude=-74.0060,
    flood_depth=2.0,
    country_code='US',     # Override automatic inference
    building_type='commercial',
    area_m2=500,
    region='North AMERICA'  # Override automatic region
)
```

### 4. Batch Processing Without Coordinates
```python
# Process multiple locations by country
locations = [
    {
        'flood_depth': 1.5,
        'country_code': 'DE',
        'building_type': 'residential',
        'area_m2': 120
    },
    {
        'flood_depth': 2.0,
        'country_code': 'FR',
        'building_type': 'commercial',
        'area_m2': 200
    }
]

results = []
for location in locations:
    result = calculator.calculate_damage_by_country(**location)
    results.append(result)
```

## Performance Benefits

### Without Coordinates:
- ✅ Faster execution (no coordinate validation)
- ✅ Simpler code
- ✅ No need to look up coordinates
- ✅ Direct country specification

### With Coordinates:
- ✅ Automatic country inference
- ✅ Geographic context in results
- ✅ Useful for mapping applications

## Supported Countries

The library supports **248 countries** with specific damage data. Some examples:

| Country Code | Country Name | Region |
|--------------|--------------|---------|
| US | United States | North AMERICA |
| DE | Germany | EUROPE |
| FR | France | EUROPE |
| BR | Brazil | Centr&South_AMERICA |
| JP | Japan | ASIA |
| AU | Australia | OCEANIA |
| ZA | South Africa | AFRICA |

## Error Handling

### Valid Usage:
```python
# ✅ Country code provided
result = calculator.calculate_damage_by_country(
    flood_depth=1.5,
    country_code='DE'
)

# ✅ Coordinates provided
result = calculator.calculate_jrc_damage(
    latitude=52.52,
    longitude=13.40,
    flood_depth=1.5
)
```

### Invalid Usage:
```python
# ❌ Neither country nor coordinates
result = calculator.calculate_jrc_damage(
    flood_depth=1.5
)
# Raises: DataValidationError

# ❌ Only one coordinate
result = calculator.calculate_jrc_damage(
    latitude=52.52,
    flood_depth=1.5
)
# Raises: DataValidationError
```

## Migration Guide

### If you currently use coordinates:
```python
# OLD WAY (still works)
result = calculator.calculate_jrc_damage(
    latitude=52.5200,
    longitude=13.4050,
    flood_depth=1.5,
    building_type='residential',
    area_m2=120
)

# NEW WAY (simpler)
result = calculator.calculate_damage_by_country(
    flood_depth=1.5,
    country_code='DE',  # Germany
    building_type='residential',
    area_m2=120
)
```

## Conclusion

**Coordinates are optional!** If you know the country code, you can skip coordinates entirely and get the same accurate results with simpler code.

Choose the approach that best fits your use case:
- **Have country codes?** → Use `calculate_damage_by_country()`
- **Have coordinates but no country?** → Use `calculate_jrc_damage()` with coordinates
- **Want maximum control?** → Provide both coordinates and country code

---

**Happy flood risk analysis!** 🌊📊