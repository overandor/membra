from pathlib import Path

from core.storage import LocalObjectStorage



def test_local_storage_roundtrip(tmp_path: Path):
    storage = LocalObjectStorage(root=tmp_path / "storage")

    source = tmp_path / "sample.txt"
    source.write_text("membra-test", encoding="utf-8")

    stored = storage.put_file(
        source_path=source,
        tenant_id="tenant-a",
        purpose="proof",
        content_type="text/plain",
    )

    assert stored.provider == "local"
    assert stored.byte_size > 0
    assert storage.verify_hash(stored.object_key, stored.sha256)
