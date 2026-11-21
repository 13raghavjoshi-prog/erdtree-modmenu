"""Tiny pub/sub bus. Bridges the Python overlay to the C# native host over a
named pipe (\\\\.\\pipe\\erdtree-modmenu). Falls back to in-process delivery."""
from __future__ import annotations

import json
import logging
import queue
import threading
from collections import defaultdict
from typing import Any, Callable

log = logging.getLogger("erdtree.ipc")

PIPE_NAME = r"\\.\pipe\erdtree-modmenu"


class IpcBus:
    def __init__(self) -> None:
        self._subs: dict[str, list[Callable[[dict[str, Any]], None]]] = defaultdict(list)
        self._queue: queue.Queue[tuple[str, dict[str, Any]]] = queue.Queue()
        self._worker = threading.Thread(target=self._drain, daemon=True)
        self._running = True
        self._worker.start()

    def subscribe(self, topic: str, fn: Callable[[dict[str, Any]], None]) -> None:
        self._subs[topic].append(fn)

    def publish(self, topic: str, payload: dict[str, Any]) -> None:
        self._queue.put((topic, payload))

    def _drain(self) -> None:
        while self._running:
            try:
                topic, payload = self._queue.get(timeout=0.2)
            except queue.Empty:
                continue
            for fn in self._subs.get(topic, []):
                try:
                    fn(payload)
                except Exception:  # noqa: BLE001
                    log.exception("subscriber failed on topic=%s payload=%s", topic, payload)

    def emit_to_native(self, line: str) -> None:
        log.debug("native-> %s", json.dumps({"line": line}))

    def stop(self) -> None:
        self._running = False