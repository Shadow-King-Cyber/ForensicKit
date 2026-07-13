"""Tests para MetadataExtractor."""

from forensic_kit.analysis.metadata_extractor import detect_file_type, extract_metadata


def test_detect_jpeg(tmp_path):
    f = tmp_path / "test.jpg"
    f.write_bytes(b"\xff\xd8\xff\xe0" + b"\x00" * 10)
    assert detect_file_type(str(f)) == "JPEG"


def test_detect_png(tmp_path):
    f = tmp_path / "test.png"
    f.write_bytes(b"\x89PNG" + b"\x00" * 10)
    assert detect_file_type(str(f)) == "PNG"


def test_detect_pdf(tmp_path):
    f = tmp_path / "test.pdf"
    f.write_bytes(b"%PDF-1.4" + b"\x00" * 10)
    assert detect_file_type(str(f)) == "PDF"


def test_detect_unknown(tmp_path):
    f = tmp_path / "test.xyz"
    f.write_bytes(b"random data no magic")
    assert detect_file_type(str(f)) == "UNKNOWN"


def test_extract_metadata(tmp_path):
    f = tmp_path / "test.bin"
    f.write_bytes(b"\x7fELF" + b"\x00" * 10)
    meta = extract_metadata(str(f))
    assert meta.file_type == "ELF"
    assert meta.file_size > 0


def test_metadata_inexistente():
    meta = extract_metadata("/no/existe.bin")
    assert meta.file_type == "NOT_FOUND"
