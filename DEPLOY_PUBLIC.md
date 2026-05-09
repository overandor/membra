# Deploy MEMBRA API to Get Public Links

## Quick Deploy to Railway (Web Interface - No CLI Required)

1. **Go to Railway:** https://railway.app/new
2. **Click:** "Deploy from GitHub repo"
3. **Select:** `overandor/membra` repository
4. **Railway will auto-detect:** Python/FastAPI
5. **Add Environment Variables:**
   ```
   DEBUG=False
   SECRET_KEY=your-random-secret-key-here
   DATABASE_URL=postgresql://user:password@host:5432/membra
   REDIS_URL=redis://host:6379/0
   ```
6. **Click:** "Deploy"
7. **Wait ~2 minutes** for deployment to complete
8. **Your public links will appear:**
   - API: `https://your-project-name.railway.app`
   - Swagger UI: `https://your-project-name.railway.app/docs`
   - ReDoc: `https://your-project-name.railway.app/redoc`
   - Custom UI: `https://your-project-name.railway.app/docs-ui`
   - OpenAPI Spec: `https://your-project-name.railway.app/openapi.json`

## Alternative: Render (Web Interface)

1. **Go to Render:** https://render.com
2. **Click:** "New +" → "Web Service"
3. **Connect:** GitHub repository `overandor/membra`
4. **Configure:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
5. **Add Environment Variables** (same as above)
6. **Click:** "Create Web Service"
7. **Your public links will appear after deployment**

## Current Status

✅ Code pushed to GitHub: https://github.com/overandor/membra
✅ Deployment configurations ready (Dockerfile, railway.json, render.yaml)
✅ OpenAPI spec saved
✅ Custom docs UI created

**Next Step:** Go to https://railway.app/new and deploy from GitHub to get public links.
