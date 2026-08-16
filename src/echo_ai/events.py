"""События ECHO AI OS."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class Event:
    topic: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
