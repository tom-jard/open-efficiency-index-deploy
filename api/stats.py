from http.server import BaseHTTPRequestHandler
import json
import sqlite3
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        try:
            # Database connection
            db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'open_efficiency_index.db')
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            
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
            
            response = {
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
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {"error": str(e)}
            self.wfile.write(json.dumps(error_response).encode())