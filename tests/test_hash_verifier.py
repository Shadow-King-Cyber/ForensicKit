"""Tests para HashVerifier."""

from forensic_kit.analysis.hash_verifier import compute_hash, verify_hash, compute_multiple_hashes


def test_compute_hash(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("hello")
    h = compute_hash(str(f), "sha256")
    assert len(h) == 64


def test_verify_hash_match(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("data")
    h = compute_hash(str(f), "sha256")
    result = verify_hash(str(f), h, "sha256")
    assert result.match is True


def test_verify_hash_mismatch(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("data")
    result = verify_hash(str(f), "wrong", "sha256")
    assert result.match is False


def test_multiple_hashes(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("test")
    hashes = compute_multiple_hashes(str(f))
    assert len(hashes) == 4
    assert all(len(h) > 0 for h in hashes.values())
