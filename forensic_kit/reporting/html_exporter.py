"""Exportador HTML de reportes forenses con Chart.js."""

from __future__ import annotations

from pathlib import Path
from jinja2 import Environment

from .report_builder import ForensicReport


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>ForensicKit — Reporte {{ report.case_id }}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: monospace; background: #0d1117; color: #c9d1d9; padding: 20px; }
        h1 { color: #58a6ff; }
        h2 { color: #8b949e; }
        .summary { display: flex; gap: 10px; margin: 20px 0; }
        .box { padding: 15px; border-radius: 8px; text-align: center; min-width: 80px; }
        .critico { background: #8b0000; } .alto { background: #cc5500; }
        .medio { background: #ccaa00; color: #000; } .bajo { background: #228b22; }
        .info { background: #444; }
        table { border-collapse: collapse; width: 100%; margin: 10px 0; }
        th, td { border: 1px solid #30363d; padding: 8px; text-align: left; }
        th { background: #161b22; }
        canvas { max-width: 400px; margin: 20px auto; }
    </style>
</head>
<body>
    <h1>ForensicKit — Reporte de Análisis Forense</h1>
    <p><strong>Caso:</strong> {{ report.case_id }} | <strong>Examinador:</strong> {{ report.examiner }}</p>
    <p><strong>Severidad general:</strong> {{ report.overall_severity }}</p>

    <h2>Resumen</h2>
    <div class="summary">
        {% for level, count in report.summary.items() %}
        <div class="box {{ level|lower }}"><div style="font-size:1.5em">{{ count }}</div><div>{{ level }}</div></div>
        {% endfor %}
    </div>

    <canvas id="chart"></canvas>

    <h2>Hallazgos</h2>
    <table>
        <tr><th>Categoría</th><th>Detalle</th><th>Severidad</th><th>Evidencia</th></tr>
        {% for f in report.findings %}
        <tr><td>{{ f.category }}</td><td>{{ f.detail }}</td><td>{{ f.severity }}</td><td>{{ f.evidence[:100] }}</td></tr>
        {% endfor %}
    </table>

    <script>
        new Chart(document.getElementById('chart'), {
            type: 'doughnut',
            data: {
                labels: ['Critico', 'Alto', 'Medio', 'Bajo', 'Info'],
                datasets: [{
                    data: [{{ report.summary.get('Critico',0) }}, {{ report.summary.get('Alto',0) }}, {{ report.summary.get('Medio',0) }}, {{ report.summary.get('Bajo',0) }}, {{ report.summary.get('Info',0) }}],
                    backgroundColor: ['#8b0000', '#cc5500', '#ccaa00', '#228b22', '#444']
                }]
            },
            options: { plugins: { legend: { labels: { color: '#c9d1d9' } } } }
        });
    </script>
</body>
</html>
"""


def export_html(report: ForensicReport, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    env = Environment()
    template = env.from_string(HTML_TEMPLATE)
    html = template.render(report=report)

    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(html)

    return output_path
