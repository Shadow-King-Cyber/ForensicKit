"""Detector de esteganografía — detecta datos ocultos en archivos."""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


@dataclass
class StegoFinding:
    """Resultado de la detección de esteganografía."""
    file_path: str
    technique: str     # "lsb_anomaly", "high_entropy", "trailing_data"
    confidence: str    # "high", "medium", "low"
    detail: str
    evidence: str


def calculate_entropy(data: bytes) -> float:
    """Calcula la entropía de Shannon."""
    if not data:
        return 0.0
    counts = Counter(data)
    length = len(data)
    entropy = 0.0
    for count in counts.values():
        p = count / length
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def detect_lsb_anomaly(file_path: str | Path) -> StegoFinding | None:
    """Detecta anomalías en LSB que pueden indicar esteganografía."""
    try:
        data = Path(file_path).read_bytes()
        if len(data) < 100:
            return None

        # Analizar distribución de bits LSB
        lsb_bits = [byte & 1 for byte in data[:10000]]
        ones_count = sum(lsb_bits)
        total = len(lsb_bits)
        ratio = ones_count / total

        # Distribución uniforme (~0.5) puede indicar LSB stego
        if 0.45 < ratio < 0.55 and total > 500:
            return StegoFinding(
                file_path=str(file_path),
                technique="lsb_anomaly",
                confidence="medium",
                detail=f"Distribución LSB inusualmente uniforme: {ratio:.3f}",
                evidence=f"ones={ones_count}/{total}, ratio={ratio:.3f}",
            )
    except Exception:
        pass
    return None


def detect_high_entropy(file_path: str | Path, threshold: float = 7.5) -> StegoFinding | None:
    """Detecta secciones con entropía inusualmente alta (posibles datos cifrados)."""
    try:
        data = Path(file_path).read_bytes()
        if len(data) < 100:
            return None

        entropy = calculate_entropy(data[:10000])
        if entropy > threshold:
            return StegoFinding(
                file_path=str(file_path),
                technique="high_entropy",
                confidence="low",
                detail=f"Entropía alta: {entropy:.2f} (umbral: {threshold})",
                evidence=f"entropy={entropy:.2f}, size={len(data)}",
            )
    except Exception:
        pass
    return None


def detect_trailing_data(file_path: str | Path) -> StegoFinding | None:
    """Detecta datos al final del archivo que no corresponden al formato."""
    try:
        data = Path(file_path).read_bytes()
        if len(data) < 50:
            return None

        # Buscar fin de archivo conocido y datos después de él
        eof_markers = {
            "JPEG": [b"\xff\xd9"],
            "PNG": [b"IEND"],
            "GIF": [b"\x00;"],
        }

        file_type = ""
        if data[:3] == b"\xff\xd8\xff":
            file_type = "JPEG"
        elif data[:4] == b"\x89PNG":
            file_type = "PNG"
        elif data[:3] == b"GIF":
            file_type = "GIF"

        if file_type in eof_markers:
            for marker in eof_markers[file_type]:
                idx = data.find(marker)
                if idx >= 0 and idx < len(data) - len(marker) - 10:
                    trailing = data[idx + len(marker):]
                    if len(trailing) > 10:
                        return StegoFinding(
                            file_path=str(file_path),
                            technique="trailing_data",
                            confidence="high",
                            detail=f"Datos extra después del EOF de {file_type}: {len(trailing)} bytes",
                            evidence=f"trailing_size={len(trailing)}",
                        )
    except Exception:
        pass
    return None


def scan_file(file_path: str | Path) -> list[StegoFinding]:
    """Escanea un archivo buscando indicadores de esteganografía."""
    findings: list[StegoFinding] = []

    lsb = detect_lsb_anomaly(file_path)
    if lsb:
        findings.append(lsb)

    entropy = detect_high_entropy(file_path)
    if entropy:
        findings.append(entropy)

    trailing = detect_trailing_data(file_path)
    if trailing:
        findings.append(trailing)

    return findings
