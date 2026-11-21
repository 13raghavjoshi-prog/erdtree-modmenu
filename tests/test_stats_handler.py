from erdtree_modmenu.handlers.stats_handler import StatsHandler, StatPatch, CAPS


class _FakeEngine:
    def __init__(self) -> None:
        self.writes: list[tuple[int, bytes]] = []

    def write(self, addr: int, data: bytes) -> None:
        self.writes.append((addr, data))


def test_clamps_vigor_to_cap() -> None:
    eng = _FakeEngine()
    handler = StatsHandler(engine=eng, player_base=0x1000)  # type: ignore[arg-type]
    applied = handler.apply([StatPatch(name="vigor", value=999)])
    assert applied["vigor"] == CAPS["vigor"]


def test_rejects_unknown_stat() -> None:
    handler = StatsHandler(engine=_FakeEngine(), player_base=0x0)  # type: ignore[arg-type]
    try:
        handler.apply([StatPatch(name="luck", value=10)])
    except KeyError:
        return
    raise AssertionError("expected KeyError for unknown stat")