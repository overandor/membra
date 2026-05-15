from core.events import LocalEventBus



def test_event_bus_publish_and_recent():
    bus = LocalEventBus(max_events=10)

    event = bus.publish(
        topic="asset.created",
        payload={"asset_id": "a1"},
    )

    assert event.topic == "asset.created"

    recent = bus.recent(limit=5)

    assert len(recent) == 1
    assert recent[0].payload["asset_id"] == "a1"
