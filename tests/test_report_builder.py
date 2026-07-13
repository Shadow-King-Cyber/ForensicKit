"""Tests para ReportBuilder."""

from forensic_kit.reporting.report_builder import ForensicReport, ForensicFinding


def test_build_summary():
    report = ForensicReport(case_id="c001", examiner="test")
    report.findings.append(ForensicFinding(category="a", detail="d", severity="Critico"))
    report.findings.append(ForensicFinding(category="b", detail="d", severity="Alto"))
    report.findings.append(ForensicFinding(category="c", detail="d", severity="Info"))
    report.build_summary()
    assert report.summary["Critico"] == 1
    assert report.summary["Alto"] == 1
    assert report.overall_severity == "Critico"


def test_summary_vacio():
    report = ForensicReport(case_id="c001", examiner="test")
    report.build_summary()
    assert report.overall_severity == "Info"
    assert all(v == 0 for v in report.summary.values())
