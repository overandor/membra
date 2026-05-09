#!/bin/bash

# MEMBRA API Server Deployment Script
# A marketplace you talk to.

echo "🚀 Starting MEMBRA API Server..."
echo "📦 A marketplace you talk to"
echo "🏠 Need nearby. Earn locally."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying .env.example to .env"
    cp .env.example .env
    echo "✅ Please edit .env with your configuration"
fi

# Install dependencies if needed
if [ ! -d ".venv" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the server
echo "🌐 Starting server on http://0.0.0.0:8000"
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
