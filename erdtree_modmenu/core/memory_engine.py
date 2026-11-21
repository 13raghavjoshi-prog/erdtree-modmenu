"""Read/write primitives. Everything funnels through here so handlers stay
free of raw ctypes noise."""
from __future__ import annotations

import ctypes
import struct
from typing import Any

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)


class MemoryEngine:
    def __init__(self, pid: int, handle: int) -> None:
        self.pid = pid
        self.handle = handle
        self._read_cache: dict[int, bytes] = {}

    def read(self, address: int, size: int) -> bytes:
        buf = ctypes.create_string_buffer(size)
        read = ctypes.c_size_t(0)
        ok = kernel32.ReadProcessMemory(
            self.handle, ctypes.c_void_p(address), buf, size, ctypes.byref(read)
        )
        if not ok:
            raise OSError(ctypes.get_last_error(), f"RPM failed @ {address:#x}")
        return buf.raw[: read.value]

    def write(self, address: int, data: bytes) -> None:
        written = ctypes.c_size_t(0)
        ok = kernel32.WriteProcessMemory(
            self.handle, ctypes.c_void_p(address), data, len(data), ctypes.byref(written)
        )
        if not ok:
            raise OSError(ctypes.get_last_error(), f"WPM failed @ {address:#x}")

    def read_i32(self, address: int) -> int:
        return struct.unpack("<i", self.read(address, 4))[0]

    def write_f32(self, address: int, value: float) -> None:
        self.write(address, struct.pack("<f", value))

    def resolve_chain(self, base: int, offsets: list[int]) -> int:
        ptr = base
        for off in offsets[:-1]:
            ptr = self.read_i64(ptr + off)
        return ptr + offsets[-1]

    def read_i64(self, address: int) -> int:
        return struct.unpack("<q", self.read(address, 8))[0]

    def snapshot(self, address: int, size: int) -> bytes:
        data = self.read(address, size)
        self._read_cache[address] = data
        return data

    def detach(self) -> None:
        if self.handle:
            kernel32.CloseHandle(self.handle)
            self.handle = 0