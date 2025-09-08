from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Test response without database for now
        response = {
            "status": "API Working!",
            "database_stats": {
                "total_models": 400,
                "total_energy_star_models": 320,
                "energy_star_percentage": 80.0,
                "categories": 4
            },
            "test_deployment": "SUCCESS - Vercel deployment working!",
            "methodology": {
                "scoring_algorithm": "Weighted composite: 40% efficiency + 30% cost + 30% carbon",
                "regional_factors": "Electricity pricing and grid carbon intensity by state",
                "data_sources": ["DOE Compliance Certification", "EPA Emissions", "EIA Pricing"]
            }
        }
        
        self.wfile.write(json.dumps(response).encode())