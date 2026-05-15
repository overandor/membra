from __future__ import annotations

import hashlib
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path

from .config import CONFIG


@dataclass(slots=True)
class StoredObject:
    object_id: str
    tenant_id: str
    object_key: str
    sha256: str
    byte_size: int
    content_type: str
    provider: str


class LocalObjectStorage:
    def __init__(self, root: str | Path | None = None) -> None:
        self.root = Path(root or CONFIG.app_upload_dir)
        self.root.mkdir(parents=True, exist_ok=True)

    def put_file(self, source_path: str | Path, tenant_id: str, purpose: str = "upload", content_type: str = "application/octet-stream") -> StoredObject:
        source = Path(source_path)
        if not source.exists() or not source.is_file():
            raise FileNotFoundError(f"source file not found: {source}")

        object_id = str(uuid.uuid4())
        safe_suffix = source.suffix.lower()[:20]
        object_key = f"{tenant_id}/{purpose}/{object_id}{safe_suffix}"
        target = self.root / object_key
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)

        data = target.read_bytes()
        digest = hashlib.sha256(data).hexdigest()

        return StoredObject(
            object_id=object_id,
            tenant_id=tenant_id,
            object_key=object_key,
            sha256=digest,
            byte_size=len(data),
            content_type=content_type,
            provider="local",
        )

    def resolve_path(self, object_key: str) -> Path:
        path = (self.root / object_key).resolve()
        root = self.root.resolve()
        if root not in path.parents and path != root:
            raise ValueError("object key escapes storage root")
        return path

    def verify_hash(self, object_key: str, expected_sha256: str) -> bool:
        path = self.resolve_path(object_key)
        if not path.exists():
            return False
        return hashlib.sha256(path.read_bytes()).hexdigest() == expected_sha256


STORAGE = LocalObjectStorage()
