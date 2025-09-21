# 🛡️ Protecting ENERGY STAR

**An open-source safeguard for efficiency standards**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/tom-jard/open-efficiency-index-deploy)

[🌐 **Live Demo**](https://open-efficiency-index-deploy.vercel.app) | [📊 **Search Database**](https://open-efficiency-index-deploy.vercel.app/web/) | [🗺️ **Regional Map**](https://open-efficiency-index-deploy.vercel.app/web/regional-efficiency-map.html)

---

## ✨ **Protecting 30 Years of Efficiency Progress**

Unlike traditional efficiency databases that risk policy changes, Protecting ENERGY STAR provides:

🛡️ **Legacy Preservation** - Community-driven protection for ENERGY STAR's 30-year foundation
🏭 **Authentic Data** - Built on **5,807 real ENERGY STAR certified appliances** from government APIs
🗺️ **Enhanced Regional Awareness** - Adding location-specific cost and emissions to ENERGY STAR data
📊 **Open-Source Guarantee** - Ensuring efficiency standards remain publicly available forever
🔍 **True Government Standards** - Based on actual ENERGY STAR test procedures and certifications  

### **Example: Real GE Profile Clothes Washer (PFQ83HSSW***)**
- **Efficiency Score**: Based on real IMEF (Integrated Modified Energy Factor) from ENERGY STAR testing
- **California**: Higher electricity cost, lower carbon impact (clean grid)  
- **Texas**: Lower electricity cost, higher carbon impact (fossil fuel grid)

*Real appliance efficiency from government certification database - not synthetic or estimated data.*

---

## 🚀 **Quick Deploy**

### **One-Click Vercel Deployment**
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/tom-jard/open-efficiency-index-deploy)

### **Local Development**
```bash
# Clone and setup
git clone https://github.com/tom-jard/open-efficiency-index-deploy.git
cd open-efficiency-index-deploy
pip install -r requirements.txt

# Start API server
python api/efficiency_api.py

# Open web interface
open web/index.html
# OR serve with Python: cd web && python -m http.server 8081
```

### **Production Deployment**
```bash
# With Gunicorn (recommended)
gunicorn -w 4 -b 0.0.0.0:8080 api.efficiency_api:app

# With Docker (coming soon)
docker build -t open-efficiency-index .
docker run -p 8080:8080 open-efficiency-index
```

---

## 🎯 **Core Innovation: Honest Efficiency Scoring**

### **The Problem We Solved**
Traditional efficiency ratings suffer from misleading composite scores and regional blindness. We discovered that even sophisticated systems can use fundamentally flawed algorithms.

### **Our Solution: Separation of Concerns**

**True Efficiency** (intrinsic to appliance):
- **Refrigerators**: Storage volume ÷ annual energy (ft³/kWh-year)
- **Dishwashers**: Place settings ÷ energy per cycle (settings/kWh) 
- **Clothes Washers**: Capacity ÷ energy per load (ft³/kWh-load)
- **Water Heaters**: Uniform Energy Factor (industry standard)

**Regional Impact** (location-dependent):
- **Cost**: Annual energy × local electricity rates
- **Carbon**: Annual energy × local grid emissions

**Honest Distribution**: Percentile ranking within category - most appliances score 20-80%, only top performers earn 90%+.

---

## 📊 **Sample Results**

### **Database Coverage**
- **5,807 real ENERGY STAR certified appliances** across 4 major categories
- **Authentic government data**: Official ENERGY STAR certification database
- **Real manufacturers**: GE Profile, Samsung, LG, Whirlpool, Frigidaire, Bosch, American, A.O. Smith, Rheem
- **Actual model numbers**: Like PFQ83HSSW*** (not synthetic Model-C0084 placeholders)
- **Regional calculations**: All 50 US states with real electricity pricing and grid data
- **Gas appliances**: Water heaters with proper gas energy conversion and pricing

### **Data Sources (100% Real Government Data)**
- **Refrigerators**: 4,323 certified models from ENERGY STAR dataset p5st-her9
- **Dishwashers**: 645 certified models from ENERGY STAR dataset q8py-6w3f  
- **Clothes Washers**: 335 certified models from ENERGY STAR dataset bghd-e2wd
- **Water Heaters**: 504 certified models from ENERGY STAR dataset 6sbi-yuk2 (gas and electric)

