#!/usr/bin/env python3
"""
Open Efficiency Index - Serverless API Index
============================================
Main API endpoint for Vercel serverless deployment.
Imports the main Flask app from efficiency_api.py
"""

from efficiency_api import app

# Export the Flask app for Vercel
# Vercel will automatically handle WSGI
handler = app