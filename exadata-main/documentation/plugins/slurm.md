# Plugin
The Slurm plugin (time series data) collects some aggragated data from the Slurm Workload Manager server of the Cineca clusters. NOTE: it is a work in progress and may have some inconsistencies.

## Plugin-specific columns

|Column|Description|
|------|-----------|
|partition|Name of assigned partition (anonymized)|
|qos|Quality of Service (anonymized, categorical)|
|job_state|State of the job, see enum job_states for possible values|
|user_id|User ID for a job or job step (anonymized)|

## Metrics
|Metric|Description|Value type|Sampling period|
|------|-----------|----------|---------------|
|cluster_cpu_util|Total number of CPU used in the cluster in percent|int|5s|
|cluster_memory_util|Total RAM used in the cluster in percent|int|5s|
|job_id|Per Job status (anonymized)|int|None (based on jobs)|
|num_nodes|Per Job number of nodes|int|None (based on jobs)|
|s21.cluster_cpu_util|Total number of CPU used in the cluster in percent|float|10s (per partition and qos)|
|s21.cluster_gpu_util|Total number of GPU used in the cluster in percent|float|10s (per partition and qos)|
|s21.cluster_mem_util|Total RAM used in the cluster in percent|float|10s (per partition and qos)|
|s21.jobs.avg_waiting_hour|The average time (hours) the running jobs stayed in the PENDING status|float|10s (per partition and qos)|
|s21.jobs.eligible|The number of pending jobs already eligible for execution and waiting only for resources|int|10s (per partition and qos)|
|s21.jobs.eligible_v2|The number of pending jobs already eligible for execution and waiting only for resources|int|10s (per partition and qos)|
|s21.jobs.nodes_eligible|The number of node requested by the eligible jobs|int|10s (per partition and qos)|
|s21.jobs.nodes_eligible_v2|The number of node requested by the eligible jobs|int|10s (per partition and qos)|
|s21.jobs.p95_waiting_hour|95th percentile of the jobs' waiting time |float|10s (per partition and qos)|
|s21.jobs.tot_gpus|Total number of GPUs requested by the jobs|int|10s (per partition and qos)|
|s21.jobs.tot_jobs|Total number of jobs|int|10s (per partition and qos)|
|s21.jobs.tot_node_hour|The product of the waiting time (hours) and the number of nodes for the jobs in the PENDING state.|float|10s (per partition and qos)|
|s21.jobs.tot_nodes|Total number of nodes requested by the jobs|int|10s (per partition and qos)|
|s21.totals.cpus_alloc|Total number of CPUs allocated to a job|int|10s (per partition and qos)|
|s21.totals.cpus_config|Total number of CPUs configured in the batch scheduler|int|10s (per partition and qos)|
|s21.totals.cpus_down|Total number of CPUs not usable|int|10s (per partition and qos)|
|s21.totals.cpus_eligible|Total number of CPUs usable|int|10s (per partition and qos)|
|s21.totals.cpus_idle|Total number of CPUs not allocated to a job|int|10s (per partition and qos)|
|s21.totals.gpus_alloc|Total number of GPUs allocated to a job|int|10s (per partition and qos)|
|s21.totals.gpus_config|Total number of GPUs configured in the batch scheduler|int|10s (per partition and qos)|
|s21.totals.gpus_down|Total number of GPUs not usable|int|10s (per partition and qos)|
|s21.totals.gpus_eligible|Total number of GPUs usable|int|10s (per partition and qos)|
|s21.totals.gpus_idle|Total number of GPUs not allocated to a job|int|10s (per partition and qos)|
|s21.totals.memory_alloc|Total RAM allocated (MB)|int|10s (per partition and qos)|
|s21.totals.memory_config|Total RAM configured in the batch scheduler (MB)|int|10s (per partition and qos)|
|s21.totals.memory_down|Total RAM not usable (MB)|int|10s (per partition and qos)|
|s21.totals.memory_eligible|Total RAM usable (MB)|int|10s (per partition and qos)|
|s21.totals.memory_idle|Total RAM not allocated to a job (MB)|int|10s (per partition and qos)|
|s21.totals.total_nodes_alloc|Total number of nodes allocated to a job|int|10s (per partition and qos)|
|s21.totals.total_nodes_config|Total number of nodes configured in the batch scheduler|int|10s (per partition and qos)|
|s21.totals.total_nodes_down|Total number of nodes not usable|int|10s (per partition and qos)|
|s21.totals.total_nodes_eligible|Total number of nodes usable|int|10s (per partition and qos)|
|s21.totals.total_nodes_idle|Total number of nodes not allocated to a job|int|10s (per partition and qos)|
|s21.totals.total_nodes_mixed|Total number of nodes in the MIXED state|int|10s (per partition and qos)|
|total_cpus_alloc|Total number of CPUs allocated to a job|int|5s|
|total_cpus_config|Total number of CPUs configured in the batch scheduler|int|5s|
|total_cpus_down|Total number of CPUs not usable|int|5s|
|total_cpus_eligible|Total number of CPUs usable|int|5s|
|total_cpus_idle|Total number of CPUs not allocated to a job|int|5s|
|total_memory_alloc|Total RAM allocated (MB)|int|5s|
|total_memory_config|Total RAM configured in the batch scheduler (MB)|int|5s|
|total_memory_down|Total RAM not usable (MB)|int|5s|
|total_memory_eligible|Total RAM usable (MB)|int|5s|
|total_memory_idle|Total RAM not allocated to a job (MB)|int|5s|
|total_nodes_alloc|Total number of nodes allocated to a job|int|5s|
|total_nodes_config|Total number of nodes configured in the batch scheduler|int|5s|
|total_nodes_down|Total number of nodes not usable|int|5s|
|total_nodes_eligible|Total number of nodes usable|int|5s|
|total_nodes_idle|Total number of nodes not allocated to a job|int|5s|
|total_nodes_mixed|Total number of nodes in the MIXED state|int|5s|