"""Tests para DiskImager."""

from forensic_kit.collection.disk_imager import create_image, compute_hashes, verify_image


def test_create_image(tmp_path):
    src = tmp_path / "source.bin"
    src.write_bytes(b"test data for forensic imaging")
    dst = tmp_path / "image.dd"
    result = create_image(str(src), str(dst))
    assert result.size_bytes == 30
    assert len(result.md5) == 32
    assert len(result.sha256) == 64


def test_compute_hashes(tmp_path):
    f = tmp_path / "test.bin"
    f.write_bytes(b"hello world")
    hashes = compute_hashes(str(f))
    assert "md5" in hashes
    assert "sha256" in hashes
    assert "sha512" in hashes


def test_verify_image_match(tmp_path):
    src = tmp_path / "src.bin"
    src.write_bytes(b"verify me")
    dst = tmp_path / "dst.bin"
    result = create_image(str(src), str(dst))
    verification = verify_image(str(dst), expected_md5=result.md5)
    assert verification["md5_match"] is True


def test_verify_image_mismatch(tmp_path):
    f = tmp_path / "test.bin"
    f.write_bytes(b"data")
    verification = verify_image(str(f), expected_md5="wronghash")
    assert verification["md5_match"] is False
