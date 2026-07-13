"""Gestor de alcance — valida rutas/dispositivos autorizados."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ScopeEntry:
    """Entrada de alcance autorizado."""
    path: str
    note: str = ""
    allow_imaging: bool = True


@dataclass
class ScopeManager:
    """Carga y valida rutas contra un archivo JSON de alcance."""
    authorized_by: str = ""
    authorization_date: str = ""
    targets: list[ScopeEntry] = field(default_factory=list)

    @classmethod
    def from_file(cls, path: str | Path) -> ScopeManager:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Archivo de alcance no encontrado: {path}")
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        targets = [
            ScopeEntry(
                path=t["path"].strip(),
                note=t.get("note", ""),
                allow_imaging=t.get("allow_imaging", True),
            )
            for t in data.get("targets", [])
        ]
        return cls(
            authorized_by=data.get("authorized_by", ""),
            authorization_date=data.get("authorization_date", ""),
            targets=targets,
        )

    def is_authorized(self, target_path: str) -> bool:
        target_path = str(Path(target_path).resolve())
        return any(
            str(Path(t.path).resolve()) == target_path or target_path.startswith(str(Path(t.path).resolve()))
            for t in self.targets
        )

    @property
    def paths(self) -> set[str]:
        return {t.path for t in self.targets}
