import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
from plugins.plugin_logic import PluginLogic

class SLURMLogic(PluginLogic):
    '''
    Different from the other plugins, due to tags being different for different metrics.
    "common_cols" and "specific_cols_per_metric" are given instead of a common "sel_cols".
    '''
    def __init__(self):
        super().__init__()

        self.data_path = '/nas/cinecadataset/Comp_2/slurm_pub'

        # tags common to all metric
        self.common_cols = ['plugin', 'name', 'timestamp', 'value']

        # non-common tags that have to be read (metric-specific)
        self.specific_cols_per_metric = {'cluster_cpu_util': [],
                                         'cluster_memory_util': [],
                                         'job_id': ['partition', 'user_id', 'job_state'],
                                         'num_nodes': ['partition', 'user_id', 'job_state'],
                                         's21.cluster_cpu_util': ['partition'],
                                         's21.cluster_gpu_util': ['partition'],
                                         's21.cluster_mem_util': ['partition'],
                                         's21.jobs.avg_waiting_hour': ['qos', 'partition', 'job_state'],
                                         's21.jobs.eligible': ['qos', 'partition', 'job_state'],
                                         's21.jobs.eligible_v2': ['qos', 'partition', 'job_state'],
                                         's21.jobs.nodes_eligible': ['qos', 'partition', 'job_state'],
                                         's21.jobs.nodes_eligible_v2': ['qos', 'partition', 'job_state'],
                                         's21.jobs.p95_waiting_hour': ['qos', 'partition', 'job_state'],
                                         's21.jobs.tot_gpus': ['qos', 'partition', 'job_state'],
                                         's21.jobs.tot_jobs': ['qos', 'partition', 'job_state'],
                                         's21.jobs.tot_node_hour': ['qos', 'partition', 'job_state'],
                                         's21.jobs.tot_nodes': ['qos', 'partition', 'job_state'],
                                         's21.totals.cpus_alloc': ['partition'],
                                         's21.totals.cpus_config': ['partition'],
                                         's21.totals.cpus_down': ['partition'],
                                         's21.totals.cpus_eligible': ['partition'],
                                         's21.totals.cpus_idle': ['partition'],
                                         's21.totals.gpus_alloc': ['partition'],
                                         's21.totals.gpus_config': ['partition'],
                                         's21.totals.gpus_down': ['partition'],
                                         's21.totals.gpus_eligible': ['partition'],
                                         's21.totals.gpus_idle': ['partition'],
                                         's21.totals.memory_alloc': ['partition'],
                                         's21.totals.memory_config': ['partition'],
                                         's21.totals.memory_down': ['partition'],
                                         's21.totals.memory_eligible': ['partition'],
                                         's21.totals.memory_idle': ['partition'],
                                         's21.totals.total_nodes_alloc': ['partition'],
                                         's21.totals.total_nodes_config': ['partition'],
                                         's21.totals.total_nodes_down': ['partition'],
                                         's21.totals.total_nodes_eligible': ['partition'],
                                         's21.totals.total_nodes_idle': ['partition'],
                                         's21.totals.total_nodes_mixed': ['partition'],
                                         'total_cpus_alloc': [],
                                         'total_cpus_config': [],
                                         'total_cpus_down': [],
                                         'total_cpus_eligible': [],
                                         'total_cpus_idle': [],
                                         'total_memory_alloc': [],
                                         'total_memory_config': [],
                                         'total_memory_down': [],
                                         'total_memory_eligible': [],
                                         'total_memory_idle': [],
                                         'total_nodes_alloc': [],
                                         'total_nodes_config': [],
                                         'total_nodes_down': [],
                                         'total_nodes_eligible': [],
                                         'total_nodes_idle': [],
                                         'total_nodes_mixed': []}
                                         #'alloc_drain': ['partition'],

        # tags that are to be dictionary encoded, when available
        self.wanted_dict_tags = ['qos', 'partition', 'user_id', 'job_state']

        self.type_per_tag = {'': pa.int64(),
                             'chnl': pa.string(),
                             'cluster': pa.string(),
                             'job_state': pa.string(),
                             'name': pa.string(),
                             'plugin': pa.string(),
                             'partition': pa.string(),
                             'qos': pa.string(),
                             'user_id':pa.int32(),
                             'timestamp': pa.timestamp('ms', tz='UTC')}
                             #'partition': pa.uint8(),
                             #'qos': pa.uint8(),
    
        self.dict_cols_per_metric= self.filter_tags_by_metric(self.wanted_dict_tags, self.specific_cols_per_metric)

        self.value_type_per_metric = {'total_memory_eligible':pa.int32(),
                                      's21.jobs.tot_gpus':pa.int32(),
                                      'cluster_cpu_util':pa.int32(),
                                      'total_memory_down':pa.int32(),
                                      'total_memory_config':pa.int32(),
                                      's21.jobs.nodes_eligible':pa.int32(),
                                      'cluster_memory_util':pa.int32(),
                                      's21.totals.total_nodes_down':pa.int32(),
                                      's21.jobs.eligible_v2':pa.int32(),
                                      's21.totals.memory_alloc':pa.int32(),
                                      's21.totals.memory_down':pa.int32(),
                                      's21.totals.total_nodes_eligible':pa.int32(),
                                      'total_cpus_down':pa.int32(),
                                      's21.totals.memory_config':pa.int32(),
                                      'total_nodes_alloc':pa.int32(),
                                      'total_cpus_idle':pa.int32(),
                                      's21.totals.total_nodes_mixed':pa.int32(),
                                      's21.totals.cpus_alloc':pa.int32(),
                                      's21.totals.total_nodes_idle':pa.int32(),
                                      's21.jobs.eligible':pa.int32(),
                                      's21.totals.memory_eligible':pa.int32(),
                                      's21.totals.total_nodes_config':pa.int32(),
                                      'total_memory_alloc':pa.int32(),
                                      'num_nodes':pa.int32(),
                                      'total_nodes_mixed':pa.int32(),
                                      's21.cluster_cpu_util':pa.float64(),
                                      'total_memory_idle':pa.int32(),
                                      'total_nodes_eligible':pa.int32(),
                                      'total_cpus_eligible':pa.int32(),
                                      's21.totals.cpus_down':pa.int32(),
                                      's21.totals.cpus_idle':pa.int32(),
                                      'total_nodes_config':pa.int32(),
                                      's21.totals.cpus_eligible':pa.int32(),
                                      'total_nodes_idle':pa.int32(),
                                      's21.jobs.avg_waiting_hour':pa.float64(),
                                      'total_nodes_down':pa.int32(),
                                      's21.totals.memory_idle':pa.int32(),
                                      's21.totals.gpus_alloc':pa.int32(),
                                      's21.totals.gpus_idle':pa.int32(),
                                      'total_cpus_config':pa.int32(),
                                      's21.jobs.nodes_eligible_v2':pa.int32(),
                                      's21.jobs.p95_waiting_hour':pa.float64(),
                                      'total_cpus_alloc':pa.int32(),
                                      's21.jobs.tot_nodes':pa.int32(),
                                      's21.cluster_mem_util':pa.float64(),
                                      's21.jobs.tot_jobs':pa.int32(),
                                      's21.cluster_gpu_util':pa.float64(),
                                      's21.jobs.tot_node_hour':pa.float64(),
                                      's21.totals.total_nodes_alloc':pa.int32(),
                                      's21.totals.gpus_down':pa.int32(),
                                      'job_id':pa.int32(),
                                      's21.totals.gpus_config':pa.int32(),
                                      's21.totals.gpus_eligible':pa.int32(),
                                      's21.totals.cpus_config':pa.int32()}
                                      #'alloc_drain':pa.int32(),
    
    def filter_tags_by_metric(self, wanted_tags, available_per_metric):
        filtered_per_metric = {}
        
        for metric, available_tags in available_per_metric.items():
            filtered_per_metric[metric] = []
            for tag in available_tags:
                if tag in wanted_tags:
                    filtered_per_metric[metric].append(tag)
        
        return filtered_per_metric


    def get_schema_in(self, metric):
        metric_tags = self.common_cols + self.specific_cols_per_metric[metric]
        metric_tags.remove('value')
        
        fields = [('value', self.value_type_per_metric[metric])]
        for tag in metric_tags:
            fields.append((tag, self.type_per_tag[tag]))
        
        schema_in = pa.schema(fields)

        return schema_in

    def get_schema_out(self, metric):
        
        common_fields = [('plugin', self.type_per_tag['plugin']),
                         ('metric', self.type_per_tag['name']),
                         ('year_month', pa.string()),
                         ('timestamp', pa.timestamp('ms', tz='UTC')),
                         ('value', self.value_type_per_metric[metric])]

        metric_specific_fields = [(tag, self.type_per_tag[tag]) for tag in self.specific_cols_per_metric[metric]]

        schema_out = pa.schema(common_fields + metric_specific_fields)

        return schema_out

    def get_preprocessing_step1(self):
        """In SLURM different metrics have different schemas."""
        def preprocessing(batches, schema_out):

            specific_out_cols = [x for x in schema_out.names if x not in self.common_cols and x not in ['metric', 'year_month']]

            for batch in batches:

                metric = batch['name']

                # extracting month and year
                year_month = pc.strftime(batch['timestamp'], '%y-%m')
                
                # creating new batch from single arrays
                arrays = [batch['plugin'], metric, year_month, batch['timestamp'], batch['value']]
                if specific_out_cols:
                    arrays += [batch[col] for col in specific_out_cols]
                batch = pa.RecordBatch.from_arrays(arrays, schema=schema_out)
            
                yield batch

        return preprocessing

    def get_preprocessing_step2(self):
        """
        Parquet to Parquet.
        In SLURM different metrics have different schemas.
        """
        def preprocessing(batches, metric_name, schema_out, anonymization_dictionaries):
            for batch in batches:
                
                batch_size = len(batch)
                metric = pa.array([metric_name]*batch_size, type=pa.string())
                plugin = pa.array(['slurm_pub']*batch_size)

                # extracting month and year
                year_month = pc.strftime(batch['timestamp'], '%y-%m')

                # truncating timestamp
                timestamp = pc.floor_temporal(batch['timestamp'], unit='second')


                arrays = [plugin, metric, year_month, timestamp]
                for tag in batch.schema:
                    name = tag.name

                    if name in ['plugin', 'metric', 'year_month', 'timestamp']:
                        continue

                    # anonymization per tag
                    if name in anonymization_dictionaries.keys():
                        # anonymize (dictionary mapping)
                        old_values = batch[name].to_pandas()

                        if name == 'user_id':
                            old_values = old_values.astype('Int64')

                        new_values = old_values.apply(lambda x: x if pd.isnull(x) else anonymization_dictionaries[name][x])
                        arrays.append(pa.array(new_values))
                    # metric-specific anonymization
                    elif metric_name == 'job_id' and name == 'value':
                        old_values = batch[name].to_pandas()
                        new_values = old_values.apply(lambda x: x if pd.isnull(x) else anonymization_dictionaries['job_id'][x])
                        arrays.append(pa.array(new_values))
                    else:
                        arrays.append(batch[name])

                # creating new batch from single arrays
                batch = pa.RecordBatch.from_arrays(arrays, schema=schema_out)
            
                yield batch

        return preprocessing
