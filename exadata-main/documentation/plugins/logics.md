# Logics
Logics is a data collection system already installed at Cineca. It is specialized for collecting power consumption data from equipment in the different rooms, typically using multimeters that communicate via Modbus protocol. The ExaMon plugin dedicated to collecting this data interfaces to the Logics database (RDBMS) via its REST API.

NOTE: Since the translation process is fully automated, the same inconsistencies present in the original db may result in the ExaMon database: e.g., metric names in the Italian language, units of measure as metric name, etc.

## Plugin-specific columns

|Column|Description|
|------|-----------|
|panel|The name of the electrical panel within the computer rooms|
|device|The name of the device, connected to the panel, of which the multimeter measures the parameters|

## Metrics

|Metric|Description|Unit|Value type|
|------|-----------|----|----------|
|Bad_values|Status flag indicating that the metric reported for the specified panel/device could be unreliable|_|int|
|Comlost|Status flag indicating issue in the sensor communication link|_|float|
|Corrente|Current|A|float|
|Corrente_L1|Three-phase current Line 1|A|float|
|Corrente_L2|Three-phase current Line 2|A|float|
|Corrente_L3|Three-phase current Line 3|A|float|
|Dcie|Data Center Infrastructure Efficiency|_|float|
|Energia|Energy|kWh|float|
|Fattore_di_potenza|Power Factor|COS|float|
|Frequenza|AC Frequency|Hz|float|
|Gateway|Modbus gateway|_|string|
|ID_Modbus|Modbus device id|_|int|
|Mvar|Reactive Power|MVAR|float|
|Mvarh|Reactive Energy|MVARh|float|
|Mw|Power|MW|float|
|Mwh|Energy|MWh|float|
|Potenza|Power|kW|float|
|Potenza_attiva|Power|kW|float|
|Prototype|Sensor Type|_|string|
|Pue|Power Usage Effectiveness|_|float|
|Stato|Global status of the data center|_|int|
|Status|Global status flag for the specified panel/device metric|_|int|
|Tensione|Voltage|V|int|
|Tot|Total Power consumed by the data center|kW|float|
|Tot_cdz|Total Power consumed by the CRACs units|kW|float|
|Tot_chiller|Total Power consumed by the Chillers|kW|float|
|Tot_ict|Total Power consumed by the IT devices|kW|float|
|Tot_qpompe|Total Power consumed by the liquid cooling devices|kW|float|
|Tot_servizi|Total Power consumed by the auxiliary services|kW|float|
|Volt1|Three-phase voltage Line 1|V|int|
|Volt2|Three-phase voltage Line 2|V|float|
|Volt3|Three-phase voltage Line 3|V|int|
|address|Modbus ip address|_|string|
|deviceid|Modbus device id|_|int|
|pit|Total Power consumed by the IT devices|W|int|
|pt|Total Power consumed by the data center|W|int|
|pue|Power Usage Effectiveness|_|float|