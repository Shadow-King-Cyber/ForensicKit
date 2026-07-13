"""Tests para TimelineBuilder."""

from forensic_kit.analysis.timeline_builder import build_timeline


def test_timeline_directorio_inexistente():
    events = build_timeline("/no/existe")
    assert len(events) == 0


def test_timeline_directorio_temporal(tmp_path):
    (tmp_path / "file1.txt").write_text("a")
    (tmp_path / "file2.txt").write_text("b")
    events = build_timeline(str(tmp_path), max_depth=1)
    assert len(events) >= 4  # 2 archivos x 3 eventos (created, modified, accessed)


def test_timeline_ordenado(tmp_path):
    import time
    f1 = tmp_path / "a.txt"
    f1.write_text("first")
    time.sleep(0.01)
    f2 = tmp_path / "b.txt"
    f2.write_text("second")
    events = build_timeline(str(tmp_path), max_depth=1)
    timestamps = [e.timestamp for e in events]
    assert timestamps == sorted(timestamps)
