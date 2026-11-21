"""AOB scanner used by feature handlers to locate structures across patches."""
from __future__ import annotations

import re
from dataclasses import dataclass

from erdtree_modmenu.core.memory_engine import MemoryEngine

_PATTERN = re.compile(r"^[0-9A-F? ]+$", re.IGNORECASE)


@dataclass(frozen=True)
class ScanRegion:
    start: int
    size: int


class SignatureScanner:
    def __init__(self, engine: MemoryEngine, chunk: int = 0x10000) -> None:
        self.engine = engine
        self.chunk = chunk

    def _compile(self, sig: str) -> tuple[bytes, bytes]:
        if not _PATTERN.match(sig):
            raise ValueError(f"bad signature: {sig!r}")
        clean = sig.replace(" ", "")
        mask = bytearray()
        values = bytearray()
        for i in range(0, len(clean), 2):
            pair = clean[i : i + 2]
            if pair == "??":
                mask.append(0)
                values.append(0)
            else:
                mask.append(0xFF)
                values.append(int(pair, 16))
        return bytes(values), bytes(mask)

    def find(self, region: ScanRegion, sig: str) -> list[int]:
        values, mask = self._compile(sig)
        hits: list[int] = []
        cursor = region.start
        end = region.start + region.size
        while cursor < end:
            size = min(self.chunk, end - cursor)
            try:
                blob = self.engine.read(cursor, size)
            except OSError:
                break
            for i in range(0, len(blob) - len(values)):
                if all((blob[i + j] & mask[j]) == values[j] for j in range(len(values))):
                    hits.append(cursor + i)
            cursor += size - len(values)
        return hits