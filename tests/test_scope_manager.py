"""Tests para ScopeManager."""

import json
import pytest
from forensic_kit.core.scope_manager import ScopeManager


@pytest.fixture
def scope_file(tmp_path):
    data = {
        "authorized_by": "Forense Lead",
        "authorization_date": "2026-01-01",
        "targets": [{"path": "/evidence/case001", "note": "Lab", "allow_imaging": True}],
    }
    path = tmp_path / "scope.json"
    path.write_text(json.dumps(data))
    return path


def test_cargar_alcance(scope_file):
    sm = ScopeManager.from_file(scope_file)
    assert len(sm.targets) == 1
    assert sm.authorized_by == "Forense Lead"


def test_archivo_no_encontrado():
    with pytest.raises(FileNotFoundError):
        ScopeManager.from_file("/no/existe.json")


def test_paths_property(scope_file):
    sm = ScopeManager.from_file(scope_file)
    assert "/evidence/case001" in sm.paths
