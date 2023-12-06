import sys
import logging
from examon.examon import Examon, ExamonQL
import pytz
import pandas as pd
import multiprocessing
import datetime
import os
import random
import time
from configparser import ConfigParser
  
       
plugin_has_cluster_tag = { 
    'ganglia_pub': True,
    'ipmi_pub': True,
    'logics_pub': False,
    'nagios_pub': True,
    'schneider_pub': False,
    'slurm_pub': True,
    'vertiv_pub': False,
    'weather_pub': False,
    'job_table' : 'job_table' # no real plugin, just for names (paths etc.)
}  


wanted_tags_per_plugin = {
    'vertiv_pub': ['*'], #['device'],
    'schneider_pub': ['*'], #['panel'],
    'ganglia_pub': ['*'],
    'slurm_pub': ['*'], #['partition', 'job_state', 'user_id', 'qos'],
    'ipmi_pub': ['*'],  
    'logics_pub': ['*'], 
    'nagios_pub': ['*'], 
    'vertiv_pub': ['*'], 
    'weather_pub': ['*'] 
}



def check_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)
        print(path+" ==> CREATED.")


def csv_file_name_creator(path, file_name, log=False):
    '''
    Create a file name.
    '''
    counter = 0
    while os.path.isfile(path+file_name):
        counter += 1
        file_name, file_fromat = file_name.split('.csv')[0], file_name.split('.csv')[1:]
        file_fromat = 'csv' + '.'.join(file_fromat)
        file_name = file_name.split('(')[0]+'('+str(counter)+').'+file_fromat
    print('File name is : '+str(file_name))    
    if log == True:
        logger.info('File name is : '+str( file_name))
    return file_name


def csv_save_data(data, path, file_name):
    if not os.path.isdir(path):
        logger.info('There is no path ==>'+str(path))
        os.makedirs(path)
        logger.info('Path created! ==> '+str(path))
    try:
        file_name_checked = csv_file_name_creator(path, file_name)
        if file_name_checked != file_name:
            logger.info('There is file with same name - '+str(file_name)+' - so the file name updated to'+str(file_name_checked))
        data.to_csv(path+'/'+file_name_checked, compression='gzip', encoding='utf-8')
    except Exception as e:
        logger.error('Error'+str(e))


def check_follow_file(pth, follow_file):
    if not os.path.isfile(pth + follow_file):
        if not os.path.isdir(pth):
            logger.info('There is no path ==>'+str(pth))
            os.makedirs(pth)
            logger.info('Path created! ==> '+str(pth))
        pd.DataFrame([['2020-03-09 00:00:00', 0, 0]], columns=['datetime', 'row', 'col']).to_csv(pth + follow_file, index=False)
        logger.info(pth + follow_file+' created')
        

def metrics_chunks(metrics_dataframe, number_rows_chunks):
    
    mrt_chunks = [metrics_dataframe[i:i+number_rows_chunks].copy()
                  for i in range(0, metrics_dataframe.shape[0], number_rows_chunks)]
    random.shuffle(mrt_chunks)
    return mrt_chunks

                
def dxt(sq, tstart, tstop, metric, plugin, selected_tags):
    if plugin_has_cluster_tag[plugin]== True:
        df = sq.SELECT(*selected_tags).FROM(metric).WHERE(cluster='marconi100').TSTART(tstart).TSTOP(tstop).execute().df_table
    
    elif plugin_has_cluster_tag[plugin] == False:
        df = sq.SELECT(*selected_tags).FROM(metric).TSTART(tstart).TSTOP(tstop).execute().df_table
    
    elif plugin_has_cluster_tag[plugin]== 'job_table':    
        sq.jc.JOB_TABLES.add('job_info_marconi100')
        data = sq.SELECT('*').FROM('job_info_marconi100').TSTART(tstart).TSTOP(tstop).execute()
        df = pd.read_json(data)

    return df

      
