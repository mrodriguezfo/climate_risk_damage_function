#!/usr/bin/env python3
"""
Process missing building types from JRC Excel file.
Adds support for agriculture, infrastructure, and transport.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def process_max_damage_sheet(excel_file, sheet_name, output_file):
    """Process a MaxDamage sheet and save as parquet."""
    print(f"📊 Processing {sheet_name}...")
    
    try:
        # Read the sheet
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        
        # The first row usually contains headers, let's check the structure
        print(f"   Original shape: {df.shape}")
        print(f"   Columns: {list(df.columns)}")
        
        # Find the actual data start (skip header rows)
        data_start_row = None
        for i, row in df.iterrows():
            if pd.notna(row.iloc[0]) and str(row.iloc[0]).strip() not in ['', 'Country', 'country']:
                # Check if this looks like a country name
                if len(str(row.iloc[0]).strip()) > 1:
                    data_start_row = i
                    break
        
        if data_start_row is None:
            print(f"   ⚠️  Could not find data start row in {sheet_name}")
            return False
        
        # Get the header row (usually one row before data starts)
        header_row = max(0, data_start_row - 1)
        headers = df.iloc[header_row].fillna('').astype(str).tolist()
        
        # Extract data from data_start_row onwards
        data_df = df.iloc[data_start_row:].copy()
        data_df.columns = headers
        
        # Clean up the dataframe
        # Remove rows where the first column is empty or NaN
        data_df = data_df[data_df.iloc[:, 0].notna()]
        data_df = data_df[data_df.iloc[:, 0].astype(str).str.strip() != '']
        
        # Rename first column to 'country'
        if len(data_df.columns) > 0:
            data_df = data_df.rename(columns={data_df.columns[0]: 'country'})
        
        # Remove completely empty columns
        data_df = data_df.dropna(axis=1, how='all')
        
        # Convert numeric columns
        for col in data_df.columns[1:]:  # Skip country column
            try:
                data_df[col] = pd.to_numeric(data_df[col], errors='coerce')
            except:
                pass
        
        # Remove rows where country is still empty after cleaning
        data_df = data_df[data_df['country'].notna()]
        data_df = data_df[data_df['country'].astype(str).str.strip() != '']
        
        print(f"   Processed shape: {data_df.shape}")
        print(f"   Sample countries: {data_df['country'].head(3).tolist()}")
        
        if len(data_df) > 0:
            # Save as parquet
            data_df.to_parquet(output_file, index=False)
            print(f"   ✅ Saved to {output_file}")
            return True
        else:
            print(f"   ⚠️  No valid data found in {sheet_name}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error processing {sheet_name}: {e}")
        return False

def main():
    """Process missing building types."""
    excel_file = Path("Damage function.xlsx")
    output_dir = Path("processed_jrc_data")
    
    if not excel_file.exists():
        print(f"❌ Excel file not found: {excel_file}")
        return
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Define the missing building types to process
    missing_types = [
        ("MaxDamage-Agriculture", "max_damage_agriculture_jrc.parquet"),
        ("MaxDamage-Infrastructure", "max_damage_infrastructure_jrc.parquet"),
        ("MaxDamage-Transport", "max_damage_transport_jrc.parquet")
    ]
    
    print("🏗️ Processing missing building types from JRC Excel")
    print("=" * 60)
    
    success_count = 0
    for sheet_name, output_filename in missing_types:
        output_file = output_dir / output_filename
        if process_max_damage_sheet(excel_file, sheet_name, output_file):
            success_count += 1
        print()
    
    print(f"✅ Successfully processed {success_count}/{len(missing_types)} building types")
    
    # List all processed files
    print("\n📁 All processed files:")
    for file in sorted(output_dir.glob("*.parquet")):
        print(f"   - {file.name}")

if __name__ == "__main__":
    main()