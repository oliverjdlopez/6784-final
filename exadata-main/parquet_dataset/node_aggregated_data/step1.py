import sys
sys.path.append('/nas/home/cdisanti/examon-dataset/parquet_dataset/query_tool')
from query_tool import M100DataClient
import pyarrow as pa
import pandas as pd
import numpy as np
import time
import multiprocessing as mp
import os


NPROC=48
dataset_path = '/nas/cinecadataset/parquet_testbed/dataset_zstd_9_mid_fix'
results_path = './results_temp'
pa.set_io_thread_count(48)
pa.set_cpu_count(48)


def custom_resampler(arraylike):
    if len(arraylike):
        avg = np.sum(arraylike)/len(arraylike)
        std = np.std(arraylike)
        m = min(arraylike)
        M = max(arraylike)
        return (avg, std, m, M)
    else:
        return(np.nan, np.nan, np.nan, np.nan)


def resample_metric(df, metric, freq = '15T'):
    fdf = df
    fdf = fdf.set_index('timestamp')
    fdf = fdf.resample(rule = freq, origin = 'start_day').apply(custom_resampler)
    
    new_cols = [f'{metric}_avg', f'{metric}_std', f'{metric}_min', f'{metric}_max']
    fdf[new_cols] = pd.DataFrame(fdf['value'].tolist(), index=fdf.index)
    fdf = fdf.drop('value', axis = 1)
    return fdf
        

def resample_metric_mp(queue, month, iolock, metric, freq = '15T'):
    while True:
        node_tuple = queue.get()

        if node_tuple is None:
            break
        
        node, df_node = node_tuple

        resampled_col = resample_metric(df_node.drop('node', axis=1), metric, freq).reset_index()

        out_path = os.path.join(results_path, f'/node={node}/metric={metric}/year_month={month}')
        os.makedirs(out_path, exist_ok=True)
        resampled_col.to_parquet(os.path.join(out_path,'a_0.parquet'), index=False)
        #with iolock:
        #    print(f'[Worker] Wrote {out_path}')

    #with iolock:
    #    print('[Worker] Done.')


if __name__ == '__main__':

    client = M100DataClient(dataset_path)

    metrics =  client.metrics_per_plugin['ipmi']

    months = pd.date_range('2020-03-01', '2022-09-01', freq='MS').strftime('%y-%m').tolist()

    for i, metric in enumerate(metrics):
        s0 = time.time()
        for month in months:

            s1=time.time()
            df = client.query(metric, columns=['timestamp', 'value', 'node'], year_month=month)
            print(time.time()-s1)

            # splitting df by node; not parallelized atm...
            s3 = time.time()
            dfs = [x for x in df.groupby('node')]
            del df

            with mp.Manager() as manager:
                queue = mp.Queue()
                iolock = mp.Lock()
                pool = mp.Pool(NPROC, initializer=resample_metric_mp, initargs=(queue,
                                                                                month,
                                                                                iolock,
                                                                                metric,
                                                                                '15T'))


            while len(dfs) > 0:
                queue.put(dfs.pop())


            # terminate workers
            for _ in range(NPROC):
                queue.put(None)

            # waiting
            pool.close()
            pool.join()

            print(f'Done {metric} {month} in {time.time()-s1}')

        print(f'Done {i+1} ({metric}) in {time.time()-s0}')
