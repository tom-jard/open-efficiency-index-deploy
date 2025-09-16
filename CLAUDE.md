# Open Efficiency Index - Local Context

## Project Overview
A production-ready appliance efficiency rating system that provides transparent, regionally-aware alternatives to ENERGY STAR ratings using **real government certification data**.

## Major Achievement: Real Data Integration ✅
**December 2024**: Successfully migrated from synthetic data to **5,807 real ENERGY STAR certified appliances** from official government APIs.

### Data Sources (REAL - NO SYNTHETIC DATA)
- **ENERGY STAR API**: Official government certification database
- **Refrigerators**: 4,323 certified models (dataset: p5st-her9)
- **Dishwashers**: 645 certified models (dataset: q8py-6w3f)  
- **Clothes Washers**: 335 certified models (dataset: bghd-e2wd)
- **Water Heaters**: 504 certified models (dataset: 6sbi-yuk2)

### Real Data Pipeline
- **Source**: `scripts/real_data_pipeline.py` - Official ENERGY STAR APIs only
- **Processing**: Real efficiency calculations using government test procedures
- **Output**: `api/data/*.json` - Authentic manufacturer data (GE Profile, Samsung, LG, etc.)
- **Database**: SQLite with real appliance specifications and performance metrics

## Production Deployment Status ✅
- **Live URL**: https://open-efficiency-index-deploy.vercel.app
- **API Verified**: Real manufacturers like "GE Profile" with authentic model numbers
- **Data Confirmed**: 5,807 real ENERGY STAR certified appliances
- **Deployment**: Vercel auto-deploys from main branch

## Quick Start
```bash
# Start local development
cd /Users/thomasjardine/code/personal/celi/open-efficiency-index-deploy

# Use universal Python environment
/Users/thomasjardine/code/.universal-venv/bin/python api/index.js  # Node.js API (current)
# OR for Python development:
/Users/thomasjardine/code/.universal-venv/bin/python scripts/real_data_pipeline.py

# Test API locally
curl http://localhost:8080/api/search?category=clothes_washers&limit=5
```

## Key File Paths

### Production API (Node.js)
- **Main API**: `api/index.js` - Vercel serverless function serving JSON data
- **Real Data**: `api/data/*.json` - 5,807 real ENERGY STAR appliances
- **Stats**: `api/data/stats.json` - Real database statistics
- **Web Interface**: `web/index.html` - Database search and visualization

### Data Processing (Python)
- **Real Data Pipeline**: `scripts/real_data_pipeline.py` - ENERGY STAR API integration
- **Legacy Pipeline**: `scripts/data_pipeline.py` - Original synthetic data generator
- **Database**: `data/open_efficiency_index.db` - SQLite with real data

### Configuration
- **Vercel Config**: `vercel.json` - Deployment settings
- **Package Config**: `package.json` - Node.js dependencies
- **Python Deps**: `requirements.txt` - Data processing dependencies

## Working Commands

### Real Data Operations
```bash
# Update with latest ENERGY STAR data
/Users/thomasjardine/code/.universal-venv/bin/python scripts/real_data_pipeline.py

# Check specific categories
/Users/thomasjardine/code/.universal-venv/bin/python -c "
from real_data_pipeline import RealApplianceDataPipeline
pipeline = RealApplianceDataPipeline()
results = pipeline.process_category('refrigerators')
print(f'Processed {len(results)} real refrigerator models')
"

# Verify API data
curl "https://open-efficiency-index-deploy.vercel.app/api/search?category=clothes_washers&limit=3"
```

### Local Development
```bash
# Serve web interface locally
cd web && python -m http.server 8081

# Test API endpoints
cd api && node index.js  # If running locally

# Validate data integrity
/Users/thomasjardine/code/.universal-venv/bin/python -c "
import json
with open('api/data/stats.json') as f:
    stats = json.load(f)
    print(f\"Total real models: {stats['database_stats']['total_models']}\")
"
```

