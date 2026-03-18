rayhunter.api
=============

.. autoclass:: rayhunter.api.RayhunterApi
   :show-inheritance:
   :no-members:

   .. rubric:: Properties

   .. autoproperty:: active_recording

   .. autoproperty:: configuration

   .. note::

      ``configuration`` is a read/write property.  Reading it calls
      :meth:`get_config`; assigning to it calls :meth:`set_config` and
      triggers a device reboot.

   .. rubric:: Recording control

   .. automethod:: start_recording
   .. automethod:: stop_recording

   .. rubric:: Manifest and captures

   .. automethod:: get_manifest
   .. automethod:: get_qmdl_file
   .. automethod:: get_pcap_file
   .. automethod:: get_zip
   .. automethod:: get_analysis_report_file
   .. automethod:: get_analysis_status

   .. rubric:: File management

   .. automethod:: delete_recording
   .. automethod:: delete_all_recordings

   .. rubric:: System information

   .. automethod:: get_system_stats
   .. automethod:: get_time
   .. automethod:: get_log

   .. rubric:: Configuration

   .. automethod:: get_config
   .. automethod:: set_config

   .. rubric:: Notifications

   .. automethod:: send_test_notification
