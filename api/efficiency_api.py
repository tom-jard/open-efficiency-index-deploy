#!/usr/bin/env python3
"""
Open Efficiency Index - REST API
================================
Flask API for product search and efficiency scoring.
Production-ready deployment with proper error handling.
"""

import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import pandas as pd
from pathlib import Path
import json
import logging
from typing import Dict, List, Optional

# Load environment variables (skip dotenv for serverless)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Skip if dotenv not available in serverless

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS
if os.getenv('ENABLE_CORS', 'true').lower() == 'true':
    CORS(app)

# Database connection with environment-aware path
DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/open_efficiency_index.db')
DB_PATH = Path(__file__).parent.parent / DATABASE_PATH

# Fallback to scripts/data for development
if not DB_PATH.exists():
    DB_PATH = Path(__file__).parent.parent / "scripts" / "data" / "open_efficiency_index.db"
    logger.warning(f"Using fallback database path: {DB_PATH}")

# Additional fallback for serverless (relative to api/)
if not DB_PATH.exists():
    DB_PATH = Path(__file__).parent.parent / "scripts" / "open_efficiency_index.db"
    logger.warning(f"Using serverless fallback database path: {DB_PATH}")

if not DB_PATH.exists():
    logger.error(f"Database not found at {DB_PATH}")
    # In serverless, just log error but don't fail completely
    DB_PATH = None

if DB_PATH:
    logger.info(f"Using database: {DB_PATH}")
else:
    logger.error("No database available - API will return errors")

def get_db_connection():
    """Get database connection with error handling."""
    if not DB_PATH:
        raise FileNotFoundError("Database not available in serverless environment")
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise

def safe_execute_query(query: str, params: tuple = ()) -> List[Dict]:
    """Execute database query with proper error handling."""
    try:
        conn = get_db_connection()
        cursor = conn.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    except Exception as e:
        logger.error(f"Query execution failed: {query} - {e}")
        raise

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested resource does not exist'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

@app.route('/')
def index():
    """API documentation endpoint."""
    return jsonify({
        "name": "Open Efficiency Index API",
        "version": "1.0.0",
        "description": "Alternative to ENERGY STAR with transparent, regional-aware efficiency scoring",
        "endpoints": {
            "/search": "Search appliances by category, manufacturer, or model",
            "/categories": "List all appliance categories",
            "/top-performers/{category}": "Get top-rated appliances by category",
            "/compare": "Compare multiple appliances",
            "/regional-impact/{appliance_id}": "Get regional cost/carbon impact",
            "/stats": "Get database statistics"
        },
        "data_sources": [
            "DOE Compliance Certification Database",
            "EPA Emissions Factors",
            "EIA Regional Electricity Pricing"
        ]
    })

@app.route('/categories')
def get_categories():
    """Get all appliance categories with statistics."""
    conn = get_db_connection()
    
    categories = {}
    tables = ['refrigerators_scored', 'dishwashers_scored', 'water_heaters_scored', 'clothes_washers_scored']
    
    for table in tables:
        try:
            cursor = conn.execute(f"""
                SELECT 
                    COUNT(*) as total_models,
                    AVG(open_efficiency_score) as avg_score,
                    COUNT(CASE WHEN energy_star_certified = 1 THEN 1 END) as energy_star_count
                FROM {table}
            """)
            stats = cursor.fetchone()
            
            category_name = table.replace('_scored', '')
            categories[category_name] = {
                'total_models': stats['total_models'],
                'average_score': round(stats['avg_score'], 1),
                'energy_star_percentage': round((stats['energy_star_count'] / stats['total_models']) * 100, 1),
                'api_endpoint': f'/search?category={category_name}'
            }
        except:
            pass
    
    conn.close()
    return jsonify(categories)

