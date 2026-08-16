from echo_ai import Event, Runtime
from echo_ai.memory import JsonMemoryStore


def test_runtime_dispatches_topic_and_wildcard_handlers() -> None:
    runtime = Runtime()
    seen: list[str] = []
    runtime.subscribe("boot", lambda event: seen.append(event.topic))
    runtime.subscribe("*", lambda event: seen.append("*"))
    runtime.emit(Event("boot"))
    assert seen == ["boot", "*"]


def test_memory_persists_records(tmp_path) -> None:
    store = JsonMemoryStore(tmp_path / "memory.json")
    saved = store.remember("ECHO готов")
    assert JsonMemoryStore(tmp_path / "memory.json").all() == [saved]
