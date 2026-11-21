"""CLI helper: run the AOB scanner over the .text section and dump hits."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from erdtree_modmenu.core.memory_engine import MemoryEngine
from erdtree_modmenu.core.process_attach import ProcessAttacher
from erdtree_modmenu.core.signature_scanner import ScanRegion, SignatureScanner


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=lambda v: int(v, 16), required=True)
    ap.add_argument("--size", type=lambda v: int(v, 16), default=0x400000)
    ap.add_argument("--db", default="data/signatures.json")
    args = ap.parse_args()

    attacher = ProcessAttacher()
    pid = attacher.auto_discover()
    if pid is None:
        raise SystemExit("eldenring.exe not running")
    engine = MemoryEngine(pid, attacher.open_handle(pid))
    scanner = SignatureScanner(engine)
    sigs = json.loads(Path(args.db).read_text("utf-8"))
    region = ScanRegion(start=args.start, size=args.size)
    for name, sig in sigs.items():
        hits = scanner.find(region, sig)
        print(f"{name}: {[hex(h) for h in hits[:5]]}")
    engine.detach()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())