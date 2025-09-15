#!/usr/bin/env python3
"""
Open Efficiency Index - Serverless API Index
============================================
Main API endpoint for Vercel serverless deployment.
"""

from flask import Flask, jsonify
import os

# Create a simple test app first
app = Flask(__name__)

@app.route('/')
def root():
    return jsonify({
        "status": "OK",
        "service": "Open Efficiency Index API",
        "version": "1.0.0",
        "message": "API is running in serverless mode"
    })

@app.route('/test')
def test():
    return jsonify({"test": "working"})

# Try to import main app if available
try:
    from efficiency_api import app as main_app
    # Register routes from main app
    app.register_blueprint(main_app, url_prefix='/main')
except Exception as e:
    @app.route('/error')
    def error():
        return jsonify({"error": f"Failed to load main app: {str(e)}"})

# Export for Vercel
handler = app