from plugins.vertiv_logic import VertivLogic
from plugins.schneider_logic import SchneiderLogic
from plugins.ipmi_logic import IPMILogic
from plugins.ganglia_logic import GangliaLogic
from plugins.logics_logic import LogicsLogic
from plugins.nagios_logic import NagiosLogic
from plugins.weather_logic import WeatherLogic
from plugins.slurm_logic import SLURMLogic
from plugins.job_table_logic import JobTableLogic

def get_plugin_logic(plugin):
    if plugin == 'vertiv':
        return VertivLogic()
    elif plugin == 'schneider':
        return SchneiderLogic()
    elif plugin == 'ipmi':
        return IPMILogic()
    elif plugin == 'ganglia':
        return GangliaLogic()
    elif plugin == 'logics':
        return LogicsLogic()
    elif plugin == 'nagios':
        return NagiosLogic()
    elif plugin == 'weather':
        return WeatherLogic()
    elif plugin == 'slurm':
        return SLURMLogic()
    elif plugin == 'job_table':
        return JobTableLogic()
    else:
        raise AttributeError(f'No plugin named {plugin}.')

