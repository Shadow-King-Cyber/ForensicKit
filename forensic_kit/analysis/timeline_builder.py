"""Constructor de timeline forense — ordena eventos por timestamps."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TimelineEvent:
    """Evento en la timeline forense."""
    timestamp: float
    timestamp_human: str
    event_type: str      # "created", "modified", "accessed", "changed"
    file_path: str
    details: str


def build_timeline(directory: str | Path, max_depth: int = 3) -> list[TimelineEvent]:
    """Construye una timeline forense a partir de timestamps de archivos."""
    directory = Path(directory)
    events: list[TimelineEvent] = []

    if not directory.exists():
        return events

    def _scan(path: Path, depth: int) -> None:
        if depth > max_depth:
            return
        try:
            for entry in path.iterdir():
                try:
                    stat = entry.stat()
                    for event_type, ts in [
                        ("created", stat.st_ctime),
                        ("modified", stat.st_mtime),
                        ("accessed", stat.st_atime),
                    ]:
                        from datetime import datetime, timezone
                        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
                        events.append(TimelineEvent(
                            timestamp=ts,
                            timestamp_human=dt.isoformat(),
                            event_type=event_type,
                            file_path=str(entry),
                            details=f"{event_type}: {entry.name}",
                        ))
                    if entry.is_dir():
                        _scan(entry, depth + 1)
                except (PermissionError, OSError):
                    continue
        except (PermissionError, OSError):
            pass

    _scan(directory, 0)
    events.sort(key=lambda e: e.timestamp)
    return events


def events_to_json(events: list[TimelineEvent]) -> list[dict]:
    """Convierte eventos a lista de diccionarios para serialización."""
    return [
        {
            "timestamp": e.timestamp,
            "timestamp_human": e.timestamp_human,
            "event_type": e.event_type,
            "file_path": e.file_path,
            "details": e.details,
        }
        for e in events
    ]
