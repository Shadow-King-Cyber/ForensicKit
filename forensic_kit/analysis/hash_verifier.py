"""Verificador de hashes — verifica integridad de evidencia."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class HashResult:
    """Resultado de verificación de hash."""
    file_path: str
    algorithm: str
    computed_hash: str
    expected_hash: str
    match: bool


def compute_hash(file_path: str | Path, algorithm: str = "sha256") -> str:
    """Calcula el hash de un archivo."""
    h = hashlib.new(algorithm)
    try:
        with open(file_path, "rb") as fh:
            for chunk in iter(lambda: fh.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return ""


def verify_hash(file_path: str | Path, expected: str, algorithm: str = "sha256") -> HashResult:
    """Verifica si el hash de un archivo coincide con el esperado."""
    computed = compute_hash(file_path, algorithm)
    return HashResult(
        file_path=str(file_path),
        algorithm=algorithm,
        computed_hash=computed,
        expected_hash=expected,
        match=computed == expected,
    )


def compute_multiple_hashes(file_path: str | Path) -> dict[str, str]:
    """Calcula MD5, SHA1, SHA256 y SHA512 de un archivo."""
    results: dict[str, str] = {}
    for algo in ["md5", "sha1", "sha256", "sha512"]:
        results[algo] = compute_hash(file_path, algo)
    return results
