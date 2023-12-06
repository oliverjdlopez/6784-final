import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
from plugins.plugin_logic import PluginLogic

class LogicsLogic(PluginLogic):
    def __init__(self):
        super().__init__()

        self.data_path = '/nas/cinecadataset/Comp_2/logics_pub'

        self.sel_cols = ['plugin', 'name', 'timestamp', 'value', 'panel', 'device']
                
        self.value_type_per_metric = {'deviceid': pa.int32(),
                                      'Tot': pa.float32(),
                                      'Volt2': pa.float32(),
                                      'Potenza_attiva': pa.float32(),
                                      'pit': pa.int32(),
                                      'Corrente_L3': pa.float32(),
                                      'Volt3': pa.int32(),
                                      'Pue': pa.float32(),
                                      'ID_Modbus': pa.int32(),
                                      'Bad_values': pa.int32(),
                                      'pt': pa.int32(),
                                      'Mwh': pa.float32(),
                                      'Tot_qpompe': pa.float32(),
                                      'pue': pa.float32(),
                                      'Corrente_L1': pa.float32(),
                                      'Mw': pa.float32(),
                                      'Fattore_di_potenza': pa.float32(),
                                      'Tot_cdz': pa.float32(),
                                      'Tot_chiller': pa.float32(),
                                      'Comlost': pa.float32(),
                                      'Tot_servizi': pa.float32(),
                                      'Potenza': pa.float32(),
                                      'Mvar': pa.float32(),
                                      'Stato': pa.int32(),
                                      'Tensione': pa.int32(),
                                      'Dcie': pa.float32(),
                                      'Status': pa.int32(),
                                      'Frequenza': pa.float32(),
                                      'Prototype': pa.string(),
                                      'address': pa.string(),
                                      'Corrente': pa.float32(),
                                      'Mvarh': pa.float64(),
                                      'Tot_ict': pa.float32(),
                                      'Volt1': pa.int32(),
                                      'Gateway': pa.string(),
                                      'Energia': pa.float64(),
                                      'Corrente_L2': pa.float32()}
        
        self.dict_cols_per_metric = {'deviceid':['device', 'panel'],
                                     'Tot':['device', 'panel'],
                                     'Volt2':['device', 'panel'],
                                     'Potenza_attiva':['device', 'panel'],
                                     'pit':['device', 'panel'],
                                     'Corrente_L3':['device', 'panel'],
                                     'Volt3':['device', 'panel'],
                                     'Pue':['device', 'panel'],
                                     'ID_Modbus':['device', 'panel'],
                                     'Bad_values':['device', 'panel'],
                                     'pt':['device', 'panel'],
                                     'Mwh':['device', 'panel'],
                                     'Tot_qpompe':['device', 'panel'],
                                     'pue':['device', 'panel'],
                                     'Corrente_L1':['device', 'panel'],
                                     'Mw':['device', 'panel'],
                                     'Fattore_di_potenza':['device', 'panel'],
                                     'Tot_cdz':['device', 'panel'],
                                     'Tot_chiller':['device', 'panel'],
                                     'Comlost':['device', 'panel'],
                                     'Tot_servizi':['device', 'panel'],
                                     'Potenza':['device', 'panel'],
                                     'Mvar':['device', 'panel'],
                                     'Stato':['device', 'panel'],
                                     'Tensione':['device', 'panel'],
                                     'Dcie':['device', 'panel'],
                                     'Status':['device', 'panel'],
                                     'Frequenza':['device', 'panel'],
                                     'Prototype':['device', 'panel', 'value'],
                                     'address':['device', 'panel', 'value'],
                                     'Corrente':['device', 'panel'],
                                     'Mvarh':['device', 'panel'],
                                     'Tot_ict':['device', 'panel'],
                                     'Volt1':['device', 'panel'],
                                     'Gateway':['device', 'panel', 'value'],
                                     'Energia':['device', 'panel'],
                                     'Corrente_L2':['device', 'panel']}
        
    def get_schema_in(self, metric):

        schema_in = pa.schema([('', pa.int64()),
                               ('asset', pa.string()),
                               ('chnl', pa.string()),
                               ('device', pa.string()),
                               ('facility', pa.string()),
                               ('name', pa.string()),
                               ('org', pa.string()),
                               ('panel', pa.string()),
                               ('plugin', pa.string()),
                               ('timestamp', pa.timestamp('s', tz='UTC')),
                               ('type', pa.string()),
                               ('units', pa.string()),
                               ('value', pa.string())])
   
        return schema_in

    def get_schema_out(self, metric):
        schema_out = pa.schema([("plugin", pa.string()),
                                ("metric", pa.string()),
                                ("year_month", pa.string()),
                                ("timestamp", pa.timestamp('s', tz='UTC')),
                                ('value', self.value_type_per_metric[metric]),
                                ("panel", pa.string()),
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
                arrays = [batch['plugin'], metric, year_month, batch['timestamp'], value, batch['panel'], batch['device']]
                batch = pa.RecordBatch.from_arrays(arrays, schema=schema_out)
            
                yield batch

        return preprocessing

    def get_preprocessing_step2(self):
        """Parquet to Parquet."""
        def preprocessing(batches, metric_name, schema_out):
            for batch in batches:

                
                batch_size = len(batch)
                metric = pa.array([metric_name]*batch_size, type=pa.string())
                plugin = pa.array(['logics_pub']*batch_size)

                # extracting month and year
                year_month = pc.strftime(batch['timestamp'], '%y-%m')
                
                # creating new batch from single arrays
                arrays = [plugin, metric, year_month, batch['timestamp'], batch['value'], batch['panel'], batch['device']]
                batch = pa.RecordBatch.from_arrays(arrays, schema=schema_out)
            
                yield batch

        return preprocessing
    