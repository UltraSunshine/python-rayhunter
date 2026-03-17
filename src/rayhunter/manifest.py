from dataclasses import dataclass
from typing import List, Optional


@dataclass
class QmdlManifestEntry:

    """Metadata for a single QMDL capture file.

    Attributes:
        arch (str): The architecture on which the OS was running.
        last_message_time (str): The timestamp of the last message captured in this file.
        name (str): The name of the QMDL file.
        qmdl_size_bytes (int): The total size in bytes of this QMDL file.
        rayhunter_version (str): The rayhunter daemon version which generated the file.
        start_time (str): The start time of this capture file.    
        stop_reason (Optional[str]): The reason this capture was stopped, if it's stopped.
        system_os (str): The OS version that created this file.
    """

    arch: str
    last_message_time: str
    name: str
    qmdl_size_bytes: int
    rayhunter_version: str
    start_time: str
    stop_reason: Optional[str]
    system_os: str


@dataclass
class QmdlManifest:

    """A collection of metadata for all QMDL capture files available on this system.

    Attributes:
        entries (List[QmdlManifestEntry]): A list of metadata for all finalized QMDL capture files available on this system.
        current_entry (Optional[QmdlManifestEntry]): An optional value containing information on the active capture, or `None` if there is no active capture.
    
    """

    entries: List[QmdlManifestEntry]
    current_entry: Optional[QmdlManifestEntry]

    @staticmethod
    def from_dict(qmdl_manifest: dict):
        qmdl_manifest["entries"] = [QmdlManifestEntry(**x) for x in qmdl_manifest["entries"]]
        if qmdl_manifest["current_entry"] is not None:
            qmdl_manifest["current_entry"] = QmdlManifestEntry(**qmdl_manifest["current_entry"])
        return QmdlManifest(**qmdl_manifest)
