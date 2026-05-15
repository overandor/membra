from core.proofbook import calculate_event_hash, verify_chain



def test_proof_chain_validates():
    previous = "GENESIS"

    timestamp_1, hash_1 = calculate_event_hash(
        previous_hash=previous,
        entity_type="asset",
        entity_id="1",
        event_type="created",
        payload={"name": "alpha"},
        created_at="2025-01-01T00:00:00+00:00",
    )

    timestamp_2, hash_2 = calculate_event_hash(
        previous_hash=hash_1,
        entity_type="asset",
        entity_id="1",
        event_type="updated",
        payload={"name": "beta"},
        created_at="2025-01-01T00:01:00+00:00",
    )

    result = verify_chain([
        {
            "entity_type": "asset",
            "entity_id": "1",
            "event_type": "created",
            "payload": {"name": "alpha"},
            "created_at": timestamp_1,
            "event_hash": hash_1,
        },
        {
            "entity_type": "asset",
            "entity_id": "1",
            "event_type": "updated",
            "payload": {"name": "beta"},
            "created_at": timestamp_2,
            "event_hash": hash_2,
        },
    ])

    assert result["valid"] is True
