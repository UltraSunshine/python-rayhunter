"""
Deletion tests.

Deletes a single recording by name, then deletes all remaining recordings,
verifying the manifest reflects each operation.
"""

from rayhunter import RayhunterApi


def test_delete_single_recording(api: RayhunterApi, recorded_filenames: list[str]):
    """Delete the first recorded capture by name and confirm it is removed from the manifest."""
    assert recorded_filenames, "No recorded filenames available — recording tests must run first"
    filename = recorded_filenames[0]
    print(f"\nDeleting recording: {filename}")

    result = api.delete_recording(filename)

    assert result is True, (
        f"delete_recording('{filename}') returned False — deletion may have failed"
    )

    manifest = api.get_manifest()
    remaining_names = {entry.name for entry in manifest.entries}
    assert filename not in remaining_names, (
        f"Recording '{filename}' still present in manifest after deletion. "
        f"Manifest entries: {remaining_names}"
    )

    for still_present in recorded_filenames[1:]:
        assert still_present in remaining_names, (
            f"Recording '{still_present}' was unexpectedly removed during single-file deletion"
        )

    print(f"Recording '{filename}' successfully deleted")


def test_delete_all_recordings(api: RayhunterApi):
    """Delete all recordings and confirm the manifest entries list is empty."""
    if api.active_recording:
        api.stop_recording()

    print("\nDeleting all recordings...")
    result = api.delete_all_recordings()

    assert result is True, "delete_all_recordings() returned False — deletion may have failed"

    manifest = api.get_manifest()
    assert len(manifest.entries) == 0, (
        f"Expected manifest to be empty after delete_all_recordings(), "
        f"but {len(manifest.entries)} entries remain: "
        f"{[e.name for e in manifest.entries]}"
    )
    assert manifest.current_entry is None, (
        "Expected no active recording after delete_all_recordings()"
    )

    print("All recordings deleted. Manifest is empty.")