---

## 🌍 **Regional Awareness**

Our system calculates separate regional impact using real data:

**Electricity Pricing** (EIA data):
- California: 24.1¢/kWh (expensive)
- Texas: 12.8¢/kWh (cheap)  
- US Average: 16.5¢/kWh

**Grid Emissions** (EPA eGRID):
- California: 0.45 lbs CO₂/kWh (clean renewables)
- Texas: 0.95 lbs CO₂/kWh (fossil fuel heavy)
- US Average: 0.85 lbs CO₂/kWh

**Gas Pricing** (EIA data):
- Natural Gas US Average: $1.28/therm
- California: $1.85/therm (expensive)
- Texas: $1.05/therm (cheap)

**Same Appliance, Different Impact**: A high-efficiency refrigerator costs $39/year in Texas vs $73/year in California, but produces 288 vs 136 lbs CO₂ respectively. Gas water heaters show similar regional variations in cost and emissions.

---

## 🔌 **API & Integration**

### **REST API Endpoints**
```bash
# Search real ENERGY STAR appliances with filters
GET /api/search?category=refrigerators&manufacturer=Samsung&min_score=80&limit=10

# Get real appliance data by category  
GET /api/search?category=clothes_washers&limit=5

# Database statistics (real data counts)
GET /api/stats
```

### **Response Format**
```json
{
  "category": "clothes_washers",
  "total_results": 5,
  "filters": {
    "manufacturer": null,
    "min_score": 0
  },
  "appliances": [{
    "manufacturer": "GE Profile",
    "model_number": "PFQ83HSSW***",
    "open_efficiency_score": 87,
    "efficiency_rating": "A", 
    "annual_energy_kwh": 152,
    "annual_cost_us_average": 25.08,
    "annual_co2_lbs_us_average": 129.2,
    "integrated_modified_energy_factor": 2.65,
    "energy_star_certified": true,
    "data_source": "ENERGY_STAR_OFFICIAL"
  }]
}
```

---

## 🏗️ **Project Structure**

```
open-efficiency-index/
├── 📊 api/                 # Node.js serverless API
│   ├── index.js            # Main Vercel serverless function
│   └── data/              # Real ENERGY STAR data (5,807 appliances)
│       ├── refrigerators.json      # 4,323 real certified refrigerators
│       ├── dishwashers.json        # 645 real certified dishwashers  
│       ├── clothes_washers.json    # 335 real certified clothes washers
│       ├── water_heaters.json      # 504 real certified water heaters
│       └── stats.json             # Real database statistics
├── 🌐 web/                # Consumer web interface
│   ├── index.html         # Database search & comparison
│   └── regional-efficiency-map.html  # Interactive state map
├── 📈 data/               # Legacy SQLite database (development)
│   └── open_efficiency_index.db     
├── 🔧 scripts/            # Data processing pipelines
│   ├── real_data_pipeline.py       # REAL ENERGY STAR API integration  
│   └── data_pipeline.py           # Legacy synthetic data generator
├── 📖 documentation/      # Comprehensive guides
└── 🧪 tests/             # Testing and validation
```

---

## 🎓 **Academic Context**

### **CELI Fellowship Capstone Project**
This project was developed as part of the Clean Energy Leadership Institute (CELI) fellowship program, demonstrating rapid policy technology prototyping.

### **Policy Innovation: Safeguarding Efficiency Standards**
- **Legacy Protection**: Community backup for potentially threatened ENERGY STAR program
- **Democratic Access**: Ensuring efficiency data remains publicly accessible
- **Regional Equity**: Addresses geographic disparities in energy costs and emissions
- **Open Standards**: Promotes transparency in efficiency rating methodologies
- **Consumer Empowerment**: Provides actionable information for informed appliance purchases

### **"Protecting Standards" Methodology**
Community-driven system using **authentic ENERGY STAR certification data**, demonstrating how open-source technology can safeguard public efficiency standards with verified, trustworthy government information - ensuring 30 years of progress remains protected.

