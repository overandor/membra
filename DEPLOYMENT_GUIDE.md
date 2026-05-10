# MEMBRA Deployment Guide - Reimagined LLM UI/UX

## Overview
This guide covers deploying MEMBRA with the new modern chat interface featuring streaming responses, message history, and suggested actions.

## Architecture

MEMBRA is a fullstack application with:
- **Frontend**: Next.js 14 (Typescript/React) with Tailwind CSS
- **Backend**: FastAPI (Python) with async streaming support
- **Database**: PostgreSQL
- **Cache**: Redis (optional)
- **Hosting**: Render.com (recommended) or Railway.com

## Features - New LLM UI/UX

✨ **Modern Chat Interface**
- Message history with persistent state
- Real-time streaming responses
- Suggested actions/quick replies below each response
- Optimized for mobile and desktop
- Dark theme with amber accents

🚀 **Performance**
- Server-side streaming for faster perceived response times
- Optimized component rendering with React 18
- Tailwind CSS for minimal bundle size

🎯 **User Experience**
- One-click suggested actions
- Loading states with animations
- Error handling with fallback responses
- Auto-scroll to latest message

## Local Development

### Prerequisites
- Node.js 18+
- Python 3.10+
- PostgreSQL 14+
- Redis 7+ (optional)

### Setup

1. **Install dependencies**
   ```bash
   # Root dependencies
   npm install
   
   # Web app
   cd apps/web
   npm install
   
   # API
   cd ../../apps/api
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   # API
   cp apps/api/.env.example apps/api/.env.local
   
   # Web
   cp apps/web/.env.example apps/web/.env.local
   ```

3. **Start local services with Docker**
   ```bash
   docker-compose up -d
   ```

   This starts:
   - PostgreSQL on port 5432
   - Redis on port 6379
   - API will run on port 8000

4. **Run development servers**
   ```bash
   # Terminal 1: Web app
   cd apps/web
   npm run dev
   # Opens http://localhost:3000
   
   # Terminal 2: API
   cd apps/api
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the application**
   - Web: http://localhost:3000
   - API Docs: http://localhost:8000/docs
   - Redoc: http://localhost:8000/redoc

## Deployment to Render

### 1. Connect Repository (one-time)
- Go to [Render.com](https://render.com)
- Connect your GitHub repository
- Select `render-new.yaml` for deployment

### 2. Environment Variables

Set these in Render dashboard:

**Web Service (membra-web)**
```
NEXT_PUBLIC_API_URL=https://membra-api.onrender.com
```

**API Service (membra-api)**
```
DATABASE_URL=postgresql://...  (auto-set by Render)
REDIS_URL=...  (auto-set by Render)
OPENAI_API_KEY=sk-...  (if using OpenAI)
DEBUG=false
```

### 3. Deploy

```bash
# Push to main branch
git push origin main

# Render will automatically:
# 1. Build both services
# 2. Migrate database
# 3. Start services
# 4. Point to your domain
```

### 4. Monitor Deployment
- Render Dashboard: View logs and status
- Health check: `https://membra-api.onrender.com/health`
- API Docs: `https://membra-api.onrender.com/docs`

## Deployment to Railway

### 1. Create New Project
```bash
railway init
```

### 2. Add Services
```bash
# Add PostgreSQL
railway add postgres

# Add Redis
railway add redis
```

### 3. Configure
```bash
# Set environment variables
railway variables set NEXT_PUBLIC_API_URL=...
railway variables set OPENAI_API_KEY=...
```

### 4. Deploy
```bash
railway up
```

## Docker Deployment (Local/Self-hosted)

### Build Images

```bash
# Build API image
docker build -t membra-api:latest .

# Build Web image (requires Dockerfile.web)
docker build -t membra-web:latest -f Dockerfile.web apps/web/
```

### Run with Docker Compose

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## API Endpoints (Streaming)

### Chat Endpoint (with streaming)
```
POST /api/v1/chat

Request:
{
  "message": "What items can I rent nearby?",
  "user_id": "user_123"
}

Response: Server-Sent Events (streaming text)
```

### Chat Endpoint (non-streaming)
```
POST /api/v1/chat/ask

Request:
{
  "message": "What items can I rent nearby?",
  "user_id": "user_123"
}

Response (JSON):
{
  "response": "I found 3 items...",
  "suggestions": ["Show me more", "What's the cheapest?"]
}
```

## Performance Optimization

### Frontend
- Next.js: `npm run build` for production build
- CSS: Tailwind CSS with PurgeCSS removes unused styles
- Images: Optimize with Next.js Image component
- Code splitting: Automatic with Next.js

### Backend
- Async endpoints with FastAPI
- Connection pooling for database
- Redis caching for frequent queries
- Streaming responses for perceived performance

### Database
- Indexes on frequently queried columns
- Connection pooling (PgBouncer)
- Query optimization
- Regular VACUUM maintenance

## Monitoring & Logging

### Render Dashboard
- View real-time logs
- Monitor CPU/Memory usage
- Set up alerts
- View deployment history

### Local Logs
```bash
# API logs
docker-compose logs -f membra-api

# Web app logs (in terminal)
npm run dev
```

## Troubleshooting

### Web can't connect to API
- Check API URL in environment: `NEXT_PUBLIC_API_URL`
- Verify API is running: `curl https://membra-api.onrender.com/health`
- Check CORS configuration in API

### Slow responses
- Check database connection: View query logs
- Monitor Redis: `redis-cli`
- Profile with Render analytics

### Database issues
- View Render database logs
- Check migrations: `alembic current`
- Verify connection string: `$DATABASE_URL`

## Scaling

### Vertical Scaling (higher tier)
- Render: Upgrade instance type
- Railway: Increase resource allocation

### Horizontal Scaling
- Use Railway's multi-region deployment
- Implement load balancing (Nginx, HAProxy)
- Database read replicas

## Contributing

1. Create feature branch
2. Make changes to components or API
3. Test locally
4. Push and create PR
5. Deploy to staging first

## Support

- API Documentation: `/docs` (Swagger UI)
- GitHub Issues: Report bugs
- Render Support: For infrastructure issues
