"""Recuperación de archivos — busca archivos eliminados por magic bytes."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .metadata_extractor import MAGIC_BYTES


@dataclass
class RecoveredFile:
    """Archivo potencialmente recuperado."""
    offset: int
    file_type: str
    size_estimate: str
    evidence: str


def scan_for_deleted_files(file_path: str | Path, chunk_size: int = 1024 * 1024) -> list[RecoveredFile]:
    """Escanea un archivo/binario buscando magic bytes de archivos eliminados.

    Útil para escanear imágenes de disco buscando archivos que fueron
    eliminados pero no sobrescritos.
    """
    recovered: list[RecoveredFile] = []

    try:
        with open(file_path, "rb") as fh:
            offset = 0
            while True:
                chunk = fh.read(chunk_size)
                if not chunk:
                    break

                for file_type, signatures in MAGIC_BYTES.items():
                    for sig in signatures:
                        idx = 0
                        while True:
                            idx = chunk.find(sig, idx)
                            if idx == -1:
                                break
                            recovered.append(RecoveredFile(
                                offset=offset + idx,
                                file_type=file_type,
                                size_estimate="unknown",
                                evidence=f"Magic bytes {sig.hex()} at offset {offset + idx}",
                            ))
                            idx += 1

                offset += len(chunk)
    except Exception:
        pass

    return recovered


def carve_file(source: str | Path, offset: int, length: int, output: str | Path) -> bool:
    """Extrae un bloque de bytes de un archivo fuente."""
    try:
        with open(source, "rb") as fh:
            fh.seek(offset)
            data = fh.read(length)
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        Path(output).write_bytes(data)
        return True
    except Exception:
        return False
