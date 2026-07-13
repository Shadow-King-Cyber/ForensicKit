"""Recolección de estado de red."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class NetworkInfo:
    """Información de red recolectada."""
    interfaces: list[dict[str, str]]
    connections: list[dict[str, str]]
    arp_table: list[dict[str, str]]


def collect_network_info() -> NetworkInfo:
    """Recolecta estado actual de la red del sistema."""
    interfaces = _get_interfaces()
    connections = _get_connections()
    arp = _get_arp_table()

    return NetworkInfo(
        interfaces=interfaces,
        connections=connections,
        arp_table=arp,
    )


def _get_interfaces() -> list[dict[str, str]]:
    interfaces: list[dict[str, str]] = []
    try:
        import psutil
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        for name, addr_list in addrs.items():
            info = {"name": name, "addresses": []}
            for addr in addr_list:
                info["addresses"].append({
                    "family": str(addr.family),
                    "address": addr.address,
                    "netmask": addr.netmask,
                })
            if name in stats:
                info["is_up"] = str(stats[name].isup)
                info["speed"] = str(stats[name].speed)
            interfaces.append(info)
    except ImportError:
        interfaces.append({"name": "unknown", "note": "psutil no disponible"})
    return interfaces


def _get_connections() -> list[dict[str, str]]:
    connections: list[dict[str, str]] = []
    try:
        import psutil
        for conn in psutil.net_connections():
            connections.append({
                "local": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "",
                "remote": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "",
                "status": conn.status,
                "pid": str(conn.pid) if conn.pid else "",
            })
    except (ImportError, PermissionError):
        connections.append({"note": "psutil no disponible o sin permisos"})
    return connections


def _get_arp_table() -> list[dict[str, str]]:
    arp: list[dict[str, str]] = []
    try:
        import psutil
        # psutil no tiene ARP directamente, usar datos simulados
        arp.append({"note": "Requiere implementación específica por SO"})
    except ImportError:
        pass
    return arp
