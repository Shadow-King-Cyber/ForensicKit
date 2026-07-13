"""Tests para FileRecovery."""

from forensic_kit.analysis.file_recovery import scan_for_deleted_files


def test_scan_inexistente():
    found = scan_for_deleted_files("/no/existe.bin")
    assert len(found) == 0


def test_scan_con_jpeg(tmp_path):
    f = tmp_path / "disk.img"
    # Simular un disco con un JPEG embebido
    f.write_bytes(b"\x00" * 100 + b"\xff\xd8\xff\xe0" + b"\x00" * 50)
    found = scan_for_deleted_files(str(f))
    assert len(found) > 0
    assert any(r.file_type == "JPEG" for r in found)


def test_scan_con_png(tmp_path):
    f = tmp_path / "disk.img"
    f.write_bytes(b"\x00" * 100 + b"\x89PNG" + b"\x00" * 50)
    found = scan_for_deleted_files(str(f))
    assert len(found) > 0
    assert any(r.file_type == "PNG" for r in found)
