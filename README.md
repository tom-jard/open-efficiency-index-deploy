# 🏡 Open Efficiency Index

**A transparent, regionally-aware alternative to ENERGY STAR appliance ratings**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/open-efficiency-index)

[🌐 **Live Demo**](https://open-efficiency-index.vercel.app) | [📊 **Search Database**](https://open-efficiency-index.vercel.app/web/) | [🗺️ **Regional Map**](https://open-efficiency-index.vercel.app/web/regional-efficiency-map.html)

---

## ✨ **What Makes This Different**

Unlike ENERGY STAR's binary qualified/not-qualified ratings, the Open Efficiency Index provides:

🎯 **Honest Performance Ratings** - Based on actual appliance performance (ft³/kWh, place settings/kWh)  
🗺️ **Regional Awareness** - Shows how location affects your costs and environmental impact  
📊 **Transparent Methodology** - All algorithms and data sources are open source  
🔍 **Graduated Scoring** - 0-100 percentile ranking with realistic distribution  

### **Example: Same Samsung Refrigerator, Different States**
- **Efficiency Score**: 93% (A+ rating) - **SAME everywhere**
- **California**: $73/year, 136 lbs CO₂ (clean grid, high cost)  
- **Texas**: $39/year, 288 lbs CO₂ (dirty grid, low cost)

*The appliance doesn't become "more efficient" in different states - only cost and environmental impact change.*

---

## 🚀 **Quick Deploy**

### **One-Click Vercel Deployment**
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/open-efficiency-index)

### **Local Development**
```bash
# Clone and setup
git clone https://github.com/yourusername/open-efficiency-index.git
cd open-efficiency-index
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
- **400+ appliances** across 4 major categories
- **Realistic score distribution**: 10-95% range (not artificial 0-100 sequence)
- **Regional calculations**: All 50 US states with real electricity pricing and grid data
- **Honest ratings**: A+ reserved for truly exceptional efficiency (top 10% of products)

### **Top Performers by True Efficiency**
- **Refrigerators**: Samsung Model-R0029 (93rd percentile efficiency)
- **Dishwashers**: Frigidaire Model-D0075 (87th percentile efficiency)  
- **Clothes Washers**: Frigidaire Model-C0075 (95th percentile efficiency)
- **Water Heaters**: High-efficiency models with 0.90+ UEF ratings

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

**Same Appliance, Different Impact**: A high-efficiency refrigerator costs $39/year in Texas vs $73/year in California, but produces 288 vs 136 lbs CO₂ respectively.

---

## 🔌 **API & Integration**

### **REST API Endpoints**
```bash
# Search appliances with filters
GET /search?category=refrigerators&manufacturer=Samsung&min_score=80&limit=10

# Get top performers by category  
GET /top-performers/refrigerators?limit=5

# Compare multiple models
GET /compare?model=Model-R0029&model=Model-R0051

# Get comprehensive stats
GET /stats

