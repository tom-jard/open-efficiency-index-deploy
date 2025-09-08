#!/usr/bin/env python3
"""
Statistics API endpoint - Get overall database statistics.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from .db_utils import get_db_connection

app = Flask(__name__)
CORS(app)

def handler(request):
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
        except Exception as e:
            stats[table.replace('_scored', '')] = {'error': str(e)}
    
    conn.close()
    
    return jsonify({
        "database_stats": {
            "total_models": total_models,
            "total_energy_star_models": total_energy_star,
            "energy_star_percentage": round((total_energy_star / total_models) * 100, 1) if total_models > 0 else 0,
            "categories": len([s for s in stats.values() if 'error' not in s])
        },
        "by_category": stats,
        "methodology": {
            "scoring_algorithm": "Weighted composite: 40% efficiency + 30% cost + 30% carbon",
            "regional_factors": "Electricity pricing and grid carbon intensity by state",
            "data_sources": ["DOE Compliance Certification", "EPA Emissions", "EIA Pricing"]
        }
    })