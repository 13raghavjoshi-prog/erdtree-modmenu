"""Argument helpers shared by entry.py and scripts/."""
from __future__ import annotations

import argparse


def add_common_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--verbose", action="store_true", help="debug logging")
    parser.add_argument("--config", default="config/default.toml")
    parser.add_argument("--no-overlay", action="store_true", help="headless mode")
    return parser