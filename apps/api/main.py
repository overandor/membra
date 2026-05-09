from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, inventory, marketplace

app = FastAPI(
    title="MEMBRA API",
    description="A marketplace you talk to. Chat-first AI local commerce platform.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api")
app.include_router(inventory.router, prefix="/api")
app.include_router(marketplace.router, prefix="/api")

@app.get("/")
def root():
    return {
        "name": "MEMBRA API",
        "tagline": "A marketplace you talk to.",
        "status": "running",
        "version": "1.0.0",
    }

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}
