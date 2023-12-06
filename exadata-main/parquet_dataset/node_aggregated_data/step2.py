import sys
sys.path.append('/nas/home/cdisanti/examon-dataset/parquet_dataset/query_tool')
from query_tool import M100DataClient
import os
import time
import logging
import multiprocessing as mp
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

NPROC=48
dataset_path = '/nas/cinecadataset/parquet_testbed/dataset_zstd_9_mid_fix'
step1_path = './results_temp'
results_path = './aggregated_data_per_node'
pa.set_io_thread_count(48)
pa.set_cpu_count(48)

def worker(queue, ipmi_metrics):
    logger = logging.getLogger(__name__)
    while True:
        queue_tuple = queue.get()

        if queue_tuple is None:
            break
            
        s = time.time()

        node, state_node = queue_tuple

        first_done = False
        for i, metric in enumerate(ipmi_metrics):
            node_metric_path = os.path.join(step1_path, f'/node={node}/metric={metric}/')
            if os.path.exists(node_metric_path):
                #s = time.time()
                cols = ['timestamp'] + [metric+suffix for suffix in ['_avg', '_std', '_min', '_max']]
                
                if first_done:
                    df_o = pq.read_table(node_metric_path, columns=cols).to_pandas()
                    df = df.merge(df_o, how='inner', on='timestamp')
                else:
                    df = pq.read_table(node_metric_path, columns=cols).to_pandas()
                    first_done = True
      
                if len(df) == 0:
                    logging.info(f'[{node}] Empty when joining with {metric}: interrupting')
                    break
                #   logging.info(node, metric, i, time.time()-s, len(df))


        # left join with labels
        if first_done and len(df)>0:
            df = df.merge(state_node, how='left', on='timestamp').drop('node', axis=1)

            #df.to_parquet(os.path.join('./aggregated_data_per_node',f'{node}.parquet'), index=False)
            df = pa.Table.from_pandas(df)
            pq.write_table(df,
                           os.path.join('./aggregated_data_per_node',f'{node}.parquet'),
                           compression='zstd',
                           compression_level=19)
        
        logging.info(f'[{node}] Done in {time.time()-s}')


if __name__ == '__main__':

    # logger
    logging.basicConfig(filename='./logs/step2_1.log',
                        level=logging.INFO,
                        format='[%(asctime)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    s0 = time.time()
    client = M100DataClient(dataset_path)
 
    ipmi_metrics = sorted(client.metrics_per_plugin['ipmi'])
    ipmi_metrics.remove('0_0') # test metric that still has to be removed 
    ipmi_nodes = [x.split('=')[1] for x in os.listdir(step1_path)]
    
    s1=time.time()
    labels = client.query('state',
                          description='batchs::client::state',
                          columns=['timestamp', 'value', 'node'])
        
    labels = labels[labels.node.isin(ipmi_nodes)]
    labels.node = labels.node.cat.remove_unused_categories()
    logging.info(time.time()-s1)

    # splitting labels by node
    s2 = time.time()
    label_nodes = [x for x in labels.groupby('node')]
    logging.info(time.time()-s2)
    del labels
    
    os.makedirs(results_path, exist_ok=True)

    # multiprocessing
    queue = mp.Queue()
    #iolock = mp.Lock()

    s3 = time.time()
    while len(label_nodes) > 0:
        queue.put(label_nodes.pop())
    logging.info(time.time()-s3)

    # terminate workers
    for _ in range(NPROC):
        queue.put(None)

    pool = mp.Pool(NPROC, initializer=worker, initargs=(queue,
                                                        ipmi_metrics))

    # waiting
    pool.close()
    pool.join()

    logging.info(f'Done all in {time.time()-s0}')
