# Librería de Cálculo de Daños por Inundación con Datos JRC

Una librería completa en Python para calcular daños económicos causados por inundaciones, basada en las funciones de daño globales del **Joint Research Centre (JRC)** de la Comisión Europea.

## 🌟 Características Principales

### ✅ Funciones de Daño Globales del JRC
- **270 funciones de daño** procesadas del JRC (2017)
- **7 regiones geográficas**: Europa, América del Norte, América Central y del Sur, Asia, África, Oceanía, Global
- **6 tipos de edificación**: Residencial, Comercial, Industrial, Transporte, Infraestructura, Agricultura
- **9 profundidades de inundación**: 0.0 a 6.0 metros

### ✅ Valores Máximos de Daño por País
- **248 países** con datos específicos
- Valores diferenciados por tipo de edificación
- Datos económicos en EUR (base 2010)
- Ajustes automáticos por contexto económico

### ✅ Análisis de Incertidumbre
- Desviaciones estándar del JRC
- Intervalos de confianza (68% y 95%)
- Análisis de sensibilidad

### ✅ Funcionalidades Avanzadas
- Inferencia automática de región por coordenadas
- Cálculos por lotes para múltiples ubicaciones
- Soporte para códigos ISO de países
- Validación completa de datos de entrada

## 📦 Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd flood_damage_library

# Instalar dependencias
pip install -r requirements.txt

# Procesar datos del JRC (requerido)
python process_jrc_excel.py
```

## 🚀 Uso Rápido

### Cálculo Básico

```python
from flood_damage_library import JRCFloodDamageCalculator

# Inicializar calculadora
calculator = JRCFloodDamageCalculator(data_directory="./processed_jrc_data")

# Calcular daño para una ubicación
result = calculator.calculate_jrc_damage(
    latitude=52.5200,      # Berlín
    longitude=13.4050,
    flood_depth=1.5,       # 1.5 metros
    country_code='DE',     # Alemania
    building_type='residential',
    area_m2=120           # 120 m²
)

print(f"Daño económico: €{result['damage_assessment']['economic_damage_eur']:,.2f}")
print(f"Ratio de daño: {result['damage_assessment']['damage_ratio']:.1%}")
```

### Análisis por Lotes

```python
# Múltiples ubicaciones
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
print(f"Daño total: €{total_damage:,.2f}")
```

## 📊 Estructura de Datos

### Resultado de Cálculo

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
    'jrc_data': {
        'region_used': 'EUROPE',
        'max_damage_structure': 522.69,
        'max_damage_content': 261.35,
        'data_source': 'JRC Global Flood Depth-Damage Functions Database'
    },
    'uncertainty_analysis': {
        'standard_deviation_ratio': 0.20,
        'damage_standard_deviation_eur': 9396.49,
        'confidence_interval_95': {
            'lower_eur': 28565.46,
            'upper_eur': 65399.42
        },
        'confidence_interval_68': {
            'lower_eur': 37585.95,
            'upper_eur': 56378.93
        }
    }
}
```

## 🌍 Regiones y Tipos Soportados

### Regiones JRC
- **EUROPE**: Europa
- **North AMERICA**: América del Norte
- **Centr&South_AMERICA**: América Central y del Sur
- **ASIA**: Asia
- **AFRICA**: África
- **OCEANIA**: Oceanía
- **GLOBAL**: Función global (promedio)

### Tipos de Edificación
- **residential**: Edificios residenciales
- **commercial**: Edificios comerciales
- **industrial**: Edificios industriales

### Países con Datos
248 países incluidos con valores específicos de daño máximo.

## 📈 Ejemplos Avanzados

### Comparación entre Regiones

```python
# Comparar daños para las mismas condiciones en diferentes regiones
regions = ['EUROPE', 'North AMERICA', 'ASIA', 'GLOBAL']
country_mapping = {'EUROPE': 'DE', 'North AMERICA': 'US', 'ASIA': 'JP', 'GLOBAL': 'US'}

for region in regions:
    result = calculator.calculate_jrc_damage(
        latitude=50.0, longitude=10.0,
        flood_depth=1.5,
        country_code=country_mapping[region],
        building_type='residential',
        area_m2=100,
        region=region
    )
    
    damage = result['damage_assessment']['economic_damage_eur']
    ratio = result['damage_assessment']['damage_ratio']
    print(f"{region:20}: €{damage:8,.0f} (ratio: {ratio:.1%})")
```

