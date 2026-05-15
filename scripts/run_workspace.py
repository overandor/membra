"""Run the MEMBRA OS workspace.

Starts the root MEMBRA OS command center on PORT or 8000.
If modules/Membra_kpi is present, also starts the primary KPI product on 8001.

Usage:
    python scripts/run_workspace.py

This is Replit-friendly: one command supervises the root OS app plus the primary
product app when the module has been bootstrapped.
"""
from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
ROOT_PORT = os.getenv("PORT", "8000")
KPI_PORT = os.getenv("MEMBRA_KPI_PORT", "8001")


class ManagedProcess:
    def __init__(self, name: str, command: list[str], cwd: Path, env: dict[str, str] | None = None) -> None:
        self.name = name
        self.command = command
        self.cwd = cwd
        self.env = env or os.environ.copy()
        self.process: subprocess.Popen | None = None

    def start(self) -> None:
        print(f"[membra-os] starting {self.name}: {' '.join(self.command)}", flush=True)
        self.process = subprocess.Popen(self.command, cwd=self.cwd, env=self.env)

    def stop(self) -> None:
        if not self.process or self.process.poll() is not None:
            return
        print(f"[membra-os] stopping {self.name}", flush=True)
        self.process.terminate()

    def poll(self) -> int | None:
        if not self.process:
            return None
        return self.process.poll()


def build_processes() -> list[ManagedProcess]:
    processes = [
        ManagedProcess(
            "membra-root",
            [PYTHON, "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", ROOT_PORT],
            ROOT,
        )
    ]
    kpi_dir = ROOT / "modules" / "Membra_kpi"
    if (kpi_dir / "app.py").exists():
        env = os.environ.copy()
        env.setdefault("PORT", KPI_PORT)
        env.setdefault("APP_BASE_URL", f"http://localhost:{KPI_PORT}")
        env.setdefault("DB_PATH", str(kpi_dir / "data" / "membra.db"))
        env.setdefault("UPLOAD_DIR", str(kpi_dir / "static" / "uploads"))
        migrations = kpi_dir / "scripts" / "apply_migrations.py"
        if migrations.exists():
            print("[membra-os] applying Membra_kpi migrations", flush=True)
            subprocess.run([PYTHON, str(migrations)], cwd=kpi_dir, env=env, check=False)
        processes.append(
            ManagedProcess(
                "membra-kpi",
                [PYTHON, "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", KPI_PORT],
                kpi_dir,
                env,
            )
        )
    else:
        print("[membra-os] modules/Membra_kpi not found. Run: python scripts/bootstrap_modules.py", flush=True)
    return processes


def main() -> None:
    processes = build_processes()
    for process in processes:
        process.start()

    shutdown = False

    def handle_signal(signum, frame):  # type: ignore[no-untyped-def]
        nonlocal shutdown
        shutdown = True
        print(f"[membra-os] received signal {signum}", flush=True)
        for proc in processes:
            proc.stop()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    try:
        while not shutdown:
            for proc in processes:
                code = proc.poll()
                if code is not None:
                    print(f"[membra-os] {proc.name} exited with code {code}", flush=True)
                    shutdown = True
            time.sleep(1)
    finally:
        for proc in processes:
            proc.stop()
        time.sleep(1)


if __name__ == "__main__":
    main()
