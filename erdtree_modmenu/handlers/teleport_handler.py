"""Map-coordinate teleport. Writes to the WorldPosition struct tracked by the
PhysicsCharacter, so it must be applied on a frame boundary via a queued tick."""
from __future__ import annotations

import time
from dataclasses import dataclass

from erdtree_modmenu.core.memory_engine import MemoryEngine

WORLD_POS_OFFSET = 0x6C8


@dataclass(frozen=True)
class Waypoint:
    name: str
    x: float
    y: float
    z: float


WELL_KNOWN: dict[str, Waypoint] = {
    "roundtable_hold": Waypoint("Roundtable Hold", 452.0, -1.2, 812.0),
    "first_step": Waypoint("First Step", -118.5, 8.0, 921.4),
    "stormveil_gate": Waypoint("Stormveil Gate", 33.1, 12.0, 401.6),
    "leyndell_capital": Waypoint("Leyndell Capital", 108.4, 41.3, 1345.8),
    "haligtree_roots": Waypoint("Haligtree Roots", 1201.2, -60.4, 1802.1),
}


class TeleportHandler:
    def __init__(self, engine: MemoryEngine, player_base: int) -> None:
        self.engine = engine
        self.player_base = player_base

    def _write_vec3(self, addr: int, x: float, y: float, z: float) -> None:
        import struct

        self.engine.write(addr, struct.pack("<fff", x, y, z))

    def teleport(self, waypoint: Waypoint) -> None:
        addr = self.player_base + WORLD_POS_OFFSET
        self._write_vec3(addr, waypoint.x, waypoint.y, waypoint.z)
        time.sleep(0.05)  # let the physics tick settle before next write

    def teleport_named(self, name: str) -> Waypoint:
        wp = WELL_KNOWN.get(name)
        if wp is None:
            raise KeyError(f"unknown waypoint {name!r}")
        self.teleport(wp)
        return wp