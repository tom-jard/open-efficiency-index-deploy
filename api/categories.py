#!/usr/bin/env python3
"""
Categories API endpoint - List all appliance categories with statistics.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from .db_utils import get_db_connection

app = Flask(__name__)
CORS(app)

def handler(request):
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
                'api_endpoint': f'/api/search?category={category_name}'
            }
        except Exception as e:
            categories[table.replace('_scored', '')] = {'error': str(e)}
    
    conn.close()
    return jsonify(categories)