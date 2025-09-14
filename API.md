# 🔌 Open Efficiency Index API

**RESTful API for appliance efficiency data with regional cost and carbon calculations**

**Base URL**: `http://localhost:8080` (development) | `https://your-domain.com/api` (production)

---

## 📋 **Quick Reference**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/stats` | GET | Database statistics and methodology |
| `/search` | GET | Search appliances with filters |
| `/top-performers/{category}` | GET | Top-rated appliances by category |
| `/compare` | GET | Compare multiple appliances |
| `/categories` | GET | Available appliance categories |
| `/regional-impact/{model}` | GET | Regional cost/carbon variations |

---

## 🔍 **Search Appliances**

**Endpoint**: `GET /search`

**Description**: Search appliances with optional filters for category, manufacturer, efficiency score, and more.

### **Parameters**

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `category` | string | No | Appliance category | `refrigerators`, `dishwashers` |
| `manufacturer` | string | No | Brand filter | `Samsung`, `LG`, `Bosch` |
| `min_score` | integer | No | Minimum efficiency score (0-100) | `80` |
| `max_score` | integer | No | Maximum efficiency score (0-100) | `95` |
| `energy_star` | boolean | No | ENERGY STAR certified only | `true`, `false` |
| `limit` | integer | No | Maximum results (default: 50) | `10` |

### **Example Requests**

```bash
# All Samsung refrigerators with score 80+
GET /search?category=refrigerators&manufacturer=Samsung&min_score=80&limit=10

# ENERGY STAR certified dishwashers
GET /search?category=dishwashers&energy_star=true

# Top-scoring appliances across all categories  
GET /search?min_score=90&limit=25
```

### **Response Format**

```json
{
  "appliances": [
    {
      "manufacturer": "Samsung",
      "model_number": "Model-R0029",
      "open_efficiency_score": 99.1,
      "efficiency_rating": "A+", 
      "energy_star_certified": 0,
      "annual_energy_kwh": 303.0,
      "annual_cost_us_average": 50.0,
      "annual_co2_lbs_us_average": 257.6
    }
  ],
  "total_results": 1,
  "category": "refrigerators",
  "filters": {
    "manufacturer": "Samsung",
    "min_score": 80,
    "max_score": 100,
    "energy_star_only": false
  }
}
```

---

## 🏆 **Top Performers**

**Endpoint**: `GET /top-performers/{category}`

**Description**: Get the highest-rated appliances in a specific category.

### **Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `category` | string | Yes | `refrigerators`, `dishwashers`, `water_heaters`, `clothes_washers` |

### **Query Parameters**

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `limit` | integer | No | Maximum results | `10` |

### **Example Requests**

```bash
# Top 5 refrigerators  
GET /top-performers/refrigerators?limit=5

# Top 3 dishwashers
GET /top-performers/dishwashers?limit=3
```

### **Response Format**

```json
{
  "category": "refrigerators",
  "appliances": [
    {
      "manufacturer": "Samsung",
      "model_number": "Model-R0029",
      "open_efficiency_score": 99.1,
      "efficiency_rating": "A+",
      "annual_energy_kwh": 303.0,
      "annual_cost_us_average": 50.0,
      "annual_co2_lbs_us_average": 257.6
    }
  ],
  "total_results": 5
}
```

---

## 🔄 **Compare Appliances**

**Endpoint**: `GET /compare`

**Description**: Compare multiple appliances side-by-side with efficiency scores and regional impact.

### **Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `models` | string | Yes | Comma-separated model numbers |

### **Example Requests**

```bash
# Compare three refrigerators
GET /compare?models=Model-R0029,Model-R0051,Model-R0094

# Compare top dishwasher models  
GET /compare?models=Model-D0075,Model-D0023,Model-D0068
```

### **Response Format**

```json
{
  "comparison": [
    {
      "manufacturer": "Samsung", 
      "model_number": "Model-R0029",
      "category": "refrigerators",
      "open_efficiency_score": 99.1,
      "efficiency_rating": "A+",
      "annual_energy_kwh": 303.0,
      "annual_cost_us_average": 50.0,
      "annual_co2_lbs_us_average": 257.6
    },
    {
      "manufacturer": "GE",
      "model_number": "Model-R0051", 
      "category": "refrigerators",
      "open_efficiency_score": 97.0,
      "efficiency_rating": "A+",
      "annual_energy_kwh": 397.2,
      "annual_cost_us_average": 65.5,
      "annual_co2_lbs_us_average": 337.6
    }
  ],
  "models_found": 2,
  "models_requested": 2
}
```

---

## 📊 **Database Statistics**

**Endpoint**: `GET /stats`

**Description**: Get comprehensive database statistics and methodology information.

### **Example Request**

```bash
GET /stats
```

### **Response Format**

```json
{
  "database_info": {
    "total_appliances": 400,
    "categories": {
      "refrigerators": 100,
      "dishwashers": 100, 
      "water_heaters": 100,
      "clothes_washers": 100
    },
    "energy_star_certified": 124,
    "score_distribution": {
      "A+": 52,
      "A": 68,
      "B": 126,
      "C": 118,
      "D": 24,
      "F": 12
    }
  },
  "methodology": {
    "scoring_algorithm": "Absolute performance thresholds",
    "regional_markets": 5,
    "last_updated": "2025-09-14"
  }
}
```

---

