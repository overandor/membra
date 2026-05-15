from __future__ import annotations

from .config import CONFIG
from .module_registry import module_summary
from .providers import provider_status



def runtime_status() -> dict:
    modules = module_summary()
    providers = provider_status()

    return {
        "app_env": CONFIG.app_env,
        "app_name": CONFIG.app_name,
        "app_version": CONFIG.app_version,
        "database_path": CONFIG.app_db_path,
        "upload_dir": CONFIG.app_upload_dir,
        "module_count": modules["module_count"],
        "active_module_count": len(modules["active_modules"]),
        "provider_status": providers,
        "dry_run_external_execution": CONFIG.dry_run_external_execution,
    }
