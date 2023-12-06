import re
from ast import literal_eval
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import numpy as np
from plugins.plugin_logic import PluginLogic

class JobTableLogic(PluginLogic):
    def __init__(self):
        super().__init__()

        self.data_path = '/nas/cinecadataset/Comp_2/job_table'

        # new selection
        self.sel_cols = ['accrue_time',
                         'alloc_node',
                         'alloc_sid',
                         'array_job_id',
                         'array_max_tasks',
                         'array_task_id',
                         'array_task_str',
                         'array_task_throttle',
                         'assoc_id',
                         'batch_flag',
                         'batch_host',
                         'billable_tres',
                         'bitflags',
                         'boards_per_node',
                         'contiguous',
                         'cores_per_socket',
                         'cpus_alloc_layout',
                         'cpus_allocated',
                         'cpus_per_task',
                         'cpus_per_tres',
                         'dependency',
                         'derived_ec',
                         'eligible_time',
                         'end_time',
                         'exc_nodes',
                         'exit_code',
                         'features',
                         'group_id',
                         'job_id',
                         'job_state',
                         'last_sched_eval',
                         'max_cpus',
                         'max_nodes',
                         'mem_per_cpu',
                         'mem_per_node',
                         'min_memory_cpu',
                         'min_memory_node',
                         'nice',
                         'nodes',
                         'ntasks_per_board',
                         'ntasks_per_core',
                         'ntasks_per_core_str',
                         'ntasks_per_node',
                         'ntasks_per_socket',
                         'ntasks_per_socket_str',
                         'num_cpus',
                         'num_nodes',
                         'num_tasks',
                         'partition',
                         'pn_min_cpus',
                         'pn_min_memory',
                         'pn_min_tmp_disk',
                         'power_flags',
                         'priority',
                         'profile',
                         'qos',
                         'reboot',
                         'req_nodes',
                         'req_switch',
                         'requeue',
                         'resize_time',
                         'restart_cnt',
                         'resv_name',
                         'run_time',
                         'run_time_str',
                         'sched_nodes',
                         'shared',
                         'show_flags',
                         'sockets_per_board',
                         'sockets_per_node',
                         'start_time',
                         'state_reason',
                         'submit_time',
                         'suspend_time',
                         'threads_per_core',
                         'time_limit',
                         'time_limit_str',
                         'time_min',
                         'tres_alloc_str',
                         'tres_bind',
                         'tres_freq',
                         'tres_per_job',
                         'tres_per_node',
                         'tres_per_socket',
                         'tres_per_task',
                         'tres_req_str',
                         'user_id',
                         'wait4switch',
                         'wckey']

        self.value_type_per_metric = {'job_info_marconi100': None}

        self.dict_cols_per_metric = {'job_info_marconi100': None}
                

    def get_schema_in(self, metric):
        
        fields = []
        fields.append(("start_time", pa.timestamp('s', tz='UTC')))
        fields.append(("end_time", pa.timestamp('s', tz='UTC')))
        fields.append(("submit_time", pa.timestamp('s', tz='UTC')))
        fields.extend([(tag, pa.string()) for tag in self.sel_cols if tag not in ['start_time', 'end_time', 'submit_time']])
        schema_in = pa.schema(fields)

        return schema_in

    def get_schema_out(self, metric):

        schema_out = pa.schema([("plugin", pa.string()),
                                ("metric", pa.string()),
                                ("year_month", pa.string()),
                                ('accrue_time', pa.timestamp('ms', tz='UTC')),
                                ('alloc_node', pa.string()),
                                ('alloc_sid', pa.uint32()),
                                ('array_job_id', pa.uint32()),
                                ('array_max_tasks', pa.uint32()),
                                ('array_task_id', pa.uint32()),
                                ('array_task_str', pa.string()),
                                ('array_task_throttle', pa.uint16()),
                                ('assoc_id', pa.int32()),
                                ('batch_flag', pa.uint16()),
                                ('batch_host', pa.string()),
                                ('billable_tres', pa.uint32()),
                                ('bitflags', pa.uint32()),
                                ('boards_per_node', pa.uint16()),
                                ('contiguous', pa.bool_()),
                                ('cores_per_socket', pa.uint16()),
                                ('cpus_alloc_layout', pa.string()),
                                ('cpus_allocated', pa.string()),
                                ('cpus_per_task', pa.uint32()),
                                ('cpus_per_tres', pa.string()),
                                ('dependency', pa.string()),
                                ('derived_ec', pa.string()),
                                ('eligible_time', pa.timestamp('ms', tz='UTC')),
                                ('end_time', pa.timestamp('ms', tz='UTC')),
                                ('exc_nodes', pa.string()),
                                ('exit_code', pa.string()),
                                ('features', pa.string()),
                                ('group_id', pa.uint32()),
                                ('job_id', pa.uint32()),
                                ('job_state', pa.string()),
                                ('last_sched_eval', pa.timestamp('ms', tz='UTC')),
                                ('max_cpus', pa.uint16()),
                                ('max_nodes', pa.uint32()),
                                ('mem_per_cpu', pa.bool_()),
                                ('mem_per_node', pa.bool_()),
                                ('min_memory_cpu', pa.uint32()),
                                ('min_memory_node', pa.uint32()),
                                ('nice', pa.int32()),
                                ('nodes', pa.string()),
                                ('ntasks_per_board', pa.uint16()),
                                ('ntasks_per_core', pa.uint16()),
                                ('ntasks_per_core_str', pa.string()),
                                ('ntasks_per_node', pa.uint32()),
                                ('ntasks_per_socket', pa.uint32()),
                                ('ntasks_per_socket_str', pa.string()),
                                ('num_cpus', pa.uint32()),
                                ('num_nodes', pa.uint16()),
                                ('num_tasks', pa.uint32()),
                                ('partition', pa.string()),
                                ('pn_min_cpus', pa.uint32()),
                                ('pn_min_memory', pa.uint32()),
                                ('pn_min_tmp_disk', pa.uint16()),
                                ('power_flags', pa.uint16()),
                                ('priority', pa.uint32()),
                                ('profile', pa.uint16()),
                                ('qos', pa.string()),
                                ('reboot', pa.uint16()),
                                ('req_nodes', pa.string()),
                                ('req_switch', pa.uint16()),
                                ('requeue', pa.bool_()),
                                ('resize_time', pa.timestamp('ms', tz='UTC')),
                                ('restart_cnt', pa.uint16()),
                                ('resv_name', pa.string()),
                                ('run_time', pa.uint32()),
                                ('run_time_str', pa.string()),
                                ('sched_nodes', pa.string()),
                                ('shared', pa.string()),
                                ('show_flags', pa.uint16()),
                                ('sockets_per_board', pa.uint16()),
                                ('sockets_per_node', pa.uint16()),
                                ('start_time', pa.timestamp('ms', tz='UTC')),
                                ('state_reason', pa.string()),
                                ('submit_time', pa.timestamp('ms', tz='UTC')),
                                ('suspend_time', pa.timestamp('ms', tz='UTC')),
                                ('threads_per_core', pa.uint16()),
                                ('time_limit', pa.uint32()),
                                ('time_limit_str', pa.string()),
                                ('time_min', pa.uint16()),
                                ('tres_alloc_str', pa.string()),
                                ('tres_bind', pa.string()),
                                ('tres_freq', pa.string()),
                                ('tres_per_job', pa.string()),
                                ('tres_per_node', pa.string()),
                                ('tres_per_socket', pa.string()),
                                ('tres_per_task', pa.string()),
                                ('tres_req_str', pa.string()),
                                ('user_id', pa.uint32()),
                                ('wait4switch', pa.uint32()),
                                ('wckey', pa.string())])


        return schema_out

    def get_preprocessing_step1(self):
        def preprocessing(batches, schema_out):
            for batch in batches:


                metric = pa.array(['job_info_marconi100']*len(batch))

                # "synthetic" plugin column
                plugin = pa.array(['job_table']*len(batch))

                # extracting month and year
                year_month = pc.strftime(batch['start_time'], '%y-%m')
                
                # creating new batch from single arrays
                arrays = [plugin, metric, year_month, batch['start_time'], batch['end_time'], batch['submit_time']]
                arrays.extend([batch[tag] for tag in self.sel_cols if tag not in ['start_time',
                                                                                  'end_time',
                                                                                  'submit_time']])

                batch = pa.RecordBatch.from_arrays(arrays, schema=schema_out)
            
                yield batch

        return preprocessing

    def get_preprocessing_step2(self):
        """
        Parquet to Parquet.
        Job table: timestamp aligning, anonymization and dtype setting/conversion.
        
        NaT timestamps due to DST ambguity.
        end_time is used for year_month creation, like timestamp in other plugins.
        Current solution: keep NaT for ambigous values, set year_month according to original file (fragment)
        """
        
        timestamp_cols = ['suspend_time',
                          'end_time',
                          'resize_time',
                          'submit_time',
                          'accrue_time',
                          'eligible_time',
                          'start_time']
        

        def preprocessing(batches, metric_name, schema_out, anonymization_dictionaries):
            def anonymize_cpus_allocated(x):
                if pd.isna(x):
                    return None

                d = literal_eval(x) 
                keys = d.keys()
                new_d = {}
                for key in keys:
                    new_d[anonymization_dictionaries['node'][key]] = d[key]
                return str(new_d)
            
            def anonymize_cpus_alloc_layout(x):
                if pd.isna(x):
                    return None

                d = literal_eval(x) 
                
                keys = d.keys()
                new_d = {}
                for key in keys:
                    if key == '' or key not in anonymization_dictionaries['node']:
                        new_key = None
                    else:
                        new_key = anonymization_dictionaries['node'][key] 
                    new_d[new_key] = d[key]
                return str(new_d)

            re_compute = re.compile('r\d{3}n\d{2}') # rXXXnYY
            re_multi = re.compile('(r\d{3})n\[(.*?)\]') # rXXX[...] with inside XX-YY and/or XX,YY
            def parse_and_anonymize_nodes(x):
                if pd.isna(x):
                    return None
                
                regular = re_compute.findall(x)
                multi = re_multi.findall(x)
                
                # adding regular nodes
                new_nodes = regular
                
                # adding multi nodes
                if multi:
                    for rack, nodes in multi:
                        inside_nodes = nodes.split(',')
                        
                        for inside_node in inside_nodes:
                            if '-' in inside_node:
                                start, end = inside_node.split('-')
                                for i in range(int(start), int(end)+1):
                                    new_nodes.append(rack+'n'+str(i).zfill(2))
                            else:
                                new_nodes.append(rack+'n'+inside_node)
                        
                return str([anonymization_dictionaries['node'][node] for node in new_nodes])

            # processing
            for batch in batches:
                
                batch_size = len(batch)
                metric = pa.array([metric_name]*batch_size, type=pa.string())
                plugin = pa.array(['job_table']*batch_size)
                #year_month = pc.strftime(batch['start_time'], '%y-%m')

                
                arrays = [plugin, metric]
                for name in self.sel_cols:

                    new_values = batch[name].to_pandas()

                    if pd.api.types.is_object_dtype(new_values):
                        new_values = new_values.replace('', None)

                    # enabling conversion to int for values where ".0" due to float->string
                    if schema_out[schema_out.get_field_index(name)].type in [pa.int32(), pa.uint8(),
                                                                             pa.uint16(), pa.uint32()]:
                        new_values = new_values \
                                     .apply(lambda x: x if pd.isna(x) else x.split('.')[0]) \
                                     .astype('Int64')

                    ### timestamps ### 
                    if name in timestamp_cols:
                        new_values = pd.to_datetime(new_values)

                        # timestamp fix (all timestamp cols)
                        # from localized naive (Europe/Rome) to UTC
                        # ambigous values (due to DST) -> NaT
                        new_values = new_values.dt.tz_localize(None) \
                                               .dt.tz_localize('Europe/Rome', ambiguous='NaT') \
                                               .dt.tz_convert('UTC')
                                               #.dt.tz_localize('Europe/Rome', ambiguous=False) \

                        # extracting month and year
                        if name == 'end_time':
                            year_month = new_values.dt.strftime('%y-%m')
                            if year_month.isna().sum() > 0:
                                if year_month.isna().all():
                                    print('all NaTs in the batch.', flush=True)
                                # handling NaT due to DST by putting in the most common month in the batch... 
                                mode_month = year_month[~year_month.isna()].mode().values[0]
                                print(f'mode month: {mode_month}')
                                year_month =  year_month.fillna(mode_month)

                            year_month = pa.array(year_month)
                            arrays.insert(2, year_month)

                    ### anonymization ### 
                    # anonymize tags that require substring substitution
                    if name == 'dependency':
                        q = re.compile('[\d]+')
                        f = lambda x: str(anonymization_dictionaries['job_id'][int(x.group(0))])
                        for idx, value in enumerate(new_values):
                                if value is None:
                                    continue

                                new_value = q.sub(f, value)                                
                                new_values[idx] = new_value
                    elif name == 'cpus_alloc_layout':
                        new_values = new_values.apply(anonymize_cpus_alloc_layout)
                    elif name == 'cpus_allocated':
                        new_values = new_values.apply(anonymize_cpus_allocated)
                    elif name in ['exc_nodes', 'req_nodes']:
                        new_values = new_values.apply(lambda x: None if pd.isna(x) else ','.join(literal_eval(x)))
                        new_values = new_values.apply(parse_and_anonymize_nodes)
                    elif name in ['nodes', 'sched_nodes']:
                        new_values = new_values.apply(parse_and_anonymize_nodes)
                    # anonymize (dictionary mapping)
                    elif name in anonymization_dictionaries.keys():
                        new_values = new_values.apply(lambda x: x if pd.isnull(x)
                                                                  else anonymization_dictionaries[name][x])

                    arrays.append(pa.array(new_values))

                batch = pa.RecordBatch.from_arrays(arrays, schema=schema_out)
                yield batch

        return preprocessing
