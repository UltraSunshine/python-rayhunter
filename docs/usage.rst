Usage
=====

Installation
------------

Install via pip::

    pip install python-rayhunter

Quick Start
-----------

Connect to a Rayhunter device and interact with its API::

    from rayhunter import RayhunterApi

    api = RayhunterApi(hostname="192.168.1.1", port=8080)

    # Check if a recording is currently in progress
    if api.active_recording:
        print("Recording is active")

    # Fetch the QMDL manifest
    manifest = api.get_manifest()
    for entry in manifest.entries:
        print(f"Capture: {entry.name}, started at {entry.start_time}")

    # Download a QMDL file
    qmdl_data = api.get_qmdl_file("capture.qmdl")
    with open("capture.qmdl", "wb") as f:
        f.write(qmdl_data)

    # Download a PCAP file (dynamically generated from QMDL)
    pcap_data = api.get_pcap_file("capture.qmdl")
    with open("capture.pcap", "wb") as f:
        f.write(pcap_data)

    # Download an analysis report
    report = api.get_analysis_report_file("capture.qmdl")
    with open("report.json", "wb") as f:
        f.write(report)

Recording Control
-----------------

Start and stop recordings::

    from rayhunter import RayhunterApi

    api = RayhunterApi(hostname="192.168.1.1", port=8080)

    # Start a new recording (stops any active recording first)
    api.start_recording()

    # Stop the current recording
    api.stop_recording()

System Statistics
-----------------

Retrieve disk and memory utilization from the device::

    from rayhunter import RayhunterApi

    api = RayhunterApi(hostname="192.168.1.1", port=8080)

    stats = api.system_stats()

    disk = stats.disk_stats
    print(f"Disk partition: {disk.partition}")
    print(f"Total disk: {disk.total_size} bytes")
    print(f"Used disk:  {disk.used_size} bytes ({disk.used_percent}%)")

    mem = stats.memory_stats
    print(f"Total memory: {mem.total} bytes")
    print(f"Used memory:  {mem.used} bytes")
    print(f"Free memory:  {mem.free} bytes")
