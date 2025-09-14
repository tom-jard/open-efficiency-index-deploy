#!/usr/bin/env python3
"""
Search API endpoint - Search appliances with filters.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from .db_utils import get_db_connection

app = Flask(__name__)
CORS(app)

def handler(request):
    """Search appliances with filters."""
    # Parse query parameters
    args = request.args if hasattr(request, 'args') else {}
    
    category = args.get('category')
    manufacturer = args.get('manufacturer')
    model = args.get('model')
    min_score = float(args.get('min_score', 0))
    max_score = float(args.get('max_score', 100))
    energy_star_only = args.get('energy_star', '').lower() == 'true'
    limit = int(args.get('limit', 50))
    
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
    try:
        cursor = conn.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cursor.fetchall()]
        has_co2_column = 'annual_co2_lbs_us_average' in columns
    except:
        has_co2_column = False
    
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