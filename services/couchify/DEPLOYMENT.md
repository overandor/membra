# Couchify Deployment Guide

## Production Deployment to Render

### Prerequisites
- GitHub account
- Render account (free tier available)
- Stripe account (for payments)
- Hugging Face token (optional, for higher LLM rate limits)

### Quick Deploy

1. **Push to GitHub**
```bash
cd /Users/jo/Downloads/booking/booking-concierge
# Create a new GitHub repository and add it as remote
git remote add origin https://github.com/YOUR_USERNAME/couchify.git
git branch -M main
git push -u origin main
```

2. **Deploy to Render**
- Go to https://dashboard.render.com
- Click "New +"
- Select "Web Service"
- Connect your GitHub repository
- Render will automatically detect `render.yaml`
- Click "Deploy"

3. **Configure Environment Variables**
After deployment, add these in Render dashboard:
- `STRIPE_SECRET_KEY`: Your Stripe secret key
- `STRIPE_CONNECT_REDIRECT_URI`: Your deployed URL + `/stripe/connect/callback`
- `HUGGINGFACE_TOKEN`: Your HF token (optional)

### Next.js Frontend Deployment

1. **Deploy to Vercel**
```bash
cd /Users/jo/Downloads/booking/couchify-frontend
vercel
```

2. **Configure Environment Variable**
- `NEXT_PUBLIC_API_URL`: Your deployed Render API URL

### Architecture

**Backend (Render)**
- FastAPI with PostgreSQL database
- LLM integration via Hugging Face (Qwen 2.5-3B)
- Stripe Connect for payments
- Database-backed spaces and bookings

**Frontend (Vercel)**
- Next.js 16 with TypeScript
- Tailwind CSS for styling
- Guest booking flow
- Host dashboard

### API Endpoints

**Database-backed:**
- `GET /api/v2/spaces` - List spaces with filters
- `POST /api/v2/spaces` - Create space (host)
- `POST /api/v2/bookings` - Create booking

**Stripe Connect:**
- `POST /stripe/connect/onboarding` - Start host onboarding
- `GET /stripe/connect/status/{host_id}` - Check onboarding status
- `POST /stripe/payment-intent` - Create payment intent

**Chat/LLM (existing):**
- `POST /chat/session` - Start chat session
- `POST /chat/message` - Send message with LLM
- `POST /chat/analyze-image` - Analyze image for similar spaces

### Monitoring

- Render dashboard: https://dashboard.render.com
- Health check: `https://your-app.onrender.com/health`
- Revenue stats: `https://your-app.onrender.com/revenue`
