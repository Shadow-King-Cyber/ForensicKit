"""Tests para StegoDetector."""

from forensic_kit.analysis.stego_detector import (
    calculate_entropy, detect_lsb_anomaly, detect_high_entropy,
    detect_trailing_data, scan_file
)


def test_entropy_vacia():
    assert calculate_entropy(b"") == 0.0


def test_entropy_repetida():
    assert calculate_entropy(b"\x00" * 1000) == 0.0


def test_entropy_alta():
    data = bytes(range(256)) * 10
    assert calculate_entropy(data) > 5.0


def test_scan_file_inexistente():
    findings = scan_file("/no/existe.bin")
    assert len(findings) == 0


def test_detect_high_entropy(tmp_path):
    # Crear archivo con alta entropía (datos variados)
    f = tmp_path / "entropy.bin"
    f.write_bytes(bytes(range(256)) * 100)
    finding = detect_high_entropy(str(f), threshold=7.0)
    assert finding is not None
    assert finding.technique == "high_entropy"


def test_lsb_normal(tmp_path):
    # Archivo con bytes todos iguales — LSB uniforme
    f = tmp_path / "lsb.bin"
    f.write_bytes(b"\x00" * 1000)
    finding = detect_lsb_anomaly(str(f))
    # Todos los bits LSB son 0, ratio = 0.0, no se detecta
    assert finding is None