### Análisis de Sensibilidad por Profundidad

```python
import matplotlib.pyplot as plt

depths = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0]
damages = []

for depth in depths:
    result = calculator.calculate_jrc_damage(
        latitude=52.5200, longitude=13.4050,
        flood_depth=depth,
        country_code='DE',
        building_type='residential',
        area_m2=100
    )
    damages.append(result['damage_assessment']['economic_damage_eur'])

plt.figure(figsize=(10, 6))
plt.plot(depths, damages, 'b-o', linewidth=2, markersize=8)
plt.xlabel('Profundidad de Inundación (m)')
plt.ylabel('Daño Económico (EUR)')
plt.title('Función de Daño - Edificios Residenciales (Europa)')
plt.grid(True, alpha=0.3)
plt.show()
```

## 🔧 API Completa

### JRCFloodDamageCalculator

#### Métodos Principales

```python
# Cálculo individual
calculate_jrc_damage(latitude, longitude, flood_depth, 
                    country_code=None, building_type='residential', 
                    area_m2=None, region=None)

# Cálculo por lotes
calculate_damage_batch_jrc(locations)

# Información disponible
get_available_regions()
get_available_building_types()
get_countries_with_data(building_type='residential')
```

#### Parámetros

- **latitude** (float): Latitud (-90 a 90)
- **longitude** (float): Longitud (-180 a 180)
- **flood_depth** (float): Profundidad en metros (≥ 0)
- **country_code** (str, opcional): Código ISO del país
- **building_type** (str): 'residential', 'commercial', 'industrial'
- **area_m2** (float, opcional): Área en metros cuadrados
- **region** (str, opcional): Región JRC específica

## 📋 Validación de Datos

La librería incluye validación automática para:

- ✅ Coordenadas geográficas válidas
- ✅ Profundidades de inundación no negativas
- ✅ Tipos de edificación soportados
- ✅ Códigos de país válidos
- ✅ Áreas positivas

## 🧪 Tests

```bash
# Ejecutar todos los tests
python -m pytest tests/ -v

# Tests específicos de JRC
python -m pytest tests/test_jrc_calculator.py -v

# Tests con cobertura
python -m pytest tests/ --cov=flood_damage_library --cov-report=html
```

## 📚 Fuente de Datos

Los datos provienen de:

**"Global flood depth-damage functions database"**
- Joint Research Centre (JRC), European Commission
- Abril 2017
- Archivo: `copy_of_global_flood_depth-damage_functions__30102017.xlsx`

### Procesamiento de Datos

```bash
# Procesar archivo Excel del JRC
python process_jrc_excel.py

# Archivos generados:
# - processed_jrc_data/damage_functions_jrc.parquet
# - processed_jrc_data/max_damage_residential_jrc.parquet
# - processed_jrc_data/max_damage_commercial_jrc.parquet
# - processed_jrc_data/max_damage_industrial_jrc.parquet
# - processed_jrc_data/iso_table_jrc.parquet
```

## 🎯 Casos de Uso

### 1. Evaluación de Riesgo de Inundación
```python
# Evaluar múltiples escenarios de profundidad
scenarios = [0.5, 1.0, 1.5, 2.0, 3.0]
for depth in scenarios:
    result = calculator.calculate_jrc_damage(
        latitude=40.7128, longitude=-74.0060,  # Nueva York
        flood_depth=depth,
        country_code='US',
        building_type='commercial',
        area_m2=500
    )
    print(f"Profundidad {depth}m: €{result['damage_assessment']['economic_damage_eur']:,.0f}")
```

