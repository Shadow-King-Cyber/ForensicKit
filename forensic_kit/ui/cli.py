"""CLI para ForensicKit usando Click."""

from __future__ import annotations

import click

from ..core.scope_manager import ScopeManager
from ..core.audit_logger import AuditLogger
from ..collection.disk_imager import create_image, compute_hashes
from ..collection.log_collector import collect_system_logs
from ..collection.network_collector import collect_network_info
from ..analysis.metadata_extractor import extract_metadata
from ..analysis.timeline_builder import build_timeline, events_to_json
from ..analysis.hash_verifier import compute_multiple_hashes, verify_hash
from ..analysis.stego_detector import scan_file as scan_stego
from ..analysis.file_recovery import scan_for_deleted_files
from ..reporting.report_builder import ForensicReport, ForensicFinding
from ..reporting.json_exporter import export_json
from ..reporting.html_exporter import export_html


@click.group()
@click.option("--scope", default="scope.json", help="Ruta al archivo scope.json")
@click.option("--log", "log_file", default="audit_log.jsonl", help="Ruta al log de auditoría")
@click.pass_context
def cli(ctx: click.Context, scope: str, log_file: str) -> None:
    """ForensicKit — Herramienta de análisis forense digital."""
    ctx.ensure_object(dict)
    ctx.obj["logger"] = AuditLogger(log_file)


@cli.command()
@click.option("--source", required=True, help="Archivo fuente a imaginar")
@click.option("--output", required=True, help="Archivo de salida de la imagen")
@click.pass_context
def image(ctx: click.Context, source: str, output: str) -> None:
    """Crea una imagen forense con verificación hash."""
    click.echo(f"[*] Creando imagen forense de {source}...")
    result = create_image(source, output)
    ctx.obj["logger"].log("DISK_IMAGE", source, "CREATED", extra={"output": output})
    click.echo(f"[+] Imagen creada: {result.size_bytes} bytes")
    click.echo(f"  MD5:    {result.md5}")
    click.echo(f"  SHA256: {result.sha256}")
    click.echo(f"  SHA512: {result.sha512}")


@cli.command()
@click.option("--path", "file_path", required=True, help="Archivo a analizar")
@click.pass_context
def metadata(ctx: click.Context, file_path: str) -> None:
    """Extrae metadata de un archivo."""
    result = extract_metadata(file_path)
    click.echo(f"[+] Tipo: {result.file_type}")
    click.echo(f"[+] Tamaño: {result.file_size} bytes")
    click.echo(f"[+] Magic: {result.magic_bytes}")
    for k, v in result.metadata.items():
        click.echo(f"  {k}: {v}")


@cli.command()
@click.option("--path", "file_path", required=True, help="Archivo a verificar hashes")
@click.pass_context
def hashes(ctx: click.Context, file_path: str) -> None:
    """Calcula hashes de un archivo."""
    hashes_dict = compute_multiple_hashes(file_path)
    for algo, h in hashes_dict.items():
        click.echo(f"  {algo}: {h}")


@cli.command()
@click.option("--path", "dir_path", default="/", help="Directorio para timeline")
@click.option("--depth", default=3, help="Profundidad máxima")
@click.pass_context
def timeline(ctx: click.Context, dir_path: str, depth: int) -> None:
    """Construye timeline forense de un directorio."""
    click.echo(f"[*] Construyendo timeline de {dir_path}...")
    events = build_timeline(dir_path, max_depth=depth)
    click.echo(f"[+] Eventos encontrados: {len(events)}")
    for e in events[:20]:
        click.echo(f"  {e.timestamp_human} [{e.event_type}] {e.file_path}")
    if len(events) > 20:
        click.echo(f"  ... y {len(events) - 20} más")


@cli.command()
@click.option("--path", "file_path", required=True, help="Archivo a escanear")
@click.pass_context
def stego(ctx: click.Context, file_path: str) -> None:
    """Detecta esteganografía en un archivo."""
    findings = scan_stego(file_path)
    if findings:
        click.echo(f"[+] Hallazgos de esteganografía: {len(findings)}")
        for f in findings:
            click.echo(f"  [{f.confidence}] {f.technique}: {f.detail}")
    else:
        click.echo("[+] No se detectó esteganografía")


@cli.command()
@click.option("--file", "file_path", required=True, help="Imagen de disco a escanear")
@click.pass_context
def recover(ctx: click.Context, file_path: str) -> None:
    """Busca archivos eliminados en una imagen de disco."""
    click.echo(f"[*] Escaneando {file_path} para recuperar archivos...")
    found = scan_for_deleted_files(file_path)
    click.echo(f"[+] Archivos potenciales encontrados: {len(found)}")
    for f in found[:20]:
        click.echo(f"  Offset {f.offset}: {f.file_type} — {f.evidence}")


@cli.command()
@click.option("--output", default="reporte", help="Prefijo de salida")
@click.option("--format", "fmt", type=click.Choice(["json", "html", "both"]), default="both")
@click.pass_context
def report(ctx: click.Context, output: str, fmt: str) -> None:
    """Generar reporte forense."""
    report_obj = ForensicReport(case_id="case-001", examiner="forensic-kit")

    click.echo("[*] Recolectando logs del sistema...")
    logs = collect_system_logs()
    for log in logs:
        report_obj.findings.append(ForensicFinding(
            category="system_log",
            detail=f"Log recolectado: {log.path} ({log.line_count} líneas)",
            severity="Info",
            evidence=f"size={log.size_bytes}",
        ))

    report_obj.build_summary()

    if fmt in ("json", "both"):
        p = export_json(report_obj, f"{output}.json")
        click.echo(f"[+] Reporte JSON: {p}")
    if fmt in ("html", "both"):
        p = export_html(report_obj, f"{output}.html")
        click.echo(f"[+] Reporte HTML: {p}")


def main() -> None:
    """Punto de entrada principal."""
    cli(obj={})
