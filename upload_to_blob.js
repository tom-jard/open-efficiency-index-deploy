require('dotenv').config();
const { put } = require('@vercel/blob');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Database path
const dbPath = path.join(__dirname, 'data/open_efficiency_index.db');

// Function to query SQLite and return JSON
function queryDatabase(category) {
    return new Promise((resolve, reject) => {
        const db = new sqlite3.Database(dbPath);
        
        db.all(`SELECT * FROM ${category}_scored ORDER BY open_efficiency_score DESC`, (err, rows) => {
            if (err) {
                reject(err);
            } else {
                resolve(rows);
            }
            db.close();
        });
    });
}

// Upload category data to Blob
async function uploadCategory(category) {
    try {
        console.log(`Exporting ${category}...`);
        const data = await queryDatabase(category);
        
        const { url } = await put(`appliances/${category}.json`, JSON.stringify(data, null, 2), {
            access: 'public',
            contentType: 'application/json'
        });
        
        console.log(`✅ ${category}: ${data.length} appliances → ${url}`);
        return { category, count: data.length, url };
        
    } catch (error) {
        console.error(`❌ Error uploading ${category}:`, error);
        return null;
    }
}

// Upload stats
async function uploadStats() {
    try {
        const categories = ['refrigerators', 'dishwashers', 'clothes_washers', 'water_heaters'];
        const stats = {};
        let totalModels = 0;
        
        for (const category of categories) {
            try {
                const data = await queryDatabase(category);
                stats[category] = data.length;
                totalModels += data.length;
            } catch (error) {
                stats[category] = 0;
            }
        }
        
        const statsData = {
            database_stats: {
                total_models: totalModels,
                categories: Object.values(stats).filter(c => c > 0).length
            },
            by_category: stats
        };
        
        const { url } = await put('appliances/stats.json', JSON.stringify(statsData, null, 2), {
            access: 'public',
            contentType: 'application/json'
        });
        
        console.log(`✅ Stats uploaded → ${url}`);
        return { url, data: statsData };
        
    } catch (error) {
        console.error('❌ Error uploading stats:', error);
        return null;
    }
}

// Main upload function
async function uploadAllData() {
    console.log('🚀 Starting upload to Vercel Blob...\n');
    
    const categories = ['refrigerators', 'dishwashers', 'clothes_washers', 'water_heaters'];
    const results = [];
    
    // Upload each category
    for (const category of categories) {
        const result = await uploadCategory(category);
        if (result) results.push(result);
    }
    
    // Upload stats
    const statsResult = await uploadStats();
    
    console.log('\n📊 Upload Summary:');
    console.log('==================');
    
    results.forEach(r => {
        console.log(`${r.category}: ${r.count} appliances`);
    });
    
    if (statsResult) {
        console.log(`Total: ${statsResult.data.database_stats.total_models} appliances across ${statsResult.data.database_stats.categories} categories`);
    }
    
    console.log('\n✅ All data uploaded to Vercel Blob successfully!');
}

// Run the upload
uploadAllData().catch(console.error);