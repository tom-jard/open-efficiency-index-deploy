const { list, head } = require('@vercel/blob');

// Cache for blob data to avoid repeated fetches
const cache = new Map();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

async function fetchFromBlob(path) {
    const cacheKey = path;
    const cached = cache.get(cacheKey);
    
    if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
        return cached.data;
    }
    
    try {
        const response = await fetch(`https://blob.vercel-storage.com/appliances/${path}`);
        if (!response.ok) {
            throw new Error(`Failed to fetch ${path}: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Cache the result
        cache.set(cacheKey, {
            data,
            timestamp: Date.now()
        });
        
        return data;
    } catch (error) {
        console.error(`Error fetching ${path}:`, error);
        throw error;
    }
}

// API route handlers
export default async function handler(req, res) {
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
                message: 'Powered by Vercel Blob Storage',
                endpoints: {
                    '/search': 'Search appliances',
                    '/stats': 'Database statistics'
                }
            });
        }
        
        if (path === 'stats') {
            // Stats endpoint
            const stats = await fetchFromBlob('stats.json');
            return res.json(stats);
        }
        
        if (path === 'search') {
            // Search endpoint
            const { category, manufacturer, brand, min_score, min_efficiency, limit = 20 } = req.query;
            
            if (!category) {
                return res.status(400).json({ error: 'Category is required' });
            }
            
            // Fetch category data from blob
            const appliances = await fetchFromBlob(`${category}.json`);
            
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
}