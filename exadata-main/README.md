# M100 ExaData

Reference repository for the M100 ExaData project.

## Datasets
<center>

|Name|Included months|Total size (GB)|Link (DOI)|
|----|---------------|---------------|----------|
Dataset 1|from 20-03 to 20-12 (included)|44.6|[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7588815.svg)](https://doi.org/10.5281/zenodo.7588815)
Dataset 2|from 21-01 to 21-06 (included)|45.3|[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7589131.svg)](https://doi.org/10.5281/zenodo.7589131)
Dataset 3|from 21-07 to 21-09 (included)|41.7|[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7589320.svg)](https://doi.org/10.5281/zenodo.7589320)
Dataset 4|from 21-10 to 21-12 (included)|44.9|[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7589630.svg)](https://doi.org/10.5281/zenodo.7589630)
Dataset 5|from 22-01 to 22-02 (included)|24|[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7589942.svg)](https://doi.org/10.5281/zenodo.7589942)
Dataset 6|22-03|31.5|[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7590061.svg)](https://doi.org/10.5281/zenodo.7590061)
Dataset 7|22-04|33.4|[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7590308.svg)](https://doi.org/10.5281/zenodo.7590308)
Dataset 8|22-05|33.2|[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7590547.svg)](https://doi.org/10.5281/zenodo.7590547)
Dataset 9|22-06|27.7|[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7590555.svg)](https://doi.org/10.5281/zenodo.7590555)
Dataset 10|22-07|31.4|[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7590565.svg)](https://doi.org/10.5281/zenodo.7590565)
Dataset 11|22-08|37.9|[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7590574.svg)](https://doi.org/10.5281/zenodo.7590574)
Dataset 12|22-09|34.1|[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7590583.svg)](https://doi.org/10.5281/zenodo.7590583)
Time-aggregated (anomaly detection)| from 20-03 to 22-09 (included)|24.8|[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7541722.svg)](https://doi.org/10.5281/zenodo.7541722)|

</center>

The total size is relative to the whole datasets, data can be downloaded with finer granularity (i.e. months, racks) for some of them.


## Repository structure

- `documentation`: descriptions of the plugins (ExaMon), including related metadata (metrics, tags); spatial distribution of racks.
- `examples`: applications of the dataset described in the "technical validation" part of the paper.
- `parquet_dataset/csv_to_parquet`: scripts used to produce the final Parquet dataset, starting from the extracted CSVs (ExaMon).
- `parquet_dataset/query_tool`: simple tool to load a slice of the dataset into a Pandas DataFrame.
- `parquet_dataset/node_aggregated_data`: scripts to create the anomaly detection dataset.
- `data_extraction`: scripts used to extract the data from ExaMon (in CSV format).
- `data_catalog`: data catalog.

## References

Main technologies:
- Parquet (2.6): https://parquet.apache.org/
- PyArrow (9.0.0): https://arrow.apache.org/
- Pandas (1.5.1): https://pandas.pydata.org/
