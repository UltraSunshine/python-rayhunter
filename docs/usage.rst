Usage Guide
===========

Installation
------------

.. code-block:: bash

   pip install python-rayhunter

Requirements
~~~~~~~~~~~~

- Python >= 3.11
- `requests <https://pypi.org/project/requests/>`_ >= 2.32.2

Quick Start
-----------

All interaction with a Rayhunter device happens through :class:`~rayhunter.api.RayhunterApi`.
Instantiate it with the hostname (or IP address) and port of your device:

.. code-block:: python

   from rayhunter import RayhunterApi

   api = RayhunterApi(hostname="192.168.1.1", port=8080)

Checking Recording Status
-------------------------

The :attr:`~rayhunter.api.RayhunterApi.active_recording` property returns ``True`` if a
capture is currently in progress:

.. code-block:: python

   if api.active_recording:
       print("A recording is currently in progress")

Fetching the QMDL Manifest
---------------------------

The manifest lists all capture files available on the device, plus the currently active
capture (if any).  Use :meth:`~rayhunter.api.RayhunterApi.get_manifest` to retrieve it:

.. code-block:: python

   manifest = api.get_manifest()

   for entry in manifest.entries:
       print(f"{entry.name} — started {entry.start_time}, size {entry.qmdl_size_bytes} bytes")

   if manifest.current_entry:
       print(f"Active capture: {manifest.current_entry.name}")

Downloading Capture Files
-------------------------

Use the filenames from the manifest to download raw captures, PCAP files, or analysis
reports.

.. code-block:: python

   # Raw QMDL capture data
   qmdl_data = api.get_qmdl_file("capture.qmdl")

   # PCAP file (dynamically generated from QMDL by the Rayhunter binary)
   pcap_data = api.get_pcap_file("capture.qmdl")

   # Analysis report
   report_data = api.get_analysis_report_file("capture.qmdl")

   # ZIP containing both the QMDL and the generated PCAP
   zip_data = api.get_zip("capture.qmdl")

Controlling Recordings
----------------------

.. code-block:: python

   # Start a new recording (stops any active recording first)
   api.start_recording()

   # Stop the current recording
   api.stop_recording()

   # Delete a specific recording
   api.delete_recording("capture.qmdl")

   # Delete all recordings (not available in debug mode)
   api.delete_all_recordings()

System Statistics
-----------------

:meth:`~rayhunter.api.RayhunterApi.get_system_stats` returns a
:class:`~rayhunter.system_stats.SystemStats` object containing disk, memory, and
battery information:

.. code-block:: python

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

Configuration
-------------

Read and update the runtime configuration of a connected device using the
:attr:`~rayhunter.api.RayhunterApi.configuration` property or the lower-level
:meth:`~rayhunter.api.RayhunterApi.get_config` /
:meth:`~rayhunter.api.RayhunterApi.set_config` methods.

.. warning::

   Setting the configuration triggers a device reboot.

.. code-block:: python

   config = api.configuration          # fetch current config
   config.debug_mode = True
   api.configuration = config          # push updated config (reboots device)

Analysis Status
---------------

Check which QMDL files have been analyzed, are queued, or are currently being processed:

.. code-block:: python

   status = api.get_analysis_status()

   print("Finished:", status.finished)
   print("Queued:  ", status.queued)
   if status.running:
       print("Running: ", status.running)

Time
----

Retrieve the device clock and its current offset:

.. code-block:: python

   t = api.get_time()
   print(f"System time: {t.system_time}")
   print(f"Adjusted time (+{t.offset_seconds}s): {t.adjusted_time}")

Notifications
-------------

Trigger a test notification to the ``ntfy_url`` configured on the device:

.. code-block:: python

   api.send_test_notification()

Device Log
----------

Download the current device log as raw bytes (UTF-8 plaintext):

.. code-block:: python

   log_bytes = api.get_log()
   print(log_bytes.decode("utf-8"))
