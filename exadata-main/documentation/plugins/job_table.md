# Job table
Collects information regarding the jobs executed on the cluster (and store in the SLURM database);
the information collected are those provided by users at submission time.

Only one metric is present: `job_info_marconi100`.

## Plugin-specific columns

|Column|Description|Type|
|------|-----------|----|
|accrue_time|Accrue time associated with the job|timestamp|
|alloc_node|Nodes allocated to the job|string|
|alloc_sid|Local session ID used to submit the job|int|
|array_job_id|Job ID of a job array or 0 if N/A (anonymized)|int|
|array_max_tasks|Maximum number of running tasks|int|
|array_task_id|Task ID of a job array|int|
|array_task_str|String expression of task IDs in this record|string|
|array_task_throttle|The maximum number of tasks in a job array that can execute at the same time|int|
|assoc_id|ID of the job association|int|
|batch_flag|Batch flag set (1 yes, 0 otherwise)|int|
|batch_host|Name of host running batch script|string|
|billable_tres|Billable Trackable Resource (TRES) cache; updated upon resize|int|
|bitflags|Various job flags|int|
|boards_per_node|Boards per node required by job|int|
|contiguous|1 if job requires contiguous nodes|bool|
|cores_per_socket|Cores per socket required by job|int|
|cpus_alloc_layout|Map: list of cpu allocated per node|string|
|cpus_allocated|Map: number of cpu allocated per node|string|
|cpus_per_task|Number of processors required for each task|int|
|cpus_per_tres|Semicolon-delimited list of TRES=# values|string|
|dependency|Synchronize job execution with other jobs; a job can start only after its dependencies have completed (anonymized)|string|
|derived_ec|Highest exit code of all job steps|string|
|eligible_time|Time job is eligible for running|timestamp|
|end_time|Time of termination, actual or expected|timestamp|
|exc_nodes|Comma-separated list of excluded nodes|string|
|exit_code|Exit code for job (status from wait call)|string|
|features|Comma-separated list of required features|string|
|group_id|Group job submitted as|int|
|job_id|Job ID (anonymized)|int|
|job_state|State of the job, see enum job_states for possible values|string|
|last_sched_eval|Last time the job was evaluated for scheduling|timestamp|
|max_cpus|Maximum number of cpus usable by job|int|
|max_nodes|Maximum number of nodes usable by job|int|
|mem_per_cpu|1 if the job has exceeded the amount of per-CPU memory allowed, 0 otherwise|bool|
|mem_per_node|1 if the job has exceeded the amount of per-node memory allowed, 0 otherwise|bool|
|metric|Partitioning column|string|
|min_memory_cpu|Minimum real memory required per allocated CPU|int|
|min_memory_node|Minimum real memory required per node|int|
|nice|Nice value (adjustment to a job's scheduling priority)|int|
|nodes|List of nodes allocated to job|string|
|ntasks_per_board|Number of tasks to invoke on each board|int|
|ntasks_per_core|Number of tasks to invoke on each core|int|
|ntasks_per_core_str|Number of tasks to invoke on each core as string|string|
|ntasks_per_node|Number of tasks to invoke on each node|int|
|ntasks_per_socket|Number of tasks to invoke on each socket|int|
|ntasks_per_socket_str|Number of tasks to invoke on each socket as string|string|
|num_cpus|Number of CPUs (processors) requested by the job or allocated to it if already running|int|
|num_nodes|Number of nodes allocated to the job or the minimum number of nodes required by a pending job|int|
|num_tasks|Number of tasks requested by a job or job step|int|
|partition|Name of assigned partition (anonymized)|string|
|plugin|Partitioning column|string|
|pn_min_cpus|Minimum # CPUs per node, default=0|int|
|pn_min_memory|Minimum real memory per node, default=0|int|
|pn_min_tmp_disk|Minimum temporary disk per node, default=0|int|
|power_flags|Power management flags, see SLURM_POWERFLAGS|int|
|priority|Relative priority of the job, 0=held, 1=required nodes DOWN/DRAINED|int|
|profile|Level of acct_gather_profile {all / none}|int|
|qos|Quality of Service (anonymized, categorical)|string|
|reboot|Node reboot requested before start|int|
|req_nodes|Comma-separated list of required nodes|string|
|req_switch|Minimum number of switches|int|
|requeue|Enable or disable job requeue option|bool|
|resize_time|Time of latest size change|timestamp|
|restart_cnt|Count of job restarts|int|
|resv_name|Reservation name|string|
|run_time|Job run time (seconds)|int|
|run_time_str|Job run time (seconds) as string|string|
|sched_nodes|For pending jobs, a list of the nodes expected to be used when the job is started|string|
|shared|1 if job can share nodes with other jobs, 0 otherwise|string|
|show_flags|Determine the level of details requested|int|
|sockets_per_board|Sockets per board allocated to the job|int|
|sockets_per_node|Sockets per node required by job|int|
|start_time|Time execution begins (actual or expected)|timestamp|
|state_reason|Reason job still pending or failed,see slurm.h:enum job_state_reason|string|
|submit_time|Time of job submission|timestamp|
|suspend_time|Time job last suspended or resumed|timestamp|
|threads_per_core|Threads per core required by job|int|
|time_limit|Maximum run time in minutes or INFINITE|int|
|time_limit_str|Maximum run time in minutes or INFINITE as string|string|
|time_min|Minimum run time in minutes or INFINITE|int|
|tres_alloc_str|Trackable resources allocated to the job|string|
|tres_bind|Trackable resources task binding requested by the job or job step|string|
|tres_freq|Trackable resources frequencies requested by the job or job step|string|
|tres_per_job|Trackable resources requested by the job|string|
|tres_per_node|Trackable resources per node requested by the job or job step|string|
|tres_per_socket|Trackable resources per socket requested by the job or job step|string|
|tres_per_task|Trackable resources per task requested by the job or job step|string|
|tres_req_str|TRES requested by the job as string|string|
|user_id|User ID for a job or job step (anonymized)|int|
|wait4switch|Maximum time to wait for minimum switches|int|
|wckey|Workload Characterization Key of a job|string|
|year_month|Partitioning column ("YY-MM")|string|
