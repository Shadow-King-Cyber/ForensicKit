"""Exportador JSON de reportes forenses."""

from __future__ import annotations

import json
from pathlib import Path

from .report_builder import ForensicReport


def export_json(report: ForensicReport, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "case_id": report.case_id,
        "examiner": report.examiner,
        "overall_severity": report.overall_severity,
        "summary": report.summary,
        "findings": [
            {
                "category": f.category,
                "detail": f.detail,
                "severity": f.severity,
                "evidence": f.evidence,
                "file_path": f.file_path,
            }
            for f in report.findings
        ],
    }

    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)

    return output_path
