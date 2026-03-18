"""
Recording cycle tests.

Starts and stops three recordings, each separated by a ~1 minute wait,
and verifies that each completed recording appears in the manifest.
"""

import time

from rayhunter import RayhunterApi
from rayhunter.manifest import QmdlManifest, QmdlManifestEntry

RECORDING_DURATION_SECONDS = 60


def _run_recording_cycle(api: RayhunterApi, cycle_number: int) -> str:
    """
    Start a recording, wait RECORDING_DURATION_SECONDS, then stop it.

    Returns the name of the newly created manifest entry.
    """
    manifest_before: QmdlManifest = api.get_manifest()
    names_before: set[str] = {entry.name for entry in manifest_before.entries}

    print(f"\n[Cycle {cycle_number}] Starting recording...")
    api.start_recording()
    assert api.active_recording, (
        f"[Cycle {cycle_number}] Expected an active recording immediately after start_recording()"
    )

    print(f"[Cycle {cycle_number}] Recording active. Waiting {RECORDING_DURATION_SECONDS}s...")
    time.sleep(RECORDING_DURATION_SECONDS)

    print(f"[Cycle {cycle_number}] Stopping recording...")
    api.stop_recording()
    assert not api.active_recording, (
        f"[Cycle {cycle_number}] Expected no active recording immediately after stop_recording()"
    )

    manifest_after: QmdlManifest = api.get_manifest()
    new_entries: list[QmdlManifestEntry] = [
        entry for entry in manifest_after.entries if entry.name not in names_before
    ]

    assert len(new_entries) == 1, (
        f"[Cycle {cycle_number}] Expected exactly 1 new manifest entry after stopping, "
        f"but found {len(new_entries)}: {[e.name for e in new_entries]}"
    )

    filename = new_entries[0].name
    print(f"[Cycle {cycle_number}] New recording saved as: {filename}")
    return filename


def test_recording_cycle_1(api: RayhunterApi, recorded_filenames: list[str]):
    """Start and stop the first recording, confirming it appears in the manifest."""
    filename = _run_recording_cycle(api, cycle_number=1)
    assert filename, "Expected a non-empty filename from cycle 1"
    recorded_filenames.append(filename)


def test_recording_cycle_2(api: RayhunterApi, recorded_filenames: list[str]):
    """Start and stop the second recording, confirming it appears in the manifest."""
    filename = _run_recording_cycle(api, cycle_number=2)
    assert filename, "Expected a non-empty filename from cycle 2"
    recorded_filenames.append(filename)


def test_recording_cycle_3(api: RayhunterApi, recorded_filenames: list[str]):
    """Start and stop the third recording, confirming it appears in the manifest."""
    filename = _run_recording_cycle(api, cycle_number=3)
    assert filename, "Expected a non-empty filename from cycle 3"
    recorded_filenames.append(filename)


def test_three_recordings_in_manifest(api: RayhunterApi, recorded_filenames: list[str]):
    """Sanity-check that the manifest contains at least the three recordings we just made."""
    assert len(recorded_filenames) == 3, (
        "Internal test state error: expected 3 recorded filenames to be tracked"
    )
    manifest = api.get_manifest()
    manifest_names = {entry.name for entry in manifest.entries}
    for filename in recorded_filenames:
        assert filename in manifest_names, (
            f"Recording '{filename}' not found in manifest. "
            f"Manifest entries: {manifest_names}"
        )
