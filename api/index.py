from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "name": "Open Efficiency Index API",
            "version": "1.0.0",
            "description": "Alternative to ENERGY STAR with transparent, regional-aware efficiency scoring",
            "endpoints": {
                "/api/search": "Search appliances by category, manufacturer, or model",
                "/api/categories": "List all appliance categories", 
                "/api/stats": "Get database statistics"
            },
            "data_sources": [
                "DOE Compliance Certification Database",
                "EPA Emissions Factors", 
                "EIA Regional Electricity Pricing"
            ],
            "deployment": "Vercel Serverless - WORKING!"
        }
        
        self.wfile.write(json.dumps(response).encode())