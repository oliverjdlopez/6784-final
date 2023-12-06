import time
import pickle
import multiprocessing as mp
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.compute as pc
from plugins.plugin_logic_factory import get_plugin_logic

#pa.set_cpu_count(45)
NPROC=4

plugin = 'job_table'
og_path = '/nas/cinecadataset/parquet_testbed/dataset_zstd_9'
output_dataset = '/nas/cinecadataset/parquet_testbed/dataset_zstd_9_mid_fix_node_anonymized'

# anonymization dictionaries
anon_dicts_path = '/nas/home/cdisanti/dump_scripts_and_data/parquet_tests/anonymization_dictionaries/'
job_id_dict = pickle.load(open(anon_dicts_path + 'job_id_dict.pkl', 'rb'))
user_id_dict = pickle.load(open(anon_dicts_path + 'user_id_dict.pkl', 'rb'))
partition_dict = pickle.load(open(anon_dicts_path + 'partition_dict.pkl', 'rb'))
qos_dict = pickle.load(open(anon_dicts_path + 'qos_dict.pkl', 'rb'))
node_dict = pickle.load(open(anon_dicts_path + 'node_dict.pkl', 'rb'))

anonymization_dictionaries = {}
anonymization_dictionaries['job_id'] = job_id_dict
anonymization_dictionaries['array_job_id'] = job_id_dict
anonymization_dictionaries['dependency'] = job_id_dict
anonymization_dictionaries['partition'] = partition_dict
anonymization_dictionaries['qos'] = qos_dict
anonymization_dictionaries['user_id'] = user_id_dict
anonymization_dictionaries['node'] = node_dict
anonymization_dictionaries['alloc_node'] = node_dict
anonymization_dictionaries['batch_host'] = node_dict

def midnight_fix(fragment):
    tab = fragment.to_table()

    hours = pc.hour(tab['end_time'])
    minutes = pc.minute(tab['end_time'])
    seconds = pc.second(tab['end_time'])
    millis = pc.millisecond(tab['end_time'])

    filt00 = pc.and_(pc.equal(hours, 22), pc.equal(minutes, 0))
    filt01 = pc.and_(pc.equal(seconds, 0), pc.equal(millis, 0))
    filt0 = pc.and_(filt00, filt01)
    filt10 = pc.and_(pc.equal(hours, 23), pc.equal(minutes, 0))
    filt1 = pc.and_(filt10, filt01)
    filt = pc.or_(filt0, filt1)

    df = tab.filter(filt).to_pandas()
    df_filtered = df.drop_duplicates()

    filtered_chunk = pa.Table.from_pandas(df_filtered, schema=tab.schema)
    new_tab = pa.concat_tables([tab.filter(pc.invert(filt)), filtered_chunk])

    batches = new_tab.to_batches(None)
    for batch in batches:
        yield batch

if __name__ == '__main__':
    s = time.time()

    schema_in = pickle.load(open('./schema_metadata/common_schema.pkl', 'rb'))
    part_cols_dictionaries = pickle.load(open('./schema_metadata/part_cols_dictionaries.pkl', 'rb'))


    # plugin specific "logic" and CSVs path
    plugin_logic = get_plugin_logic(plugin)
    plugin_path = plugin_logic.data_path
    
    metrics = list(plugin_logic.value_type_per_metric.keys())

    for i, metric in enumerate(metrics):
        print(i, metric, flush=True)
        sm = time.time()

        # metric-specific schema_in and schema_out (PyArrow)
        schema_out = plugin_logic.get_schema_out(metric)
        #schema_in = schema_out
        schema_in = None # job_table, changed schema out

        # reading from parquet dataset (first complete iteration)
        part = ds.partitioning(schema_in,
                               flavor='hive',
                               dictionaries=part_cols_dictionaries)
        dataset = ds.dataset(og_path, partitioning=part, schema=schema_in)

        fragments = dataset.get_fragments(ds.field('metric')==metric)

        processed_batches = []
        for fragment in fragments:

            batches = midnight_fix(fragment)

            batch_processing_fn = plugin_logic.get_preprocessing_step2()
            processed_batches.extend(batch_processing_fn(batches,
                                                         metric,
                                                         schema_out,
                                                         anonymization_dictionaries))

        # materializing one single table, to get larger row_groups with write_dataset
        new_tab = pa.Table.from_batches(processed_batches)

        # metric-specific columns to dictionary encode
        dict_cols = plugin_logic.dict_cols_per_metric[metric]

        # writing processed batches to the partitioned dataset
        write_options = ds.ParquetFileFormat(). \
                        make_write_options(compression='zstd',
                                            compression_level=9,
                                            version='2.6',
                                            use_dictionary=dict_cols,
                                            data_page_version='2.0',
                                            data_page_size = 2*1024**2) 
        
        ds.write_dataset(new_tab,
                        base_dir = output_dataset,
                        basename_template = 'a_{i}.parquet',
                        format = 'parquet',
                        partitioning = ['year_month', 'plugin', 'metric'],
                        schema = schema_out,
                        partitioning_flavor = 'hive',
                        file_options = write_options,
                        existing_data_behavior='delete_matching',
                        min_rows_per_group=2*10**5,
                        max_rows_per_group=5*10**5,
                        max_open_files=1000)

        print(f'Done {metric} in {time.time()-sm} seconds.', flush=True)

    print(f'Done all in {time.time()-s} seconds.')
