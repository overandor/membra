"""MEMBRA OS command center.

Root orchestrator for the MEMBRA repo family. This app does not replace the
specialized modules. It reads modules/registry.json and exposes a Replit-friendly
command-center website and registry APIs.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

APP_NAME = "MEMBRA OS Command Center"
APP_VERSION = "1.0.0"
ROOT = Path(__file__).resolve().parent
REGISTRY_PATH = ROOT / "modules" / "registry.json"
templates = Jinja2Templates(directory=str(ROOT / "templates"))
app = FastAPI(title=APP_NAME, version=APP_VERSION)


def load_registry() -> dict[str, Any]:
    if not REGISTRY_PATH.exists():
        raise HTTPException(status_code=500, detail="modules/registry.json missing")
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def modules() -> list[dict[str, Any]]:
    data = load_registry()
    return sorted(data.get("modules", []), key=lambda item: int(item.get("priority", 999)))


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    mods = modules()
    runtime_services = [m for m in mods if m.get("health_path")]
    primary = next((m["id"] for m in mods if m.get("replit_style") == "primary_deployable"), "n/a")
    return templates.TemplateResponse(
        "os_home.html",
        {
            "request": request,
            "modules": mods,
            "module_count": len(mods),
            "service_count": len(runtime_services),
            "primary_module": primary,
        },
    )


@app.get("/docs", response_class=HTMLResponse)
def docs(request: Request):
    return templates.TemplateResponse("os_docs.html", {"request": request})


@app.get("/api/health")
def health():
    return {"ok": True, "app": APP_NAME, "version": APP_VERSION, "registry_exists": REGISTRY_PATH.exists()}


@app.get("/api/registry")
def registry():
    return load_registry()


@app.get("/api/modules")
def api_modules():
    return {"modules": modules()}


@app.get("/api/modules/{module_id}")
def api_module(module_id: str):
    for module in modules():
        if module.get("id") == module_id:
            return module
    raise HTTPException(status_code=404, detail="module not found")


@app.get("/api/replit-plan")
def replit_plan():
    primary = [m for m in modules() if m.get("replit_style") == "primary_deployable"]
    services = [m for m in modules() if m.get("replit_style") == "service"]
    return {
        "recommended_mode": "single-product first, OS workspace second",
        "primary_deployable": primary,
        "service_modules": services,
        "bootstrap_commands": [
            "python scripts/bootstrap_modules.py",
            "python scripts/status_modules.py",
            "cd modules/Membra_kpi && python scripts/apply_migrations.py && uvicorn app:app --host 0.0.0.0 --port 8001",
        ],
    }


@app.get("/api/health-check-modules")
async def health_check_modules():
    """Best-effort local health check for modules already running on their default ports."""
    results: list[dict[str, Any]] = []
    timeout = httpx.Timeout(2.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        for module in modules():
            port = module.get("default_port")
            health_path = module.get("health_path")
            if not port or not health_path:
                results.append({"id": module["id"], "status": "not_runtime_service"})
                continue
            url = f"http://127.0.0.1:{port}{health_path}"
            try:
                response = await client.get(url)
                results.append({"id": module["id"], "url": url, "status": response.status_code, "ok": response.status_code < 400})
            except Exception as exc:
                results.append({"id": module["id"], "url": url, "status": "offline", "ok": False, "error": str(exc)})
    return {"results": results}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=False)
