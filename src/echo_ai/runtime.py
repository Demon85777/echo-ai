"""Среда выполнения и диспетчеризация событий."""

from __future__ import annotations

from collections.abc import Callable

from .events import Event

Handler = Callable[[Event], None]


class Runtime:
    def __init__(self) -> None:
        self._subscriptions: dict[str, list[Handler]] = {}

    def subscribe(self, topic: str, handler: Handler) -> None:
        if not topic:
            raise ValueError("Тема события не может быть пустой.")
        self._subscriptions.setdefault(topic, []).append(handler)

    def emit(self, event: Event) -> None:
        for handler in self._subscriptions.get(event.topic, ()):
            handler(event)
        for handler in self._subscriptions.get("*", ()):
            handler(event)