@app.route('/search')
def search_appliances():
    """Search appliances with filters."""
    category = request.args.get('category')
    manufacturer = request.args.get('manufacturer') or request.args.get('brand')  # Support both 'manufacturer' and 'brand'
    model = request.args.get('model')
    min_score = request.args.get('min_score', type=float) or request.args.get('min_efficiency', type=float) or 0  # Support both parameters
    max_score = request.args.get('max_score', type=float, default=100)
    energy_star_only = request.args.get('energy_star', type=bool, default=False)
    limit = request.args.get('limit', type=int, default=50)
    
    if not category:
        return jsonify({"error": "Category parameter required"}), 400
    
    conn = get_db_connection()
    table_name = f"{category}_scored"
    
    # Build query
    conditions = ["1=1"]
    params = []
    
    if manufacturer:
        conditions.append("manufacturer LIKE ?")
        params.append(f"%{manufacturer}%")
        
    if model:
        conditions.append("model_number LIKE ?")
        params.append(f"%{model}%")
        
    conditions.append("open_efficiency_score BETWEEN ? AND ?")
    params.extend([min_score, max_score])
    
    if energy_star_only:
        conditions.append("energy_star_certified = 1")
    
    # Check if CO2 column exists for this table
    check_conn = get_db_connection()
    cursor = check_conn.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    has_co2_column = 'annual_co2_lbs_us_average' in columns
    check_conn.close()
    
    # Build query with conditional CO2 column
    co2_select = "annual_co2_lbs_us_average" if has_co2_column else "0 as annual_co2_lbs_us_average"
    
    query = f"""
        SELECT 
            manufacturer,
            model_number,
            open_efficiency_score,
            efficiency_rating,
            energy_star_certified,
            annual_cost_us_average,
            annual_energy_kwh,
            {co2_select}
        FROM {table_name}
        WHERE {' AND '.join(conditions)}
        ORDER BY open_efficiency_score DESC
        LIMIT ?
    """
    params.append(limit)
    
    try:
        cursor = conn.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        
        return jsonify({
            "category": category,
            "total_results": len(results),
            "filters": {
                "manufacturer": manufacturer,
                "model": model,
                "min_score": min_score,
                "max_score": max_score,
                "energy_star_only": energy_star_only
            },
            "appliances": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/top-performers/<category>')
def get_top_performers(category):
    """Get top-rated appliances by category."""
    limit = request.args.get('limit', type=int, default=20)
    
    conn = get_db_connection()
    table_name = f"{category}_scored"
    
    # Check if CO2 column exists for this table
    check_conn = get_db_connection()
    cursor = check_conn.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    has_co2_column = 'annual_co2_lbs_us_average' in columns
    check_conn.close()
    
    # Build query with conditional CO2 column
    co2_select = "annual_co2_lbs_us_average" if has_co2_column else "0 as annual_co2_lbs_us_average"
    
    try:
        cursor = conn.execute(f"""
            SELECT 
                manufacturer,
                model_number,
                open_efficiency_score,
                efficiency_rating,
                energy_star_certified,
                annual_cost_us_average,
                annual_energy_kwh,
                {co2_select}
            FROM {table_name}
            ORDER BY open_efficiency_score DESC
            LIMIT ?
        """, (limit,))
        
        results = [dict(row) for row in cursor.fetchall()]
        
        return jsonify({
            "category": category,
            "top_performers": results,
            "methodology": {
                "scoring": "Weighted composite: 40% efficiency + 30% cost savings + 30% carbon reduction",
                "baseline": "Percentile ranking within category",
                "regional_factors": "US average electricity pricing and grid emissions"
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/compare')
def compare_appliances():
    """Compare multiple appliances."""
    models = request.args.getlist('model')  # e.g., ?model=Model-R0001&model=Model-R0002
    
    if len(models) < 2:
        return jsonify({"error": "At least 2 models required for comparison"}), 400
    
    if len(models) > 5:
        return jsonify({"error": "Maximum 5 models for comparison"}), 400
    
    conn = get_db_connection()
    results = []
    
    # Search across all tables
    tables = ['refrigerators_scored', 'dishwashers_scored', 'water_heaters_scored', 'clothes_washers_scored']
    
    for model in models:
        found = False
        for table in tables:
            try:
                cursor = conn.execute(f"""
                    SELECT 
                        '{table.replace('_scored', '')}' as category,
                        manufacturer,
                        model_number,
                        open_efficiency_score,
                        efficiency_rating,
                        energy_star_certified,
                        annual_cost_us_average,
                        annual_energy_kwh,
                        annual_co2_lbs_us_average
                    FROM {table}
                    WHERE model_number = ?
                """, (model,))
                
                result = cursor.fetchone()
                if result:
                    results.append(dict(result))
                    found = True
                    break
            except:
                continue
        
        if not found:
            results.append({"model_number": model, "error": "Not found"})
    
    conn.close()
    
    # Calculate comparison insights
    valid_results = [r for r in results if 'error' not in r]
    if len(valid_results) >= 2:
        scores = [r['open_efficiency_score'] for r in valid_results]
        best_model = max(valid_results, key=lambda x: x['open_efficiency_score'])
        worst_model = min(valid_results, key=lambda x: x['open_efficiency_score'])
        
        comparison_insights = {
            "score_range": f"{min(scores):.1f} - {max(scores):.1f}",
            "best_performer": f"{best_model['manufacturer']} {best_model['model_number']} ({best_model['open_efficiency_score']:.1f})",
            "potential_savings": f"${worst_model['annual_cost_us_average'] - best_model['annual_cost_us_average']:.0f}/year by choosing the most efficient"
        }
    else:
        comparison_insights = {}
    
    return jsonify({
        "comparison": results,
        "insights": comparison_insights
    })

@app.route('/regional-impact/<model_number>')
def get_regional_impact(model_number):
    """Get regional cost and carbon impact for specific appliance."""
    conn = get_db_connection()
    
    # Search across all tables
    tables = ['refrigerators_scored', 'dishwashers_scored', 'water_heaters_scored', 'clothes_washers_scored']
    
    for table in tables:
        try:
            cursor = conn.execute(f"""
                SELECT 
                    manufacturer,
                    model_number,
                    annual_cost_us_average,
                    annual_cost_california,
                    annual_cost_texas,
                    annual_cost_new_york,
                    annual_cost_florida,
                    annual_co2_lbs_us_average,
                    annual_co2_lbs_california,
                    annual_co2_lbs_texas,
                    annual_co2_lbs_new_york,
                    annual_co2_lbs_florida
                FROM {table}
                WHERE model_number = ?
            """, (model_number,))
            
            result = cursor.fetchone()
            if result:
                data = dict(result)
                
                # Organize regional data
                regions = {
                    'US_Average': {
                        'annual_cost': data['annual_cost_us_average'],
                        'annual_co2_lbs': data['annual_co2_lbs_us_average']
                    },
                    'California': {
                        'annual_cost': data['annual_cost_california'],
                        'annual_co2_lbs': data['annual_co2_lbs_california']
                    },
                    'Texas': {
                        'annual_cost': data['annual_cost_texas'],
                        'annual_co2_lbs': data['annual_co2_lbs_texas']
                    },
                    'New_York': {
                        'annual_cost': data['annual_cost_new_york'],
                        'annual_co2_lbs': data['annual_co2_lbs_new_york']
                    },
                    'Florida': {
                        'annual_cost': data['annual_cost_florida'],
                        'annual_co2_lbs': data['annual_co2_lbs_florida']
                    }
                }
                
                conn.close()
                return jsonify({
                    "appliance": {
                        "manufacturer": data['manufacturer'],
                        "model": data['model_number']
                    },
                    "regional_impact": regions,
                    "insights": {
                        "highest_cost_region": max(regions.keys(), key=lambda x: regions[x]['annual_cost']),
                        "lowest_cost_region": min(regions.keys(), key=lambda x: regions[x]['annual_cost']),
                        "cost_range": f"${min(r['annual_cost'] for r in regions.values()):.0f} - ${max(r['annual_cost'] for r in regions.values()):.0f}/year"
                    }
                })
        except:
            continue
    
    conn.close()
    return jsonify({"error": "Model not found"}), 404

@app.route('/stats')
def get_database_stats():
    """Get overall database statistics."""
    conn = get_db_connection()
    
    stats = {}
    tables = ['refrigerators_scored', 'dishwashers_scored', 'water_heaters_scored', 'clothes_washers_scored']
    
    total_models = 0
    total_energy_star = 0
    
    for table in tables:
        try:
            cursor = conn.execute(f"""
                SELECT 
                    COUNT(*) as count,
                    AVG(open_efficiency_score) as avg_score,
                    COUNT(CASE WHEN energy_star_certified = 1 THEN 1 END) as energy_star_count
                FROM {table}
            """)
            result = cursor.fetchone()
            
            category = table.replace('_scored', '')
            stats[category] = {
                'total_models': result['count'],
                'average_score': round(result['avg_score'], 1),
                'energy_star_models': result['energy_star_count']
            }
            
            total_models += result['count']
            total_energy_star += result['energy_star_count']
        except:
            pass
    
    conn.close()
    
    return jsonify({
        "database_stats": {
            "total_models": total_models,
            "total_energy_star_models": total_energy_star,
            "energy_star_percentage": round((total_energy_star / total_models) * 100, 1),
            "categories": len(stats)
        },
        "by_category": stats,
        "methodology": {
            "scoring_algorithm": "Weighted composite: 40% efficiency + 30% cost + 30% carbon",
            "regional_factors": "Electricity pricing and grid carbon intensity by state",
            "data_sources": ["DOE Compliance Certification", "EPA Emissions", "EIA Pricing"]
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)