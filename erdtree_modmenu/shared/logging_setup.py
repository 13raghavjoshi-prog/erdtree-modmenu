from __future__ import annotations

import logging
from pathlib import Path


def setup_file_logging(log_dir: Path = Path("logs")) -> None:
    log_dir.mkdir(exist_ok=True)
    handler = logging.FileHandler(log_dir / "erdtree-modmenu.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))
    logging.getLogger().addHandler(handler)