"""
MEMBRA Main Application
A marketplace you talk to.

Chat-first AI local commerce platform that turns household inventory,
post-purchase goods, spaces, skills, storage, delivery capacity, and
local demand into permissioned neighborhood commerce.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
import os

# Import routers
from api.membra_endpoints import router as relay_router
from api.chat import router as chat_router
from api.inventory import router as inventory_router
from api.marketplace import router as marketplace_router
from api.hero import router as hero_router
from api.split_order import router as split_order_router
from api.split_pulse import router as split_pulse_router
from api.wallet import router as wallet_router
from api.scan import router as scan_router
from api.price import router as price_router
from api.trust import router as trust_router
from api.camera import router as camera_router

# Future routers to be implemented:
# from api.demand import router as demand_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    print("🚀 MEMBRA starting up...")
    print("📦 A marketplace you talk to")
    print("🏠 Need nearby. Earn locally.")
    yield
    # Shutdown
    print("🛑 MEMBRA shutting down...")


app = FastAPI(
    title="MEMBRA API",
    description="A marketplace you talk to. Chat-first AI local commerce platform.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(relay_router, prefix="/api/v1", tags=["Relay"])
app.include_router(chat_router, prefix="/api/v1", tags=["Chat"])
app.include_router(inventory_router, prefix="/api/v1", tags=["Inventory"])
app.include_router(marketplace_router, prefix="/api/v1", tags=["Marketplace"])
app.include_router(hero_router, prefix="/api/v1", tags=["Hero"])
app.include_router(split_order_router, prefix="/api/v1", tags=["SplitOrder"])
app.include_router(split_pulse_router, prefix="/api/v1", tags=["SplitPulse"])
app.include_router(wallet_router, prefix="/api/v1", tags=["Wallet"])
app.include_router(scan_router, prefix="/api/v1", tags=["Scan"])
app.include_router(price_router, prefix="/api/v1", tags=["Price"])
app.include_router(trust_router, prefix="/api/v1", tags=["Trust"])
app.include_router(camera_router, prefix="/api/v1", tags=["CameraLink"])

# Future routers:
# app.include_router(demand_router, prefix="/api/v1", tags=["Demand"])

# Mount static files for custom documentation UI
docs_path = os.path.join(os.path.dirname(__file__), "..", "docs-ui")
if os.path.exists(docs_path):
    app.mount("/docs-ui", StaticFiles(directory=docs_path), name="docs-ui")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "MEMBRA",
        "tagline": "A marketplace you talk to",
        "description": "Need nearby. Earn locally. Turn assets into access.",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
        "docs_ui": "/docs-ui"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "membra-api"}


@app.get("/api/v1")
async def api_v1():
    """API v1 information"""
    return {
        "version": "v1",
        "endpoints": {
            "chat": "/api/v1/chat",
            "inventory": "/api/v1/inventory",
            "marketplace": "/api/v1/marketplace",
            "hero": "/api/v1/hero",
            "relay": "/api/v1/relay",
            "split_order": "/api/v1/split_order",
            "split_pulse": "/api/v1/split_pulse",
            "wallet": "/api/v1/wallet",
            "scan": "/api/v1/scan",
            "price": "/api/v1/price",
            "trust": "/api/v1/trust",
            "camera": "/api/v1/camera-sessions",
            # Future endpoints:
            # "demand": "/api/v1/demand",
        },
    }


if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
