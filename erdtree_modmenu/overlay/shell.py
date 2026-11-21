"""Overlay shell. Production build embeds the C# WPF sidecar
(erdtree_native/OverlayHost.csproj); the tkinter path here is the dev fallback."""
from __future__ import annotations

import logging
import tkinter as tk
from tkinter import ttk

from erdtree_modmenu.core.memory_engine import MemoryEngine
from erdtree_modmenu.shared.ipc_bus import IpcBus

log = logging.getLogger("erdtree.overlay")


class OverlayShell:
    def __init__(self, engine: MemoryEngine, bus: IpcBus, theme: str = "erdtree-dark") -> None:
        self.engine = engine
        self.bus = bus
        self.theme = theme
        self.root: tk.Tk | None = None

    def _build(self) -> None:
        self.root = tk.Tk()
        self.root.title("erdtree-modmenu")
        self.root.geometry("420x520")
        self.root.configure(bg="#1a1614" if self.theme == "erdtree-dark" else "#ece6d4")

        header = ttk.Label(self.root, text="Elden Ring · ModMenu", font=("Consolas", 14, "bold"))
        header.pack(pady=10)

        for name, payload in (
            ("Set 99 Runes", {"runes": 999_999}),
            ("Godmode", {"hp_infinite": True}),
            ("Teleport: Roundtable", {"waypoint": "roundtable_hold"}),
            ("Inject: Golden Rune [1]", {"item": "golden_rune_1", "qty": 10}),
        ):
            ttk.Button(
                self.root,
                text=name,
                command=lambda p=payload: self.bus.publish("action", p),
            ).pack(fill="x", padx=16, pady=4)

        ttk.Label(self.root, text="v0.9.4 · offline only", foreground="#8a7f6b").pack(side="bottom", pady=6)

    def run(self) -> None:
        self._build()
        assert self.root is not None
        self.root.mainloop()