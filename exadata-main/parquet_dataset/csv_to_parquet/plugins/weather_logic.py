import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
from plugins.plugin_logic import PluginLogic

class WeatherLogic(PluginLogic):
    def __init__(self):
        super().__init__()

        self.data_path = '/nas/cinecadataset/Comp_2/weather_pub'

        self.sel_cols = ['plugin', 'name', 'timestamp', 'value', 'org', 'type']
        
        self.value_type_per_metric = {'wind_deg':pa.int32(),
                                      'visibility':pa.int32(),
                                      'dew_point':pa.float32(),
                                      'temp':pa.float32(),
                                      'uvi':pa.float32(),
                                      'feels_like':pa.float32(),
                                      'humidity':pa.int32(),
                                      'pressure':pa.int32(),
                                      'clouds':pa.int32(),
                                      'wind_speed':pa.float32()}

        self.dict_cols_per_metric = {'wind_deg': False,
                                     'visibility': False,
                                     'dew_point': False,
                                     'temp': False,
                                     'uvi': False,
                                     'feels_like': False,
                                     'humidity': False,
                                     'pressure': False,
                                     'clouds': False,
                                     'wind_speed': False}
                
    def get_schema_in(self, metric):

        schema_in = pa.schema([('', pa.int64()),
                               ('chnl', pa.string()),
                               ('facility', pa.string()),
                               ('name', pa.string()),
                               ('org', pa.string()),
                               ('plugin', pa.string()),
                               ('provider', pa.string()),
                               ('timestamp', pa.timestamp('s', tz='UTC')),
                               ('type', pa.string()),
                               ('units', pa.string()),
                               ('value', self.value_type_per_metric[metric])])

        return schema_in

    def get_schema_out(self, metric):

        schema_out = pa.schema([('plugin', pa.string()),
                                ('metric', pa.string()),
                                ('year_month', pa.string()),
                                ('timestamp', pa.timestamp('s', tz='UTC')),
                                ('value', self.value_type_per_metric[metric])])

        return schema_out

    def get_preprocessing_step1(self):
        def preprocessing(batches, schema_out):
            for batch in batches:

                # select org=cineca
                org = batch['org']
                mask = pc.equal(org, 'cineca')
                batch = batch.filter(mask)

                # select only type=current values; we don't want the forecasts
                mask = pc.equal(batch['type'], 'current')
                batch = batch.filter(mask)

                metric = batch['name']

                # extracting month and year
                year_month = pc.strftime(batch['timestamp'], '%y-%m')
                
                # creating new batch from single arrays
                arrays = [batch['plugin'], metric, year_month, batch['timestamp'], batch['value']]
                batch = pa.RecordBatch.from_arrays(arrays, schema=schema_out)
            
                yield batch

        return preprocessing

    def get_preprocessing_step2(self):
        """Parquet to Parquet."""
        def preprocessing(batches, metric_name, schema_out):
            for batch in batches:

                
                batch_size = len(batch)
                metric = pa.array([metric_name]*batch_size, type=pa.string())
                plugin = pa.array(['weather_pub']*batch_size)

                # extracting month and year
                year_month = pc.strftime(batch['timestamp'], '%y-%m')
                
                # creating new batch from single arrays
                arrays = [plugin, metric, year_month, batch['timestamp'], batch['value']]
                batch = pa.RecordBatch.from_arrays(arrays, schema=schema_out)
            
                yield batch

        return preprocessing
    