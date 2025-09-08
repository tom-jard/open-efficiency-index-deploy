# Open Efficiency Index - Vercel Deployment

## Quick Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/open-efficiency-index)

## Manual Deployment Steps

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy from project root
```bash
cd /Users/thomasjardine/code/personal/celi/capstone
vercel --prod
```

## Project Structure for Vercel

```
/
├── index.html              # Landing page
├── vercel.json            # Vercel configuration
├── requirements.txt       # Python dependencies
├── api/                   # Serverless API functions
│   ├── index.py          # API documentation
│   ├── categories.py     # Category listing
│   ├── search.py         # Appliance search
│   ├── stats.py          # Database statistics
│   └── db_utils.py       # Database utilities
├── web/                   # Static web interface
│   ├── index.html        # Main application
│   └── regional-efficiency-map.html
└── data/                  # Database files
    └── open_efficiency_index.db
```

## API Endpoints (Production)

- `GET /api/` - API documentation
- `GET /api/stats` - Database statistics
- `GET /api/categories` - All appliance categories
- `GET /api/search?category=refrigerators` - Search appliances
- `GET /web/index.html` - Consumer web interface
- `GET /web/regional-efficiency-map.html` - Regional efficiency map

## Environment Variables

No environment variables required - uses local SQLite database.

## Deployment Configuration

- **Runtime**: Python 3.9
- **Build Command**: Automatic (Vercel handles Python dependencies)
- **Output Directory**: Static files served from web/ directory
- **API Functions**: Serverless functions in api/ directory

## Post-Deployment Verification

Test these endpoints after deployment:
1. `https://your-app.vercel.app/` - Landing page
2. `https://your-app.vercel.app/api/stats` - API statistics
3. `https://your-app.vercel.app/web/index.html` - Main application
4. `https://your-app.vercel.app/api/search?category=refrigerators` - Search functionality