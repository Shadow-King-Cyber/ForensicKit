"""Recolección de logs del sistema."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class LogEntry:
    """Entrada de log recolectada."""
    source: str
    path: str
    content: str
    line_count: int
    size_bytes: int


# Rutas de logs comunes en Linux
LOG_PATHS = [
    "/var/log/syslog",
    "/var/log/auth.log",
    "/var/log/kern.log",
    "/var/log/dmesg",
    "/var/log/lastlog",
    "/var/log/wtmp",
    "/var/log/btmp",
    "/var/log/nginx/access.log",
    "/var/log/apache2/access.log",
    "/var/log/audit/audit.log",
]


def collect_log(file_path: str | Path) -> LogEntry | None:
    """Recolecta un archivo de log individual."""
    path = Path(file_path)
    if not path.exists():
        return None

    try:
        content = path.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
        return LogEntry(
            source="log_collector",
            path=str(path),
            content=content[:50000],  # Limitar a 50KB
            line_count=len(lines),
            size_bytes=path.stat().st_size,
        )
    except Exception:
        return None


def collect_system_logs(extra_paths: list[str] | None = None) -> list[LogEntry]:
    """Recolecta logs del sistema desde rutas conocidas."""
    entries: list[LogEntry] = []
    paths = LOG_PATHS + (extra_paths or [])

    for log_path in paths:
        entry = collect_log(log_path)
        if entry:
            entries.append(entry)

    return entries


def collect_directory_logs(directory: str | Path, extensions: list[str] | None = None) -> list[LogEntry]:
    """Recolecta todos los archivos de log de un directorio."""
    directory = Path(directory)
    extensions = extensions or [".log", ".txt", ".out"]
    entries: list[LogEntry] = []

    if not directory.exists():
        return entries

    for path in directory.rglob("*"):
        if path.is_file() and any(path.suffix.lower() == ext for ext in extensions):
            entry = collect_log(str(path))
            if entry:
                entries.append(entry)

    return entries
