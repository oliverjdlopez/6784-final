import pyarrow as pa
import pyarrow.compute as pc
from plugins.plugin_logic import PluginLogic

class SchneiderLogic(PluginLogic):
    def __init__(self):
        super().__init__()

        self.data_path = '/nas/cinecadataset/Comp_2/schneider_pub'

        self.sel_cols = ['plugin', 'name', 'timestamp', 'value', 'panel']

        self.value_type_per_metric = {'PLC_PLC_Q101.Min_vel_pompe': pa.int32(),
                                      'PLC_PLC_Q101.Rif_auto_p101': pa.int32(),
                                      'PLC_PLC_Q101.Alm_nostart_p102': pa.int32(),
                                      'PLC_PLC_Q101.Temp_ritorno': pa.int32(),
                                      'PLC_PLC_Q101.V_ore_tot_p102': pa.int32(),
                                      'PLC_PLC_Q101.Alm_inverter_p102': pa.int32(),
                                      'PLC_PLC_Q101.T_scambio_quadri': pa.int32(),
                                      'PLC_PLC_Q101.Manuale_p102': pa.int32(),
                                      'PLC_PLC_Q101.Rif_auto_ty142': pa.int32(),
                                      'PLC_PLC_Q101.Manuale_ty141': pa.int32(),
                                      'PLC_PLC_Q101.In_marcia_p104': pa.int32(),
                                      'PLC_PLC_Q101.Sel_misuratore': pa.int32(),
                                      'PLC_PLC_Q101.Max_ana_pos_ty141': pa.int32(),
                                      'PLC_PLC_Q101.Alm_nostart_p103': pa.int32(),
                                      'PLC_PLC_Q101.Posizione_ty142': pa.int32(),
                                      'PLC_PLC_Q101.Min_ana_out_ty142': pa.int32(),
                                      'PLC_PLC_Q101.P102_in_marcia': pa.int32(),
                                      'PLC_PLC_Q101.Diff_minuti_quadro': pa.int32(),
                                      'PLC_PLC_Q101.In_marcia_p102': pa.int32(),
                                      'PLC_PLC_Q101.Kp_pid_pompe': pa.int32(),
                                      'PLC_PLC_Q101.V_min_rem_quadro': pa.int32(),
                                      'PLC_PLC_Q101.Ore_lavoro_p102': pa.int32(),
                                      'PLC_PLC_Q101.Pb_arresto_p102': pa.int32(),
                                      'PLC_PLC_Q101.Min_ana_portata2': pa.int32(),
                                      'PLC_PLC_Q101.Temp_mandata': pa.int32(),
                                      'PLC_PLC_Q101.Pb_marcia_p103': pa.int32(),
                                      'PLC_PLC_Q101.Start_p102': pa.int32(),
                                      'PLC_PLC_Q101.Td_pid_pompe': pa.int32(),
                                      'PLC_PLC_Q101.Min_parziali_p103': pa.int32(),
                                      'PLC_PLC_Q101.V_ore_rem_cavedio': pa.int32(),
                                      'PLC_PLC_Q101.Min_lavoro_p103': pa.int32(),
                                      'PLC_PLC_Q101.Pos_valvola_2': pa.int32(),
                                      'PLC_PLC_Q101.Alm_inverter_p101': pa.int32(),
                                      'Alm_TY141': pa.int32(),
                                      'PLC_PLC_Q101.Min_visu_portata2': pa.int32(),
                                      'PLC_PLC_Q101.P101_fault': pa.int32(),
                                      'PLC_PLC_Q101.Set_man_pid_pompe': pa.int32(),
                                      'PLC_PLC_Q101.Start_p103': pa.int32(),
                                      'PLC_PLC_Q101.V_ore_parz_p102': pa.int32(),
                                      'PLC_PLC_Q101.Manuale_p103': pa.int32(),
                                      'PLC_PLC_Q101.V_ore_parz_p101': pa.int32(),
                                      'PLC_PLC_Q101.Stato_p104': pa.int32(),
                                      'PLC_PLC_Q101.Max_ana_out_ty142': pa.int32(),
                                      'PLC_PLC_Q101.Abilita_inverter': pa.int32(),
                                      'PLC_PLC_Q101.Start_p101': pa.int32(),
                                      'PLC_PLC_Q101.Start_impianto': pa.int32(),
                                      'PLC_PLC_Q101.Rif_auto_p102': pa.int32(),
                                      'PLC_PLC_Q101.P103_fault': pa.int32(),
                                      'PLC_PLC_Q101.Start_p104': pa.int32(),
                                      'PLC_PLC_Q101.Ore_lavoro_p103': pa.int32(),
                                      'PLC_PLC_Q101.Min_lavoro_p102': pa.int32(),
                                      'PLC_PLC_Q101.Td_pid_valvole': pa.int32(),
                                      'PLC_PLC_Q101.Out_pid_val': pa.int32(),
                                      'PLC_PLC_Q101.Portata_1_hmi': pa.int32(),
                                      'PLC_PLC_Q101.Alm_nostart_p101': pa.int32(),
                                      'PLC_PLC_Q101.Alm_max_t_ritorno': pa.int32(),
                                      'PLC_PLC_Q101.Diff_minuti_cavedio': pa.int32(),
                                      'PLC_PLC_Q101.Min_out_pid_valv': pa.int32(),
                                      'PLC_PLC_Q101.Rif_man_p101': pa.int32(),
                                      'PLC_PLC_Q101.V_min_rem_cavedio': pa.int32(),
                                      'PLC_PLC_Q101.V_min_rem_sala': pa.int32(),
                                      'PLC_PLC_Q101.Manuale_ty142': pa.int32(),
                                      'PLC_PLC_Q101.Alm_nostart_p104': pa.int32(),
                                      'PLC_PLC_Q101.Rif_man_ty142': pa.int32(),
                                      'PLC_PLC_Q101.Ti_pid_pompe': pa.int32(),
                                      'PLC_PLC_Q101.Min_t_mandata': pa.int32(),
                                      'PLC_PLC_Q101.Min_parz_p104': pa.int32(),
                                      'PLC_PLC_Q101.Status_w2': pa.int32(),
                                      'PLC_PLC_Q101.Ti_pid_valvole': pa.int32(),
                                      'PLC_PLC_Q101.Ore_lavoro_p104': pa.int32(),
                                      'PLC_PLC_Q101.Kp_pid_valvole': pa.int32(),
                                      'PLC_PLC_Q101.Min_visu_portata1': pa.int32(),
                                      'PLC_PLC_Q101.Alm_max_portata': pa.int32(),
                                      'PLC_PLC_Q101.Max_ana_portata2': pa.int32(),
                                      'PLC_PLC_Q101.Portata_1': pa.int32(),
                                      'PLC_PLC_Q101.Min_parz_p102': pa.int32(),
                                      'PLC_PLC_Q101.Pb_arresto_p101': pa.int32(),
                                      'PLC_PLC_Q101.Min_ana_portata1': pa.int32(),
                                      'PLC_PLC_Q101.Ore_parziali_p101': pa.int32(),
                                      'PLC_PLC_Q101.Min_ana_pos_ty141': pa.int32(),
                                      'PLC_PLC_Q101.In_marcia_p101': pa.int32(),
                                      'PLC_PLC_Q101.Allarme_on': pa.int32(),
                                      'PLC_PLC_Q101.Stato_p103': pa.int32(),
                                      'PLC_PLC_Q101.Portata_2_hmi': pa.int32(),
                                      'PLC_PLC_Q101.Set_man_pid_valv': pa.int32(),
                                      'PLC_PLC_Q101.Min_parziali_quadro': pa.int32(),
                                      'PLC_PLC_Q101.Alm_inverter_p104': pa.int32(),
                                      'PLC_PLC_Q101.Stato_p102': pa.int32(),
                                      'PLC_PLC_Q101.Allarme_presente': pa.int32(),
                                      'PLC_PLC_Q101.Max_t_mandata': pa.int32(),
                                      'PLC_PLC_Q101.T_ritorno_hmi': pa.int32(),
                                      'PLC_PLC_Q101.Min_ana_out_ty141': pa.int32(),
                                      'PLC_PLC_Q101.Min_lavoro_quadro': pa.int32(),
                                      'PLC_PLC_Q101.Portata_attiva': pa.int32(),
                                      'PLC_PLC_Q101.Cmd_valvola_1': pa.int32(),
                                      'PLC_PLC_Q101.Max_ana_out_ty141': pa.int32(),
                                      'PLC_PLC_Q101.V_ore_tot_p103': pa.int32(),
                                      'PLC_PLC_Q101.Rif_auto_attivo': pa.int32(),
                                      'PLC_PLC_Q101.Pb_marcia_p102': pa.int32(),
                                      'PLC_PLC_Q101.Max_portata': pa.int32(),
                                      'PLC_PLC_Q101.Ore_lavoro_p101': pa.int32(),
                                      'PLC_PLC_Q101.Min_parziali_p104': pa.int32(),
                                      'PLC_PLC_Q101.Manuale_p101': pa.int32(),
                                      'PLC_PLC_Q101.Delta_temp': pa.int32(),
                                      'PLC_PLC_Q101.Min_out_pid_pompe': pa.int32(),
                                      'PLC_PLC_Q101.Alm_max_t_mandata': pa.int32(),
                                      'PLC_PLC_Q101.P104_in_marcia': pa.int32(),
                                      'PLC_PLC_Q101.Pos_valvola1': pa.int32(),
                                      'PLC_PLC_Q101.Min_parziali_p101': pa.int32(),
                                      'PLC_PLC_Q101.Pb_marcia_p104': pa.int32(),
                                      'PLC_PLC_Q101.Manuale_p104': pa.int32(),
                                      'PLC_PLC_Q101.T_scambio_sala': pa.int32(),
                                      'PLC_PLC_Q101.Max_ana_pos_ty142': pa.int32(),
                                      'PLC_PLC_Q101.P104_fault': pa.int32(),
                                      'PLC_PLC_Q101.P101_in_marcia': pa.int32(),
                                      'PLC_PLC_Q101.P102_fault': pa.int32(),
                                      'PLC_PLC_Q101.Min_parz_p103': pa.int32(),
                                      'PLC_PLC_Q101.In_marcia_p103': pa.int32(),
                                      'PLC_PLC_Q101.Max_ana_portata1': pa.int32(),
                                      'PLC_PLC_Q101.Abilita_valvola2': pa.int32(),
                                      'PLC_PLC_Q101.Posizione_ty141': pa.int32(),
                                      'PLC_PLC_Q101.Ore_parziali_p103': pa.int32(),
                                      'PLC_PLC_Q101.Min_parziali_p102': pa.int32(),
                                      'PLC_PLC_Q101.Min_portata': pa.int32(),
                                      'PLC_PLC_Q101.Pb_arresto_p103': pa.int32(),
                                      'PLC_PLC_Q101.V_ore_tot_p104': pa.int32(),
                                      'PLC_PLC_Q101.Diff_minuti_sala': pa.int32(),
                                      'PLC_PLC_Q101.Pb_marcia_p101': pa.int32(),
                                      'PLC_PLC_Q101.T_mandata_hmi': pa.int32(),
                                      'PLC_PLC_Q101.V_ore_parz_p103': pa.int32(),
                                      'PLC_PLC_Q101.Pb_arresto_p104': pa.int32(),
                                      'PLC_PLC_Q101.Min_lavoro_p104': pa.int32(),
                                      'PLC_PLC_Q101.V_ore_tot_p101': pa.int32(),
                                      'PLC_PLC_Q101.Status_w1': pa.int32(),
                                      'PLC_PLC_Q101.Stato_p101': pa.int32(),
                                      'PLC_PLC_Q101.Alm_w1': pa.int32(),
                                      'PLC_PLC_Q101.Ore_parziali_p102': pa.int32(),
                                      'PLC_PLC_Q101.Min_parz_p101': pa.int32(),
                                      'PLC_PLC_Q101.Ore_parziali_p104': pa.int32(),
                                      'PLC_PLC_Q101.Rif_man_ty141': pa.int32(),
                                      'PLC_PLC_Q101.Rif_auto_ty141': pa.int32(),
                                      'PLC_PLC_Q101.V_ore_tot_quadro': pa.int32(),
                                      'PLC_PLC_Q101.Rif_inverter': pa.int32(),
                                      'PLC_PLC_Q101.T_scambio_cavedio': pa.int32(),
                                      'PLC_PLC_Q101.Max_visi_portata2': pa.int32(),
                                      'PLC_PLC_Q101.Stato_quadro': pa.int32(),
                                      'PLC_PLC_Q101.Portata_2': pa.int32(),
                                      'PLC_PLC_Q101.V_ore_parz_p104': pa.int32(),
                                      'PLC_PLC_Q101.P103_in_marcia': pa.int32(),
                                      'PLC_PLC_Q101.Alm_min_t_mandata': pa.int32(),
                                      'PLC_PLC_Q101.Min_lavoro_p101': pa.int32(),
                                      'PLC_PLC_Q101.V_ore_rem_quadro': pa.int32(),
                                      'PLC_PLC_Q101.Set_temperatura': pa.int32(),
                                      'PLC_PLC_Q101.Alm_inverter_p103': pa.int32(),
                                      'PLC_PLC_Q101.Rif_man_p102': pa.int32(),
                                      'PLC_PLC_Q101.Max_t_ritorno': pa.int32(),
                                      'PLC_PLC_Q101.V_ore_parz_quadro': pa.int32(),
                                      'PLC_PLC_Q101.Cmd_valvola_2': pa.int32(),
                                      'PLC_PLC_Q101.Out_pid_pompe': pa.int32(),
                                      'PLC_PLC_Q101.Alm_min_portata': pa.int32(),
                                      'PLC_PLC_Q101.Min_ana_pos_ty142': pa.int32(),
                                      'PLC_PLC_Q101.V_ore_rem_sala': pa.int32(),
                                      'PLC_PLC_Q101.Max_visu_portata1': pa.int32(),
                                      'PLC_PLC_Q101.Abilita_valvola1': pa.int32()}

        self.dict_cols_per_metric = {'PLC_PLC_Q101.Min_vel_pompe': ['panel'],
                                     'PLC_PLC_Q101.Rif_auto_p101': ['panel'],
                                     'PLC_PLC_Q101.Alm_nostart_p102': ['panel'],
                                     'PLC_PLC_Q101.Temp_ritorno': ['panel'],
                                     'PLC_PLC_Q101.V_ore_tot_p102': ['panel'],
                                     'PLC_PLC_Q101.Alm_inverter_p102': ['panel'],
                                     'PLC_PLC_Q101.T_scambio_quadri': ['panel'],
                                     'PLC_PLC_Q101.Manuale_p102': ['panel'],
                                     'PLC_PLC_Q101.Rif_auto_ty142': ['panel'],
                                     'PLC_PLC_Q101.Manuale_ty141': ['panel'],
                                     'PLC_PLC_Q101.In_marcia_p104': ['panel'],
                                     'PLC_PLC_Q101.Sel_misuratore': ['panel'],
                                     'PLC_PLC_Q101.Max_ana_pos_ty141': ['panel'],
                                     'PLC_PLC_Q101.Alm_nostart_p103': ['panel'],
                                     'PLC_PLC_Q101.Posizione_ty142': ['panel'],
                                     'PLC_PLC_Q101.Min_ana_out_ty142': ['panel'],
                                     'PLC_PLC_Q101.P102_in_marcia': ['panel'],
                                     'PLC_PLC_Q101.Diff_minuti_quadro': ['panel'],
                                     'PLC_PLC_Q101.In_marcia_p102': ['panel'],
                                     'PLC_PLC_Q101.Kp_pid_pompe': ['panel'],
                                     'PLC_PLC_Q101.V_min_rem_quadro': ['panel'],
                                     'PLC_PLC_Q101.Ore_lavoro_p102': ['panel'],
                                     'PLC_PLC_Q101.Pb_arresto_p102': ['panel'],
                                     'PLC_PLC_Q101.Min_ana_portata2': ['panel'],
                                     'PLC_PLC_Q101.Temp_mandata': ['panel'],
                                     'PLC_PLC_Q101.Pb_marcia_p103': ['panel'],
                                     'PLC_PLC_Q101.Start_p102': ['panel'],
                                     'PLC_PLC_Q101.Td_pid_pompe': ['panel'],
                                     'PLC_PLC_Q101.Min_parziali_p103': ['panel'],
                                     'PLC_PLC_Q101.V_ore_rem_cavedio': ['panel'],
                                     'PLC_PLC_Q101.Min_lavoro_p103': ['panel'],
                                     'PLC_PLC_Q101.Pos_valvola_2': ['panel'],
                                     'PLC_PLC_Q101.Alm_inverter_p101': ['panel'],
                                     'Alm_TY141': ['panel'],
                                     'PLC_PLC_Q101.Min_visu_portata2': ['panel'],
                                     'PLC_PLC_Q101.P101_fault': ['panel'],
                                     'PLC_PLC_Q101.Set_man_pid_pompe': ['panel'],
                                     'PLC_PLC_Q101.Start_p103': ['panel'],
                                     'PLC_PLC_Q101.V_ore_parz_p102': ['panel'],
                                     'PLC_PLC_Q101.Manuale_p103': ['panel'],
                                     'PLC_PLC_Q101.V_ore_parz_p101': ['panel'],
                                     'PLC_PLC_Q101.Stato_p104': ['panel'],
                                     'PLC_PLC_Q101.Max_ana_out_ty142': ['panel'],
                                     'PLC_PLC_Q101.Abilita_inverter': ['panel'],
                                     'PLC_PLC_Q101.Start_p101': ['panel'],
                                     'PLC_PLC_Q101.Start_impianto': ['panel'],
                                     'PLC_PLC_Q101.Rif_auto_p102': ['panel'],
                                     'PLC_PLC_Q101.P103_fault': ['panel'],
                                     'PLC_PLC_Q101.Start_p104': ['panel'],
                                     'PLC_PLC_Q101.Ore_lavoro_p103': ['panel'],
                                     'PLC_PLC_Q101.Min_lavoro_p102': ['panel'],
                                     'PLC_PLC_Q101.Td_pid_valvole': ['panel'],
                                     'PLC_PLC_Q101.Out_pid_val': ['panel'],
                                     'PLC_PLC_Q101.Portata_1_hmi': ['panel'],
                                     'PLC_PLC_Q101.Alm_nostart_p101': ['panel'],
                                     'PLC_PLC_Q101.Alm_max_t_ritorno': ['panel'],
                                     'PLC_PLC_Q101.Diff_minuti_cavedio': ['panel'],
                                     'PLC_PLC_Q101.Min_out_pid_valv': ['panel'],
                                     'PLC_PLC_Q101.Rif_man_p101': ['panel'],
                                     'PLC_PLC_Q101.V_min_rem_cavedio': ['panel'],
                                     'PLC_PLC_Q101.V_min_rem_sala': ['panel'],
                                     'PLC_PLC_Q101.Manuale_ty142': ['panel'],
                                     'PLC_PLC_Q101.Alm_nostart_p104': ['panel'],
                                     'PLC_PLC_Q101.Rif_man_ty142': ['panel'],
                                     'PLC_PLC_Q101.Ti_pid_pompe': ['panel'],
                                     'PLC_PLC_Q101.Min_t_mandata': ['panel'],
                                     'PLC_PLC_Q101.Min_parz_p104': ['panel'],
                                     'PLC_PLC_Q101.Status_w2': ['panel'],
                                     'PLC_PLC_Q101.Ti_pid_valvole': ['panel'],
                                     'PLC_PLC_Q101.Ore_lavoro_p104': ['panel'],
                                     'PLC_PLC_Q101.Kp_pid_valvole': ['panel'],
                                     'PLC_PLC_Q101.Min_visu_portata1': ['panel'],
                                     'PLC_PLC_Q101.Alm_max_portata': ['panel'],
                                     'PLC_PLC_Q101.Max_ana_portata2': ['panel'],
                                     'PLC_PLC_Q101.Portata_1': ['panel'],
                                     'PLC_PLC_Q101.Min_parz_p102': ['panel'],
                                     'PLC_PLC_Q101.Pb_arresto_p101': ['panel'],
                                     'PLC_PLC_Q101.Min_ana_portata1': ['panel'],
                                     'PLC_PLC_Q101.Ore_parziali_p101': ['panel'],
                                     'PLC_PLC_Q101.Min_ana_pos_ty141': ['panel'],
                                     'PLC_PLC_Q101.In_marcia_p101': ['panel'],
                                     'PLC_PLC_Q101.Allarme_on': ['panel'],
                                     'PLC_PLC_Q101.Stato_p103': ['panel'],
                                     'PLC_PLC_Q101.Portata_2_hmi': ['panel'],
                                     'PLC_PLC_Q101.Set_man_pid_valv': ['panel'],
                                     'PLC_PLC_Q101.Min_parziali_quadro': ['panel'],
                                     'PLC_PLC_Q101.Alm_inverter_p104': ['panel'],
                                     'PLC_PLC_Q101.Stato_p102': ['panel'],
                                     'PLC_PLC_Q101.Allarme_presente': ['panel'],
                                     'PLC_PLC_Q101.Max_t_mandata': ['panel'],
                                     'PLC_PLC_Q101.T_ritorno_hmi': ['panel'],
                                     'PLC_PLC_Q101.Min_ana_out_ty141': ['panel'],
                                     'PLC_PLC_Q101.Min_lavoro_quadro': ['panel'],
                                     'PLC_PLC_Q101.Portata_attiva': ['panel'],
                                     'PLC_PLC_Q101.Cmd_valvola_1': ['panel'],
                                     'PLC_PLC_Q101.Max_ana_out_ty141': ['panel'],
                                     'PLC_PLC_Q101.V_ore_tot_p103': ['panel'],
                                     'PLC_PLC_Q101.Rif_auto_attivo': ['panel'],
                                     'PLC_PLC_Q101.Pb_marcia_p102': ['panel'],
                                     'PLC_PLC_Q101.Max_portata': ['panel'],
                                     'PLC_PLC_Q101.Ore_lavoro_p101': ['panel'],
                                     'PLC_PLC_Q101.Min_parziali_p104': ['panel'],
                                     'PLC_PLC_Q101.Manuale_p101': ['panel'],
                                     'PLC_PLC_Q101.Delta_temp': ['panel'],
                                     'PLC_PLC_Q101.Min_out_pid_pompe': ['panel'],
                                     'PLC_PLC_Q101.Alm_max_t_mandata': ['panel'],
                                     'PLC_PLC_Q101.P104_in_marcia': ['panel'],
                                     'PLC_PLC_Q101.Pos_valvola1': ['panel'],
                                     'PLC_PLC_Q101.Min_parziali_p101': ['panel'],
                                     'PLC_PLC_Q101.Pb_marcia_p104': ['panel'],
                                     'PLC_PLC_Q101.Manuale_p104': ['panel'],
                                     'PLC_PLC_Q101.T_scambio_sala': ['panel'],
                                     'PLC_PLC_Q101.Max_ana_pos_ty142': ['panel'],
                                     'PLC_PLC_Q101.P104_fault': ['panel'],
                                     'PLC_PLC_Q101.P101_in_marcia': ['panel'],
                                     'PLC_PLC_Q101.P102_fault': ['panel'],
                                     'PLC_PLC_Q101.Min_parz_p103': ['panel'],
                                     'PLC_PLC_Q101.In_marcia_p103': ['panel'],
                                     'PLC_PLC_Q101.Max_ana_portata1': ['panel'],
                                     'PLC_PLC_Q101.Abilita_valvola2': ['panel'],
                                     'PLC_PLC_Q101.Posizione_ty141': ['panel'],
                                     'PLC_PLC_Q101.Ore_parziali_p103': ['panel'],
                                     'PLC_PLC_Q101.Min_parziali_p102': ['panel'],
                                     'PLC_PLC_Q101.Min_portata': ['panel'],
                                     'PLC_PLC_Q101.Pb_arresto_p103': ['panel'],
                                     'PLC_PLC_Q101.V_ore_tot_p104': ['panel'],
                                     'PLC_PLC_Q101.Diff_minuti_sala': ['panel'],
                                     'PLC_PLC_Q101.Pb_marcia_p101': ['panel'],
                                     'PLC_PLC_Q101.T_mandata_hmi': ['panel'],
                                     'PLC_PLC_Q101.V_ore_parz_p103': ['panel'],
                                     'PLC_PLC_Q101.Pb_arresto_p104': ['panel'],
                                     'PLC_PLC_Q101.Min_lavoro_p104': ['panel'],
                                     'PLC_PLC_Q101.V_ore_tot_p101': ['panel'],
                                     'PLC_PLC_Q101.Status_w1': ['panel'],
                                     'PLC_PLC_Q101.Stato_p101': ['panel'],
                                     'PLC_PLC_Q101.Alm_w1': ['panel'],
                                     'PLC_PLC_Q101.Ore_parziali_p102': ['panel'],
                                     'PLC_PLC_Q101.Min_parz_p101': ['panel'],
                                     'PLC_PLC_Q101.Ore_parziali_p104': ['panel'],
                                     'PLC_PLC_Q101.Rif_man_ty141': ['panel'],
                                     'PLC_PLC_Q101.Rif_auto_ty141': ['panel'],
                                     'PLC_PLC_Q101.V_ore_tot_quadro': ['panel'],
                                     'PLC_PLC_Q101.Rif_inverter': ['panel'],
                                     'PLC_PLC_Q101.T_scambio_cavedio': ['panel'],
                                     'PLC_PLC_Q101.Max_visi_portata2': ['panel'],
                                     'PLC_PLC_Q101.Stato_quadro': ['panel'],
                                     'PLC_PLC_Q101.Portata_2': ['panel'],
                                     'PLC_PLC_Q101.V_ore_parz_p104': ['panel'],
                                     'PLC_PLC_Q101.P103_in_marcia': ['panel'],
                                     'PLC_PLC_Q101.Alm_min_t_mandata': ['panel'],
                                     'PLC_PLC_Q101.Min_lavoro_p101': ['panel'],
                                     'PLC_PLC_Q101.V_ore_rem_quadro': ['panel'],
                                     'PLC_PLC_Q101.Set_temperatura': ['panel'],
                                     'PLC_PLC_Q101.Alm_inverter_p103': ['panel'],
                                     'PLC_PLC_Q101.Rif_man_p102': ['panel'],
                                     'PLC_PLC_Q101.Max_t_ritorno': ['panel'],
                                     'PLC_PLC_Q101.V_ore_parz_quadro': ['panel'],
                                     'PLC_PLC_Q101.Cmd_valvola_2': ['panel'],
                                     'PLC_PLC_Q101.Out_pid_pompe': ['panel'],
                                     'PLC_PLC_Q101.Alm_min_portata': ['panel'],
                                     'PLC_PLC_Q101.Min_ana_pos_ty142': ['panel'],
                                     'PLC_PLC_Q101.V_ore_rem_sala': ['panel'],
                                     'PLC_PLC_Q101.Max_visu_portata1': ['panel'],
                                     'PLC_PLC_Q101.Abilita_valvola1': ['panel']}

    def get_schema_in(self, metric):
        schema_in = pa.schema([('', pa.int64()),
                               ('asset', pa.string()),
                               ('chnl', pa.string()),
                               ('facility', pa.string()),
                               ('name', pa.string()),
                               ('org', pa.string()),
                               ('panel', pa.string()),
                               ('plugin', pa.string()),
                               ('timestamp', pa.timestamp('s', tz='UTC')),
                               ('value', self.value_type_per_metric[metric])])
                               #('value', pa.string())])
        return schema_in

    def get_schema_out(self, metric):
        schema_out = pa.schema([("plugin", pa.string()),
                                ("metric", pa.string()),
                                ("year_month", pa.string()),
                                ("timestamp", pa.timestamp('s', tz='UTC')),
                                ('value', self.value_type_per_metric[metric]),
                                ("panel", pa.string())])
                                #("value", pa.float32()), 
                                #("month", pa.uint8()),
                                #("year", pa.uint16()),
        return schema_out

    def get_preprocessing_step1(self):
        def preprocessing(batches, schema_out):
            for batch in batches:

                metric = batch['name']

                # extracting month and year
                year_month = pc.strftime(batch['timestamp'], '%y-%m')
                
                # creating new batch from single arrays
                arrays = [batch['plugin'], metric, year_month, batch['timestamp'], batch['value'], batch['panel']]
                batch = pa.RecordBatch.from_arrays(arrays, schema=schema_out)
            
                yield batch

        return preprocessing

    def get_preprocessing_step2(self):
        """Parquet to Parquet."""
        def preprocessing(batches, metric_name, schema_out):
            for batch in batches:

                
                batch_size = len(batch)
                metric = pa.array([metric_name]*batch_size, type=pa.string())
                plugin = pa.array(['schneider_pub']*batch_size)

                # extracting month and year
                year_month = pc.strftime(batch['timestamp'], '%y-%m')
                
                # creating new batch from single arrays
                arrays = [plugin, metric, year_month, batch['timestamp'], batch['value'], batch['panel']]
                batch = pa.RecordBatch.from_arrays(arrays, schema=schema_out)
            
                yield batch

        return preprocessing
    
