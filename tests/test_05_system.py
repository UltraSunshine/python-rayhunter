"""
System API tests.

Verifies that the time, time offset, system stats, and log endpoints
can be reached and their responses correctly deserialized.
"""

from rayhunter import RayhunterApi
from rayhunter.system_stats import SystemStats, DiskStats, MemoryStats, RuntimeMetadata
from rayhunter.time import TimeResponse


def test_get_time(api: RayhunterApi):
    """Fetch the current time from the device and verify all fields deserialize correctly."""
    response = api.get_time()

    assert isinstance(response, TimeResponse), (
        "Expected get_time() to return a TimeResponse instance"
    )
    assert isinstance(response.adjusted_time, str) and response.adjusted_time, (
        "Expected adjusted_time to be a non-empty string"
    )
    assert isinstance(response.system_time, str) and response.system_time, (
        "Expected system_time to be a non-empty string"
    )
    assert isinstance(response.offset_seconds, int), (
        "Expected offset_seconds to be an int"
    )

    print(f"\nTime — system: {response.system_time}, adjusted: {response.adjusted_time}, offset: {response.offset_seconds}s")


def test_get_time_offset(api: RayhunterApi):
    """Fetch the time offset from the device and verify it is an integer."""
    offset = api.get_time_offset()

    assert isinstance(offset, int), (
        f"Expected get_time_offset() to return an int, got {type(offset).__name__}"
    )

    print(f"\nTime offset: {offset}s")


def test_get_system_stats(api: RayhunterApi):
    """Fetch system stats from the device and verify all nested fields deserialize correctly."""
    stats = api.get_system_stats()

    assert isinstance(stats, SystemStats), (
        "Expected get_system_stats() to return a SystemStats instance"
    )

    assert isinstance(stats.disk_stats, DiskStats), (
        "Expected disk_stats to be a DiskStats instance"
    )
    assert stats.disk_stats.total_size > 0, "Expected total disk size to be greater than 0"
    assert stats.disk_stats.used_size >= 0, "Expected used disk size to be non-negative"
    assert stats.disk_stats.available_size >= 0, "Expected available disk size to be non-negative"
    assert isinstance(stats.disk_stats.partition, str) and stats.disk_stats.partition, (
        "Expected partition to be a non-empty string"
    )

    assert isinstance(stats.memory_stats, MemoryStats), (
        "Expected memory_stats to be a MemoryStats instance"
    )
    assert stats.memory_stats.total > 0, "Expected total memory to be greater than 0"
    assert stats.memory_stats.used >= 0, "Expected used memory to be non-negative"
    assert stats.memory_stats.free >= 0, "Expected free memory to be non-negative"

    assert isinstance(stats.runtime_metadata, RuntimeMetadata), (
        "Expected runtime_metadata to be a RuntimeMetadata instance"
    )
    assert isinstance(stats.runtime_metadata.arch, str) and stats.runtime_metadata.arch, (
        "Expected arch to be a non-empty string"
    )
    assert isinstance(stats.runtime_metadata.rayhunter_version, str) and stats.runtime_metadata.rayhunter_version, (
        "Expected rayhunter_version to be a non-empty string"
    )
    assert isinstance(stats.runtime_metadata.system_os, str) and stats.runtime_metadata.system_os, (
        "Expected system_os to be a non-empty string"
    )

    print(
        f"\nSystem stats — arch: {stats.runtime_metadata.arch}, "
        f"rayhunter: {stats.runtime_metadata.rayhunter_version}, "
        f"disk: {stats.disk_stats.used_size:,}/{stats.disk_stats.total_size:,} bytes, "
        f"memory: {stats.memory_stats.used:,}/{stats.memory_stats.total:,} bytes"
    )


def test_get_log(api: RayhunterApi):
    """Retrieve the device log and verify it is non-empty, valid UTF-8 text."""
    data = api.get_log()

    assert isinstance(data, bytes), "Expected get_log() to return bytes"
    assert len(data) > 0, "Expected log file to be non-empty"

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as e:
        raise AssertionError(f"Log file is not valid UTF-8: {e}") from e

    assert len(text.strip()) > 0, "Expected log file to contain non-whitespace content"

    print(f"\nLog size: {len(data):,} bytes, first line: {text.splitlines()[0]!r}")
