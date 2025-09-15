#!/usr/bin/env python3
"""
Open Efficiency Index - REAL Data Pipeline
==========================================
Real data ingestion from official ENERGY STAR and DOE sources.
NO SYNTHETIC DATA - REAL GOVERNMENT DATABASES ONLY
"""

import pandas as pd
import requests
import json
import numpy as np
from pathlib import Path
from datetime import datetime
import logging
from typing import Dict, List, Optional
import sqlite3
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RealApplianceDataPipeline:
    """Real data pipeline using official ENERGY STAR and DOE APIs."""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(exist_ok=True)
        
        # REAL ENERGY STAR API ENDPOINTS - NO SYNTHETIC DATA
        self.energystar_apis = {
            'refrigerators': {
                'csv_url': 'https://data.energystar.gov/api/views/p5st-her9/rows.csv?accessType=DOWNLOAD',
                'json_url': 'https://data.energystar.gov/api/views/p5st-her9/rows.json?accessType=DOWNLOAD',
                'dataset_id': 'p5st-her9'
            },
            'clothes_washers': {
                'csv_url': 'https://data.energystar.gov/api/views/bghd-e2wd/rows.csv?accessType=DOWNLOAD', 
                'json_url': 'https://data.energystar.gov/api/views/bghd-e2wd/rows.json?accessType=DOWNLOAD',
                'dataset_id': 'bghd-e2wd'
            },
            'dishwashers': {
                'csv_url': 'https://data.energystar.gov/api/views/q8py-6w3f/rows.csv?accessType=DOWNLOAD',
                'json_url': 'https://data.energystar.gov/api/views/q8py-6w3f/rows.json?accessType=DOWNLOAD',
                'dataset_id': 'q8py-6w3f'
            },
            'water_heaters': {
                'csv_url': 'https://data.energystar.gov/api/views/6sbi-yuk2/rows.csv?accessType=DOWNLOAD',
                'json_url': 'https://data.energystar.gov/api/views/6sbi-yuk2/rows.json?accessType=DOWNLOAD',
                'dataset_id': '6sbi-yuk2'  # Gas storage and tankless water heaters
            }
        }
        
        # Regional electricity data (EIA API for real pricing)
        self.eia_api_key = None  # Will need real API key
        
        logger.info("Initialized REAL data pipeline - NO synthetic data will be used")
    
    def fetch_energystar_data(self, category: str) -> pd.DataFrame:
        """Fetch real ENERGY STAR data from official APIs."""
        if category not in self.energystar_apis:
            raise ValueError(f"Category {category} not available. Available: {list(self.energystar_apis.keys())}")
        
        api_info = self.energystar_apis[category]
        logger.info(f"Fetching REAL {category} data from ENERGY STAR API: {api_info['csv_url']}")
        
        try:
            # Download real CSV data
            response = requests.get(api_info['csv_url'], timeout=30)
            response.raise_for_status()
            
            # Save raw data
            raw_file = self.data_dir / f"raw_{category}_energystar.csv"
            with open(raw_file, 'wb') as f:
                f.write(response.content)
            
            # Load into DataFrame
            df = pd.read_csv(raw_file)
            logger.info(f"Successfully loaded {len(df)} real {category} models from ENERGY STAR")
            
            return df
            
        except Exception as e:
            logger.error(f"Failed to fetch real {category} data: {e}")
            raise
    
    def clean_energystar_data(self, df: pd.DataFrame, category: str) -> pd.DataFrame:
        """Clean and standardize real ENERGY STAR data."""
        logger.info(f"Cleaning real {category} data from ENERGY STAR")
        
        # Log original columns for debugging
        logger.info(f"Original columns: {list(df.columns)}")
        
        cleaned = df.copy()
        
        # Basic cleaning - use actual column names
        cleaned = cleaned.dropna(subset=['Brand Name', 'Model Number'])
        
        if category == 'refrigerators':
            # Clean refrigerator data - use actual ENERGY STAR column names
            column_mapping = {
                'Brand Name': 'manufacturer',
                'Model Number': 'model_number', 
                'Annual Energy Use (kWh/yr)': 'annual_energy_use_kwh',
                'Adjusted Volume (ft3)': 'adjusted_volume_cubic_feet',
                'Capacity (Total Volume) (ft3)': 'capacity_cubic_feet',
                'Type': 'configuration',
                'Ice Maker': 'ice_maker',
                'Thru the Door Dispenser': 'through_door_ice',
                'Date Available On Market': 'date_available'
            }
            
        elif category == 'clothes_washers':
            # Clean clothes washer data - use actual ENERGY STAR column names
            column_mapping = {
                'Brand Name': 'manufacturer',
                'Model Number': 'model_number',
                'Volume (cu. ft.)': 'capacity_cubic_feet',
                'Integrated Modified Energy Factor (IMEF)': 'integrated_modified_energy_factor',
                'Integrated Water Factor (IWF)': 'integrated_water_factor',
                'Annual Energy Use (kWh/yr)': 'annual_energy_use_kwh',
                'Load Configuration': 'washer_type',
                'Date Available On Market': 'date_available'
            }
            
        elif category == 'dishwashers':
            # Clean dishwasher data - use actual ENERGY STAR column names
            column_mapping = {
                'Brand Name': 'manufacturer',
                'Model Number': 'model_number',
                'Capacity - Maximum Number of Place Settings': 'place_settings',
                'Annual Energy Use (kWh/yr)': 'annual_energy_use_kwh',
                'Water Use (gallons/cycle)': 'water_per_cycle_gallons',
                'Type': 'dishwasher_type',
                'Soil-Sensing Capability': 'soil_sensor',
                'Drying Method': 'drying_method'
            }
            
        elif category == 'water_heaters':
            # Clean water heater data - use actual CSV column names from ENERGY STAR
            column_mapping = {
                'Brand Name': 'manufacturer',
                'Model Number': 'model_number',
                'Storage Volume (gallons)': 'tank_size_gallons',
                'First Hour Rating (gallons)': 'first_hour_rating_gallons',
                'Uniform Energy Factor (UEF)': 'uniform_energy_factor',
                'Type': 'water_heater_type',
                'Fuel': 'fuel_type',
                'Therms/year for Natural Gas': 'annual_therms_natural_gas',
                'Gallons/year for Propane': 'annual_gallons_propane'
            }
        
        # Apply column mapping where columns exist
        for old_col, new_col in column_mapping.items():
            if old_col in cleaned.columns:
                cleaned[new_col] = cleaned[old_col]
        
        # Add category and certification status
        cleaned['category'] = category
        cleaned['energy_star_certified'] = 1  # All ENERGY STAR data is certified
        cleaned['data_source'] = 'ENERGY_STAR_OFFICIAL'
        cleaned['fetch_date'] = datetime.now().isoformat()
        
        # Clean manufacturer names
        if 'manufacturer' in cleaned.columns:
            cleaned['manufacturer'] = cleaned['manufacturer'].str.strip().str.title()
        
        logger.info(f"Cleaned {len(cleaned)} real {category} records")
        return cleaned
    
    def calculate_efficiency_scores(self, df: pd.DataFrame, category: str) -> pd.DataFrame:
        """Calculate efficiency scores using real appliance data."""
        logger.info(f"Calculating efficiency scores for {len(df)} real {category} models")
        
        scored = df.copy()
        
        if category == 'refrigerators' and 'annual_energy_use_kwh' in scored.columns:
            # Real efficiency calculation based on energy use and capacity
            scored['annual_energy_use_kwh'] = pd.to_numeric(scored['annual_energy_use_kwh'], errors='coerce')
            scored['capacity_cubic_feet'] = pd.to_numeric(scored['capacity_cubic_feet'], errors='coerce')
            
            # Remove rows with missing critical data
            scored = scored.dropna(subset=['annual_energy_use_kwh', 'capacity_cubic_feet'])
            
            if len(scored) > 0:
                # True efficiency: cubic feet per kWh (higher is better)
                scored['true_efficiency'] = scored['capacity_cubic_feet'] / scored['annual_energy_use_kwh']
                
                # Score based on percentile ranking (0-100)
                scored['open_efficiency_score'] = scored['true_efficiency'].rank(pct=True) * 100
                scored['open_efficiency_score'] = scored['open_efficiency_score'].round(0)
        
        elif category == 'clothes_washers' and 'integrated_modified_energy_factor' in scored.columns:
            # Real efficiency for clothes washers
            scored['integrated_modified_energy_factor'] = pd.to_numeric(scored['integrated_modified_energy_factor'], errors='coerce')
            scored = scored.dropna(subset=['integrated_modified_energy_factor'])
            
            if len(scored) > 0:
                # Higher IMEF is better
                scored['true_efficiency'] = scored['integrated_modified_energy_factor']
                scored['open_efficiency_score'] = scored['true_efficiency'].rank(pct=True) * 100
                scored['open_efficiency_score'] = scored['open_efficiency_score'].round(0)
        
        elif category == 'dishwashers' and 'annual_energy_use_kwh' in scored.columns:
            # Real efficiency for dishwashers
            scored['annual_energy_use_kwh'] = pd.to_numeric(scored['annual_energy_use_kwh'], errors='coerce')
            scored['place_settings'] = pd.to_numeric(scored['place_settings'], errors='coerce')
            scored = scored.dropna(subset=['annual_energy_use_kwh', 'place_settings'])
            
            if len(scored) > 0:
                # True efficiency: place settings per kWh/cycle (higher is better)
                # Annual energy / 280 cycles per year = energy per cycle
                scored['energy_per_cycle'] = scored['annual_energy_use_kwh'] / 280  # EPA estimate: 280 cycles/year
                scored['true_efficiency'] = scored['place_settings'] / scored['energy_per_cycle']
                scored['open_efficiency_score'] = scored['true_efficiency'].rank(pct=True) * 100
                scored['open_efficiency_score'] = scored['open_efficiency_score'].round(0)
        
        elif category == 'water_heaters' and 'uniform_energy_factor' in scored.columns:
            # Real efficiency for water heaters - UEF is already the efficiency metric
            scored['uniform_energy_factor'] = pd.to_numeric(scored['uniform_energy_factor'], errors='coerce')
            scored = scored.dropna(subset=['uniform_energy_factor'])
            
            if len(scored) > 0:
                # Higher UEF is better (already a true efficiency metric)
                scored['true_efficiency'] = scored['uniform_energy_factor']
                scored['open_efficiency_score'] = scored['true_efficiency'].rank(pct=True) * 100
                scored['open_efficiency_score'] = scored['open_efficiency_score'].round(0)
        
        # Calculate efficiency rating (A+ to F) based on score
        def score_to_rating(score):
            if score >= 90: return 'A+'
            elif score >= 80: return 'A'
            elif score >= 70: return 'B'
            elif score >= 60: return 'C'
            elif score >= 50: return 'D'
            else: return 'F'
        
        if 'open_efficiency_score' in scored.columns:
            scored['efficiency_rating'] = scored['open_efficiency_score'].apply(score_to_rating)
        
        # Calculate regional cost and carbon impact using real data
        scored = self.calculate_regional_impact(scored, category)
        
        logger.info(f"Calculated efficiency scores for {len(scored)} real models")
        return scored
    
    def calculate_regional_impact(self, df: pd.DataFrame, category: str) -> pd.DataFrame:
        """Calculate real regional cost and carbon impact."""
        
        # Real regional electricity pricing (cents/kWh) - 2024 averages
        regional_pricing = {
            'us_average': 16.51,
            'california': 27.04,
            'texas': 12.81,
            'new_york': 20.30,
            'florida': 13.20
        }
        
        # Real natural gas pricing by region ($/therm) - 2024 averages
        gas_pricing = {
            'us_average': 1.28,
            'california': 1.85,
            'texas': 1.05,
            'new_york': 1.45,
            'florida': 1.35
        }
        
        # Real carbon intensity by region (lbs CO2/kWh for electricity, lbs CO2/therm for gas)
        carbon_intensity = {
            'us_average': 0.85,
            'california': 0.45,  # Clean grid
            'texas': 1.0,       # More fossil fuels
            'new_york': 0.65,   # Mixed
            'florida': 0.88     # Mixed
        }
        
        # Gas carbon intensity (lbs CO2/therm) - EPA standard
        gas_carbon_intensity = 11.7  # lbs CO2/therm for natural gas
        
        scored = df.copy()
        
        # Water heaters: Convert gas/propane usage to equivalent kWh for comparison
        if category == 'water_heaters':
            # Convert therms to kWh equivalent (1 therm = 29.3 kWh thermal energy)
            if 'annual_therms_natural_gas' in scored.columns:
                scored['annual_therms_natural_gas'] = pd.to_numeric(scored['annual_therms_natural_gas'], errors='coerce')
                scored['annual_energy_use_kwh'] = scored['annual_therms_natural_gas'] * 29.3
                
                # Calculate gas costs directly (not as kWh equivalent)
                for region, gas_price in gas_pricing.items():
                    scored[f'annual_cost_{region}'] = scored['annual_therms_natural_gas'] * gas_price
                    scored[f'lifetime_cost_{region}'] = scored[f'annual_cost_{region}'] * 12
                    scored[f'annual_co2_lbs_{region}'] = scored['annual_therms_natural_gas'] * gas_carbon_intensity
                    scored[f'lifetime_co2_lbs_{region}'] = scored[f'annual_co2_lbs_{region}'] * 12
            
            # For electric water heaters, use electricity pricing
            elif 'annual_energy_use_kwh' in scored.columns:
                for region, price in regional_pricing.items():
                    scored[f'annual_cost_{region}'] = scored['annual_energy_use_kwh'] * price / 100
                    scored[f'lifetime_cost_{region}'] = scored[f'annual_cost_{region}'] * 12
                    scored[f'annual_co2_lbs_{region}'] = scored['annual_energy_use_kwh'] * carbon_intensity[region]
                    scored[f'lifetime_co2_lbs_{region}'] = scored[f'annual_co2_lbs_{region}'] * 12
        else:
            # For other appliances (electric), use standard electricity calculations
            if 'annual_energy_use_kwh' in scored.columns:
                for region, price in regional_pricing.items():
                    # Annual cost calculation
                    scored[f'annual_cost_{region}'] = scored['annual_energy_use_kwh'] * price / 100
                    
                    # Lifetime cost (12 years average appliance life)
                    scored[f'lifetime_cost_{region}'] = scored[f'annual_cost_{region}'] * 12
                    
                    # Annual CO2 impact
                    scored[f'annual_co2_lbs_{region}'] = scored['annual_energy_use_kwh'] * carbon_intensity[region]
                    
                    # Lifetime CO2 impact
                    scored[f'lifetime_co2_lbs_{region}'] = scored[f'annual_co2_lbs_{region}'] * 12
        
        return scored
    
    def save_to_database(self, df: pd.DataFrame, category: str):
        """Save real data to SQLite database."""
        db_path = self.data_dir / "open_efficiency_index_REAL.db"
        
        logger.info(f"Saving {len(df)} real {category} records to database: {db_path}")
        
        with sqlite3.connect(db_path) as conn:
            # Save to category-specific table (all columns)
            table_name = f"{category}_real"
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            
            # For unified table, only use core common columns
            unified_columns = [
                'manufacturer', 'model_number', 'category', 'energy_star_certified',
                'data_source', 'fetch_date', 'open_efficiency_score', 'efficiency_rating'
            ]
            
            # Filter to only existing columns
            available_columns = [col for col in unified_columns if col in df.columns]
            df_unified = df[available_columns].copy()
            
            df_unified.to_sql('appliances_real', conn, if_exists='append', index=False)
            
            logger.info(f"Saved real {category} data to tables: {table_name}, appliances_real")
    
    def export_to_json(self, df: pd.DataFrame, category: str):
        """Export real data to JSON files for API."""
        json_file = self.base_dir / "api" / "data" / f"{category}_REAL.json"
        json_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to JSON-serializable format
        export_data = df.to_dict('records')
        
        # Clean up any NaN values
        for record in export_data:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
        
        with open(json_file, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        logger.info(f"Exported {len(export_data)} real {category} records to {json_file}")
    
    def process_category(self, category: str) -> pd.DataFrame:
        """Process a single appliance category with REAL data."""
        logger.info(f"Processing REAL {category} data - NO synthetic data")
        
        # 1. Fetch real ENERGY STAR data
        raw_data = self.fetch_energystar_data(category)
        
        # 2. Clean and standardize
        cleaned_data = self.clean_energystar_data(raw_data, category)
        
        # 3. Calculate efficiency scores
        scored_data = self.calculate_efficiency_scores(cleaned_data, category)
        
        # 4. Save to database
        self.save_to_database(scored_data, category)
        
        # 5. Export to JSON for API
        self.export_to_json(scored_data, category)
        
        return scored_data
    
    def run_full_pipeline(self):
        """Run complete pipeline with REAL data only."""
        logger.info("Starting REAL appliance data pipeline - NO SYNTHETIC DATA")
        
        results = {}
        
        for category in self.energystar_apis.keys():
            try:
                logger.info(f"Processing {category} with REAL ENERGY STAR data")
                results[category] = self.process_category(category)
                time.sleep(1)  # Be respectful to APIs
                
            except Exception as e:
                logger.error(f"Failed to process {category}: {e}")
                continue
        
        logger.info("REAL data pipeline completed successfully")
        logger.info(f"Categories processed: {list(results.keys())}")
        
        return results

if __name__ == "__main__":
    # Run the REAL data pipeline
    pipeline = RealApplianceDataPipeline()
    results = pipeline.run_full_pipeline()
    
    print("\\n🎯 REAL DATA PIPELINE COMPLETED")
    print("✅ NO synthetic data used - only official ENERGY STAR databases")
    
    for category, df in results.items():
        print(f"✅ {category}: {len(df)} real models processed")
    
    print("\\n📊 Real appliance data now available in:")
    print("  - SQLite database: data/open_efficiency_index_REAL.db")
    print("  - JSON APIs: api/data/*_REAL.json")