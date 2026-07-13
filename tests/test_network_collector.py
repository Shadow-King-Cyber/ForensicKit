"""Tests para NetworkCollector."""

from forensic_kit.collection.network_collector import collect_network_info


def test_collect_network_info():
    info = collect_network_info()
    assert hasattr(info, "interfaces")
    assert hasattr(info, "connections")
    assert hasattr(info, "arp_table")
    assert isinstance(info.interfaces, list)
