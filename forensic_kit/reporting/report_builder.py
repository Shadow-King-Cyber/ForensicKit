"""Constructor de reportes forenses."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ForensicFinding:
    """Hallazgo forense."""
    category: str
    detail: str
    severity: str
    evidence: str = ""
    file_path: str = ""


@dataclass
class ForensicReport:
    """Reporte forense completo."""
    case_id: str
    examiner: str
    findings: list[ForensicFinding] = field(default_factory=list)
    summary: dict[str, int] = field(default_factory=dict)
    overall_severity: str = "Info"

    def build_summary(self) -> None:
        summary: dict[str, int] = {"Critico": 0, "Alto": 0, "Medio": 0, "Bajo": 0, "Info": 0}
        for f in self.findings:
            if f.severity in summary:
                summary[f.severity] += 1
        self.summary = summary
        values = {"Critico": 4, "Alto": 3, "Medio": 2, "Bajo": 1, "Info": 0}
        max_val = max((values.get(f.severity, 0) for f in self.findings), default=0)
        self.overall_severity = {v: k for k, v in values.items()}.get(max_val, "Info")
