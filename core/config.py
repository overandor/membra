from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(slots=True)
class RuntimeConfig:
    app_env: str
    app_name: str
    app_version: str
    app_db_path: str
    app_upload_dir: str
    llm_provider: str
    groq_base_url: str
    groq_model: str
    ollama_base_url: str
    ollama_model: str
    object_storage_provider: str
    queue_provider: str
    metrics_enabled: bool
    allow_payout_execution: bool
    allow_chain_execution: bool
    dry_run_external_execution: bool



def _bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}



def load_config() -> RuntimeConfig:
    return RuntimeConfig(
        app_env=os.getenv("APP_ENV", "local"),
        app_name=os.getenv("APP_NAME", "MEMBRA"),
        app_version=os.getenv("APP_VERSION", "0.1.0"),
        app_db_path=os.getenv("APP_DB_PATH", "membra.db"),
        app_upload_dir=os.getenv("APP_UPLOAD_DIR", "membra_uploads"),
        llm_provider=os.getenv("LLM_PROVIDER", "auto"),
        groq_base_url=os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1"),
        groq_model=os.getenv("GROQ_TEXT_MODEL", "llama-3.1-8b-instant"),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama3.1"),
        object_storage_provider=os.getenv("OBJECT_STORAGE_PROVIDER", "local"),
        queue_provider=os.getenv("QUEUE_PROVIDER", "local"),
        metrics_enabled=_bool_env("METRICS_ENABLED", True),
        allow_payout_execution=_bool_env("ALLOW_PAYOUT_EXECUTION", False),
        allow_chain_execution=_bool_env("ALLOW_CHAIN_EXECUTION", False),
        dry_run_external_execution=_bool_env("DRY_RUN_EXTERNAL_EXECUTION", True),
    )


CONFIG = load_config()
