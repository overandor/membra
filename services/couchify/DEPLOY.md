# Couchify — Deployment Guide

## Quick Deploy Options

### Option 1: Render (Recommended — Free Tier)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → "New Web Service"
3. Connect your GitHub repo
4. Render will auto-detect `render.yaml` and configure everything
5. Add environment variables in Render dashboard:
   - `HUGGINGFACE_TOKEN` — your HF inference token
   - `STRIPE_SECRET_KEY` — Stripe secret (optional, for payments)
   - `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER` — for SMS (optional)
5. Deploy

### Option 2: Docker (Any Platform)

```bash
docker build -t couchify .
docker run -p 8000:8000 -e PORT=8000 couchify
```

For cloud platforms that inject `$PORT`:
```bash
docker run -p 8000:$PORT -e PORT=$PORT couchify
```

### Option 3: Railway

1. Push to GitHub
2. Go to [railway.app](https://railway.app) → "New Project" → "Deploy from GitHub repo"
3. Add environment variables in Railway dashboard
4. Railway auto-detects Dockerfile

### Option 4: Vercel (Serverless — Requires Restructure)

FastAPI can run on Vercel using ASGI adapters, but this requires restructuring into `/api` routes. Not recommended for this architecture.

## Environment Variables

Copy `.env.example` to `.env` and fill in:

| Variable | Required | Description |
|----------|----------|-------------|
| `HUGGINGFACE_TOKEN` | Yes | Hugging Face API token for LLM inference |
| `LLM_MODEL` | No | Model to use (default: `meta-llama/Llama-3.2-3B-Instruct`) |
| `STRIPE_SECRET_KEY` | No | For payment processing |
| `STRIPE_PUBLISHABLE_KEY` | No | For payment processing |
| `TWILIO_ACCOUNT_SID` | No | For SMS verification |
| `TWILIO_AUTH_TOKEN` | No | For SMS verification |
| `TWILIO_PHONE_NUMBER` | No | For SMS verification |
| `ENVIRONMENT` | No | `development` or `production` |

## Post-Deploy Verification

```bash
curl https://your-app-url.com/health
curl https://your-app-url.com/stats
```

## Architecture

- **Frontend**: Static HTML/JS in `/static/chat.html`
- **Backend**: FastAPI (`api_v2.py`) with tool-calling orchestrator
- **LLM**: Hugging Face Inference API (fallback to local Ollama)
- **Payments**: Stripe (optional)
- **SMS**: Twilio (optional)
