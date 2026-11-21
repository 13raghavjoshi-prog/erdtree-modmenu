# Contributing to erdtree-modmenu

Thanks for poking at the codebase. This is a hobbyist Elden Ring modding
project — keep PRs offline-focused. Anything that tries to defeat
EasyAntiCheat in online sessions is out of scope and will be closed.

## Local setup

```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m erdtree_modmenu.bootstrap.entry --verbose
```

## Where things live

- `erdtree_modmenu/core/` — process attach, memory engine, AOB scanner
- `erdtree_modmenu/handlers/` — one file per feature (stats, inventory, teleport)
- `erdtree_modmenu/overlay/` — dev tkinter shell
- `erdtree_native/` — C# WPF overlay host (dotnet 8)
- `data/` — signature DB and item id tables

## Adding a new feature handler

1. Create `erdtree_modmenu/handlers/<feature>_handler.py`
2. Expose offsets as module-level constants, not inline magic
3. Write a clamp test under `tests/`
4. Register the action in `overlay/shell.py`

## Style

- Python 3.11+, `from __future__ import annotations`
- No `print()` in library code — use `logging`
- Handlers must never touch `ctypes` directly; go through `MemoryEngine`