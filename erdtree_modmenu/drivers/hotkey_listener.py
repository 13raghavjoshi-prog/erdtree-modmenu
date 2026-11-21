"""Global hotkey listener built on RegisterHotKey. F8 toggles the overlay,
F9 triggers the last queued action, F10 dumps a memory snapshot for debugging."""
from __future__ import annotations

import ctypes
import threading
from ctypes import wintypes
from typing import Callable

user32 = ctypes.WinDLL("user32", use_last_error=True)
MOD_NOREPEAT = 0x4000
WM_HOTKEY = 0x0312

VK_F8, VK_F9, VK_F10 = 0x77, 0x78, 0x79


class HotkeyListener:
    def __init__(self, bindings: dict[int, Callable[[], None]]) -> None:
        self.bindings = bindings
        self._thread: threading.Thread | None = None

    def _loop(self) -> None:
        for vk in self.bindings:
            user32.RegisterHotKey(None, vk, MOD_NOREPEAT, vk)
        msg = wintypes.MSG()
        try:
            while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
                if msg.message == WM_HOTKEY:
                    cb = self.bindings.get(msg.wParam)
                    if cb:
                        cb()
        finally:
            for vk in self.bindings:
                user32.UnregisterHotKey(None, vk)

    def start(self) -> None:
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()