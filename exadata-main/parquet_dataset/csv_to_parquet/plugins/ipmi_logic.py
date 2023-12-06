import pyarrow as pa
import pyarrow.compute as pc
import pandas as pd
from plugins.plugin_logic import PluginLogic

class IPMILogic(PluginLogic):
    def __init__(self):
        super().__init__()

        self.data_path = '/nas/cinecadataset/Comp_2/ipmi_pub'

        self.sel_cols = ['plugin', 'name', 'timestamp', 'value', 'node']

        self.value_type_per_metric = {'p1_core18_temp': pa.int32(),
                                      'dimm2_temp': pa.int32(),
                                      'p1_core5_temp': pa.int32(),
                                      'ps0_input_power': pa.int32(),
                                      'p0_core12_temp': pa.int32(),
                                      'p1_power': pa.int32(),
                                      'gpu3_core_temp': pa.int32(),
                                      'ps0_output_volta': pa.float32(),
                                      'p0_core14_temp': pa.int32(),
                                      'dimm11_temp': pa.int32(),
                                      'ps0_output_curre': pa.int32(),
                                      'dimm5_temp': pa.int32(),
                                      'p0_core2_temp': pa.int32(),
                                      'gpu1_core_temp': pa.int32(),
                                      'dimm0_temp': pa.int32(),
                                      'p0_core9_temp': pa.int32(),
                                      'p1_core13_temp': pa.int32(),
                                      'p0_core18_temp': pa.int32(),
                                      'p0_core13_temp': pa.int32(),
                                      'dimm13_temp': pa.int32(),
                                      'p0_core23_temp': pa.int32(),
                                      'ambient': pa.float32(),
                                      'gv100card0': pa.int32(),
                                      'ps0_input_voltag': pa.int32(),
                                      'p1_core20_temp': pa.int32(),
                                      'dimm14_temp': pa.int32(),
                                      'p1_core16_temp': pa.int32(),
                                      'p0_core5_temp': pa.int32(),
                                      'gv100card4': pa.int32(),
                                      'gpu3_mem_temp': pa.int32(),
                                      'fan1_0': pa.int32(),
                                      'p0_vdd_temp': pa.int32(),
                                      'ps1_input_voltag': pa.int32(),
                                      'p1_core19_temp': pa.int32(),
                                      'p1_mem_power': pa.int32(),
                                      'p1_core22_temp': pa.int32(),
                                      'p0_mem_power': pa.int32(),
                                      'p1_core7_temp': pa.int32(),
                                      'dimm10_temp': pa.int32(),
                                      'p0_core16_temp': pa.int32(),
                                      'p1_core15_temp': pa.int32(),
                                      'p0_io_power': pa.int32(),
                                      'fan3_1': pa.int32(),
                                      'p0_core22_temp': pa.int32(),
                                      'dimm4_temp': pa.int32(),
                                      'p0_core20_temp': pa.int32(),
                                      'dimm7_temp': pa.int32(),
                                      'dimm15_temp': pa.int32(),
                                      'p0_core0_temp': pa.int32(),
                                      'p0_core11_temp': pa.int32(),
                                      'gpu4_mem_temp': pa.int32(),
                                      'p1_core23_temp': pa.int32(),
                                      'p1_core2_temp': pa.int32(),
                                      'gpu1_mem_temp': pa.int32(),
                                      'gpu4_core_temp': pa.int32(),
                                      'p1_core3_temp': pa.int32(),
                                      'p0_core8_temp': pa.int32(),
                                      'fan3_0': pa.int32(),
                                      'dimm9_temp': pa.int32(),
                                      'p0_core15_temp': pa.int32(),
                                      'p0_core1_temp': pa.int32(),
                                      'fan_disk_power': pa.int32(),
                                      'gv100card1': pa.int32(),
                                      'fan0_1': pa.int32(),
                                      'p1_core9_temp': pa.int32(),
                                      'dimm6_temp': pa.int32(),
                                      'dimm1_temp': pa.int32(),
                                      'gv100card3': pa.int32(),
                                      'p1_core14_temp': pa.int32(),
                                      'ps1_input_power': pa.int32(),
                                      'p1_core8_temp': pa.int32(),
                                      'p1_core21_temp': pa.int32(),
                                      'fan2_1': pa.int32(),
                                      'p0_core4_temp': pa.int32(),
                                      'p1_core12_temp': pa.int32(),
                                      'fan0_0': pa.int32(),
                                      'dimm12_temp': pa.int32(),
                                      'ps1_output_volta': pa.float32(),
                                      'p1_core0_temp': pa.int32(),
                                      'dimm3_temp': pa.int32(),
                                      'p0_core21_temp': pa.int32(),
                                      'pcie': pa.float32(),
                                      'p1_core10_temp': pa.int32(),
                                      'fan2_0': pa.int32(),
                                      'p0_core3_temp': pa.int32(),
                                      'p1_core6_temp': pa.int32(),
                                      'p0_core7_temp': pa.int32(),
                                      'gpu0_mem_temp': pa.int32(),
                                      'total_power': pa.int32(),
                                      'dimm8_temp': pa.int32(),
                                      'p0_core10_temp': pa.int32(),
                                      'p1_core4_temp': pa.int32(),
                                      'p1_core17_temp': pa.int32(),
                                      'p1_core11_temp': pa.int32(),
                                      'gpu0_core_temp': pa.int32(),
                                      'p0_core17_temp': pa.int32(),
                                      'p0_power': pa.int32(),
                                      'p0_core6_temp': pa.int32(),
                                      'p0_core19_temp': pa.int32(),
                                      'p1_vdd_temp': pa.int32(),
                                      'ps1_output_curre': pa.int32(),
                                      'p1_core1_temp': pa.int32(),
                                      'fan1_1': pa.int32(),
                                      'p1_io_power': pa.int32()}
                                      #'0_0': pa.int32(),

        self.dict_cols_per_metric = {'p1_core18_temp': ['node'],
                                     'dimm2_temp': ['node'],
                                     'p1_core5_temp': ['node'],
                                     'ps0_input_power': ['node'],
                                     'p0_core12_temp': ['node'],
                                     'p1_power': ['node'],
                                     'gpu3_core_temp': ['node'],
                                     'ps0_output_volta': ['node'],
                                     'p0_core14_temp': ['node'],
                                     'dimm11_temp': ['node'],
                                     'ps0_output_curre': ['node'],
                                     'dimm5_temp': ['node'],
                                     'p0_core2_temp': ['node'],
                                     'gpu1_core_temp': ['node'],
                                     'dimm0_temp': ['node'],
                                     'p0_core9_temp': ['node'],
                                     'p1_core13_temp': ['node'],
                                     'p0_core18_temp': ['node'],
                                     'p0_core13_temp': ['node'],
                                     'dimm13_temp': ['node'],
                                     'p0_core23_temp': ['node'],
                                     'ambient': ['node'],
                                     'gv100card0': ['node'],
                                     'ps0_input_voltag': ['node'],
                                     'p1_core20_temp': ['node'],
                                     'dimm14_temp': ['node'],
                                     'p1_core16_temp': ['node'],
                                     'p0_core5_temp': ['node'],
                                     'gv100card4': ['node'],
                                     'gpu3_mem_temp': ['node'],
                                     'fan1_0': ['node'],
                                     'p0_vdd_temp': ['node'],
                                     'ps1_input_voltag': ['node'],
                                     'p1_core19_temp': ['node'],
                                     'p1_mem_power': ['node'],
                                     'p1_core22_temp': ['node'],
                                     'p0_mem_power': ['node'],
                                     'p1_core7_temp': ['node'],
                                     'dimm10_temp': ['node'],
                                     'p0_core16_temp': ['node'],
                                     'p1_core15_temp': ['node'],
                                     'p0_io_power': ['node'],
                                     'fan3_1': ['node'],
                                     'p0_core22_temp': ['node'],
                                     'dimm4_temp': ['node'],
                                     'p0_core20_temp': ['node'],
                                     'dimm7_temp': ['node'],
                                     'dimm15_temp': ['node'],
                                     'p0_core0_temp': ['node'],
                                     'p0_core11_temp': ['node'],
                                     'gpu4_mem_temp': ['node'],
                                     'p1_core23_temp': ['node'],
                                     'p1_core2_temp': ['node'],
                                     'gpu1_mem_temp': ['node'],
                                     'gpu4_core_temp': ['node'],
                                     'p1_core3_temp': ['node'],
                                     'p0_core8_temp': ['node'],
                                     'fan3_0': ['node'],
                                     'dimm9_temp': ['node'],
                                     'p0_core15_temp': ['node'],
                                     'p0_core1_temp': ['node'],
                                     'fan_disk_power': ['node'],
                                     'gv100card1': ['node'],
                                     'fan0_1': ['node'],
                                     'p1_core9_temp': ['node'],
                                     'dimm6_temp': ['node'],
                                     'dimm1_temp': ['node'],
                                     'gv100card3': ['node'],
                                     'p1_core14_temp': ['node'],
                                     'ps1_input_power': ['node'],
                                     'p1_core8_temp': ['node'],
                                     'p1_core21_temp': ['node'],
                                     'fan2_1': ['node'],
                                     'p0_core4_temp': ['node'],
                                     'p1_core12_temp': ['node'],
                                     'fan0_0': ['node'],
                                     'dimm12_temp': ['node'],
                                     'ps1_output_volta': ['node'],
                                     'p1_core0_temp': ['node'],
                                     'dimm3_temp': ['node'],
                                     'p0_core21_temp': ['node'],
                                     'pcie': ['node'],
                                     'p1_core10_temp': ['node'],
                                     'fan2_0': ['node'],
                                     'p0_core3_temp': ['node'],
                                     'p1_core6_temp': ['node'],
                                     'p0_core7_temp': ['node'],
                                     'gpu0_mem_temp': ['node'],
                                     'total_power': ['node'],
                                     'dimm8_temp': ['node'],
                                     'p0_core10_temp': ['node'],
                                     'p1_core4_temp': ['node'],
                                     'p1_core17_temp': ['node'],
                                     'p1_core11_temp': ['node'],
                                     'gpu0_core_temp': ['node'],
                                     'p0_core17_temp': ['node'],
                                     'p0_power': ['node'],
                                     'p0_core6_temp': ['node'],
                                     'p0_core19_temp': ['node'],
                                     'p1_vdd_temp': ['node'],
                                     'ps1_output_curre': ['node'],
                                     'p1_core1_temp': ['node'],
                                     'fan1_1': ['node'],
                                     'p1_io_power': ['node']}
                                     #'0_0': ['node'],
    
    def get_schema_in(self, metric_name):
        schema_in = pa.schema([('', pa.int64()),
                               ('chnl', pa.string()),
                               ('cluster', pa.string()),
                               ('name', pa.string()),
                               ('node', pa.string()),
                               ('org', pa.string()),
                               ('plugin', pa.string()),
                               ('rack', pa.int64()),
                               ('slot', pa.int64()),
                               ("timestamp", pa.timestamp('us', tz='UTC')),
                               ('units', pa.string()),
                               ("value", self.value_type_per_metric[metric_name])])
        return schema_in

    def get_schema_out(self, metric_name):
        schema_out = pa.schema([("plugin", pa.string()),
                                ("metric", pa.string()),
                                ("year_month", pa.string()),
                                ("timestamp", pa.timestamp('ms', tz='UTC')),
                                ("value", self.value_type_per_metric[metric_name]), 
                                ("node", pa.string())])
                                #("timestamp", pa.timestamp('s', tz='UTC')),
        return schema_out

    def get_preprocessing_step1(self):
        def preprocessing(batches, schema_out):
            for batch in batches:

                metric = batch['name']
                
                # extracting month and year
                year_month = pc.strftime(batch['timestamp'], '%y-%m')

                # creating new batch from single arrays
                arrays = [batch['plugin'], metric, year_month, batch['timestamp'], batch['value'], batch['node']]
                batch = pa.RecordBatch.from_arrays(arrays, schema=schema_out)
            
                yield batch

        return preprocessing

    def get_preprocessing_step2(self):
        """Parquet to Parquet."""
        def preprocessing(batches, metric_name, schema_out, anonymization_dictionaries):
            for batch in batches:

                
                batch_size = len(batch)
                metric = pa.array([metric_name]*batch_size, type=pa.string())
                plugin = pa.array(['ipmi_pub']*batch_size)

                # extracting month and year
                year_month = pc.strftime(batch['timestamp'], '%y-%m')

                # truncating timestamp
                timestamp = pc.floor_temporal(batch['timestamp'], unit='second')
                
                # anonymize nodes
                # remove ".m100.cineca.it" when present
                node = batch['node'].to_pandas(). \
                       apply(lambda x: x if pd.isnull else x.split('.m100.cineca.it')[0]). \
                       apply(lambda x: str(anonymization_dictionaries['node'][x]))

                # creating new batch from single arrays
                arrays = [plugin, metric, year_month, timestamp, batch['value'], node]
                batch = pa.RecordBatch.from_arrays(arrays, schema=schema_out)
            
                yield batch

        return preprocessing
