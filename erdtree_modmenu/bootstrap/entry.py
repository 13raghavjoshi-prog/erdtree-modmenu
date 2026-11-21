"""Process entry point. Resolves the target process, wires the IPC bus,
and hands control to the overlay shell (rendered via a C# sidecar in
production, tkinter fallback for dev)."""
from __future__ import annotations

import argparse
import logging
import sys

from erdtree_modmenu.core.process_attach import ProcessAttacher
from erdtree_modmenu.core.memory_engine import MemoryEngine
from erdtree_modmenu.overlay.shell import OverlayShell
from erdtree_modmenu.shared.ipc_bus import IpcBus
from erdtree_modmenu.shared.config import load_config


def _configure_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def launch(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="erdtree-modmenu")
    parser.add_argument("--pid", type=int, default=None, help="Target process id")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--config", default="config/default.toml")
    args = parser.parse_args(argv)

    _configure_logging(args.verbose)
    log = logging.getLogger("erdtree.bootstrap")

    cfg = load_config(args.config)
    attacher = ProcessAttacher(exe_name=cfg["target"]["exe"])
    pid = args.pid or attacher.auto_discover()
    if pid is None:
        log.error("Elden Ring process not found (EasyAntiCheat must be disabled for offline use)")
        return 2

    engine = MemoryEngine(pid=pid, handle=attacher.open_handle(pid))
    bus = IpcBus()
    shell = OverlayShell(engine=engine, bus=bus, theme=cfg["overlay"]["theme"])
    try:
        shell.run()
    finally:
        engine.detach()
    return 0


if __name__ == "__main__":
    sys.exit(launch())