## 📂 **Categories**

**Endpoint**: `GET /categories`

**Description**: List all available appliance categories with counts and top performers.

### **Example Request**

```bash
GET /categories
```

### **Response Format**

```json
{
  "categories": [
    {
      "name": "refrigerators",
      "display_name": "Refrigerators", 
      "total_count": 100,
      "energy_star_count": 31,
      "top_performer": {
        "model_number": "Model-R0029",
        "manufacturer": "Samsung",
        "score": 99.1
      }
    }
  ]
}
```

---

## 🌍 **Regional Impact**

**Endpoint**: `GET /regional-impact/{model_number}`

**Description**: Get detailed regional cost and carbon impact variations for a specific appliance.

### **Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model_number` | string | Yes | Appliance model number |

### **Example Request**

```bash
GET /regional-impact/Model-R0029
```

### **Response Format**

```json
{
  "appliance": {
    "manufacturer": "Samsung",
    "model_number": "Model-R0029",
    "category": "refrigerators",
    "open_efficiency_score": 99.1,
    "annual_energy_kwh": 303.0
  },
  "regional_impact": {
    "us_average": {
      "annual_cost": 50.0,
      "annual_co2_lbs": 257.6,
      "electricity_rate_cents_kwh": 16.5,
      "grid_emissions_lbs_co2_kwh": 0.85
    },
    "california": {
      "annual_cost": 73.0,
      "annual_co2_lbs": 136.4,
      "electricity_rate_cents_kwh": 24.1,
      "grid_emissions_lbs_co2_kwh": 0.45
    },
    "texas": {
      "annual_cost": 38.8,
      "annual_co2_lbs": 287.9,
      "electricity_rate_cents_kwh": 12.8,
      "grid_emissions_lbs_co2_kwh": 0.95
    }
  }
}
```

---

## ❌ **Error Handling**

### **Standard Error Response**

```json
{
  "error": "Invalid category. Supported categories: refrigerators, dishwashers, water_heaters, clothes_washers",
  "status_code": 400
}
```

### **Common HTTP Status Codes**

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | Success | Request processed successfully |
| 400 | Bad Request | Invalid parameters or malformed request |
| 404 | Not Found | Requested appliance/category not found |
| 500 | Server Error | Internal processing error |

### **Error Examples**

```bash
# Invalid category
GET /search?category=invalid_category
# → 400 Bad Request

# Model not found  
GET /regional-impact/NonexistentModel
# → 404 Not Found

# Invalid score range
GET /search?min_score=150
# → 400 Bad Request: Score must be between 0 and 100
```

---

## 🚀 **Rate Limiting**

### **Development**
- **No rate limiting** for local development
- All endpoints available without restrictions

### **Production** 
- **1000 requests per hour** per IP address
- **Burst allowance**: 50 requests per minute
- **Headers included** in response:
  - `X-RateLimit-Limit`: Total requests allowed per hour
  - `X-RateLimit-Remaining`: Requests remaining in current hour
  - `X-RateLimit-Reset`: Unix timestamp when limit resets

---

## 🔧 **Development Setup**

### **Start API Server**

```bash
# Install dependencies
pip install -r requirements.txt

# Generate database (if needed)
python scripts/data_pipeline.py

# Start development server
python api/efficiency_api.py

# API available at http://localhost:8080
```

### **Test Endpoints**

```bash
# Test basic functionality
curl "http://localhost:8080/stats"

# Test search functionality  
curl "http://localhost:8080/search?category=refrigerators&limit=3"

# Test comparison
curl "http://localhost:8080/compare?models=Model-R0029,Model-R0051"
```

---

## 📚 **Integration Examples**

### **JavaScript/Frontend**

```javascript
// Search for top-rated refrigerators
async function getTopRefrigerators() {
  const response = await fetch('/search?category=refrigerators&min_score=90&limit=10');
  const data = await response.json();
  return data.appliances;
}

// Compare multiple models
async function compareModels(modelNumbers) {
  const models = modelNumbers.join(',');
  const response = await fetch(`/compare?models=${models}`);
  return await response.json();
}
```

### **Python/Backend**

```python
import requests

# Get database statistics
def get_database_stats():
    response = requests.get('http://localhost:8080/stats')
    return response.json()

# Search for ENERGY STAR dishwashers
def get_energy_star_dishwashers():
    params = {
        'category': 'dishwashers',
        'energy_star': 'true',
        'limit': 20
    }
    response = requests.get('http://localhost:8080/search', params=params)
    return response.json()['appliances']
```

### **cURL/Command Line**

```bash
#!/bin/bash

# Get top performers across all categories
echo "Top Performers by Category:"
for category in refrigerators dishwashers water_heaters clothes_washers; do
  echo "=== $category ==="
  curl -s "http://localhost:8080/top-performers/$category?limit=3" | \
    jq '.appliances[] | "\(.manufacturer) \(.model_number): \(.open_efficiency_score)"'
done
```

---

## 🔗 **Related Documentation**

- **Main README**: [README.md](README.md) - Project overview and quick start
- **Technical Details**: [documentation/README.md](documentation/README.md) - Comprehensive documentation  
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md) - Development guidelines
- **Web Interface**: Access at `http://localhost:8081/` when running locally

---

**API Version**: 1.0  
**Last Updated**: September 14, 2025  
**Compatibility**: All endpoints maintain backward compatibility