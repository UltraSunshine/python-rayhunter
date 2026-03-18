# python-rayhunter

Unofficial Python bindings for EFF's [Rayhunter](https://github.com/EFForg/rayhunter) API.

> **Note:** This project is not affiliated with the EFF or the Rayhunter project.

## Compatibility

This library version is compatible with **version 0.10.2** of the Rayhunter API. I'll keep this library current as I update my own devices, but please open an issue if you notice any compatibility issues with newer versions before I get around to fixing them!

## Documentation

Full documentation can be found on [Read The Docs](https://python-rayhunter.readthedocs.io/en/latest/index.html).

## Requirements

- Python >= 3.11
- [requests](https://pypi.org/project/requests/) >= 2.32.2

## Installation

```bash
pip install python-rayhunter
```

## Quick Start

```python
from rayhunter import RayhunterApi

api = RayhunterApi(hostname="192.168.1.1", port=8080)
```

## Usage

### Check recording status

```python
if api.active_recording:
    print("A recording is currently in progress")
```

### Fetch the QMDL manifest

The manifest lists all capture files available on the device, plus the active capture (if any).

```python
manifest = api.get_manifest()

for entry in manifest.entries:
    print(f"{entry.name} — started {entry.start_time}, size {entry.qmdl_size_bytes} bytes")

if manifest.current_entry:
    print(f"Active capture: {manifest.current_entry.name}")
```

### Download capture files

Use the filenames from the manifest to download files.

```python
# Raw QMDL capture data
qmdl_data = api.get_qmdl_file("capture.qmdl")

# PCAP file (dynamically generated from QMDL by the Rayhunter binary)
pcap_data = api.get_pcap_file("capture.qmdl")

# Analysis report
report_data = api.get_analysis_report_file("capture.qmdl")

# ZIP containing both the QMDL and the generated PCAP
zip_data = api.get_zip("capture.qmdl")
```

### Control recordings

```python
# Start a new recording (stops any active recording first)
api.start_recording()

# Stop the current recording
api.stop_recording()

# Delete a specific recording
api.delete_recording("capture.qmdl")

# Delete all recordings (not available in debug mode)
api.delete_all_recordings()
```

### System statistics

```python
stats = api.get_system_stats()

disk = stats.disk_stats
print(f"Partition:  {disk.partition} ({disk.mounted_on})")
print(f"Disk usage: {disk.used_size}/{disk.total_size} bytes ({disk.used_percent}% used)")

mem = stats.memory_stats
print(f"Memory:     {mem.used}/{mem.total} bytes used, {mem.free} bytes free")

meta = stats.runtime_metadata
print(f"Rayhunter {meta.rayhunter_version} on {meta.system_os} ({meta.arch})")

if stats.battery_status:
    bat = stats.battery_status
    print(f"Battery: {bat.level}% {'(charging)' if bat.is_plugged_in else ''}")
```

### Configuration

> **Warning:** Setting the configuration triggers a device reboot.

```python
# Read/write via property
config = api.configuration
config.debug_mode = True
api.configuration = config

# Or use the explicit methods
config = api.get_config()
config.colorblind_mode = True
api.set_config(config)
```

### Analysis status

```python
status = api.get_analysis_status()

print("Finished:", status.finished)
print("Queued:  ", status.queued)
if status.running:
    print("Running: ", status.running)
```

### Time

```python
t = api.get_time()
print(f"System time: {t.system_time}")
print(f"Adjusted time (+{t.offset_seconds}s): {t.adjusted_time}")
```

### Notifications

```python
api.send_test_notification()
```

### Device log

```python
log_bytes = api.get_log()
print(log_bytes.decode("utf-8"))
```

## API Reference

### `RayhunterApi(hostname, port)`

The main client for interacting with the Rayhunter API.

| Method / Property | Returns | Description |
|---|---|---|
| `active_recording` | `bool` | `True` if a recording is currently in progress |
| `configuration` | `Config` | Read/write property for runtime configuration (setter triggers reboot) |
| `start_recording()` | — | Start a new recording (stops any active recording first) |
| `stop_recording()` | — | Stop the active recording |
| `get_manifest()` | `QmdlManifest` | Fetch the QMDL manifest from the device |
| `get_qmdl_file(filename)` | `bytes` | Download a raw QMDL capture file |
| `get_pcap_file(filename)` | `bytes` | Download a PCAP file (generated on demand) |
| `get_zip(filename)` | `bytes` | Download a ZIP containing the QMDL and generated PCAP |
| `get_analysis_report_file(filename)` | `bytes` | Download the analysis report for a capture |
| `get_analysis_status()` | `AnalysisStatus` | Show analysis status for all QMDL files |
| `delete_recording(filename)` | `bool` | Delete a specific recording |
| `delete_all_recordings()` | `bool` | Delete all recordings (unavailable in debug mode) |
| `get_system_stats()` | `SystemStats` | Fetch disk, memory, and battery stats |
| `get_time()` | `TimeResponse` | Get device time and offset |
| `get_log()` | `bytes` | Download the device log (UTF-8 plaintext) |
| `get_config()` | `Config` | Get the current runtime configuration |
| `set_config(config)` | — | Update runtime configuration (triggers reboot) |
| `send_test_notification()` | — | Send a test notification to the configured ntfy URL |

### `QmdlManifest`

| Attribute | Type | Description |
|---|---|---|
| `entries` | `List[QmdlManifestEntry]` | All finalised capture files on the device |
| `current_entry` | `Optional[QmdlManifestEntry]` | The active capture, or `None` |

### `QmdlManifestEntry`

| Attribute | Type | Description |
|---|---|---|
| `arch` | `str` | Architecture the OS was running on |
| `last_message_time` | `str` | Timestamp of the last captured message |
| `name` | `str` | Capture file name |
| `qmdl_size_bytes` | `int` | Size of the QMDL file in bytes |
| `rayhunter_version` | `str` | Rayhunter daemon version that generated the file |
| `start_time` | `str` | Timestamp when the capture started |
| `stop_reason` | `Optional[str]` | Reason the capture was stopped, if stopped |
| `system_os` | `str` | OS version that created the file |

### `AnalysisStatus`

| Attribute | Type | Description |
|---|---|---|
| `finished` | `List[str]` | Files that have been analyzed |
| `queued` | `List[str]` | Files queued for analysis |
| `running` | `Optional[str]` | File currently being analyzed |

### `Config`

| Attribute | Type | Description |
|---|---|---|
| `analyzers` | `AnalyzerConfig` | Supported and enabled analyzers |
| `colorblind_mode` | `bool` | Change the color of the low and high vis displays |
| `debug_mode` | `bool` | Enhance logging |
| `device` | `str` | Internal device name |
| `enabled_notifications` | `List[str]` | Types of enabled notifications |
| `key_input_mode` | `int` | Lock or enable key inputs |
| `min_space_to_continue_recording_mb` | `int` | Minimum space (MB) needed to continue a recording |
| `min_space_to_start_recording_mb` | `int` | Minimum space (MB) needed to start a recording |
| `ntfy_url` | `Optional[str]` | URL for ntfy push notifications |
| `port` | `int` | Port number to listen on |
| `qmdl_store_path` | `str` | Absolute path where Rayhunter stores QMDL files |
| `ui_level` | `int` | Display configuration |

| Method | Returns | Description |
|---|---|---|
| `to_dict()` | `dict` | Convert to a dict for POSTing back to the device |

### `AnalyzerConfig`

Each attribute corresponds to a supported analyzer and is set to `True` if enabled.

| Attribute | Type |
|---|---|
| `connection_redirect_2g_downgrade` | `bool` |
| `diagnostic_analyzer` | `bool` |
| `imsi_requested` | `bool` |
| `incomplete_sib` | `bool` |
| `lte_sib6_and_7_downgrade` | `bool` |
| `nas_null_cipher` | `bool` |
| `null_cipher` | `bool` |
| `test_analyzer` | `bool` |

### `SystemStats`

| Attribute | Type | Description |
|---|---|---|
| `battery_status` | `Optional[BatteryState]` | Battery information (if available) |
| `disk_stats` | `DiskStats` | Disk usage information |
| `memory_stats` | `MemoryStats` | Memory usage information |
| `runtime_metadata` | `RuntimeMetadata` | System and binary information |

### `DiskStats`

| Attribute | Type | Description |
|---|---|---|
| `available_bytes` | `Optional[int]` | Available disk space in bytes |
| `available_size` | `int` | Available disk space in bytes (converted from string) |
| `mounted_on` | `str` | Mount point (e.g. `/data`) |
| `partition` | `str` | Partition Rayhunter is mounted on (e.g. `ubi0:usrfs`) |
| `total_size` | `int` | Total disk size in bytes |
| `used_percent` | `int` | Percentage of disk space in use |
| `used_size` | `int` | Used disk space in bytes |

### `MemoryStats`

| Attribute | Type | Description |
|---|---|---|
| `total` | `int` | Total memory in bytes |
| `used` | `int` | Used memory in bytes |
| `free` | `int` | Free memory in bytes |

### `BatteryState`

| Attribute | Type | Description |
|---|---|---|
| `is_plugged_in` | `bool` | Whether the battery is currently being charged |
| `level` | `int` | Battery level as a percentage |

### `RuntimeMetadata`

| Attribute | Type | Description |
|---|---|---|
| `arch` | `str` | CPU architecture (e.g. `armv7l`) |
| `rayhunter_version` | `str` | Rayhunter cargo package version |
| `system_os` | `str` | Operating system sysname and release |

### `TimeResponse`

| Attribute | Type | Description |
|---|---|---|
| `adjusted_time` | `str` | Adjusted time (system time + offset) |
| `offset_seconds` | `int` | Current offset in seconds |
| `system_time` | `str` | Raw system time (without clock offset) |

### `ReportMetadata`

| Attribute | Type | Description |
|---|---|---|
| `analyzers` | `List[AnalyzerMetadata]` | Analyzers in use for this analysis |
| `rayhunter` | `RuntimeMetadata` | Runtime metadata during recording and analysis |
| `report_version` | `int` | Version of the reporting format |

### `AnalyzerMetadata`

| Attribute | Type | Description |
|---|---|---|
| `description` | `str` | Description of what the analyzer does |
| `name` | `str` | Analyzer name |
| `version` | `int` | Deployed version of the analyzer code |

### `Device`

Enumeration of supported device types (`IntEnum`).

| Value | Int |
|---|---|
| `orbic` | 0 |
| `tplink` | 1 |
| `tmobile` | 2 |
| `wingtech` | 3 |
| `pinephone` | 4 |
| `us801` | 5 |

### `EventType`

Event severity levels (`IntEnum`).

| Value | Int |
|---|---|
| `Informational` | 0 |
| `Low` | 1 |
| `Medium` | 2 |
| `High` | 3 |

### `NotificationType`

Notification types (`IntEnum`).

| Value | Int |
|---|---|
| `Warning` | 0 |
| `LowBattery` | 1 |

## License

Since "do what you'd like and don't blame me," isn't necessarily legally binding, this repository uses the [MIT LICENSE](LICENSE).
