#!/usr/bin/env python3
"""
Export SQLite database to static JSON files
"""

import sqlite3
import json
from pathlib import Path

# Database path
db_path = Path("data/open_efficiency_index.db")
output_dir = Path("api/data")

def export_category(category):
    """Export a category to JSON file"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    try:
        cursor = conn.execute(f"SELECT * FROM {category}_scored ORDER BY open_efficiency_score DESC")
        results = [dict(row) for row in cursor.fetchall()]
        
        # Save to JSON file
        output_file = output_dir / f"{category}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Exported {len(results)} {category} to {output_file}")
        return len(results)
        
    except Exception as e:
        print(f"Error exporting {category}: {e}")
        return 0
    finally:
        conn.close()

def export_stats():
    """Export database stats"""
    conn = sqlite3.connect(db_path)
    
    categories = ['refrigerators', 'dishwashers', 'clothes_washers', 'water_heaters']
    stats = {}
    total_models = 0
    
    for category in categories:
        try:
            cursor = conn.execute(f"SELECT COUNT(*) as count FROM {category}_scored")
            count = cursor.fetchone()[0]
            stats[category] = count
            total_models += count
        except:
            stats[category] = 0
    
    conn.close()
    
    stats_data = {
        "database_stats": {
            "total_models": total_models,
            "categories": len([c for c in stats.values() if c > 0])
        },
        "by_category": stats
    }
    
    # Save stats
    output_file = output_dir / "stats.json"
    with open(output_file, 'w') as f:
        json.dump(stats_data, f, indent=2)
    
    print(f"Exported stats to {output_file}")
    return stats_data

if __name__ == "__main__":
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Export all categories
    categories = ['refrigerators', 'dishwashers', 'clothes_washers', 'water_heaters']
    
    for category in categories:
        export_category(category)
    
    # Export stats
    export_stats()
    
    print("Export complete!")