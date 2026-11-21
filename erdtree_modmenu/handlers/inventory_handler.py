"""Item injection into the player's inventory grid. Uses the item-id table
from data/item_ids.json and writes into the InventorySlot array in place."""
from __future__ import annotations

import json
from pathlib import Path

from erdtree_modmenu.core.memory_engine import MemoryEngine

INVENTORY_BASE_OFFSET = 0x2A10
SLOT_STRIDE = 0x10
MAX_SLOTS = 2688


class InventoryHandler:
    def __init__(self, engine: MemoryEngine, player_base: int, data_dir: Path) -> None:
        self.engine = engine
        self.player_base = player_base
        self.item_ids = json.loads((data_dir / "item_ids.json").read_text("utf-8"))

    def find_free_slot(self) -> int | None:
        for idx in range(MAX_SLOTS):
            addr = self.player_base + INVENTORY_BASE_OFFSET + idx * SLOT_STRIDE
            current = self.engine.read_i32(addr)
            if current == 0:
                return idx
        return None

    def inject(self, item_name: str, quantity: int = 1) -> int:
        item_id = self.item_ids.get(item_name)
        if item_id is None:
            raise KeyError(f"unknown item {item_name!r}")
        slot = self.find_free_slot()
        if slot is None:
            raise RuntimeError("inventory full — clear a slot first")
        addr = self.player_base + INVENTORY_BASE_OFFSET + slot * SLOT_STRIDE
        self.engine.write(addr, item_id.to_bytes(4, "little"))
        self.engine.write(addr + 0x4, min(quantity, 999).to_bytes(4, "little"))
        return slot

    def clear_slot(self, slot: int) -> None:
        addr = self.player_base + INVENTORY_BASE_OFFSET + slot * SLOT_STRIDE
        self.engine.write(addr, b"\x00" * SLOT_STRIDE)