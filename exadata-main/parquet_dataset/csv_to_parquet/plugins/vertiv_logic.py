import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
from plugins.plugin_logic import PluginLogic

class VertivLogic(PluginLogic):
    def __init__(self):
        super().__init__()

        self.data_path = '/nas/cinecadataset/Comp_2/vertiv_pub'

        self.sel_cols = ['plugin', 'name', 'timestamp', 'value', 'device']
                
        self.value_type_per_metric = {'Ext_Air_Sensor_A_Humidity': pa.float32(),
                                      'Ext_Air_Sensor_A_Temperature': pa.float32(),
                                      'Actual_Return_Humidity_Set_Point': pa.float32(),
                                      'Ext_Air_Sensor_B_Temperature': pa.float32(),
                                      'Dehumidifier_Utilization': pa.float32(),
                                      'Underflow_Static_Pressure': pa.float32(),
                                      'Ext_Air_Sensor_C_Humidity': pa.float32(),
                                      'Supply_Air_Temperature_Set_Point': pa.float32(),
                                      'Fan_Speed': pa.float32(),
                                      'Filter_Pressure_Drop': pa.float32(),
                                      'Reheat_Utilization': pa.float32(),
                                      'Free_Cooling_Valve_Open_Position': pa.float32(),
                                      'Humidity_Set_Point': pa.float32(),
                                      'Free_Cooling_Fluid_Temperature': pa.float32(),
                                      'Actual_Return_Air_Temperature_Set_Point': pa.float32(),
                                      'Ext_Air_Sensor_B_Humidity': pa.float32(),
                                      'Return_Air_Temperature': pa.float32(),
                                      'Compressor_Utilization': pa.float32(),
                                      'Humidifier_Utilization': pa.float32(),
                                      'Supply_Air_Temperature': pa.float32(),
                                      'Free_Cooling_Status': pa.float32(),
                                      'Return_Humidity': pa.float32(),
                                      'Ext_Air_Sensor_C_Temperature': pa.float32(),
                                      'Hot_Water___Hot_Gas_Valve_Open_Position': pa.float32(),
                                      'Adjusted_Humidity': pa.float32()}
        
        self.dict_cols_per_metric = {'Ext_Air_Sensor_A_Humidity': ['device'],
                                     'Ext_Air_Sensor_A_Temperature': ['device'],
                                     'Actual_Return_Humidity_Set_Point': ['device'],
                                     'Ext_Air_Sensor_B_Temperature': ['device'],
                                     'Dehumidifier_Utilization': ['device'],
                                     'Underflow_Static_Pressure': ['device'],
                                     'Ext_Air_Sensor_C_Humidity': ['device'],
                                     'Supply_Air_Temperature_Set_Point': ['device'],
                                     'Fan_Speed': ['device'],
                                     'Filter_Pressure_Drop': ['device'],
                                     'Reheat_Utilization': ['device'],
                                     'Free_Cooling_Valve_Open_Position': ['device'],
                                     'Humidity_Set_Point': ['device'],
                                     'Free_Cooling_Fluid_Temperature': ['device'],
                                     'Actual_Return_Air_Temperature_Set_Point': ['device'],
                                     'Ext_Air_Sensor_B_Humidity': ['device'],
                                     'Return_Air_Temperature': ['device'],
                                     'Compressor_Utilization': ['device'],
                                     'Humidifier_Utilization': ['device'],
                                     'Supply_Air_Temperature': ['device'],
                                     'Free_Cooling_Status': ['device'],
                                     'Return_Humidity': ['device'],
                                     'Ext_Air_Sensor_C_Temperature': ['device'],
                                     'Hot_Water___Hot_Gas_Valve_Open_Position': ['device'],
                                     'Adjusted_Humidity': ['device']}
 
 
    def get_schema_in(self, metric):
        schema_in = pa.schema([('', pa.int64()),
                               ('asset', pa.string()),
                               ('chnl', pa.string()),
                               ('device', pa.string()),
                               ('facility', pa.string()),
                               ('name', pa.string()),
                               ('org', pa.string()),
                               ('plugin', pa.string()),
                               ('room', pa.string()),
                               ('timestamp', pa.timestamp('s', tz='UTC')),
                               ('units', pa.string()),
                               ('value', pa.string())])
                               # read as string due to 'Unavailable' and 'unknown' values
                               #('value', self.value_type_per_metric[metric])])
        return schema_in

    def get_schema_out(self, metric):
        schema_out = pa.schema([("plugin", pa.string()),
                                ("metric", pa.string()),
                                ("year_month", pa.string()),
                                ("timestamp", pa.timestamp('s', tz='UTC')),
                                ('value', self.value_type_per_metric[metric]),
                                ("device", pa.string())])
        return schema_out

    def get_preprocessing_step1(self):
        def preprocessing(batches, schema_out):
            for batch in batches:

                metric = batch['name']

                # change strings to NaNs, to comply with output numerical formats
                value = pd.to_numeric(batch['value'].to_pandas(), errors='coerce')
                value = pa.Array.from_pandas(value)
                
                # extracting month and year
                year_month = pc.strftime(batch['timestamp'], '%y-%m')
                
                # creating new batch from single arrays
                arrays = [batch['plugin'], metric, year_month, batch['timestamp'], value, batch['device']]
                batch = pa.RecordBatch.from_arrays(arrays, schema=schema_out)
            
                yield batch

        return preprocessing

    def get_preprocessing_step2(self):
        """Parquet to Parquet."""
        def preprocessing(batches, metric_name, schema_out):
            for batch in batches:

                
                batch_size = len(batch)
                metric = pa.array([metric_name]*batch_size, type=pa.string())
                plugin = pa.array(['vertiv_pub']*batch_size)

                # extracting month and year
                year_month = pc.strftime(batch['timestamp'], '%y-%m')
                
                # creating new batch from single arrays
                arrays = [plugin, metric, year_month, batch['timestamp'], batch['value'], batch['device']]
                batch = pa.RecordBatch.from_arrays(arrays, schema=schema_out)
            
                yield batch

        return preprocessing
