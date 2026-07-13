"""Tests para EvidenceChain."""

from forensic_kit.core.evidence_chain import EvidenceChain


def test_record_entry():
    chain = EvidenceChain(case_id="case-001")
    entry = chain.record("created", "evidence-001", "Imagen creada")
    assert entry.evidence_id == "evidence-001"
    assert entry.action == "created"
    assert len(chain.entries) == 1


def test_to_json():
    chain = EvidenceChain(case_id="case-001")
    chain.record("created", "ev-001", "test")
    j = chain.to_json()
    assert "case-001" not in j  # entries only, not case_id
    assert "ev-001" in j


def test_save_and_load(tmp_path):
    chain = EvidenceChain(case_id="case-001")
    chain.record("created", "ev-001", "test")
    path = tmp_path / "chain.json"
    chain.save(path)
    loaded = EvidenceChain.from_json("case-001", path.read_text())
    assert len(loaded.entries) == 1
