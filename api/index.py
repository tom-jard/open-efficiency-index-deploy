from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Database path setup for Vercel
def get_db_path():
    # Try different possible locations
    possible_paths = [
        Path(__file__).parent.parent / "data" / "open_efficiency_index.db",
        Path(__file__).parent.parent / "scripts" / "open_efficiency_index.db",
        Path(__file__).parent.parent / "scripts" / "data" / "open_efficiency_index.db"
    ]
    
    for path in possible_paths:
        if path.exists():
            return str(path)
    
    return None

def get_db_connection():
    db_path = get_db_path()
    if not db_path:
        raise FileNotFoundError("Database not found")
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def root():
    return jsonify({
        "status": "OK",
        "service": "Open Efficiency Index API",
        "message": "API is running"
    })

@app.route('/search')
def search():
    try:
        category = request.args.get('category', '')
        manufacturer = request.args.get('manufacturer') or request.args.get('brand', '')
        min_score = float(request.args.get('min_score', 0) or request.args.get('min_efficiency', 0))
        limit = int(request.args.get('limit', 20))
        
        if not category:
            return jsonify({"error": "Category is required"}), 400
            
        conn = get_db_connection()
        table_name = f"{category}_scored"
        
        # Build query
        query = f"SELECT * FROM {table_name} WHERE 1=1"
        params = []
        
        if manufacturer:
            query += " AND manufacturer LIKE ?"
            params.append(f"%{manufacturer}%")
            
        if min_score > 0:
            query += " AND open_efficiency_score >= ?"
            params.append(min_score)
            
        query += " ORDER BY open_efficiency_score DESC LIMIT ?"
        params.append(limit)
        
        cursor = conn.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({
            "category": category,
            "total_results": len(results),
            "appliances": results
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stats')
def stats():
    try:
        conn = get_db_connection()
        
        # Get basic stats
        categories = ['refrigerators', 'dishwashers', 'clothes_washers', 'water_heaters']
        stats = {}
        total_models = 0
        
        for category in categories:
            try:
                cursor = conn.execute(f"SELECT COUNT(*) as count FROM {category}_scored")
                count = cursor.fetchone()['count']
                stats[category] = count
                total_models += count
            except:
                stats[category] = 0
        
        conn.close()
        
        return jsonify({
            "database_stats": {
                "total_models": total_models,
                "categories": len([c for c in stats.values() if c > 0])
            },
            "by_category": stats
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel serverless function handler
def handler(request, context):
    return app(request.environ, lambda status, headers: None)

# For local development
if __name__ == '__main__':
    app.run(debug=True)