# Regional cost and carbon impact
GET /regional-impact/Model-R0029
```

### **Response Format**
```json
{
  "appliances": [{
    "manufacturer": "Samsung",
    "model_number": "Model-R0029",
    "open_efficiency_score": 93.0,
    "efficiency_rating": "A+", 
    "annual_energy_kwh": 303.0,
    "annual_cost_us_average": 50.0,
    "annual_co2_lbs_us_average": 257.6,
    "regional_impact": {
      "California": {"annual_cost": 73.0, "annual_co2_lbs": 136.4},
      "Texas": {"annual_cost": 38.8, "annual_co2_lbs": 287.9}
    }
  }]
}
```

---

## 🏗️ **Project Structure**

```
open-efficiency-index/
├── 📊 api/                 # REST API server
│   ├── efficiency_api.py   # Main Flask application
│   └── *.py               # Modular API components
├── 🌐 web/                # Consumer interfaces
│   ├── index.html         # Database search & comparison
│   └── regional-efficiency-map.html  # Interactive state map
├── 📈 data/               # SQLite database
│   └── open_efficiency_index.db     # 400+ appliances with scores
├── 🔧 scripts/            # Data processing pipeline
│   └── data_pipeline.py   # Generate efficiency scores from raw data
├── 📖 documentation/      # Comprehensive guides
└── 🧪 tests/             # Testing and validation
```

---

## 🎓 **Academic Context**

### **CELI Fellowship Capstone Project**
This project was developed as part of the Clean Energy Leadership Institute (CELI) fellowship program, demonstrating rapid policy technology prototyping.

### **Policy Innovation**
- **Alternative Framework**: Viable replacement for potentially defunded ENERGY STAR program
- **Regional Equity**: Addresses geographic disparities in energy costs and emissions
- **Open Standards**: Promotes transparency in efficiency rating methodologies
- **Consumer Empowerment**: Provides actionable information for informed appliance purchases

### **"Vibe Coding for Good" Methodology**
Complete production-ready system delivered through focused development sessions, showing how technologists can quickly build policy alternatives that serve the public interest.

---

## 🔧 **Development Setup**

### **Prerequisites**
- Python 3.9+ 
- pip (Python package manager)
- Git

### **Local Development**
```bash
# Clone repository
git clone https://github.com/yourusername/open-efficiency-index.git
cd open-efficiency-index

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Generate data (optional - database included)
python scripts/data_pipeline.py

# Start API server
python api/efficiency_api.py

# Run tests
python scripts/test_system_validation.py
```

### **Environment Variables**
```bash
# .env file configuration
FLASK_ENV=production
DATABASE_PATH=data/open_efficiency_index.db
API_HOST=0.0.0.0
API_PORT=8080
ENABLE_CORS=true
```

---

## 🧪 **Testing & Validation**

### **Automated Testing**
```bash
# Run comprehensive system validation
python scripts/test_system_validation.py

# Expected output: 4/4 tests passed
# ✅ Database integrity (400+ appliances)
# ✅ API endpoints (6 endpoints working)
# ✅ Key research findings (ice maker analysis, regional variations)
# ✅ Web interface accessibility
```

### **API Testing**
```bash
# Test all endpoints
curl http://localhost:8080/stats
curl "http://localhost:8080/search?category=refrigerators&limit=5"
curl "http://localhost:8080/top-performers/refrigerators?limit=3"
curl "http://localhost:8080/compare?model=Model-R0029&model=Model-R0051"
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
# With Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 api.efficiency_api:app

# With Apache/Nginx
# Configure reverse proxy to http://localhost:8080
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
- 🐛 **Data Quality**: Validate efficiency calculations against manufacturer specs
- 🌐 **Regional Expansion**: Add more states, Canadian provinces, or international markets  
- 📊 **New Categories**: Expand beyond refrigerators/dishwashers/washers/water heaters
- 🔍 **Search Enhancement**: Better filtering, sorting, and recommendation algorithms
- 🎨 **UI/UX**: Improve web interface design and mobile experience

### **Development Process:**
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test locally
4. Run validation: `python scripts/test_system_validation.py`
5. Submit pull request with clear description

---

## 📄 **License & Data**

**MIT License** - Free for academic, commercial, and government use.

**Open Data Commitment**: All efficiency calculations, regional data, and methodologies are transparent and reproducible. We believe energy efficiency information should be accessible to everyone.

---

## 📞 **Contact & Support**

- **Issues**: [GitHub Issues](https://github.com/yourusername/open-efficiency-index/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/open-efficiency-index/discussions)
- **Project Lead**: Thomas Jardine (CELI Fellow 2025)
- **Live Demo**: [open-efficiency-index.vercel.app](https://open-efficiency-index.vercel.app)

---

## 🏆 **Recognition**

If this project helps you make more informed appliance decisions or advances energy efficiency transparency, please consider giving it a star! ⭐

**Making energy efficiency transparent, one appliance at a time.** 🏡✨

---

*For technical documentation, see [API.md](API.md) | For deployment details, see [documentation/](documentation/)*