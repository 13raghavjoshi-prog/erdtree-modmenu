"""Windows process discovery + handle acquisition for eldenring.exe."""
from __future__ import annotations

import ctypes
from ctypes import wintypes
from typing import Optional

PROCESS_ALL_ACCESS = 0x1F0FFF
TH32CS_SNAPPROCESS = 0x00000002
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)


class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
        ("th32ModuleID", wintypes.DWORD),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", ctypes.c_long),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", ctypes.c_char * 260),
    ]


class ProcessAttacher:
    def __init__(self, exe_name: str = "eldenring.exe") -> None:
        self.exe_name = exe_name

    def auto_discover(self) -> Optional[int]:
        snap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        if snap == -1:
            return None
        entry = PROCESSENTRY32()
        entry.dwSize = ctypes.sizeof(PROCESSENTRY32)
        try:
            if not kernel32.Process32First(snap, ctypes.byref(entry)):
                return None
            while True:
                if entry.szExeFile.decode("utf-8", "ignore").lower() == self.exe_name.lower():
                    return int(entry.th32ProcessID)
                if not kernel32.Process32Next(snap, ctypes.byref(entry)):
                    return None
        finally:
            kernel32.CloseHandle(snap)

    def open_handle(self, pid: int) -> int:
        handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        if not handle:
            raise OSError(ctypes.get_last_error(), "OpenProcess failed — run as admin")
        return int(handle)