from fastapi import FastAPI

app = FastAPI(
    title="MEMBRA API",
    description="A marketplace you talk to. Chat-first AI local commerce platform.",
    version="0.1.0",
)

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