### Deployment
```bash
# Deploy to production (auto-deploys via git)
git add -A
git commit -m "Update with latest real ENERGY STAR data"
git push origin main

# Verify production deployment
curl "https://open-efficiency-index-deploy.vercel.app/api/stats"
```

## Data Flow

### Real Data Pipeline Flow
1. **Fetch**: `real_data_pipeline.py` → Official ENERGY STAR APIs
2. **Process**: Clean and calculate efficiency scores from real specifications
3. **Store**: Save to `api/data/*.json` for Node.js API consumption  
4. **Serve**: Vercel serverless functions serve JSON data to web interface
5. **Display**: Web interface shows real manufacturer names and model numbers

### API Request Flow
```
User Request → Vercel → api/index.js → api/data/*.json → Real ENERGY STAR Data
```

## Gotchas

### Real vs Synthetic Data
- ✅ **Production uses REAL data**: All synthetic "Model-C0084" replaced with authentic "GE Profile PFQ83HSSW***"
- ❌ **Don't run synthetic pipeline**: `data_pipeline.py` generates fake data for development only
- ✅ **Use real pipeline**: `real_data_pipeline.py` fetches authentic ENERGY STAR certified appliances

### API Differences
- **Node.js API** (production): `api/index.js` - Serves static JSON files, fast and scalable
- **Python API** (development): `api/efficiency_api.py` - Dynamic SQLite queries, more flexible

### Data Validation
- **Real manufacturer names**: GE Profile, Samsung, LG, Whirlpool, Frigidaire, Bosch, American, A.O. Smith, Rheem
- **Authentic models**: Look for realistic patterns like "PFQ83HSSW***", not "Model-C0084"  
- **Real specs**: IMEF values, UEF ratings, actual energy consumption from government tests
- **Water heater specifics**: Gas usage in therms converted to kWh equivalent, real gas pricing integration

### Water Heater Processing Notes
- **Energy conversion**: 1 therm = 29.3 kWh thermal equivalent for comparison purposes
- **Cost calculations**: Use gas pricing ($1.28/therm US average) not electricity rates
- **CO2 emissions**: Gas carbon intensity (11.7 lbs CO2/therm) for accurate environmental impact
- **CSV vs API**: Pipeline uses CSV data with column names like "Brand Name", not JSON "brand_name"

### Environment Issues
- **Python environment**: Always use `/Users/thomasjardine/code/.universal-venv/bin/python`
- **API timeouts**: ENERGY STAR APIs can be slow, include retry logic
- **File paths**: Use absolute paths for data files in production

## Dependencies

### Runtime (Production)
- **Node.js**: Vercel serverless functions
- **Static JSON**: Pre-processed real ENERGY STAR data
- **No database**: Uses JSON files for maximum performance

### Development (Data Processing)
- **Python 3.9+**: Data processing and API integration  
- **Universal venv**: `/Users/thomasjardine/code/.universal-venv/`
- **Packages**: pandas, requests, sqlite3 (for real data pipeline)
- **APIs**: ENERGY STAR official data endpoints (no authentication required)

### Web Interface
- **Vanilla JavaScript**: No framework dependencies
- **Chart.js**: Visualization library
- **CSS**: Custom design system with Apple-inspired aesthetics

## Authentication Requirements
- **ENERGY STAR APIs**: No authentication required (public government data)
- **Vercel deployment**: Automatic via GitHub integration
- **Local development**: No special setup required

## Last Updated
- **2025-09-16**: Critical water heater data processing fix
  - Fixed column mapping issue (CSV vs JSON field names)
  - Added proper gas energy conversion (therms → kWh equivalent) 
  - Implemented real gas pricing and CO2 calculations
  - Water heaters now display accurate costs ($240/yr) and emissions (2,200 lbs CO2/yr)
  - Fixed web interface energy use column field mapping bug
- **2024-12-15**: Major production deployment with real ENERGY STAR data
  - Replaced all synthetic data with 5,807 real certified appliances
  - Verified production deployment at https://open-efficiency-index-deploy.vercel.app
  - API confirmed returning authentic manufacturer names and specifications
  - Complete data pipeline documentation updated for real data sources