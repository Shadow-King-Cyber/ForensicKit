"""Cadena de custodia — registra manipulación de evidencia forense."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from dataclasses import dataclass, field
from pathlib import Path

import getpass


@dataclass
class CustodyEntry:
    """Entrada en la cadena de custodia."""
    timestamp: str
    user: str
    action: str
    evidence_id: str
    description: str
    hash_before: str = ""
    hash_after: str = ""


@dataclass
class EvidenceChain:
    """Registra cada manipulación de evidencia para mantener integridad legal."""
    case_id: str
    entries: list[CustodyEntry] = field(default_factory=list)

    def record(self, action: str, evidence_id: str, description: str,
               hash_before: str = "", hash_after: str = "") -> CustodyEntry:
        entry = CustodyEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            user=self._current_user(),
            action=action,
            evidence_id=evidence_id,
            description=description,
            hash_before=hash_before,
            hash_after=hash_after,
        )
        self.entries.append(entry)
        return entry

    def to_json(self) -> str:
        return json.dumps([
            {
                "timestamp": e.timestamp,
                "user": e.user,
                "action": e.action,
                "evidence_id": e.evidence_id,
                "description": e.description,
                "hash_before": e.hash_before,
                "hash_after": e.hash_after,
            }
            for e in self.entries
        ], ensure_ascii=False, indent=2)

    def save(self, path: str | Path) -> None:
        Path(path).write_text(self.to_json(), encoding="utf-8")

    @classmethod
    def from_json(cls, case_id: str, json_str: str) -> EvidenceChain:
        data = json.loads(json_str)
        chain = cls(case_id=case_id)
        for e in data:
            chain.entries.append(CustodyEntry(**e))
        return chain

    @staticmethod
    def _current_user() -> str:
        try:
            return getpass.getuser()
        except Exception:
            return "unknown"
