# Schneider
The Schneider plugin is a dedicated data collector designed to acquire data from an industrial PLC by accessing its HMI module (from Schneider Electric).The PLC controls the valves and pumps of the liquid cooling circuit (RDHx) of Marconi 100. It consists of two (redundant) twin systems controllable by two identical HMI panels, Q101 and Q102.The examon plugin extracts and stores all the metrics available on both panels.

## Plugin-specific columns

|Column|Description|
|------|-----------|
|panel|Name of the panel|

## Metrics
|Metric|Description|Unit|Value type|Sampling period|
|------|-----------|----|----------|---------------|
|Alm_TY141|Three-way valve TY141 Alarm |pure number|int|20s (per panel)|
|PLC_PLC_Q101.Abilita_inverter|Inverter enabled|pure number|int|20s (per panel)|
|PLC_PLC_Q101.Abilita_valvola1|Valve 1 enabled|pure number|int|20s (per panel)|
|PLC_PLC_Q101.Abilita_valvola2|Valve 2 enabled|pure number|int|20s (per panel)|
|PLC_PLC_Q101.Allarme_on|Alarm on|pure number|int|20s (per panel)|
|PLC_PLC_Q101.Allarme_presente|Alarm enabled||int|20s (per panel)|
|PLC_PLC_Q101.Alm_inverter_p101|Alarm for the inverter of pump p101||int|20s (per panel)|
|PLC_PLC_Q101.Alm_inverter_p102|Alarm for the inverter of pump p102||int|20s (per panel)|
|PLC_PLC_Q101.Alm_inverter_p103|Alarm for the inverter of pump p103||int|20s (per panel)|
|PLC_PLC_Q101.Alm_inverter_p104|Alarm for the inverter of pump p104||int|20s (per panel)|
|PLC_PLC_Q101.Alm_max_portata|Maximum flow rate alarm||int|20s (per panel)|
|PLC_PLC_Q101.Alm_max_t_mandata|Supply flow maximum temperature alarm||int|20s (per panel)|
|PLC_PLC_Q101.Alm_max_t_ritorno|Return flow maximum temperature alarm||int|20s (per panel)|
|PLC_PLC_Q101.Alm_min_portata|Minimum flow rate alarm||int|20s (per panel)|
|PLC_PLC_Q101.Alm_min_t_mandata|Supply flow minimum temperature alarm||int|20s (per panel)|
|PLC_PLC_Q101.Alm_nostart_p101|Alarm of pump  p101 not started||int|20s (per panel)|
|PLC_PLC_Q101.Alm_nostart_p102|Alarm of pump  p102 not started||int|20s (per panel)|
|PLC_PLC_Q101.Alm_nostart_p103|Alarm of pump  p103 not started||int|20s (per panel)|
|PLC_PLC_Q101.Alm_nostart_p104|Alarm of pump  p104 not started||int|20s (per panel)|
|PLC_PLC_Q101.Alm_w1|||int|20s (per panel)|
|PLC_PLC_Q101.Cmd_valvola_1|Valve 1 command||int|20s (per panel)|
|PLC_PLC_Q101.Cmd_valvola_2|Valve 2 command||int|20s (per panel)|
|PLC_PLC_Q101.Delta_temp|Temperature delta |°C (x10)|int|20s (per panel)|
|PLC_PLC_Q101.Diff_minuti_cavedio|Time difference w.r.t. air shaft|minutes|int|20s (per panel)|
|PLC_PLC_Q101.Diff_minuti_quadro|Time difference w.r.t. panel|minutes|int|20s (per panel)|
|PLC_PLC_Q101.Diff_minuti_sala|Time difference w.r.t. room|minutes|int|20s (per panel)|
|PLC_PLC_Q101.In_marcia_p101|Running status of pump p101||int|20s (per panel)|
|PLC_PLC_Q101.In_marcia_p102|Running status of pump p102||int|20s (per panel)|
|PLC_PLC_Q101.In_marcia_p103|Running status of pump p103||int|20s (per panel)|
|PLC_PLC_Q101.In_marcia_p104|Running status of pump p104||int|20s (per panel)|
|PLC_PLC_Q101.Kp_pid_pompe|Proportional gain of the pump's PID||int|20s (per panel)|
|PLC_PLC_Q101.Kp_pid_valvole|Proportional gain of the valve's PID||int|20s (per panel)|
|PLC_PLC_Q101.Manuale_p101|Manual control for pump p101||int|20s (per panel)|
|PLC_PLC_Q101.Manuale_p102|Manual control for pump p102||int|20s (per panel)|
|PLC_PLC_Q101.Manuale_p103|Manual control for pump p103||int|20s (per panel)|
|PLC_PLC_Q101.Manuale_p104|Manual control for pump p104||int|20s (per panel)|
|PLC_PLC_Q101.Manuale_ty141|Manual control for valve ty141||int|20s (per panel)|
|PLC_PLC_Q101.Manuale_ty142|Manual control for valve ty142||int|20s (per panel)|
|PLC_PLC_Q101.Max_ana_out_ty141|Maximum analogical output value for valve ty141||int|20s (per panel)|
|PLC_PLC_Q101.Max_ana_out_ty142|Maximum analogical output value for valve ty142||int|20s (per panel)|
|PLC_PLC_Q101.Max_ana_portata1|Maximum analogical output value for Supply flow 1||int|20s (per panel)|
|PLC_PLC_Q101.Max_ana_portata2|Maximum analogical output value for Supply flow 2||int|20s (per panel)|
|PLC_PLC_Q101.Max_ana_pos_ty141|Maximum analogical position for valve ty141||int|20s (per panel)|
|PLC_PLC_Q101.Max_ana_pos_ty142|Maximum analogical position for valve ty142||int|20s (per panel)|
|PLC_PLC_Q101.Max_portata|Maximum Supply flow rate|m3/h (x10)|int|20s (per panel)|
|PLC_PLC_Q101.Max_t_mandata|Maximum temperature for the Supply flow|°C (x10)|int|20s (per panel)|
|PLC_PLC_Q101.Max_t_ritorno|Maximum temperature for the return flow|°C (x10)|int|20s (per panel)|
|PLC_PLC_Q101.Max_visi_portata2|||int|20s (per panel)|
|PLC_PLC_Q101.Max_visu_portata1|||int|20s (per panel)|
|PLC_PLC_Q101.Min_ana_out_ty141|Minimum analogical output value for valve ty141||int|20s (per panel)|
|PLC_PLC_Q101.Min_ana_out_ty142|Minimum analogical output value for valve ty142||int|20s (per panel)|
|PLC_PLC_Q101.Min_ana_portata1|Minimum analogical output value for Supply flow 1||int|20s (per panel)|
|PLC_PLC_Q101.Min_ana_portata2|Minimum analogical output value for Supply flow 2||int|20s (per panel)|
|PLC_PLC_Q101.Min_ana_pos_ty141|Minimum analogical valve position ty141||int|20s (per panel)|
|PLC_PLC_Q101.Min_ana_pos_ty142|Minimum analogical valve position ty142||int|20s (per panel)|
|PLC_PLC_Q101.Min_lavoro_p101|Working minutes for pump  p101|minutes|int|20s (per panel)|
|PLC_PLC_Q101.Min_lavoro_p102|Working minutes for pump p102|minutes|int|20s (per panel)|
|PLC_PLC_Q101.Min_lavoro_p103|Working minutes for pump p103|minutes|int|20s (per panel)|
|PLC_PLC_Q101.Min_lavoro_p104|Working minutes for pump p104|minutes|int|20s (per panel)|
|PLC_PLC_Q101.Min_lavoro_quadro|Working minutes for panel|minutes|int|20s (per panel)|
|PLC_PLC_Q101.Min_out_pid_pompe|Working minutes for the pump's output PID|minutes|int|20s (per panel)|
|PLC_PLC_Q101.Min_out_pid_valv|Working minutes for the valve's output PID|minutes|int|20s (per panel)|
|PLC_PLC_Q101.Min_parz_p101|Partial minutes for pump p101|minutes|int|20s (per panel)|
|PLC_PLC_Q101.Min_parz_p102|Partial minutes for pump p102|minutes|int|20s (per panel)|
|PLC_PLC_Q101.Min_parz_p103|Partial minutes for pump p103|minutes|int|20s (per panel)|
|PLC_PLC_Q101.Min_parz_p104|Partial minutes for pump p104|minutes|int|20s (per panel)|
|PLC_PLC_Q101.Min_parziali_p101|Partial minutes for pump p101|minutes|int|20s (per panel)|
|PLC_PLC_Q101.Min_parziali_p102|Partial minutes for pump p102|minutes|int|20s (per panel)|
|PLC_PLC_Q101.Min_parziali_p103|Partial minutes for pump p103|minutes|int|20s (per panel)|
|PLC_PLC_Q101.Min_parziali_p104|Partial minutes for pump p104|minutes|int|20s (per panel)|
|PLC_PLC_Q101.Min_parziali_quadro|Partial minutes for panel|minutes|int|20s (per panel)|
|PLC_PLC_Q101.Min_portata|Minimum flow rate|m3/h (x10)|int|20s (per panel)|
|PLC_PLC_Q101.Min_t_mandata|Minimum temperature for the Supply flow|°C (x10)|int|20s (per panel)|
|PLC_PLC_Q101.Min_vel_pompe|Minimum temperature for the return flow|°C (x10)|int|20s (per panel)|
|PLC_PLC_Q101.Min_visu_portata1|||int|20s (per panel)|
|PLC_PLC_Q101.Min_visu_portata2|||int|20s (per panel)|
|PLC_PLC_Q101.Ore_lavoro_p101|Working hours for pump p101|hours|int|20s (per panel)|
|PLC_PLC_Q101.Ore_lavoro_p102|Working hours for pump p102|hours|int|20s (per panel)|
|PLC_PLC_Q101.Ore_lavoro_p103|Working hours for pump p103|hours|int|20s (per panel)|
|PLC_PLC_Q101.Ore_lavoro_p104|Working hours for pump p104|hours|int|20s (per panel)|
|PLC_PLC_Q101.Ore_parziali_p101|Partial hours for pump p101|hours|int|20s (per panel)|
|PLC_PLC_Q101.Ore_parziali_p102|Partial hours for pump p102|hours|int|20s (per panel)|
|PLC_PLC_Q101.Ore_parziali_p103|Partial hours for pump p103|hours|int|20s (per panel)|
|PLC_PLC_Q101.Ore_parziali_p104|Partial hours for pump p104|hours|int|20s (per panel)|
|PLC_PLC_Q101.Out_pid_pompe|Pump's PID output||int|20s (per panel)|
|PLC_PLC_Q101.Out_pid_val|Valve's PID output||int|20s (per panel)|
|PLC_PLC_Q101.P101_fault|Fault status for pump p101||int|20s (per panel)|
|PLC_PLC_Q101.P101_in_marcia|Running status for pump p101||int|20s (per panel)|
|PLC_PLC_Q101.P102_fault|Fault status for pump p102||int|20s (per panel)|
|PLC_PLC_Q101.P102_in_marcia|Running status for pump p102||int|20s (per panel)|
|PLC_PLC_Q101.P103_fault|Fault status for pump p103||int|20s (per panel)|
|PLC_PLC_Q101.P103_in_marcia|Running status for pump p103||int|20s (per panel)|
|PLC_PLC_Q101.P104_fault|Fault status for pump p104||int|20s (per panel)|
|PLC_PLC_Q101.P104_in_marcia|Running status for pump p104||int|20s (per panel)|
|PLC_PLC_Q101.Pb_arresto_p101|||int|20s (per panel)|
|PLC_PLC_Q101.Pb_arresto_p102|||int|20s (per panel)|
|PLC_PLC_Q101.Pb_arresto_p103|||int|20s (per panel)|
|PLC_PLC_Q101.Pb_arresto_p104|||int|20s (per panel)|
|PLC_PLC_Q101.Pb_marcia_p101|||int|20s (per panel)|
|PLC_PLC_Q101.Pb_marcia_p102|||int|20s (per panel)|
|PLC_PLC_Q101.Pb_marcia_p103|||int|20s (per panel)|
|PLC_PLC_Q101.Pb_marcia_p104|||int|20s (per panel)|
|PLC_PLC_Q101.Portata_1|Flow rate sensor 1|m3/h (x50)|int|20s (per panel)|
|PLC_PLC_Q101.Portata_1_hmi|Flow rate (HMI panel) sensor 1|m3/h (x10)|int|20s (per panel)|
|PLC_PLC_Q101.Portata_2|Flow rate sensor 2|m3/h (x50)|int|20s (per panel)|
|PLC_PLC_Q101.Portata_2_hmi|Flow rate (HMI panel) sensor 2|m3/h (x10)|int|20s (per panel)|
|PLC_PLC_Q101.Portata_attiva|Active flow rate |m3/h (x10)|int|20s (per panel)|
|PLC_PLC_Q101.Pos_valvola1|Valve 1 position|% (x100)|int|20s (per panel)|
|PLC_PLC_Q101.Pos_valvola_2|Valve 2 position|% (x100)|int|20s (per panel)|
|PLC_PLC_Q101.Posizione_ty141|Valve ty141 position|% |int|20s (per panel)|
|PLC_PLC_Q101.Posizione_ty142|Valve ty142 position|%|int|20s (per panel)|
|PLC_PLC_Q101.Rif_auto_attivo|Automatic active reference |%|int|20s (per panel)|
|PLC_PLC_Q101.Rif_auto_p101|Automatic reference for pump p101|%|int|20s (per panel)|
|PLC_PLC_Q101.Rif_auto_p102|Automatic reference for pump p102|%|int|20s (per panel)|
|PLC_PLC_Q101.Rif_auto_ty141|Automatic reference for valve ty141|%|int|20s (per panel)|
|PLC_PLC_Q101.Rif_auto_ty142|Automatic reference for valve ty142|%|int|20s (per panel)|
|PLC_PLC_Q101.Rif_inverter|Inverter reference|% (x100)|int|20s (per panel)|
|PLC_PLC_Q101.Rif_man_p101|Manual reference for pump p101|%|int|20s (per panel)|
|PLC_PLC_Q101.Rif_man_p102|Manual reference for pump p102|%|int|20s (per panel)|
|PLC_PLC_Q101.Rif_man_ty141|Manual reference for valve ty141|%|int|20s (per panel)|
|PLC_PLC_Q101.Rif_man_ty142|Manual reference for valve ty142|%|int|20s (per panel)|
|PLC_PLC_Q101.Sel_misuratore|Probe selector||int|20s (per panel)|
|PLC_PLC_Q101.Set_man_pid_pompe|Manual set point for the pump's PID|% (x100)|int|20s (per panel)|
|PLC_PLC_Q101.Set_man_pid_valv|Manual set point for the valve's PID|% (x100)|int|20s (per panel)|
|PLC_PLC_Q101.Set_temperatura|Temperature set point|°C (x10)|int|20s (per panel)|
|PLC_PLC_Q101.Start_impianto|Plant start status||int|20s (per panel)|
|PLC_PLC_Q101.Start_p101|Start status for pump p101||int|20s (per panel)|
|PLC_PLC_Q101.Start_p102|Start status for pump p102||int|20s (per panel)|
|PLC_PLC_Q101.Start_p103|Start status for pump p103||int|20s (per panel)|
|PLC_PLC_Q101.Start_p104|Start status for pump p104||int|20s (per panel)|
|PLC_PLC_Q101.Stato_p101|Status for pump p101||int|20s (per panel)|
|PLC_PLC_Q101.Stato_p102|Status for pump p102||int|20s (per panel)|
|PLC_PLC_Q101.Stato_p103|Status for pump p103||int|20s (per panel)|
|PLC_PLC_Q101.Stato_p104|Status for pump p104||int|20s (per panel)|
|PLC_PLC_Q101.Stato_quadro|Panel status||int|20s (per panel)|
|PLC_PLC_Q101.Status_w1|||int|20s (per panel)|
|PLC_PLC_Q101.Status_w2|||int|20s (per panel)|
|PLC_PLC_Q101.T_mandata_hmi|Supply flow temperature (HMI panel)|°C (x10)|int|20s (per panel)|
|PLC_PLC_Q101.T_ritorno_hmi|Return flow temperature (HMI panel)|°C (x10)|int|20s (per panel)|
|PLC_PLC_Q101.T_scambio_cavedio|Exchange temperature air shaft|°C|int|20s (per panel)|
|PLC_PLC_Q101.T_scambio_quadri|Exchange temperature panels|°C|int|20s (per panel)|
|PLC_PLC_Q101.T_scambio_sala|Exchange temperature room|°C|int|20s (per panel)|
|PLC_PLC_Q101.Td_pid_pompe|Derivative gain of the pump's PID||int|20s (per panel)|
|PLC_PLC_Q101.Td_pid_valvole|Derivative gain of the valve's PID||int|20s (per panel)|
|PLC_PLC_Q101.Temp_mandata|Supply flow temperature|°C (x10)|int|20s (per panel)|
|PLC_PLC_Q101.Temp_ritorno|Return flow temperature |°C (x10)|int|20s (per panel)|
|PLC_PLC_Q101.Ti_pid_pompe|Integral gain of the pump's PID||int|20s (per panel)|
|PLC_PLC_Q101.Ti_pid_valvole|Integral gain of the valve's PID||int|20s (per panel)|
|PLC_PLC_Q101.V_min_rem_cavedio|Remaining minutes air shaft|minutes|int|20s (per panel)|
|PLC_PLC_Q101.V_min_rem_quadro|Remaining minutes panel|minutes|int|20s (per panel)|
|PLC_PLC_Q101.V_min_rem_sala|Remaining minutes room|minutes|int|20s (per panel)|
|PLC_PLC_Q101.V_ore_parz_p101|Partial hours for pump p101|Hours|int|20s (per panel)|
|PLC_PLC_Q101.V_ore_parz_p102|Partial hours for pump p102|Hours|int|20s (per panel)|
|PLC_PLC_Q101.V_ore_parz_p103|Partial hours for pump p103|Hours|int|20s (per panel)|
|PLC_PLC_Q101.V_ore_parz_p104|Partial hours for pump p104|Hours|int|20s (per panel)|
|PLC_PLC_Q101.V_ore_parz_quadro|Partial hours panel|Hours|int|20s (per panel)|
|PLC_PLC_Q101.V_ore_rem_cavedio|Remaining hours air shaft|Hours|int|20s (per panel)|
|PLC_PLC_Q101.V_ore_rem_quadro|Remaining hours panel|Hours|int|20s (per panel)|
|PLC_PLC_Q101.V_ore_rem_sala|Remaining hours room|Hours|int|20s (per panel)|
|PLC_PLC_Q101.V_ore_tot_p101|Total running hours for pump p101|Hours|int|20s (per panel)|
|PLC_PLC_Q101.V_ore_tot_p102|Total running hours for pump p102|Hours|int|20s (per panel)|
|PLC_PLC_Q101.V_ore_tot_p103|Total running hours for pump p103|Hours|int|20s (per panel)|
|PLC_PLC_Q101.V_ore_tot_p104|Total running hours for pump p104|Hours|int|20s (per panel)|
|PLC_PLC_Q101.V_ore_tot_quadro|Total running hours panel|Hours|int|20s (per panel)|