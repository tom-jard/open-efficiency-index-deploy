const fs = require('fs');
const path = require('path');

// Cache for JSON data to avoid repeated file reads
const cache = new Map();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

function loadJsonFile(filename) {
    const cacheKey = filename;
    const cached = cache.get(cacheKey);
    
    if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
        return cached.data;
    }
    
    try {
        const filePath = path.join(__dirname, 'data', filename);
        const fileContent = fs.readFileSync(filePath, 'utf8');
        const data = JSON.parse(fileContent);
        
        // Cache the result
        cache.set(cacheKey, {
            data,
            timestamp: Date.now()
        });
        
        return data;
    } catch (error) {
        console.error(`Error loading ${filename}:`, error);
        throw new Error(`Failed to load ${filename}: ${error.message}`);
    }
}

// API route handler
module.exports = async (req, res) => {
    // Set CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }
    
    if (req.method !== 'GET') {
        return res.status(405).json({ error: 'Method not allowed' });
    }
    
    const { pathname } = new URL(req.url, `http://${req.headers.host}`);
    const path = pathname.replace('/api/', '');
    
    try {
        if (path === '' || path === '/') {
            // Root API endpoint
            return res.json({
                status: 'OK',
                service: 'Open Efficiency Index API',
                message: 'Static JSON API ready',
                endpoints: {
                    '/search': 'Search appliances by category',
                    '/stats': 'Database statistics'
                }
            });
        }
        
        if (path === 'stats') {
            // Stats endpoint
            const stats = loadJsonFile('stats.json');
            return res.json(stats);
        }
        
        if (path === 'search') {
            // Search endpoint
            const { category, manufacturer, brand, min_score, min_efficiency, limit = 20 } = req.query;
            
            if (!category) {
                return res.status(400).json({ error: 'Category is required' });
            }
            
            // Load category data from JSON file
            const appliances = loadJsonFile(`${category}.json`);
            
            if (!appliances || !Array.isArray(appliances)) {
                return res.status(404).json({ error: `Category ${category} not found` });
            }
            
            // Filter results
            let filtered = appliances;
            
            const searchManufacturer = manufacturer || brand;
            if (searchManufacturer) {
                filtered = filtered.filter(app => 
                    app.manufacturer && app.manufacturer.toLowerCase().includes(searchManufacturer.toLowerCase())
                );
            }
            
            const minScore = parseFloat(min_score || min_efficiency || 0);
            if (minScore > 0) {
                filtered = filtered.filter(app => 
                    app.open_efficiency_score && app.open_efficiency_score >= minScore
                );
            }
            
            // Limit results
            const limitNum = parseInt(limit);
            const results = filtered.slice(0, limitNum);
            
            return res.json({
                category,
                total_results: results.length,
                filters: {
                    manufacturer: searchManufacturer,
                    min_score: minScore
                },
                appliances: results
            });
        }
        
        // Unknown endpoint
        return res.status(404).json({ error: 'Endpoint not found' });
        
    } catch (error) {
        console.error('API Error:', error);
        return res.status(500).json({ 
            error: 'Internal server error',
            message: error.message
        });
    }
};