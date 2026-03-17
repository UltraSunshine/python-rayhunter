import io
import logging
import requests
import urllib.parse

from .analysis import AnalysisStatus
from .configuration import AnalyzerConfig, Config
from .manifest import QmdlManifest
from .reports import ReportMetadata
from .system_stats import SystemStats
from .time import TimeResponse


class RayhunterApi:

    @property
    def active_recording(self) -> bool:
        """
        Check the manifest file to determine if there's a recording in progress.

        :return: True if there's a "current_entry" in the manifest, else False
        """
        manifest = self.get_manifest()
        return manifest.current_entry is not None
    
    @property
    def configuration(self) -> Config:
        """
        Fetch the current runtime configuration from the target device.

        :return: An instance of `Config` populated with the current runtime configuration.
        """
        return self.get_config()
    
    @configuration.setter
    def configuration(self, config: Config):
        """
        Update the Rayhunter runtime configuration to the configuration specified in the supplied parameter. This triggers a reboot.

        :param config: An instance of `Config` populated with the desired runtime configuration.
        """
        self.set_config(config)

    def __init__(self, hostname: str, port: int):
        self._url = f"http://{hostname}:{port}/"

    def _get_file_content(self, api_endpoint: str) -> bytes:
        """
        Stream a file from the given API endpoint into memory. 

        :param api_endpoint: The endpoint from which to retrieve a file
        :return: The contents of the file (bytes)
        """
        file_content = io.BytesIO()
        file_url = urllib.parse.urljoin(self._url, api_endpoint)
        logging.info(f"Downloading file from: {file_url}")
        response = requests.get(file_url, stream=True)
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=4096):
            file_content.write(chunk)
        file_content.seek(0)
        return file_content.read()

    def delete_all_recordings(self) -> bool:
        """
        Remove all saved data capture files.

        :return: True if deletion was successful, else False
        """
        deletion_successful = False
        api_endpoint = urllib.parse.urljoin(self._url, "/api/delete-all-recordings")
        logging.info(f"Calling to delete all metadata: {api_endpoint}")
        response = requests.post(api_endpoint)
        if response.status_code == 202:
            deletion_successful = True
            logging.info("Deletion successful")
        elif response.status_code == 403:
            logging.error("Deletion action unsuccessful: device is in debug mode")
        elif response.status_code == 500:
            logging.error("Deletion action unsuccessful")
        else:
            logging.error(f"Unknown response code: {response.status_code}")
        return deletion_successful
    
    def delete_recording(self, filename: str) -> bool:
        """
        Remove a specific data capture file by name. Use `get_manifest` to identify available file names.

        :param filename: The file to delete
        :returns: True if deletion was successful, else False
        """
        deletion_successful = False
        logging.info(f"Deleting QMDL file: {filename}")
        deletion_url = urllib.parse.urljoin(self._url, f"/api/delete-recording/{filename}")
        response = requests.post(deletion_url)
        if response.status_code == 202:
            deletion_successful = True
        elif response.status_code == 400:
            logging.error("Deletion action unsuccessful: bad recording name or no such recording")
        elif response.status_code == 403:
            logging.error("Deletion action unsuccessful: device is in debug mode")
        elif response.status_code == 500:
            logging.error("Deletion action unsuccessful")
        else:
            logging.error(f"Unknown response code: {response.status_code}")
        return deletion_successful

    def get_analysis_status(self) -> AnalysisStatus:
        """
        Show analysis status for all QMDL files.

        :return: An instance of `AnalysisStatus` populated from the target device.
        """
        analysis_status_url = urllib.parse.urljoin(self._url, "/api/analysis")
        logging.info(f"Fetching analysis status from: {analysis_status_url}")
        response = requests.get(analysis_status_url)
        response.raise_for_status()
        return AnalysisStatus.from_dict(response.json())

    def get_analysis_report_file(self, filename: str) -> bytes:
        """
        Fetch a copy of the analysis report for a given capture. Use `get_manifest` to identify capture names.

        :param filename: The capture file name
        :return: The contents of the analysis report file (bytes)
        """
        logging.info(f"Fetching analysis report for capture: {filename}")
        api_endpoint = f"/api/analysis-report/{filename}"
        return self._get_file_content(api_endpoint)

    def get_config(self) -> Config:
        """
        Get the current runtime configuration for Rayhunter.

        :return: An instance of `Config` populated from the target device.
        """
        config_url = urllib.parse.urljoin(self._url, "/api/config")
        logging.info(f"Fetching configuration from: {config_url}")
        response = requests.get(config_url)
        response.raise_for_status()
        return Config.from_dict(response.json())

    def get_manifest(self) -> QmdlManifest:
        """
        Fetch a copy of the QMDL manifest, used to track the names of previous and active recordings.

        :return: An instance of `QmdlManifest` populated from the target device
        """
        manifest_url = urllib.parse.urljoin(self._url, "/api/qmdl-manifest")
        logging.info(f"Fetching manifest from: {manifest_url}")
        response = requests.get(manifest_url)
        response.raise_for_status()
        return QmdlManifest.from_dict(response.json())
    
    def get_pcap_file(self, filename: str) -> bytes:
        """
        Fetch a copy of the pcap file for a given capture. PCAP is dynamically generated from QMDL by the Rayhunter binary when this API is called.

        :param filename: The capture file name (found in manifest)
        :return: The contents of the pcap file (bytes)
        """
        logging.info(f"Fetching PCAP file for capture: {filename}")
        api_endpoint = f"/api/pcap/{filename}"
        return self._get_file_content(api_endpoint)

    def get_qmdl_file(self, filename: str) -> bytes:
        """
        Fetch a copy of the given QMDL file. Use `get_manifest` to identify QMDL capture names.

        :param filename: The QMDL file name (found in manifest)
        :return: The contents of the QMDL file (bytes)
        """
        logging.info(f"Fetching QDML file for capture: {filename}")
        api_endpoint = f"/api/qmdl/{filename}"
        return self._get_file_content(api_endpoint)
    
    def get_system_stats(self):
        """
        Fetch disk and memory utilization stats from the API.
        
        :return: An instance of `SystemStats` populated from the target device.
        """
        system_stats_url = urllib.parse.urljoin(self._url, "/api/system-stats")
        logging.info(f"Fetching system stats from: {system_stats_url}")
        response = requests.get(system_stats_url)
        response.raise_for_status()
        return SystemStats.from_dict(response.json())

    def set_config(self, config: Config):
        """
        Update the Rayhunter runtime configuration to the supplied configuration options and trigger a reboot.

        :param config: An instance of `Config` populated with the desired configuration options.
        """
        target_url = urllib.parse.urljoin(self._url, "/api/config")
        logging.info(f"Updating device configuration using URL: {target_url}")
        response = requests.post(
            url=target_url,
            json=config.to_dict()
        )
        response.raise_for_status()

    def start_recording(self):
        """
        Start a new recording. Stops the active recording and starts a new one if this device is already recording.
        """
        start_recording_url = urllib.parse.urljoin(self._url, "/api/start-recording")
        logging.info(f"Starting recording with POST request to: {start_recording_url}")
        response = requests.post(start_recording_url)
        response.raise_for_status()
    
    def stop_recording(self):
        """
        Stop an active recording. Throws a 500 error if there is no active recording.
        """
        stop_recording_url = urllib.parse.urljoin(self._url, "/api/stop-recording")
        logging.info(f"Stopping recording with POST request to: {stop_recording_url}")
        response = requests.post(stop_recording_url)
        response.raise_for_status()
