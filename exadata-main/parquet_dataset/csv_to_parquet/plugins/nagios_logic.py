import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
from plugins.plugin_logic import PluginLogic

class NagiosLogic(PluginLogic):
    def __init__(self):
        super().__init__()

        self.data_path = '/nas/cinecadataset/Comp_2/nagios_pub'

        self.sel_cols = ['cluster', 'plugin', 'name', 'timestamp', 'value', 'node', 'description', 'state', 'state_type', 'host_group', 'nagiosdrained']


        self.value_type_per_metric = {'state': pa.int32()}
                                      #'hostscheduleddowtimecomments': pa.string(),
                                      #'plugin_output': pa.string(),
        self.dict_cols_per_metric = {'state': ['node', 'description', 'host_group']}
                                     #'hostscheduleddowtimecomments': ['value', 'node', 'description', 'host_group'],
                                     #'plugin_output': ['value', 'node', 'description', 'host_group'],
    def get_schema_in(self, metric):
        schema_in = pa.schema([('', pa.int64()),
                               ('timestamp', pa.timestamp('us', tz='UTC')),
                               ('name', pa.string()),
                               ('chnl', pa.string()),
                               ('cluster', pa.string()),
                               ('description', pa.string()),
                               ('host_group', pa.string()),
                               ('nagiosdrained', pa.int32()),
                               ('node', pa.string()),
                               ('org', pa.string()),
                               ('plugin', pa.string()),
                               ('rack', pa.string()),
                               ('slot', pa.string()),
                               ('state', pa.string()),
                               ('state_type', pa.string()),
                               ('value', self.value_type_per_metric[metric])])
   
        return schema_in


    # step 1
    #def get_schema_out(self, metric):
    #    schema_out = pa.schema([('plugin', pa.string()),
    #                            ('metric', pa.string()),
    #                            ('year_month', pa.string()),
    #                            ('timestamp', pa.timestamp('ms', tz='UTC')),
    #                            ('value', self.value_type_per_metric[metric]),
    #                            ('description', pa.string()),
    #                            ('host_group', pa.string()),
    #                            ('nagiosdrained', pa.string()),
    #                            ('node', pa.string()),
    #                            ('state', pa.string()),
    #                            ('state_type', pa.string())])

    def get_schema_out(self, metric):
        schema_out = pa.schema([('plugin', pa.string()),
                                ('metric', pa.string()),
                                ('year_month', pa.string()),
                                ('timestamp', pa.timestamp('ms', tz='UTC')),
                                ('value', self.value_type_per_metric[metric]),
                                ('description', pa.string()),
                                ('host_group', pa.string()),
                                ('nagiosdrained', pa.string()),
                                ('node', pa.string()),
                                ('state_type', pa.string())])
                                #('state', pa.string()), # not needed anymore in step 2

        return schema_out

    def get_preprocessing_step1(self):
        def preprocessing(batches, schema_out):
            for batch in batches:

                # filtering for cluster=marconi100 only (some CSVs cover more)
                cluster = batch['cluster']
                mask = pc.equal(cluster, 'marconi100')
                batch = batch.filter(mask)

                metric = batch['name']

                # extracting month and year
                year_month = pc.strftime(batch['timestamp'], '%y-%m')

                # creating new batch from single arrays
                arrays = [batch['plugin'], metric, year_month, batch['timestamp'], batch['value'],
                          batch['description'], batch['host_group'], batch['nagiosdrained'],
                          batch['node'], batch['state'], batch['state_type']]
                batch = pa.RecordBatch.from_arrays(arrays, schema=schema_out)

                yield batch

        return preprocessing

    def get_preprocessing_step2(self):
        """Parquet to Parquet."""
        def preprocessing(batches, metric_name, schema_out, anonymization_dictionaries):
            for batch in batches:

                batch_size = len(batch)
                metric = pa.array([metric_name]*batch_size, type=pa.string())
                plugin = pa.array(['nagios_pub']*batch_size)

                # extracting month and year
                year_month = pc.strftime(batch['timestamp'], '%y-%m')

                timestamp = pc.floor_temporal(batch['timestamp'], unit='second')
                
                # anonymize nodes
                node = batch['node'].to_pandas(). \
                       apply(lambda x: x if pd.isnull(x) else str(anonymization_dictionaries['node'][x]))
                
                # creating new batch from single arrays
                arrays = [plugin, metric, year_month, timestamp, batch['value'],
                          batch['description'], batch['host_group'], batch['nagiosdrained'],
                          node, batch['state_type']]
                batch = pa.RecordBatch.from_arrays(arrays, schema=schema_out)
            
                yield batch

        return preprocessing
