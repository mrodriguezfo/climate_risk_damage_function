"""
Calculadora de daños por inundación basada en los datos del JRC (Joint Research Centre).
Utiliza las funciones de daño globales y valores máximos por país del JRC.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Tuple
from pathlib import Path
import logging
from scipy import interpolate
from ..utils.validators import validate_coordinates, validate_flood_depth
from ..utils.exceptions import DataValidationError, CalculationError
from .data_manager import DataManager

class JRCFloodDamageCalculator:
    """
    Calculadora de daños por inundación basada en datos del JRC.
    
    Características:
    - Funciones de daño por región (Europa, América del Norte, Asia, etc.)
    - Valores máximos de daño por país y tipo de edificación
    - Soporte para múltiples tipos de edificación (residencial, comercial, industrial)
    - Análisis de incertidumbre con desviaciones estándar
    """
    
    def __init__(self, data_directory: str = "./processed_jrc_data"):
        """
        Inicializa la calculadora JRC.
        
        Args:
            data_directory: Directorio con datos procesados del JRC
        """
        self.data_directory = Path(data_directory)
        self.logger = logging.getLogger(__name__)
        
        # Cargar datos del JRC
        self._load_jrc_data()
        
        # Mapeo de regiones a países (simplificado)
        self.region_mapping = {
            'EUROPE': ['DE', 'FR', 'IT', 'ES', 'NL', 'BE', 'AT', 'CH', 'SE', 'NO', 'DK', 'FI', 'PL', 'CZ', 'HU', 'RO', 'BG', 'GR', 'PT', 'IE', 'LU', 'SK', 'SI', 'EE', 'LV', 'LT', 'CY', 'MT', 'HR', 'GB', 'IS', 'LI', 'MC', 'SM', 'VA', 'AD', 'AL', 'BA', 'ME', 'MK', 'RS', 'XK', 'MD', 'UA', 'BY', 'RU'],
            'North AMERICA': ['US', 'CA', 'MX', 'GT', 'BZ', 'SV', 'HN', 'NI', 'CR', 'PA'],
            'Centr&South_AMERICA': ['BR', 'AR', 'CL', 'PE', 'CO', 'VE', 'EC', 'BO', 'PY', 'UY', 'GY', 'SR', 'GF'],
            'ASIA': ['CN', 'IN', 'JP', 'KR', 'TH', 'VN', 'MY', 'SG', 'ID', 'PH', 'BD', 'PK', 'LK', 'MM', 'KH', 'LA', 'BN', 'TL', 'MN', 'KZ', 'UZ', 'TM', 'TJ', 'KG', 'AF', 'IR', 'IQ', 'SY', 'JO', 'LB', 'IL', 'PS', 'SA', 'YE', 'OM', 'AE', 'QA', 'BH', 'KW', 'TR', 'GE', 'AM', 'AZ'],
            'AFRICA': ['NG', 'ET', 'EG', 'ZA', 'KE', 'UG', 'DZ', 'SD', 'MA', 'AO', 'GH', 'MZ', 'MG', 'CM', 'CI', 'NE', 'BF', 'ML', 'MW', 'ZM', 'SO', 'SN', 'TD', 'ZW', 'GN', 'RW', 'BJ', 'TN', 'BI', 'ER', 'SL', 'TG', 'CF', 'LY', 'LR', 'MR', 'GA', 'BW', 'LS', 'GQ', 'GM', 'GW', 'SZ', 'DJ', 'KM', 'CV', 'ST', 'SC', 'MU'],
            'OCEANIA': ['AU', 'NZ', 'PG', 'FJ', 'SB', 'NC', 'PF', 'VU', 'WS', 'KI', 'FM', 'TO', 'MH', 'PW', 'CK', 'NU', 'TK', 'TV', 'NR', 'AS', 'GU', 'MP', 'VI', 'PR', 'UM']
        }
    
    def _load_jrc_data(self):
        """Carga los datos procesados del JRC."""
        try:
            # Cargar funciones de daño
            damage_func_file = self.data_directory / 'damage_functions_jrc.parquet'
            if damage_func_file.exists():
                self.damage_functions = pd.read_parquet(damage_func_file)
                print(f"✅ Funciones de daño JRC cargadas: {len(self.damage_functions)} registros")
            else:
                raise FileNotFoundError(f"Archivo no encontrado: {damage_func_file}")
            
            # Cargar valores máximos de daño
            self.max_damage_data = {}
            
            for building_type in ['residential', 'commercial', 'industrial']:
                file_path = self.data_directory / f'max_damage_{building_type}_jrc.parquet'
                if file_path.exists():
                    self.max_damage_data[building_type] = pd.read_parquet(file_path)
                    print(f"✅ Valores máximos {building_type} cargados: {len(self.max_damage_data[building_type])} países")
            
            # Cargar tabla ISO
            iso_file = self.data_directory / 'iso_table_jrc.parquet'
            if iso_file.exists():
                self.iso_table = pd.read_parquet(iso_file)
                print(f"✅ Tabla ISO cargada: {len(self.iso_table)} países")
            else:
                self.iso_table = pd.DataFrame()
            
        except Exception as e:
            self.logger.error(f"Error cargando datos JRC: {e}")
            raise CalculationError(f"No se pudieron cargar los datos del JRC: {e}")
    
    def calculate_jrc_damage(self,
                           latitude: float,
                           longitude: float,
                           flood_depth: float,
                           country_code: Optional[str] = None,
                           building_type: str = 'residential',
                           area_m2: Optional[float] = None,
                           region: Optional[str] = None,
                           **kwargs) -> Dict:
        """
        Calcula daños usando las funciones del JRC.
        
        Args:
            latitude: Latitud de la ubicación
            longitude: Longitud de la ubicación
            flood_depth: Profundidad de inundación en metros
            country_code: Código ISO del país (ej: 'US', 'DE', 'BR')
            building_type: Tipo de edificación ('residential', 'commercial', 'industrial')
            area_m2: Área afectada en metros cuadrados
            region: Región específica a usar (opcional)
            
        Returns:
            Diccionario con resultados detallados
        """
        # Validar entrada
        validate_coordinates(latitude, longitude)
        validate_flood_depth(flood_depth)
        
        if building_type not in ['residential', 'commercial', 'industrial']:
            raise DataValidationError(f"Tipo de edificación no soportado: {building_type}")
        
        # Inferir país y región si no se proporcionan
        if not country_code:
            country_code = self._infer_country_from_coordinates(latitude, longitude)
        
        if not region:
            region = self._get_region_for_country(country_code)
        
        # Obtener función de daño
        damage_ratio = self._get_jrc_damage_ratio(flood_depth, building_type, region)
        
        # Obtener valores máximos de daño para el país
        max_damage_data = self._get_max_damage_for_country(country_code, building_type)
        
        # Calcular área (usar valor por defecto si no se proporciona)
        if not area_m2:
            area_m2 = 100  # 100 m² por defecto
        
        # Calcular daño económico
        max_damage_per_m2 = max_damage_data.get('total_building_eur_m2', 500)  # EUR/m² por defecto
        total_value = area_m2 * max_damage_per_m2
        economic_damage = total_value * damage_ratio
        
        # Obtener información del país
        country_info = self._get_country_info(country_code)
        
        # Análisis de incertidumbre
        uncertainty_analysis = self._calculate_jrc_uncertainty(
            economic_damage, damage_ratio, building_type, region
        )
        
        # Construir resultado
        result = {
            'location': {
                'latitude': latitude,
                'longitude': longitude,
                'country_code': country_code,
                'country_name': country_info.get('country_name', 'Unknown'),
                'region': region
            },
            'flood_parameters': {
                'depth_m': flood_depth
            },
            'property_characteristics': {
                'building_type': building_type,
                'area_m2': area_m2,
                'max_damage_per_m2_eur': max_damage_per_m2,
                'total_value_eur': total_value,
                'currency': 'EUR',
                'base_year': 2010
            },
            'damage_assessment': {
                'damage_ratio': damage_ratio,
                'economic_damage_eur': economic_damage,
                'currency': 'EUR'
            },
            'jrc_data': {
                'region_used': region,
                'max_damage_structure': max_damage_data.get('max_damage_structure_eur_m2'),
                'max_damage_content': max_damage_data.get('max_damage_content_eur_m2'),
                'data_source': 'JRC Global Flood Depth-Damage Functions Database'
            },
            'uncertainty_analysis': uncertainty_analysis,
            'metadata': {
                'calculation_method': 'jrc_depth_damage_function',
                'data_version': 'JRC 2017',
                'includes_uncertainty': True
            }
        }
        
        return result
    
    def _get_jrc_damage_ratio(self, depth: float, building_type: str, region: str) -> float:
        """Obtiene el ratio de daño usando las funciones del JRC."""
        
        # Mapear tipo de edificación a clase de daño JRC
        building_type_mapping = {
            'residential': 'Residential buildings',
            'commercial': 'Commercial buildings',
            'industrial': 'Industrial buildings'
        }
        
        damage_class = building_type_mapping.get(building_type, 'Residential buildings')
        
        # Filtrar funciones de daño
        mask = (
            (self.damage_functions['damage_class'] == damage_class) &
            (self.damage_functions['region'] == region)
        )
        
        relevant_functions = self.damage_functions[mask]
        
        if relevant_functions.empty:
            # Intentar con región GLOBAL
            mask_global = (
                (self.damage_functions['damage_class'] == damage_class) &
                (self.damage_functions['region'] == 'GLOBAL')
            )
            relevant_functions = self.damage_functions[mask_global]
        
        if relevant_functions.empty:
            # Usar función genérica
            return min(1.0, depth * 0.3)  # 30% de daño por metro
        
        # Obtener datos para interpolación
        depths = relevant_functions['depth_m'].values
        ratios = relevant_functions['damage_ratio'].values
        
        if len(depths) == 1:
            return ratios[0]
        
        # Ordenar por profundidad
        sorted_indices = np.argsort(depths)
        depths_sorted = depths[sorted_indices]
        ratios_sorted = ratios[sorted_indices]
        
        # Interpolación lineal
        if depth <= depths_sorted[0]:
            return ratios_sorted[0]
        elif depth >= depths_sorted[-1]:
            return ratios_sorted[-1]
        else:
            return np.interp(depth, depths_sorted, ratios_sorted)
    
    def _get_max_damage_for_country(self, country_code: str, building_type: str) -> Dict:
        """Obtiene los valores máximos de daño para un país y tipo de edificación."""
        
        if building_type not in self.max_damage_data:
            return {'total_building_eur_m2': 500}  # Valor por defecto
        
        # Buscar por código de país
        country_data = self.max_damage_data[building_type][
            self.max_damage_data[building_type]['country'].str.upper() == country_code.upper()
        ]
        
        if country_data.empty:
            # Buscar por nombre de país en tabla ISO
            country_name = self._get_country_name_from_code(country_code)
            if country_name:
                country_data = self.max_damage_data[building_type][
                    self.max_damage_data[building_type]['country'].str.upper() == country_name.upper()
                ]
        
        if not country_data.empty:
            return country_data.iloc[0].to_dict()
        else:
            # Valores por defecto basados en el tipo de edificación
            defaults = {
                'residential': {'total_building_eur_m2': 400},
                'commercial': {'total_building_eur_m2': 600},
                'industrial': {'total_building_eur_m2': 500}
            }
            return defaults.get(building_type, {'total_building_eur_m2': 500})
    
    def _get_region_for_country(self, country_code: str) -> str:
        """Determina la región JRC para un código de país."""
        
        for region, countries in self.region_mapping.items():
            if country_code.upper() in [c.upper() for c in countries]:
                return region
        
        # Si no se encuentra, usar región global
        return 'GLOBAL'
    
    def _infer_country_from_coordinates(self, latitude: float, longitude: float) -> str:
        """Infiere el país basándose en coordenadas geográficas (simplificado)."""
        
        # Reglas geográficas básicas
        if 25 <= latitude <= 49 and -125 <= longitude <= -66:
            return 'US'
        elif 14 <= latitude <= 33 and -118 <= longitude <= -86:
            return 'MX'
        elif 42 <= latitude <= 70 and -141 <= longitude <= -52:
            return 'CA'
        elif -34 <= latitude <= 5 and -74 <= longitude <= -35:
            return 'BR'
        elif 36 <= latitude <= 71 and -10 <= longitude <= 40:
            return 'DE'  # Europa central como ejemplo
        elif 20 <= latitude <= 50 and 70 <= longitude <= 140:
            return 'CN'  # Asia
        elif -35 <= latitude <= 37 and 110 <= longitude <= 155:
            return 'AU'  # Oceanía
        else:
            return 'US'  # Por defecto
    
    def _get_country_info(self, country_code: str) -> Dict:
        """Obtiene información del país desde la tabla ISO."""
        
        if self.iso_table.empty:
            return {'country_name': 'Unknown'}
        
        # Buscar por código ISO
        country_info = self.iso_table[
            (self.iso_table['iso_alpha2'].str.upper() == country_code.upper()) |
            (self.iso_table['iso_alpha3'].str.upper() == country_code.upper())
        ]
        
        if not country_info.empty:
            return country_info.iloc[0].to_dict()
        else:
            return {'country_name': 'Unknown'}
    
    def _get_country_name_from_code(self, country_code: str) -> Optional[str]:
        """Obtiene el nombre del país desde el código ISO."""
        
        country_info = self._get_country_info(country_code)
        return country_info.get('country_name')
    
    def _calculate_jrc_uncertainty(self, economic_damage: float, damage_ratio: float, 
                                 building_type: str, region: str) -> Dict:
        """Calcula análisis de incertidumbre usando datos del JRC."""
        
        # Buscar desviación estándar en los datos JRC
        building_type_mapping = {
            'residential': 'Residential buildings',
            'commercial': 'Commercial buildings', 
            'industrial': 'Industrial buildings'
        }
        
        damage_class = building_type_mapping.get(building_type, 'Residential buildings')
        
        # Filtrar datos de incertidumbre
        uncertainty_data = self.damage_functions[
            (self.damage_functions['damage_class'] == damage_class) &
            (self.damage_functions['region'] == region) &
            (self.damage_functions['standard_deviation'].notna())
        ]
        
        if uncertainty_data.empty:
            # Usar valores por defecto
            std_dev = 0.2  # 20% de incertidumbre
        else:
            # Usar promedio de desviaciones estándar disponibles
            std_dev = uncertainty_data['standard_deviation'].mean()
        
        # Calcular intervalos de confianza
        damage_std = economic_damage * std_dev
        
        return {
            'standard_deviation_ratio': std_dev,
            'damage_standard_deviation_eur': damage_std,
            'confidence_interval_95': {
                'lower_eur': max(0, economic_damage - 1.96 * damage_std),
                'upper_eur': economic_damage + 1.96 * damage_std
            },
            'confidence_interval_68': {
                'lower_eur': max(0, economic_damage - damage_std),
                'upper_eur': economic_damage + damage_std
            },
            'data_source': 'JRC standard deviations'
        }
    
    def calculate_damage_batch_jrc(self, locations: List[Dict]) -> List[Dict]:
        """
        Calcula daños para múltiples ubicaciones usando datos JRC.
        
        Args:
            locations: Lista de diccionarios con datos de ubicación
            
        Returns:
            Lista de resultados
        """
        results = []
        
        for i, location in enumerate(locations):
            try:
                result = self.calculate_jrc_damage(
                    latitude=location['latitude'],
                    longitude=location['longitude'],
                    flood_depth=location['flood_depth'],
                    country_code=location.get('country_code'),
                    building_type=location.get('building_type', 'residential'),
                    area_m2=location.get('area_m2'),
                    region=location.get('region'),
                    **{k: v for k, v in location.items() 
                       if k not in ['latitude', 'longitude', 'flood_depth', 'country_code', 'building_type', 'area_m2', 'region']}
                )
                result['batch_index'] = i
                results.append(result)
                
            except Exception as e:
                error_result = {
                    'batch_index': i,
                    'error': str(e),
                    'location': {
                        'latitude': location.get('latitude'),
                        'longitude': location.get('longitude')
                    }
                }
                results.append(error_result)
        
        return results
    
    def get_available_regions(self) -> List[str]:
        """Obtiene las regiones disponibles en los datos JRC."""
        return self.damage_functions['region'].unique().tolist()
    
    def get_available_building_types(self) -> List[str]:
        """Obtiene los tipos de edificación disponibles."""
        return ['residential', 'commercial', 'industrial']
    
    def get_countries_with_data(self, building_type: str = 'residential') -> List[str]:
        """Obtiene la lista de países con datos disponibles."""
        if building_type in self.max_damage_data:
            return self.max_damage_data[building_type]['country'].tolist()
        return []