def TryAgain(metrics):
    
    global logger
    logger = logging.getLogger(str(os.getpid()))
    logger.setLevel(logging.INFO)
    log_file_name = 'Try_Again_'+str(os.getpid()) + '_' + datetime.datetime.strftime(datetime.datetime.now(pytz.timezone('Europe/Rome')), '%Y-%m-%d').replace(':','-').replace(' ','_')+'.log'
    formatter = logging.Formatter('%(levelname)s:%(process)d:%(processName)s:%(thread)d:%(threadName)s:%(asctime)s:%(lineno)d:%(message)s')

    if not logger.handlers:
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(loggin_path + log_file_name)
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler) 
        
    configur = ConfigParser()
    configur.read('../config.ini')
    
  
    KAIROSDB_SERVER = configur.get('examon_config','KAIROSDB_SERVER')
    KAIROSDB_PORT = configur.get('examon_config','KAIROSDB_PORT')
    USER = configur.get('examon_config','USER')
    PWD = configur.get('examon_config','PWD')
    
    ex = Examon(KAIROSDB_SERVER, port=KAIROSDB_PORT, user=USER, password=PWD, verbose=False, proxy=True)
    sq = ExamonQL(ex)
    
    logger.info('The connection to the Examon is created.')

    complete_date = pd.date_range(start='2020-03-09 00:00:00', 
                                  end=datetime.datetime.now(pytz.timezone('Europe/Rome')).date()-datetime.timedelta(days=1), 
                                  freq='24H')


    for _, row in metrics.iterrows():
        plugin, metric = row[1], row[0]
        # [Need to update if using selected tags]
        # Select tags to download
        # metric_tags = sq.DESCRIBE(metric).execute()['tag key'].tolist()
        # selected_tags = [tag for tag in wanted_tags_per_plugin[plugin] if tag in metric_tags]
        selected_tags = ['*']
        
        # Checking follow_file (retrieving holes) 
        # follow_file = pth_data_files+'/follow/'+plugin+'_'+metric+'_follow_dxt.csv'
        
        logger.info(25*'-*-')
        logger.info(str(plugin)+' -- '+str(metric))
        
        follow_file = plugin+'_'+metric+'_follow_dxt.csv'
        check_follow_file(pth_data_files+'/follow/', follow_file)
        
        
        logger.info(pth_data_files+'/follow/'+follow_file)
        remain =  set([datetime.datetime.strftime(d, '%Y-%m-%d %H:%M:%S') for d in complete_date]).\
                    difference(set(pd.read_csv(pth_data_files+'/follow/'+follow_file)['datetime']))

        if len(remain): 
            logger.info('Data Extraction Remain Dates: '+str(remain))
        else:
            logger.info('Your dataset is already updated.')


        for stop in remain:
            stop  = datetime.datetime.strptime(stop, '%Y-%m-%d %H:%M:%S') 
            start = stop - datetime.timedelta(days=1)
            try:
                result = dxt(sq=sq,
                             tstart=datetime.datetime.strftime(start, '%d-%m-%Y %H:%M:%S'),
                             tstop= datetime.datetime.strftime(stop,  '%d-%m-%Y %H:%M:%S'), 
                             metric=metric,
                             plugin=plugin, 
                             selected_tags=selected_tags)

                path = pth_data_files + '/'+plugin+'/'+metric+'/'
                rng = datetime.datetime.strftime(start, '%Y-%m-%d %H:%M:%S').replace(':','-').replace(' ','_') + '_to_' + datetime.datetime.strftime(stop, '%Y-%m-%d %H:%M:%S').replace(':','-').replace(' ','_')
                file_name = metric.replace('.','_')+'_'+rng+'.csv.gz'

                if result.shape[0] != 0:
                    csv_save_data(result, path, file_name)

                pd.DataFrame([[datetime.datetime.strftime(stop, '%Y-%m-%d %H:%M:%S'), result.shape[0], result.shape[1]]]).to_csv(pth_data_files+'follow/'+follow_file, index=False, mode='a', header=False)
                logger.info(str(plugin)+'_'+str(metric)+' Try Again Backup saved for '+str(datetime.datetime.strftime(stop, '%Y-%m-%d %H:%M:%S')) + ' Shape ' + str(result.shape))

            except Exception as e:
                print(e)
                logger.error('Error'+str(e)+' ==> '+str(plugin)+'_'+str(metric))

        logger.info(50*'+')
        
       
if __name__ == '__main__':
    now = datetime.datetime.now(pytz.timezone('Europe/Rome'))
    pth_data_files = '/nas/cinecadataset/Comp_2/'
    loggin_path =    '/nas/cinecadataset/Comp_2/log/TryAgainlog_'+str(datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S').replace(':', '-').replace(' ', '_'))+'/'
    check_dir(loggin_path)

    main_logger = logging.getLogger(str(os.getpid()))
    main_logger.setLevel(logging.INFO)
    main_log_file_name = 'Main_Try_Again_'+str(os.getpid()) + '_' + datetime.datetime.strftime(datetime.datetime.now(pytz.timezone('Europe/Rome')), '%Y-%m-%d').replace(':','-').replace(' ','_')+'.log'
    formatter = logging.Formatter('%(levelname)s:%(process)d:%(processName)s:%(thread)d:%(threadName)s:%(asctime)s:%(lineno)d:%(message)s')

    if not main_logger.handlers:
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(loggin_path + main_log_file_name)
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        main_logger.addHandler(file_handler)
        main_logger.addHandler(stream_handler) 


    time_for_start_script = 22
    processes = 15
    number_rows_chunks = 1

    metrics_dataframe = pd.read_csv('M100_metrics.csv')

    while True:
        try: 
            print('Start !!!')
            with multiprocessing.Pool(processes=processes) as pool:
                pool.map(TryAgain, metrics_chunks(metrics_dataframe=metrics_dataframe, number_rows_chunks=number_rows_chunks))
            logger.info(20*' Done ')
        except Exception as e:
            print(e)
            # main_logger.error('Error'+str(e)+' ==> '+str(plugin)+'_'+str(metric))   
        time.sleep(60*60*6)    

