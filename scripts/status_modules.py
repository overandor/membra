"""Print MEMBRA module status from modules/registry.json.

This is intentionally simple and Replit-friendly. It reports registered modules,
expected local paths, default ports, and health paths.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "modules" / "registry.json"


def main() -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    print(f"MEMBRA OS version: {data['membra_os_version']}")
    print(data["doctrine"])
    print()
    for module in sorted(data["modules"], key=lambda item: item["priority"]):
        path = ROOT / module["local_path"]
        exists = "present" if path.exists() else "missing"
        port = module.get("default_port") or "n/a"
        health = module.get("health_path") or "n/a"
        print(f"{module['priority']:02d}. {module['id']:<24} {exists:<8} port={port:<5} health={health:<14} {module['repo']}")


if __name__ == "__main__":
    main()
