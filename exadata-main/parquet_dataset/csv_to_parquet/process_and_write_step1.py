import time
import os
import pyarrow as pa
import pyarrow.dataset as ds
from pyarrow import fs
from plugins.plugin_logic_factory import get_plugin_logic

pa.set_cpu_count(45)

plugin = 'nagios'
output_dataset = '/nas/cinecadataset/parquet_testbed/test_nagios'

#def file_visitor(written_file):
#    print(f'[{datetime.datetime.now()}][Wrote] {written_file.path}')

if __name__ == '__main__':
    s = time.time()

    # plugin-specific configuration and CSVs path
    plugin_logic = get_plugin_logic(plugin)
    plugin_path = plugin_logic.data_path
    
    metrics = list(plugin_logic.value_type_per_metric.keys())

    for i, metric in enumerate(metrics):
        print(i, metric)
        sm = time.time()

        # metric-specific schema_in and schema_out (PyArrow)
        schema_in = plugin_logic.get_schema_in(metric)
        schema_out = plugin_logic.get_schema_out(metric)

        # finding all files of the metric
        fnames = [fname for fname in os.listdir(os.path.join(plugin_path, metric))
                  if fname.endswith('.csv.gz')]

        # pyarrow.dataset abstraction over the raw CSV files
        local_fs = fs.SubTreeFileSystem(os.path.join(plugin_path, metric),
                                        fs.LocalFileSystem())

        dataset = ds.FileSystemDataset. \
                  from_paths(fnames,
                             format=ds.CsvFileFormat(),
                             filesystem=local_fs,
                             schema=schema_in)


        # reading in batches (lazy)
        if plugin == 'slurm': # metric-specific tags in SLURM
            metric_cols = plugin_logic.common_cols + plugin_logic.specific_cols_per_metric[metric]
            #batches = dataset.to_batches(columns=metric_cols)
            batches = dataset.to_batches(columns=metric_cols, batch_size=2048)
        else:
            #batches = dataset.to_batches(columns=plugin_logic.sel_cols)
            batches = dataset.to_batches(columns=plugin_logic.sel_cols, batch_size=2048)

        # processing batches (lazy)
        batch_processing_fn = plugin_logic.get_preprocessing_step1()
        processed_batches = batch_processing_fn(batches, schema_out)

        # metric-specific columns to dictionary encode
        dict_cols = plugin_logic.dict_cols_per_metric[metric]

        # writing processed batches to the partitioned dataset
        write_options = ds.ParquetFileFormat(). \
                        make_write_options(compression='zstd',
                                           compression_level=9,
                                           version='2.6',
                                           use_dictionary=dict_cols,
                                           data_page_version='2.0')
        
        ds.write_dataset(processed_batches,
                         base_dir = output_dataset,
                         basename_template = 'a_{i}.parquet',
                         format = 'parquet',
                         partitioning = ['year_month', 'plugin', 'metric'],
                         schema = schema_out,
                         partitioning_flavor = 'hive',
                         file_options = write_options,
                         existing_data_behavior='delete_matching',
                         min_rows_per_group=2*10**6,
                         max_rows_per_group=10*10**6,
                         max_open_files=1000,
                         max_rows_per_file=2*10**8)
                         #file_visitor=file_visitor,

        print(f'Done {metric} in {time.time()-sm} seconds.')

    print(f'Done all in {time.time()-s} seconds.')
