"""Optional C# sidecar launcher. The sidecar hosts the WPF overlay and forwards
hotkey events back into the Python engine via stdin JSON lines."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path


class NativeBridge:
    def __init__(self, sidecar: Path) -> None:
        self.sidecar = sidecar
        self.proc: subprocess.Popen[str] | None = None

    def start(self) -> None:
        if not self.sidecar.exists():
            raise FileNotFoundError(f"sidecar not built: {self.sidecar}")
        self.proc = subprocess.Popen(
            ["dotnet", str(self.sidecar)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

    def send(self, action: str, **kwargs: object) -> None:
        if not self.proc or not self.proc.stdin:
            raise RuntimeError("sidecar not running")
        self.proc.stdin.write(json.dumps({"action": action, **kwargs}) + "\n")
        self.proc.stdin.flush()

    def stop(self) -> None:
        if self.proc:
            self.proc.terminate()
            self.proc.wait(timeout=3)