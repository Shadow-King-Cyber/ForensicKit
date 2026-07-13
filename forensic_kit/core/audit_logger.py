"""Logger de auditoría append-only — registra cada operación forense."""

from __future__ import annotations

import getpass
import json
from datetime import datetime, timezone
from pathlib import Path


class AuditLogger:
    """Logger append-only para operaciones forenses."""

    def __init__(self, path: str | Path = "audit_log.jsonl") -> None:
        self._path = Path(path)
        self._path.touch(exist_ok=True)

    def log(self, action: str, target: str, result: str, *, extra: dict | None = None) -> dict:
        record: dict = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user": self._current_user(),
            "action": action,
            "target": target,
            "result": result,
        }
        if extra:
            record["extra"] = extra
        with open(self._path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record

    def log_denied(self, action: str, target: str) -> dict:
        return self.log(action, target, "DENIED_NOT_IN_SCOPE")

    def read_all(self) -> list[dict]:
        records: list[dict] = []
        with open(self._path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records

    @staticmethod
    def _current_user() -> str:
        try:
            return getpass.getuser()
        except Exception:
            return "unknown"
