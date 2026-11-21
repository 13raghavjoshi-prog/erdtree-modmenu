from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

DEFAULTS: dict[str, Any] = {
    "target": {"exe": "eldenring.exe"},
    "overlay": {"theme": "erdtree-dark", "hotkey": "F8"},
    "safety": {"require_offline": True, "auto_backup_save": True},
}


def load_config(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        return DEFAULTS
    with p.open("rb") as fh:
        user = tomllib.load(fh)
    merged = {**DEFAULTS, **user}
    for key, val in DEFAULTS.items():
        if isinstance(val, dict) and key in user:
            merged[key] = {**val, **user[key]}
    return merged