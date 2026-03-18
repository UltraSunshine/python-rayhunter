"""
File download tests.

Downloads QMDL, PCAP, and ZIP files for a completed recording and verifies
each file is non-empty and has the expected format.
"""

import zipfile
import io

from rayhunter import RayhunterApi

_PCAP_MAGIC_LE = b"\xd4\xc3\xb2\xa1"
_PCAP_MAGIC_BE = b"\xa1\xb2\xc3\xd4"
_PCAPNG_MAGIC = b"\x0a\x0d\x0d\x0a"
_ZIP_MAGIC = b"PK"


def test_download_qmdl(api: RayhunterApi, recorded_filenames: list[str]):
    """Download a QMDL file for the first recorded capture and verify it is non-empty."""
    assert recorded_filenames, "No recorded filenames available — recording tests must run first"
    filename = recorded_filenames[0]
    print(f"\nDownloading QMDL for: {filename}")

    data = api.get_qmdl_file(filename)

    assert isinstance(data, bytes), "Expected get_qmdl_file() to return bytes"
    assert len(data) > 0, f"Downloaded QMDL file for '{filename}' is empty"
    print(f"QMDL size: {len(data):,} bytes")


def test_download_pcap(api: RayhunterApi, recorded_filenames: list[str]):
    """Download a PCAP file for the first recorded capture and verify format and content."""
    assert recorded_filenames, "No recorded filenames available — recording tests must run first"
    filename = recorded_filenames[0]
    print(f"\nDownloading PCAP for: {filename}")

    data = api.get_pcap_file(filename)

    assert isinstance(data, bytes), "Expected get_pcap_file() to return bytes"
    assert len(data) > 0, f"Downloaded PCAP file for '{filename}' is empty"

    valid_pcap_magic = (
        data[:4] in (_PCAP_MAGIC_LE, _PCAP_MAGIC_BE)
        or data[:4] == _PCAPNG_MAGIC
    )
    assert valid_pcap_magic, (
        f"PCAP file does not start with a recognised magic number. "
        f"Got: {data[:4].hex()}"
    )
    print(f"PCAP size: {len(data):,} bytes")


def test_download_zip(api: RayhunterApi, recorded_filenames: list[str]):
    """Download a ZIP archive for the first recorded capture and verify it is a valid ZIP."""
    assert recorded_filenames, "No recorded filenames available — recording tests must run first"
    filename = recorded_filenames[0]
    print(f"\nDownloading ZIP for: {filename}")

    data = api.get_zip(filename)

    assert isinstance(data, bytes), "Expected get_zip() to return bytes"
    assert len(data) > 0, f"Downloaded ZIP file for '{filename}' is empty"
    assert data[:2] == _ZIP_MAGIC, (
        f"ZIP file does not start with the PK magic number. Got: {data[:2].hex()}"
    )

    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        names = zf.namelist()
        assert len(names) > 0, "ZIP archive contains no files"
        print(f"ZIP size: {len(data):,} bytes, contents: {names}")
