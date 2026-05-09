from fastapi import FastAPI
from app.routers import camera_sessions

app = FastAPI(
    title="MEMBRA API",
    description="A marketplace you talk to. Chat-first AI local commerce platform.",
    version="0.1.0",
)

app.include_router(camera_sessions.router, prefix="/api")

@app.get("/")
def root():
    return {
        "name": "MEMBRA API",
        "tagline": "A marketplace you talk to.",
        "status": "running",
    }

@app.get("/health")
def health():
    return {"status": "ok"}
