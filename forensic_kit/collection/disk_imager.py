"""Imágenes de disco — crea copias forenses con verificación hash."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ImageResult:
    """Resultado de la creación de imagen forense."""
    source: str
    output: str
    size_bytes: int
    md5: str
    sha256: str
    sha512: str


def compute_hashes(file_path: str | Path) -> dict[str, str]:
    """Calcula MD5, SHA256 y SHA512 de un archivo."""
    md5 = hashlib.md5()
    sha256 = hashlib.sha256()
    sha512 = hashlib.sha512()

    with open(file_path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            md5.update(chunk)
            sha256.update(chunk)
            sha512.update(chunk)

    return {
        "md5": md5.hexdigest(),
        "sha256": sha256.hexdigest(),
        "sha512": sha512.hexdigest(),
    }


def create_image(source: str | Path, output: str | Path, chunk_size: int = 8192) -> ImageResult:
    """Crea una imagen forense de un archivo o directorio.

    Copia el archivo byte por byte y calcula hashes para verificación.
    """
    source = Path(source)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    size = 0
    md5 = hashlib.md5()
    sha256 = hashlib.sha256()
    sha512 = hashlib.sha512()

    with open(source, "rb") as src, open(output, "wb") as dst:
        while True:
            chunk = src.read(chunk_size)
            if not chunk:
                break
            dst.write(chunk)
            md5.update(chunk)
            sha256.update(chunk)
            sha512.update(chunk)
            size += len(chunk)

    return ImageResult(
        source=str(source),
        output=str(output),
        size_bytes=size,
        md5=md5.hexdigest(),
        sha256=sha256.hexdigest(),
        sha512=sha512.hexdigest(),
    )


def verify_image(image_path: str | Path, expected_md5: str = "", expected_sha256: str = "") -> dict[str, bool]:
    """Verifica la integridad de una imagen forense contra hashes esperados."""
    hashes = compute_hashes(image_path)
    return {
        "md5_match": not expected_md5 or hashes["md5"] == expected_md5,
        "sha256_match": not expected_sha256 or hashes["sha256"] == expected_sha256,
        "hashes": hashes,
    }