---

## 🔧 **Development Setup**

### **Prerequisites**
- Python 3.9+ 
- pip (Python package manager)
- Git

### **Local Development**
```bash
# Clone repository
git clone https://github.com/tom-jard/open-efficiency-index-deploy.git
cd open-efficiency-index-deploy

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Generate real ENERGY STAR data (replaces any existing data)
python scripts/real_data_pipeline.py

# Start API server (Node.js for production compatibility)
cd api && node index.js

# Run tests
python scripts/test_system_validation.py
```

### **Environment Variables**
```bash
# .env file configuration (for local development)
NODE_ENV=production
API_HOST=0.0.0.0
API_PORT=3000
ENABLE_CORS=true

# For Python data pipeline
DATABASE_PATH=data/open_efficiency_index.db
ENERGYSTAR_API_BASE=https://data.energystar.gov/api/views
```

---

## 🧪 **Testing & Validation**

### **Automated Testing**
```bash
# Run comprehensive system validation
python scripts/test_system_validation.py

# Expected output: Real data validation
# ✅ Database integrity (5,807 real appliances from ENERGY STAR)
# ✅ API endpoints (Node.js serverless functions working)
# ✅ Real manufacturer validation (GE Profile, Samsung, LG confirmed)
# ✅ Web interface accessibility with authentic data
```

### **API Testing**
```bash
# Test main endpoints with real data
curl https://open-efficiency-index-deploy.vercel.app/api/stats
curl "https://open-efficiency-index-deploy.vercel.app/api/search?category=refrigerators&limit=5"
curl "https://open-efficiency-index-deploy.vercel.app/api/search?category=clothes_washers&manufacturer=GE&limit=3"

# Local testing (if running locally)
curl http://localhost:3000/api/stats
curl "http://localhost:3000/api/search?category=clothes_washers&limit=5"
```

---

## 🚀 **Deployment Options**

### **Vercel (Recommended)**
- **One-click deployment**: Use the Vercel button above
- **Automatic HTTPS**: Secure by default
- **Global CDN**: Fast worldwide access
- **Zero configuration**: Works out of the box

### **Traditional Hosting**
```bash
# With Node.js (matches production environment)
npm install
npm start

# With Nginx/Apache reverse proxy  
# Configure proxy to http://localhost:3000
```

### **Docker (Coming Soon)**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "api.efficiency_api:app"]
```

---

## 🤝 **Contributing**

We welcome contributions! Areas needing help:

### **Priority Areas:**
- 🐛 **Data Quality**: Validate real ENERGY STAR efficiency calculations against additional government sources
- 🌐 **Regional Expansion**: Add Canadian provinces, EU energy labels, or international efficiency standards  
- 📊 **New Categories**: Add heat pumps, smart thermostats, or other ENERGY STAR certified appliances
- 🔍 **Search Enhancement**: Better filtering by real manufacturer specs, IMEF ranges, UEF ratings
- 🎨 **UI/UX**: Improve web interface to highlight authentic government certification badges

### **Development Process:**
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test locally
4. Run validation: `python scripts/test_system_validation.py`
5. Submit pull request with clear description

---

## 📄 **License & Data**

**MIT License** - Free for academic, commercial, and government use.

**Open Data Commitment**: All efficiency calculations, regional data, and methodologies are transparent and reproducible. We believe energy efficiency information should be accessible to everyone, backed by authentic government certification data.

---

## 📞 **Contact & Support**

- **Issues**: [GitHub Issues](https://github.com/tom-jard/open-efficiency-index-deploy/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tom-jard/open-efficiency-index-deploy/discussions)
- **Project Lead**: Thomas Jardine (CELI Fellow 2025)
- **Live Demo**: [open-efficiency-index.vercel.app](https://open-efficiency-index.vercel.app)

---

## 🏆 **Recognition**

If this project helps you make more informed appliance decisions or advances energy efficiency transparency, please consider giving it a star! ⭐

**Protecting energy efficiency standards, one appliance at a time.** 🛡️✨

---

*For technical documentation, see [API.md](API.md) | For deployment details, see [documentation/](documentation/)*