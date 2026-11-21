# Offset reference (patch 1.10.x)

| struct | field | offset | notes |
|---|---|---|---|
| PlayerGameData | vigor | `0x3C` | u32, cap 99 |
| PlayerGameData | mind | `0x40` | u32, cap 99 |
| PlayerGameData | runes | `0x6C` | u32, cap 999_999_999 |
| InventorySlot | item_id | `+0x00` | stride `0x10` |
| InventorySlot | quantity | `+0x04` | u32, cap 999 |
| PhysicsCharacter | world_pos | `0x6C8` | vec3<float> |

Offsets drift with every patch. When a handler silently no-ops, the first
thing to check is whether the signature in `data/signatures.json` still
resolves — run `python scripts/scan_signatures.py --start 0x140000000`.