"""Bootstrap MEMBRA modules into a local workspace.

Usage:
    python scripts/bootstrap_modules.py

This script reads modules/registry.json and clones missing repos into their
registered local paths. Existing paths are left untouched.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "modules" / "registry.json"


def run(cmd: list[str]) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=ROOT)


def main() -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    for module in data["modules"]:
        repo = module["repo"]
        local_path = ROOT / module["local_path"]
        if local_path.exists():
            print(f"skip existing {local_path}")
            continue
        local_path.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", repo, str(local_path)])
    print("MEMBRA modules bootstrapped.")


if __name__ == "__main__":
    main()
