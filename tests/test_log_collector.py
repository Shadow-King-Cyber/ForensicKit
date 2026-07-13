"""Tests para LogCollector."""

from forensic_kit.collection.log_collector import collect_log, collect_directory_logs


def test_collect_log_inexistente():
    entry = collect_log("/no/existe.log")
    assert entry is None


def test_collect_log_archivo(tmp_path):
    log = tmp_path / "test.log"
    log.write_text("line1\nline2\nline3\n")
    entry = collect_log(str(log))
    assert entry is not None
    assert entry.line_count == 3


def test_collect_directory_logs(tmp_path):
    (tmp_path / "a.log").write_text("log a")
    (tmp_path / "b.txt").write_text("log b")
    entries = collect_directory_logs(str(tmp_path))
    assert len(entries) >= 2
