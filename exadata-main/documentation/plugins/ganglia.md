# Ganglia
The Ganglia plugin connects to the Ganglia server (gmond), collects and translates the data payload (XML) to the ExaMon data model.

NOTE: the sampling period of the metrics has high variability, patterns are different across nodes. **The reported values are an approximation**.

## Plugin-specific columns

|Column|Description|
|------|-----------|
|node|The hostname of the server|

## Metrics
|Metric|Description|Group|Unit|Value type|Sampling period|
|------|-----------|-----|----|----------|---------------|
|GpuX_boar	int	~20s (per node)
GpuX_ecc_dbe_volatile_total	Total double bit volatile ECC errors	gpu	d_limit_violation|Board violation limit (X=0,..,3)|gpu|_|int|~20s (per node)|
|GpuX_current_clock_throttle_reasons|Current clock throttle reasons (bitmask of DCGM_CLOCKS_THROTTLE_REASON_*)|gpu|_|int|~20s (per node)|
|GpuX_ecc_dbe_aggregate_total|Total double bit aggregate (persistent) ECC errors Note: monotonically increasing|gpu|_|int|~20s (per node)|
|GpuX_ecc_dbe_volatile_total|Total double bit volatile ECC errors|gpu|_|int|~20s (per node)|
|GpuX_ecc_sbe_aggregate_total|Total single bit aggregate (persistent) ECC errors Note: monotonically increasing|gpu|_|int|~20s (per node)|
|GpuX_ecc_sbe_volatile_total|Total single bit volatile ECC errors|gpu|_|int|~20s (per node)|
|GpuX_fb_free|Free Frame Buffer in MB|gpu|mb|int|~20s (per node)|
|GpuX_fb_total|Total Frame Buffer of the GPU in MB|gpu|mb|int|~20s (per node)|
|GpuX_fb_used|Used Frame Buffer in MB|gpu|mb|int|~20s (per node)|
|GpuX_gpu_temp|Current temperature readings for the device, in degrees C|gpu|celsius|int|~20s (per node)|
|GpuX_gpu_util_samples|GPU Utilization samples|gpu|_|int|~20s (per node)|
|GpuX_gpu_utilization|GPU Utilization|gpu|%|int|~20s (per node)|
|GpuX_low_util_violation|Low utilisation violation limit|gpu|_|int|~20s (per node)|
|GpuX_mem_app_clock|Memory Application clocks|gpu|_|int|~20s (per node)|
|GpuX_mem_copy_utilization|Memory Utilization|gpu|%|int|~20s (per node)|
|GpuX_memory_clock|Memory clock for the device|gpu|megahertz|int|~20s (per node)|
|GpuX_memory_temp|Memory temperature for the device|gpu|celsius|int|~20s (per node)|
|GpuX_nvlink_bandwidth_total|NVlink total bandwidth|gpu|_|int|~20s (per node)|
|GpuX_nvlink_data_crc_error_count_total|NvLink data CRC Error Counter total for all Lanes.|gpu|_|int|~20s (per node)|
|GpuX_nvlink_flit_crc_error_count_total|NVLink flow control CRC Error Counter total for all Lanes|gpu|_|int|~20s (per node)|
|GpuX_nvlink_recovery_error_count_total|NVLink Recovery Error Counter total for all Lanes.|gpu|_|int|~20s (per node)|
|GpuX_nvlink_replay_error_count_total|NVLink Replay Error Counter total for all Lanes.|gpu|_|int|~20s (per node)|
|GpuX_power_management_limit|Current Power limit for the device|gpu|watts|int|~20s (per node)|
|GpuX_power_usage|Power usage for the device in Watts|gpu|watts|float|~20s (per node)|
|GpuX_power_violation|Power Violation time in usec|gpu|usec|int|~20s (per node)|
|GpuX_pstate|Performance state (P-State) 0-15. 0=highest|gpu|_|int|~20s (per node)|
|GpuX_reliability_violation|Reliability violation limit.|gpu|_|int|~20s (per node)|
|GpuX_retired_pages_dbe|Number of retired pages because of double bit errors Note: monotonically increasing|gpu|_|int|~20s (per node)|
|GpuX_retired_pages_pending|Number of pages pending retirement|gpu|_|int|~20s (per node)|
|GpuX_retired_pages_sbe|Number of retired pages because of single bit errors Note: monotonically increasing|gpu|_|int|~20s (per node)|
|GpuX_sm_app_clock|SM Application clocks|gpu|_|int|~20s (per node)|
|GpuX_sm_clock|SM clock for the device|gpu|megahertz|int|~20s (per node)|
|GpuX_sync_boost_violation|Sync Boost Violation time in usec|gpu|usec|int|~20s (per node)|
|GpuX_thermal_violation|Thermal Violation time in usec|gpu|usec|int, float (Gpu0)|~20s (per node)|
|GpuX_total_energy_consumption|Total energy consumption for the GPU in mJ since the driver was last reloaded|gpu|mj|float|~20s (per node)|
|GpuX_xid_errors|XID errors. The value is the specific XID error. (https://docs.nvidia.com/deploy/xid-errors/index.html#topic_4)|gpu|_|int|~20s (per node)|
|boottime|The last time that the system was started|system|s|float|1m (per node)|
|bytes_in|Number of bytes in per second|network|bytes/sec|float|5m or 40s (per node)|
|bytes_out|Number of bytes out per second|network|bytes/sec|float|5m or 40s (per node)|
|cpu_aidle|Percent of time since boot idle CPU|cpu|%|float|1m 30s (per node)|
|cpu_idle|Percentage of time that the CPU or CPUs were idle and the system did not have an outstanding disk I/O request|cpu|%|float|1m 30s (per node)|
|cpu_nice|Percentage of CPU utilization that occurred while executing at the user level with nice priority|cpu|%|float|1m 30s (per node)|
|cpu_num|The number of cpu present|cpu|cpus|int|1m (per node)|
|cpu_speed|CPU Speed in terms of MHz|cpu|mhz|int|1m (per node)|
|cpu_steal|Percentage of CPU steal that occurred while executing at the system level|cpu|%|int|1m 30s (per node)|
|cpu_system|Percentage of CPU utilization that occurred while executing at the system level|cpu|%|float|1m 30s (per node)|
|cpu_user|Percentage of CPU utilization that occurred while executing at the user level|cpu|%|float|1m 30s (per node)|
|cpu_wio|Percentage of time that the CPU or CPUs were idle during which the system had an outstanding disk I/O request|cpu|%|float|1m 30s (per node)|
|disk_free|Total free disk space|disk|gb|float|3m (per node)|
|disk_total|Total available disk space|disk|gb|float|1h (per node)|
|gexec|gexec available|core|_|string|5m (per node)|
|load_fifteen|Fifteen minute load average|load|_|float|1m 30s (per node)|
|load_five|Five minute load average|load|_|float|1m 30s (per node)|
|load_one|One minute load average|load|_|float|1m 30s (per node)|
|machine_type|System architecture|system|_|string|1m (per node)|
|mem_buffers|Amount of buffered memory|memory|kb|int|40s (per node)|
|mem_cached|Amount of cached memory|memory|kb|float|40s (per node)|
|mem_free|Amount of available memory|memory|kb|float|40s (per node)|
|mem_shared|Amount of shared memory|memory|kb|int|40s (per node)|
|mem_total|Total amount of memory displayed in KBs|memory|kb|float|1m (per node)|
|os_name|Operating system name|system|_|string|1m (per node)|
|os_release|Operating system release date|system|_|string|1m (per node)|
|part_max_used|Maximum percent used for all partitions|disk|%|float|3m (per node)|
|pkts_in|Packets in per second|network|packets/sec|float|5m or 40s (per node)|
|pkts_out|Packets out per second|network|packets/sec|float|5m or 40s (per node)|
|proc_run|Total number of running processes|process|_|int|1m 20s (per node)|
|proc_total|Total number of processes|process|_|int|1m 20s (per node)|
|swap_free|Amount of available swap memory|memory|kb|int|40s (per node)|
|swap_total|Total amount of swap space displayed in KBs|memory|kb|int|1m (per node)|