from __future__ import annotations

import hashlib
import json
from datetime import datetime, UTC
from typing import Any



def canonical_payload(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))



def calculate_event_hash(
    previous_hash: str,
    entity_type: str,
    entity_id: str,
    event_type: str,
    payload: dict[str, Any],
    created_at: str | None = None,
) -> tuple[str, str]:
    timestamp = created_at or datetime.now(UTC).isoformat()

    raw = "|".join(
        [
            previous_hash,
            timestamp,
            entity_type,
            entity_id,
            event_type,
            canonical_payload(payload),
        ]
    )

    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    return timestamp, digest



def verify_chain(events: list[dict[str, Any]]) -> dict[str, Any]:
    previous_hash = "GENESIS"

    for index, event in enumerate(events):
        timestamp, expected_hash = calculate_event_hash(
            previous_hash=previous_hash,
            entity_type=event["entity_type"],
            entity_id=str(event["entity_id"]),
            event_type=event["event_type"],
            payload=event["payload"],
            created_at=event["created_at"],
        )

        if expected_hash != event["event_hash"]:
            return {
                "valid": False,
                "broken_index": index,
                "expected_hash": expected_hash,
                "actual_hash": event["event_hash"],
            }

        previous_hash = event["event_hash"]

    return {
        "valid": True,
        "event_count": len(events),
    }
