# FRA WebGIS - Railway Deployment Guide

This Flask application with integrated React frontend is ready for deployment on Railway.

## Pre-deployment Checklist ✅

- [x] Flask app configured to use environment PORT
- [x] Procfile created with Gunicorn
- [x] requirements.txt updated with all dependencies
- [x] railway.json configuration added
- [x] Runtime specified (Python 3.11)
- [x] Production-ready error handling
- [x] Static files properly configured

## Files Added/Modified for Deployment

1. **Procfile** - Tells Railway how to start the app
2. **railway.json** - Railway-specific configuration
3. **runtime.txt** - Specifies Python version
4. **requirements.txt** - Updated with gunicorn
5. **app.py** - Modified to use environment PORT and production settings
6. **.gitignore** - Excludes unnecessary files from deployment

## Local Testing

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Test with gunicorn (production server)
gunicorn --bind 0.0.0.0:5001 app:app

# Or test with development server
python app.py
```

## Railway Deployment Steps

See RAILWAY_DEPLOYMENT.md for detailed instructions.

## Environment Variables (if needed)

Set these in Railway dashboard if your app requires them:
- DATABASE_URL (if using database)
- Any API keys or secrets

## Port Configuration

The app automatically detects Railway's PORT environment variable and falls back to 5001 for local development.

## Static Files

React build files are served from the `react_build/` directory by Flask.