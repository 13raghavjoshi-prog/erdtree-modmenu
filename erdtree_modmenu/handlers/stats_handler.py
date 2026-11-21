"""Player stat writes: runes, level, attributes. Patches the PlayerGameData
struct; values are clamped to the vanilla caps to avoid save corruption."""
from __future__ import annotations

from dataclasses import dataclass

from erdtree_modmenu.core.memory_engine import MemoryEngine

STATS_OFFSETS: dict[str, int] = {
    "vigor": 0x3C,
    "mind": 0x40,
    "endurance": 0x44,
    "strength": 0x48,
    "dexterity": 0x4C,
    "intelligence": 0x50,
    "faith": 0x54,
    "arcane": 0x58,
}

CAPS: dict[str, int] = {k: 99 for k in STATS_OFFSETS}
RUNES_ADDR_OFFSET = 0x6C


@dataclass
class StatPatch:
    name: str
    value: int


class StatsHandler:
    def __init__(self, engine: MemoryEngine, player_base: int) -> None:
        self.engine = engine
        self.player_base = player_base

    def apply(self, patches: list[StatPatch]) -> dict[str, int]:
        applied: dict[str, int] = {}
        for patch in patches:
            if patch.name not in STATS_OFFSETS:
                raise KeyError(f"unknown stat {patch.name!r}")
            clamped = max(0, min(patch.value, CAPS[patch.name]))
            self.engine.write(
                self.player_base + STATS_OFFSETS[patch.name],
                clamped.to_bytes(4, "little"),
            )
            applied[patch.name] = clamped
        return applied

    def set_runes(self, amount: int) -> int:
        amount = max(0, min(amount, 999_999_999))
        self.engine.write(
            self.player_base + RUNES_ADDR_OFFSET, amount.to_bytes(4, "little")
        )
        return amount