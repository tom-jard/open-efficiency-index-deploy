#!/usr/bin/env python3
"""
Shared database utilities for Vercel serverless functions.
"""

import sqlite3
import os
from pathlib import Path

def get_db_connection():
    """Get database connection for serverless environment."""
    # In Vercel, look for the database in the project root
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'open_efficiency_index.db')
    if not os.path.exists(db_path):
        # Fallback paths for different deployment scenarios
        fallback_paths = [
            '/tmp/open_efficiency_index.db',
            './data/open_efficiency_index.db',
            '../data/open_efficiency_index.db'
        ]
        for path in fallback_paths:
            if os.path.exists(path):
                db_path = path
                break
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn