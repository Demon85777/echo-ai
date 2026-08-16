"""Локальная постоянная память ECHO AI OS."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    content: str
    metadata: Mapping[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class JsonMemoryStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def all(self) -> list[MemoryRecord]:
        if not self.path.exists():
            return []
        return [MemoryRecord(**item) for item in json.loads(self.path.read_text(encoding="utf-8"))]

    def remember(self, content: str, metadata: Mapping[str, Any] | None = None) -> MemoryRecord:
        if not content.strip():
            raise ValueError("Содержимое памяти не может быть пустым.")
        record = MemoryRecord(content=content, metadata=metadata or {})
        records = self.all() + [record]
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps([asdict(item) for item in records], ensure_ascii=False), encoding="utf-8")
        return record

    def search(self, query: str) -> list[MemoryRecord]:
        needle = query.casefold().strip()
        return [item for item in self.all() if not needle or needle in item.content.casefold()]
