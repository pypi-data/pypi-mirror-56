from timeseries_etl.timeseries_etl import TimeSeriesEtl
from pandas import DataFrame, Timedelta


class TestEtlFunctions():
    db_type = 'vertica'
    host = '172.24.76.116'
    port = 5433
    user = 'dbadmin'
    password = 'Telvent2011'
    dbname = 'pems'
    schema = 'public'

    def test_get_measures(self):
        ts_etl = TimeSeriesEtl(self.db_type, self.host, self.port, self.user, self.password, self.dbname, self.schema)
        result = ts_etl.get_measure_ts('measure_point_5min', 23, ['speed', 'volume'],5)
        assert result.shape[0] > 0 and isinstance(result, DataFrame)

    def test_create_lists_of_tsdatainfo(self):
        list_of_tsinfo = TimeSeriesEtl.create_list_of_tsdatainfo('measure_point_5min', [1, 2, 23], ['speed', 'volume'])
        assert len(list_of_tsinfo) == 3

    def test_build_dataset(self):
        ts_etl = TimeSeriesEtl(self.db_type, self.host, self.port, self.user, self.password, self.dbname, self.schema)
        list_of_pred_info = TimeSeriesEtl.create_list_of_tsdatainfo('measure_point_5min', [1, 2, 23], ['speed', 'volume'])
        target_info = TimeSeriesEtl.create_list_of_tsdatainfo('measure_point_5min', [25], ['speed'])
        dataset = ts_etl.build_dataset(list_of_pred_info,[-1,-5],target_info,[4],5)
        min_date = dataset.index.min()
        # make sure that the first value of the first column is the same as the one that was shifted one period + 5 mins
        assert(dataset.loc[min_date]['speed_1'] == dataset.loc[min_date + Timedelta(minutes=5)]['speed_1_-5'])
        # same with a shift of 5 periods
        assert (dataset.loc[min_date]['speed_1'] == dataset.loc[min_date + Timedelta(minutes=25)]['speed_1_-25'])
        # finally with the target measure to predict. Make sure is shifted back from the horizon
        assert (dataset.loc[min_date]['speed_25_20'] == dataset.loc[min_date + Timedelta(minutes=20)]['speed_25'])

