import os
import pickle
from collections import defaultdict
import pyarrow as pa
import pyarrow.dataset as ds
from plugins.plugin_logic_factory import get_plugin_logic

#dataset_path = '/nas/cinecadataset/parquet_testbed/dataset_zstd_9'
dataset_path = '/nas/cinecadataset/parquet_testbed/dataset_zstd_9_mid_fix'
out_path = './schema_metadata'


if __name__ == '__main__':

    os.mkdir(out_path)

    # 1) dictionary encoded columns ("value" only for some metrics)
    print('Dictionary columns...')
    dict_cols = ['metric', 'plugin', 'year_month',
                 'partition', 'qos', 'job_state', #'user_id',
                 'description', 'host_group',
                 'panel', 'device',
                 'node',
                 'value']

    pickle.dump(dict_cols, open(os.path.join(out_path, 'dict_cols.pkl'), 'wb'))


    # 2) common schema ("value" column excluded)
    # In SLURM different tags for different metrics, no metric with all of them;
    # the schema is completed by the changes done in the next step (dict_cols)
    print('Common schema...')
    plugins = ['ganglia', 'ipmi', 'logics', 'nagios',
               'schneider', 'slurm', 'vertiv', 'weather',
               'job_table'] 

    schemas = []
    for plugin in plugins:
        plugin_logic = get_plugin_logic(plugin)
        metric1 = list(plugin_logic.dict_cols_per_metric.keys())[0]
        schema_out = plugin_logic.get_schema_out(metric1)

        if plugin != 'job_table':
            schema_out = schema_out.remove(schema_out.get_field_index('timestamp'))
            schema_out = schema_out.remove(schema_out.get_field_index('value'))

        schemas.append(schema_out)

    # union of schemas of all plugins
    common_schema = pa.unify_schemas(schemas)
    # common timestamp precision
    common_schema = common_schema.append(
        pa.field('timestamp', pa.timestamp('ms', tz='UTC')))

        
    # assigning correct dtype to dictionary columns
    # uint lacks support...
    for dict_col in dict_cols:

        # "value" dtype is handled in the query_tool
        if dict_col == 'value':
            continue

        common_schema = common_schema.set(
            common_schema.get_field_index(dict_col),
            pa.field(dict_col, pa.dictionary(pa.int16(), pa.string())))

    pickle.dump(common_schema, open(os.path.join(out_path, 'common_schema.pkl'), 'wb'))


    # 3) dictionaries of partitioning columns (inference)
    print('Inferring dictionaries...')

    part_schema = pa.schema([('year_month', pa.dictionary(pa.int8(), pa.string())),
                             ('plugin', pa.dictionary(pa.int8(), pa.string())),
                             ('metric', pa.dictionary(pa.int16(), pa.string()))])

    part = ds.partitioning(part_schema,
                           flavor='hive',
                           dictionaries='infer')

    parquet_format = ds.ParquetFileFormat(read_options={'dictionary_columns': dict_cols})
    data = ds.dataset(dataset_path,
                      format=parquet_format,
                      partitioning=part)

    part_cols_dictionaries ={'year_month': data.partitioning.dictionaries[0],
                             'plugin': data.partitioning.dictionaries[1],
                             'metric': data.partitioning.dictionaries[2]}

    pickle.dump(part_cols_dictionaries,
                open(os.path.join(out_path, 'part_cols_dictionaries.pkl'), 'wb'))
    

    # 4) extracting other informations from configurations of conversion scripts
    print('Other info...')
    plugins = ['ipmi', 'ganglia', 'vertiv', 'schneider',
               'weather', 'logics', 'nagios', 'slurm',
               'job_table']

    metrics_per_plugin = defaultdict(list)
    dtype_per_metric = {}
    tags_per_metric = {}
    for plugin in plugins:
        plugin_logic = get_plugin_logic(plugin)

        for metric, dtype in plugin_logic.value_type_per_metric.items():
            metrics_per_plugin[plugin].append(metric)
            dtype_per_metric[metric] = dtype    
            tags_per_metric[metric] = plugin_logic.get_schema_out(metric).names
            
    pickle.dump(dict(metrics_per_plugin),
                open(os.path.join(out_path,'metrics_per_plugin.pkl'), 'wb'))
    pickle.dump(dtype_per_metric,
                open(os.path.join(out_path,'dtype_per_metric.pkl'), 'wb'))
    pickle.dump(tags_per_metric,
                open(os.path.join(out_path,'tags_per_metric.pkl'), 'wb'))


    print('Done')
