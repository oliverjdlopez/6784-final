# Vertiv
The Vertiv plugin mainly collects data from the air-conditioning units (CDZ) located in room F (Marconi 100) of Cineca.The plugin uses the RESTful API interface available on the individual devices to extract the most interesting metrics.

## Plugin-specific columns

|Column|Description|
|------|-----------|
|device|Name of the device| 

## Metrics
|Metric|Description|Unit|Value type|Sampling period|
|------|-----------|----|----------|---------------|
|Actual_Return_Air_Temperature_Set_Point|Set Point of the air temperature at the device inlet|°C|float|10s (per device)|
|Actual_Return_Humidity_Set_Point|Set Point of the air humidity at the device inlet (when enabled)|%RH|float|10s (per device)|
|Adjusted_Humidity|Value of the adusted humidity|%|float|10s (per device)|
|Compressor_Utilization|Utilization level of the compressor in the cooling circuit|%|float|10s (per device)|
|Dehumidifier_Utilization|Utilization level of the dehumidifier (when enabled)|%|float|10s (per device)|
|Ext_Air_Sensor_A_Humidity|Exit air humidity retrieved by the external sensor A|%RH|float|10s (per device)|
|Ext_Air_Sensor_A_Temperature|Exit air temperature retrieved by the external sensor A|°C|float|10s (per device)|
|Ext_Air_Sensor_B_Humidity|Exit air humidity retrieved by the external sensor B|%RH|float|10s (per device)|
|Ext_Air_Sensor_B_Temperature|Exit air temperature retrieved by the external sensor B|°C|float|10s (per device)|
|Ext_Air_Sensor_C_Humidity|Exit air humidity retrieved by the external sensor C|%RH|float|10s (per device)|
|Ext_Air_Sensor_C_Temperature|Exit air temperature retrieved by the external sensor C|°C|float|10s (per device)|
|Fan_Speed|Cooling fan speed|%|float|10s (per device)|
|Filter_Pressure_Drop|Pressure drop at the inlet filter|Pa|float|10s (per device)|
|Free_Cooling_Fluid_Temperature|Temperature of the fluid in the free-cooling circuit|°C|float|10s (per device)|
|Free_Cooling_Status|Status of the free-cooling system|_|float|10s (per device)|
|Free_Cooling_Valve_Open_Position|Free-cooling three-way valve position |%|float|10s (per device)|
|Hot_Water___Hot_Gas_Valve_Open_Position|Status of the hot water/gas valve|%|float|10s (per device)|
|Humidifier_Utilization|Utilization level of the humidifier (when enabled)|%|float|10s (per device)|
|Humidity_Set_Point|Set Point of the air humidity|%RH|float|10s (per device)|
|Reheat_Utilization|Utilization level of the reheat unit (when enabled)|%|float|10s (per device)|
|Return_Air_Temperature|Temperature of the air at the device inlet|°C|float|10s (per device)|
|Return_Humidity|Humidity of the air at the device inlet|%RH|float|10s (per device)|
|Supply_Air_Temperature|Temperature of the air at the device outlet|°C|float|10s (per device)|
|Supply_Air_Temperature_Set_Point|Set Point of the air temperature at the device outlet|°C|float|10s (per device)|
|Underflow_Static_Pressure|Static pressure at the device outlet (when enabled)|Pa|float|10s (per device)|