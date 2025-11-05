#!/usr/bin/env python3
"""
Process Infrastructure and Transport sheets with special handling.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def process_infrastructure_transport():
    """Process Infrastructure and Transport sheets."""
    excel_file = Path("Damage function.xlsx")
    output_dir = Path("processed_jrc_data")
    
    print("🏗️ Processing Infrastructure and Transport sheets")
    print("=" * 60)
    
    # Process Infrastructure
    print("📊 Processing MaxDamage-Infrastructure...")
    try:
        df_infra = pd.read_excel(excel_file, sheet_name='MaxDamage-Infrastructure')
        
        # Extract country and GDP columns (first two columns with data)
        infra_data = []
        for i, row in df_infra.iterrows():
            if i == 0:  # Skip header row
                continue
            country = row.iloc[0]
            gdp = row.iloc[1]
            
            if pd.notna(country) and str(country).strip() not in ['', 'Country']:
                # Create a simplified structure with available data
                infra_data.append({
                    'country': str(country).strip(),
                    'gdp_per_capita_2010_usd': gdp if pd.notna(gdp) else 0,
                    'infrastructure_damage_eur_m2': 25.47 if pd.notna(gdp) else 0  # Default from Europe
                })
        
        df_infra_clean = pd.DataFrame(infra_data)
        df_infra_clean = df_infra_clean[df_infra_clean['country'] != '']
        
        output_file = output_dir / "max_damage_infrastructure_jrc.parquet"
        df_infra_clean.to_parquet(output_file, index=False)
        print(f"   ✅ Saved {len(df_infra_clean)} countries to {output_file}")
        
    except Exception as e:
        print(f"   ❌ Error processing Infrastructure: {e}")
    
    # Process Transport
    print("\\n📊 Processing MaxDamage-Transport...")
    try:
        df_transport = pd.read_excel(excel_file, sheet_name='MaxDamage-Transport')
        
        # Extract country and GDP columns (first two columns with data)
        transport_data = []
        for i, row in df_transport.iterrows():
            if i == 0:  # Skip header row
                continue
            country = row.iloc[0]
            gdp = row.iloc[1]
            
            if pd.notna(country) and str(country).strip() not in ['', 'Country']:
                # Create a simplified structure with available data
                transport_data.append({
                    'country': str(country).strip(),
                    'gdp_per_capita_2010_usd': gdp if pd.notna(gdp) else 0,
                    'transport_damage_eur_m2': 751 if pd.notna(gdp) else 0  # Default from Europe
                })
        
        df_transport_clean = pd.DataFrame(transport_data)
        df_transport_clean = df_transport_clean[df_transport_clean['country'] != '']
        
        output_file = output_dir / "max_damage_transport_jrc.parquet"
        df_transport_clean.to_parquet(output_file, index=False)
        print(f"   ✅ Saved {len(df_transport_clean)} countries to {output_file}")
        
    except Exception as e:
        print(f"   ❌ Error processing Transport: {e}")
    
    print("\\n📁 All processed files:")
    for file in sorted(output_dir.glob("*.parquet")):
        print(f"   - {file.name}")

if __name__ == "__main__":
    process_infrastructure_transport()