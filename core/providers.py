from __future__ import annotations

import os
from typing import Any

from .config import CONFIG



def provider_status() -> dict[str, Any]:
    return {
        "llm_provider": CONFIG.llm_provider,
        "groq_configured": bool(os.getenv("GROQ_API_KEY")),
        "ollama_base_url": CONFIG.ollama_base_url,
        "object_storage_provider": CONFIG.object_storage_provider,
        "queue_provider": CONFIG.queue_provider,
        "dry_run_external_execution": CONFIG.dry_run_external_execution,
    }



def route_text_provider() -> str:
    if CONFIG.llm_provider == "deterministic":
        return "deterministic"

    if os.getenv("GROQ_API_KEY"):
        return "groq"

    return "ollama"



def deterministic_text(prompt: str) -> dict[str, Any]:
    return {
        "success": True,
        "provider": "deterministic",
        "mode": "text",
        "response": (
            "Deterministic fallback active. "
            "No external LLM provider was required for this operation. "
            f"Prompt digest length: {len(prompt)}"
        ),
        "error": None,
    }
