"""CLI ECHO AI OS."""

from __future__ import annotations

import argparse
import json
from typing import Sequence

from .events import Event
from .runtime import Runtime


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="echo-ai")
    commands = parser.add_subparsers(dest="command", required=True)
    emit = commands.add_parser("emit")
    emit.add_argument("topic")
    emit.add_argument("--payload", default="{}")
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.payload)
    except json.JSONDecodeError as error:
        raise SystemExit(f"Некорректный JSON: {error.msg}") from error
    if not isinstance(payload, dict):
        raise SystemExit("Payload должен быть JSON-объектом.")
    event = Event(args.topic, payload)
    Runtime().emit(event)
    print(json.dumps({"id": event.id, "topic": event.topic, "payload": payload}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
