import copy

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AnalyzerConfig:

    """
    The list of supported analyzers. Each attribute corresponds to a supported analyzer and is set to `True` if the analyzer is enabled.
    """

    connection_redirect_2g_downgrade: bool
    diagnostic_analyzer: bool
    imsi_requested: bool
    incomplete_sib: bool
    lte_sib6_and_7_downgrade: bool
    nas_null_cipher: bool
    null_cipher: bool
    test_analyzer: bool

    @staticmethod
    def from_dict(analyzer_config: dict):
        return AnalyzerConfig(**analyzer_config)


@dataclass
class Config:

    """
    Rayhunter runtime configuration.

    Attributes:
        analyzers (AnalyzerConfig): Supported and enabled analyzers.
        colorblind_mode (bool): Change the color of the low and high vis displays.
        debug_mode (bool): Enhance logging.
        device (str): The internal device name.
        enabled_notifications (List[str]): A list containing the types of enabled notifications.
        key_input_mode (int): Lock or enable key inputs.
        min_space_to_start_recording_mb: The minimum space (MB) needed to continue a recording.
        min_space_to_start_recording_mb: The minimum space (MB) needed to start a recording.
        port (int): The port number to listen on.
        qmdl_store_path (str): The absolute path Rayhunter stores QMDL files.
        ui_level (int): Change the display configuration.
    """

    analyzers: AnalyzerConfig
    colorblind_mode: bool
    debug_mode: bool
    device: str
    enabled_notifications: List[str]
    key_input_mode: int
    min_space_to_continue_recording_mb: int
    min_space_to_start_recording_mb: int
    ntfy_url: Optional[str]
    port: int
    qmdl_store_path: str
    ui_level: int

    def to_dict(self) -> dict:
        """
        Convert this thing back to a dict so it can be POSTed back to the device.
        """
        runtime_config = copy.deepcopy(self.__dict__)
        runtime_config["analyzers"] = runtime_config["analyzers"].__dict__
        return runtime_config

    @staticmethod
    def from_dict(config: dict):
        config["analyzers"] = AnalyzerConfig.from_dict(config["analyzers"])
        return Config(**config)
