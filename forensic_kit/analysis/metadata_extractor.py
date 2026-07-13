"""Extractor de metadata — extrae información de archivos."""

from __future__ import annotations

import json
import struct
from dataclasses import dataclass
from pathlib import Path


# Magic bytes para identificación de tipos de archivo
MAGIC_BYTES: dict[str, list[bytes]] = {
    "JPEG": [b"\xff\xd8\xff"],
    "PNG": [b"\x89PNG"],
    "GIF": [b"GIF8"],
    "PDF": [b"%PDF"],
    "ZIP": [b"PK\x03\x04"],
    "RAR": [b"Rar!"],
    "7Z": [b"7z\xbc\xaf\x27\x1c"],
    "EXE": [b"MZ"],
    "ELF": [b"\x7fELF"],
    "DOCX": [b"PK\x03\x04"],  # ZIP-based
    "MP3": [b"ID3", b"\xff\xfb", b"\xff\xf3"],
    "MP4": [b"\x00\x00\x00\x1cftyp"],
    "WAV": [b"RIFF"],
}


@dataclass
class FileMetadata:
    """Metadata extraída de un archivo."""
    file_path: str
    file_type: str
    file_size: int
    magic_bytes: str
    metadata: dict[str, str]


def detect_file_type(file_path: str | Path) -> str:
    """Detecta el tipo de archivo por magic bytes."""
    try:
        with open(file_path, "rb") as fh:
            header = fh.read(16)
        for file_type, signatures in MAGIC_BYTES.items():
            for sig in signatures:
                if header[:len(sig)] == sig:
                    return file_type
    except Exception:
        pass
    return "UNKNOWN"


def extract_metadata(file_path: str | Path) -> FileMetadata:
    """Extrae metadata básica de un archivo."""
    path = Path(file_path)
    if not path.exists():
        return FileMetadata(
            file_path=str(file_path),
            file_type="NOT_FOUND",
            file_size=0,
            magic_bytes="",
            metadata={},
        )

    file_type = detect_file_type(path)
    size = path.stat().st_size

    try:
        with open(path, "rb") as fh:
            header = fh.read(16)
        magic_hex = header.hex()
    except Exception:
        magic_hex = ""

    metadata: dict[str, str] = {
        "extension": path.suffix,
        "created": str(path.stat().st_ctime),
        "modified": str(path.stat().st_mtime),
    }

    # Extraer metadata específica por tipo
    if file_type == "PDF":
        metadata.update(_extract_pdf_metadata(path))
    elif file_type == "ELF":
        metadata.update(_extract_elf_metadata(path))

    return FileMetadata(
        file_path=str(path),
        file_type=file_type,
        file_size=size,
        magic_bytes=magic_hex,
        metadata=metadata,
    )


def _extract_pdf_metadata(path: Path) -> dict[str, str]:
    """Extrae metadata básica de archivos PDF."""
    try:
        content = path.read_bytes()
        info: dict[str, str] = {}
        for marker in [b"/Title", b"/Author", b"/Creator", b"/Producer"]:
            idx = content.find(marker)
            if idx >= 0:
                end = content.find(b"\n", idx)
                if end == -1:
                    end = idx + 100
                info[marker.decode()[1:]] = content[idx:end].decode("latin-1", errors="replace")[:100]
        return info
    except Exception:
        return {}


def _extract_elf_metadata(path: Path) -> dict[str, str]:
    """Extrae info básica de binarios ELF."""
    try:
        with open(path, "rb") as fh:
            magic = fh.read(4)
            if magic != b"\x7fELF":
                return {}
            ei_class = struct.unpack("B", fh.read(1))[0]
            ei_data = struct.unpack("B", fh.read(1))[0]
            return {
                "class": "64-bit" if ei_class == 2 else "32-bit",
                "endian": "little" if ei_data == 1 else "big",
            }
    except Exception:
        return {}
