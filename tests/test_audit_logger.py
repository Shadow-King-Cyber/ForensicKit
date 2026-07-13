"""Tests para AuditLogger."""

import json
from forensic_kit.core.audit_logger import AuditLogger


def test_log_crea_registro(tmp_path):
    log_path = tmp_path / "test_log.jsonl"
    logger = AuditLogger(str(log_path))
    record = logger.log("DISK_IMAGE", "/evidence/img.dd", "CREATED")
    assert record["action"] == "DISK_IMAGE"
    assert record["result"] == "CREATED"


def test_log_denegado(tmp_path):
    log_path = tmp_path / "test_log.jsonl"
    logger = AuditLogger(str(log_path))
    record = logger.log_denied("SCAN", "/evidence/forbidden")
    assert record["result"] == "DENIED_NOT_IN_SCOPE"


def test_leer_todos(tmp_path):
    log_path = tmp_path / "test_log.jsonl"
    logger = AuditLogger(str(log_path))
    logger.log("A1", "t1", "OK")
    logger.log("A2", "t2", "OK")
    assert len(logger.read_all()) == 2
