from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REGISTRY_PATH = Path("infra/module-registry.json")



def load_module_registry() -> dict[str, Any]:
    if not REGISTRY_PATH.exists():
        return {"suite": "MEMBRA", "modules": []}

    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))



def list_modules() -> list[dict[str, Any]]:
    registry = load_module_registry()
    return registry.get("modules", [])



def module_summary() -> dict[str, Any]:
    modules = list_modules()

    return {
        "module_count": len(modules),
        "active_modules": [m for m in modules if m.get("status") == "active"],
        "namespace_modules": [m for m in modules if m.get("status") == "namespace"],
    }
