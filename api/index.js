const { createServer } = require('http')
const { parse } = require('url')

const server = createServer((req, res) => {
  const { pathname } = parse(req.url, true)
  
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*')
  res.setHeader('Content-Type', 'application/json')
  
  if (pathname === '/api/stats') {
    // Mock database stats for now
    const response = {
      status: "API Working!",
      database_stats: {
        total_models: 400,
        total_energy_star_models: 320,
        energy_star_percentage: 80.0,
        categories: 4
      },
      test_deployment: "SUCCESS - Vercel Node.js deployment working!",
      methodology: {
        scoring_algorithm: "Weighted composite: 40% efficiency + 30% cost + 30% carbon",
        regional_factors: "Electricity pricing and grid carbon intensity by state",
        data_sources: ["DOE Compliance Certification", "EPA Emissions", "EIA Pricing"]
      }
    }
    res.end(JSON.stringify(response))
  } else if (pathname === '/api' || pathname === '/api/') {
    const response = {
      name: "Open Efficiency Index API",
      version: "1.0.0",
      description: "Alternative to ENERGY STAR with transparent, regional-aware efficiency scoring",
      endpoints: {
        "/api/stats": "Get database statistics"
      },
      deployment: "Vercel Node.js - WORKING!"
    }
    res.end(JSON.stringify(response))
  } else {
    res.statusCode = 404
    res.end(JSON.stringify({ error: "Not found" }))
  }
})

module.exports = server