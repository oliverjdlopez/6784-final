# Parquet dataset writer

Script to convert from the downloaded dataset (CSV + gzip) to a partitioned Parquet format (2.6), using PyArrow (9.0.0).

Each plugin has a class with the relative configurations.

## Original dataset folder structure
plugin → metric → daily file
```
Comp_2/
├── follow
├── ganglia_pub
├── ipmi_pub
├── job_table
├── log
├── logics_pub
├── nagios_pub
├── schneider_pub
├── slurm_pub
├── verviv_pub
└── weather_pub
```

```
vertiv_pub/
├── Actual_Return_Air_Temperature_Set_Point
├── Actual_Return_Humidity_Set_Point
├── ....
├── Supply_Air_Temperature_Set_Point
└── Underflow_Static_Pressure
```

```
Actual_Return_Air_Temperature_Set_Point/
├── Actual_Return_Air_Temperature_Set_Point_2021-04-08_00-00-00_to_2021-04-09_00-00-00.csv.gz
├── Actual_Return_Air_Temperature_Set_Point_2021-04-09_00-00-00_to_2021-04-10_00-00-00.csv.gz
├── ...
├── Actual_Return_Air_Temperature_Set_Point_2022-09-27_00-00-00_to_2022-09-28_00-00-00.csv.gz
└── Actual_Return_Air_Temperature_Set_Point_2022-09-28_00-00-00_to_2022-09-29_00-00-00.csv.gz
```