### 2. Análisis de Cartera de Propiedades
```python
# Portfolio de propiedades
portfolio = [
    {'lat': 52.52, 'lon': 13.40, 'country': 'DE', 'type': 'residential', 'area': 120},
    {'lat': 48.86, 'lon': 2.35, 'country': 'FR', 'type': 'commercial', 'area': 200},
    {'lat': 41.90, 'lon': 12.50, 'country': 'IT', 'type': 'industrial', 'area': 800}
]

total_risk = 0
for prop in portfolio:
    result = calculator.calculate_jrc_damage(
        latitude=prop['lat'], longitude=prop['lon'],
        flood_depth=2.0,  # Escenario de 2m
        country_code=prop['country'],
        building_type=prop['type'],
        area_m2=prop['area']
    )
    total_risk += result['damage_assessment']['economic_damage_eur']

print(f"Riesgo total del portfolio: €{total_risk:,.2f}")
```

### 3. Comparación Regional
```python
# Comparar el mismo activo en diferentes regiones
asset = {'flood_depth': 1.5, 'building_type': 'residential', 'area_m2': 100}

locations = [
    {'name': 'Berlín', 'lat': 52.52, 'lon': 13.40, 'country': 'DE'},
    {'name': 'Nueva York', 'lat': 40.71, 'lon': -74.01, 'country': 'US'},
    {'name': 'Tokio', 'lat': 35.68, 'lon': 139.65, 'country': 'JP'},
    {'name': 'São Paulo', 'lat': -23.55, 'lon': -46.63, 'country': 'BR'}
]

for loc in locations:
    result = calculator.calculate_jrc_damage(
        latitude=loc['lat'], longitude=loc['lon'],
        country_code=loc['country'],
        **asset
    )
    damage = result['damage_assessment']['economic_damage_eur']
    region = result['location']['region']
    print(f"{loc['name']:12} ({region:20}): €{damage:8,.0f}")
```

## 🔍 Análisis de Incertidumbre

```python
# Análisis detallado de incertidumbre
result = calculator.calculate_jrc_damage(
    latitude=52.5200, longitude=13.4050,
    flood_depth=1.5, country_code='DE',
    building_type='residential', area_m2=100
)

uncertainty = result['uncertainty_analysis']
damage = result['damage_assessment']['economic_damage_eur']

print(f"Daño estimado: €{damage:,.2f}")
print(f"Desviación estándar: {uncertainty['standard_deviation_ratio']:.1%}")

ci_95 = uncertainty['confidence_interval_95']
print(f"IC 95%: €{ci_95['lower_eur']:,.0f} - €{ci_95['upper_eur']:,.0f}")

# Rango de incertidumbre
range_95 = ci_95['upper_eur'] - ci_95['lower_eur']
print(f"Rango de incertidumbre: ±€{range_95/2:,.0f} ({range_95/damage:.1%})")
```

## 🚨 Limitaciones y Consideraciones

### Limitaciones de los Datos
- Los datos del JRC son de 2017 y pueden no reflejar condiciones actuales
- Los valores están en EUR 2010 y pueden requerir ajustes por inflación
- Algunas regiones tienen datos limitados (especialmente África y Oceanía)

### Consideraciones de Uso
- Los resultados son estimaciones basadas en funciones promedio
- Se recomienda validar con datos locales cuando sea posible
- La incertidumbre puede ser significativa (±20-40% típicamente)

### Recomendaciones
- Usar múltiples escenarios para análisis de sensibilidad
- Considerar factores locales no capturados en las funciones globales
- Actualizar valores económicos según inflación local

## 📞 Soporte y Contribuciones

Para reportar problemas o contribuir:
1. Crear un issue en el repositorio
2. Proporcionar datos de ejemplo y descripción detallada
3. Incluir información sobre el entorno (Python, OS, etc.)

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo `LICENSE` para detalles.

## 🙏 Agradecimientos

- **Joint Research Centre (JRC)** de la Comisión Europea por proporcionar la base de datos global
- Comunidad científica de evaluación de riesgos de inundación
- Contribuidores del proyecto

---

**Versión**: 2.0.0  
**Última actualización**: Noviembre 2024  
**Compatibilidad**: Python 3.8+