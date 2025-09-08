#!/usr/bin/env python3
"""
Open Efficiency Index - Serverless API Index
============================================
Main API endpoint for Vercel serverless deployment.
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

def handler(request):
    """Main API documentation endpoint."""
    return jsonify({
        "name": "Open Efficiency Index API",
        "version": "1.0.0",
        "description": "Alternative to ENERGY STAR with transparent, regional-aware efficiency scoring",
        "endpoints": {
            "/api/search": "Search appliances by category, manufacturer, or model",
            "/api/categories": "List all appliance categories", 
            "/api/top-performers/{category}": "Get top-rated appliances by category",
            "/api/compare": "Compare multiple appliances",
            "/api/regional-impact/{appliance_id}": "Get regional cost/carbon impact",
            "/api/stats": "Get database statistics"
        },
        "data_sources": [
            "DOE Compliance Certification Database",
            "EPA Emissions Factors", 
            "EIA Regional Electricity Pricing"
        ],
        "deployment": "Vercel Serverless"
    })