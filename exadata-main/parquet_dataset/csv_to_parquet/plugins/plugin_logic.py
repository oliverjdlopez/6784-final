class PluginLogic():
    def __init__(self):

        # path relative to the plugin, original dataset (CSV+gz)
        self.data_path = None

        # selected columns that are read from the og CSVs
        self.sel_columns = None

        # type of the "value" column (output) given the metric's name
        self.value_type_per_metric = {}

        # columns that have to be dictionary encoded (Parquet), by metric
        self.dict_cols_per_metric = {}
 
    def get_schema_in(self, metric_name):
        """
        pyarrow.Schema for reading a metric from the raw CSVs (input dataset);
        "value" column"s type depends on the specific metric.
        """
        pass

    def get_schema_out(self, metric_name):
        """
        pyarrow.Schema for given metric (output dataset);
        "value" column"s type depends on the specific metric.
        """
        pass

    def get_preprocessing_step1(self, schema_out):
        """
        Function that processes all batches, converting from schema_in to schema_out.
        Step 1.
        """
        pass
    
    def get_preprocessing_step2(self, schema_out):
        """
        Function that processes all batches, converting from schema_in to schema_out.
        Step 2.
        """
        pass
    
