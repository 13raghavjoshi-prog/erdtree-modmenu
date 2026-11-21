from unittest.mock import MagicMock

import pytest

from erdtree_modmenu.core.memory_engine import MemoryEngine


@pytest.fixture
def engine() -> MemoryEngine:
    e = MemoryEngine(pid=4242, handle=0xDEADBEEF)
    e.read = MagicMock(return_value=b"\x2a\x00\x00\x00")
    return e


def test_read_i32(engine: MemoryEngine) -> None:
    assert engine.read_i32(0x7FF6A000) == 42


def test_write_f32_roundtrip() -> None:
    engine = MemoryEngine(pid=1, handle=2)
    captured: dict[int, bytes] = {}

    def fake_write(addr: int, data: bytes) -> None:
        captured[addr] = data

    engine.write = fake_write  # type: ignore[method-assign]
    engine.write_f32(0x1000, 99.5)
    assert captured[0x1000] == b"\x00\x00\xc7\x42"