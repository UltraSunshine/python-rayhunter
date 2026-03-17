from .system_stats import RuntimeMetadata
from dataclasses import dataclass
from typing import List


@dataclass
class AnalyzerMetadata:

    """
    Specific information on a given analyzer.

    Attributes:
        description (str): A description of what the analyzer does.
        name (str): The analyzer name.
        version (int): The deployed version of the analyzer code.
    """

    description: str
    name: str
    version: int

    @staticmethod
    def from_dict(analyzer_metadata: dict):
        return AnalyzerMetadata(**analyzer_metadata)


@dataclass
class ReportMetadata:

    """
    The metadata for an analyzed report.

    Attributes:
        analyzers (List[AnalyzerMetadata]): A list of analyzers were in use for this analysis.
        rayhunter (RuntimeMetadata):The runtime metadata for rayhunter during the recording and analysis.
        report_version (int): The version of the reporting format used for this analysis.
    """

    analyzers: List[AnalyzerMetadata]
    rayhunter: RuntimeMetadata
    report_version: int

    @staticmethod
    def from_dict(report_metadata: dict):
        return ReportMetadata(
            analyzers=[AnalyzerMetadata.from_dict(x) for x in report_metadata["analyzers"]],
            rayhunter=RuntimeMetadata.from_dict(report_metadata["rayhunter"]),
            report_version=report_metadata["report_version"]
        )
