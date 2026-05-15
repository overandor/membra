from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Any


@dataclass(slots=True)
class Event:
    topic: str
    payload: dict[str, Any]
    created_at: str


class LocalEventBus:
    def __init__(self, max_events: int = 1000) -> None:
        self._events: deque[Event] = deque(maxlen=max_events)

    def publish(self, topic: str, payload: dict[str, Any]) -> Event:
        event = Event(
            topic=topic,
            payload=payload,
            created_at=datetime.now(UTC).isoformat(),
        )

        self._events.append(event)
        return event

    def recent(self, limit: int = 50) -> list[Event]:
        return list(self._events)[-limit:]


EVENT_BUS = LocalEventBus()
