from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AnalysisStatus:

    """
    The system status relating to QMDL file analysis.

    Attributes:
        finished (List[str]): The list of all finished files.
        queued (List[str]): The list of all files queued for analysis.
        running (Optional[str]): The file currently being analyzed.
    """

    finished: List[str]
    queued: List[str]
    running: Optional[str]

    @staticmethod
    def from_dict(analysis_status: dict):
        return AnalysisStatus(**analysis_status)
