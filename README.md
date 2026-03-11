# python-rayhunter

Unofficial Python bindings for EFF's [Rayhunter](https://github.com/EFForg/rayhunter) API.

> **Note:** This project is not affiliated with the EFF or the Rayhunter project.


## Documentation

Full documentation can be found on [Read The Docs](https://python-rayhunter.readthedocs.io/en/latest/index.html). Please read them, I worked hard on them.

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
```

### Control recordings

```python
# Start a new recording (stops any active recording first)
api.start_recording()

# Stop the current recording
api.stop_recording()
```

### System statistics

```python
stats = api.system_stats()

disk = stats.disk_stats
print(f"Partition:  {disk.partition} ({disk.mounted_on})")
print(f"Disk usage: {disk.used_size}/{disk.total_size} bytes ({disk.used_percent}% used)")

mem = stats.memory_stats
print(f"Memory:     {mem.used}/{mem.total} bytes used, {mem.free} bytes free")
```

## API Reference

### `RayhunterApi(hostname, port)`

The main client for interacting with the Rayhunter API.

| Method | Returns | Description |
|---|---|---|
| `active_recording` | `bool` | `True` if a recording is currently in progress |
| `get_manifest()` | `QmdlManifest` | Fetch the QMDL manifest from the device |
| `get_qmdl_file(filename)` | `bytes` | Download a raw QMDL capture file |
| `get_pcap_file(filename)` | `bytes` | Download a PCAP file (generated on demand) |
| `get_analysis_report_file(filename)` | `bytes` | Download the analysis report for a capture |
| `start_recording()` | — | Start a new recording |
| `stop_recording()` | — | Stop the active recording |
| `system_stats()` | `SystemStats` | Fetch disk and memory utilisation stats |

### `QmdlManifest`

| Attribute | Type | Description |
|---|---|---|
| `entries` | `List[QmdlManifestEntry]` | All finalised capture files on the device |
| `current_entry` | `Optional[QmdlManifestEntry]` | The active capture, or `None` |

### `QmdlManifestEntry`

| Attribute | Type | Description |
|---|---|---|
| `name` | `str` | Capture file name |
| `start_time` | `str` | Timestamp when the capture started |
| `last_message_time` | `str` | Timestamp of the last captured message |
| `qmdl_size_bytes` | `int` | Size of the QMDL file in bytes |
| `analysis_size_bytes` | `int` | Size of the associated analysis file in bytes |

### `SystemStats`

| Attribute | Type | Description |
|---|---|---|
| `disk_stats` | `DiskStats` | Disk usage information |
| `memory_stats` | `MemoryStats` | Memory usage information |

### `DiskStats`

| Attribute | Type | Description |
|---|---|---|
| `partition` | `str` | Partition Rayhunter is mounted on (e.g. `ubi0:usrfs`) |
| `total_size` | `int` | Total disk size in bytes |
| `used_size` | `int` | Used disk space in bytes |
| `available_size` | `int` | Available disk space in bytes |
| `used_percent` | `int` | Percentage of disk space in use |
| `mounted_on` | `str` | Mount point (e.g. `/data`) |

### `MemoryStats`

| Attribute | Type | Description |
|---|---|---|
| `total` | `int` | Total memory in bytes |
| `used` | `int` | Used memory in bytes |
| `free` | `int` | Free memory in bytes |

## License

Since "do what you'd like and don't blame me," isn't necessarily legally binding, this repository uses the [MIT LICENSE](LICENSE).
