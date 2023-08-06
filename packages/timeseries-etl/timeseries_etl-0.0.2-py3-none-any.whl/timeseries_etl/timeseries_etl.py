# This is a module designed to extract TimeSeries as pandas Dataframes from a Database.
# It also allows to build datasets for statistics or machine learning purposes
# The main goal of the module is to extract all the data without any filtering or manipulation except from the one
# needed to build datasets


import vertica_python
import pandas as pd
from typing import List, NamedTuple


# A case class that is going to represent the information needed to go to the database and retrieve a multivariate
# timeseries"
class TSDataDef(NamedTuple):
    table: str
    item_id: int
    # We decided to use several measures to retrieve all the measures for a given item with just one query
    measures: List[str]


class VerticaDao():
    def __init__(self, host: str, port: int, user: str, password: str, dbname: str):
        """
        A DAO class to access data from Vertica. The main function is execute query which will return a pandas Dataframe
        :param host:
        :param port:
        :param user:
        :param password:
        :param dbname:
        """
        self.conn_info = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': dbname,
            # 10 minutes timeout on queries
            'read_timeout': 200000,
            # default throw error on invalid UTF-8 results
            'unicode_error': 'strict',
            # SSL is disabled by default
            'ssl': False,
            'connection_timeout': 20
            # connection timeout is not enabled by default
        }

    def execute_query(self, query: str) -> pd.DataFrame:
        """
        :param query:
        :return: Returns a pandas Dataframe with the result of the query as a table
        """
        with vertica_python.connect(**self.conn_info) as connection:
            cur = connection.cursor('dict')
            cur.execute(query)
            res_df = pd.DataFrame(cur.iterate())
        return res_df


class TimeSeriesEtl:
    def __init__(self, db_type: str, host: str, port: int, user: str, password: str, dbname: str, schema: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.schema = schema
        if db_type == 'vertica':
            self.dao = VerticaDao(host, port, user, password, dbname)

    def get_measure_ts(self, table: str, item_id: int, measures: List[str], period: int) -> pd.DataFrame:
        """
        Get a simple Pandas Dataframe representing a multivariate timeseries given by the following parameters
        :param table: The table in the DB
        :param item_id: The itemID which is normally the index of the DB table
        :param measures: A list of measures to retrieve which should match the columns in the DB
        :param period: The period of time to aggregate to
        :return: a Pandas Dataframe representing a multivariate timeseries
        """
        # example of result for item_id = 3 ['volume as volume_3', 'load as load_3']
        measures_columns = [m + ' as {0}_{1}'.format(m, item_id) for m in measures]
        query = 'select start_date, {0} from {1}.{2} where item_id = {3} order by start_date'.format(
            ', '.join(measures_columns), self.schema, table, item_id)
        df = self.dao.execute_query(query)
        if not df.empty:
            df = df.set_index('start_date')
            # eliminate duplicates
            df = df.loc[~df.index.duplicated(keep='first')]
        return df

    @staticmethod
    def create_list_of_tsdatainfo(table: str, item_ids: List[int], measure_names: List[str]) -> List[TSDataDef]:
        """
        A method that can be used to create a list of timeseries data definitions containing the item ids, the measures
        and the tables. This is just an auxiliary method
        :param table:
        :param item_ids:
        :param measure_names:
        :return:
        """
        list_res = []
        for it_id in item_ids:
            list_res.append(TSDataDef(table, it_id, measure_names))
        return list_res

    def __create_shifted_columns(self, df: pd.DataFrame, shifts: List[int], period: int) -> pd.DataFrame:
        """
        For each of the shift number in shifts, shift each of the columns of the df Dataframe. The period is just used
        to give the proper name to the shifted column
        :param df:
        :param shifts:
        :param period:
        :return:
        """
        for column in df.columns:
            for shift in shifts:
                new_column_name = '{0}_{1}'.format(column, shift * period)  # e.g volume_3_-5
                df[new_column_name] = df[column].shift(periods=-shift)
        return df

    def build_dataset(self, predictors_info: List[TSDataDef], shifts: List[int], targets_info: List[TSDataDef],
                      targets_horizon: List[int], period: int) -> pd.DataFrame:
        """
        It builds a dataset that can be used later with machine learning algorithms or used for data visualisation
        It receives a list of information about the predictors in the form of TSDataDef classes. This predictors can
        be shifted n periods through the shifts argument which can have more than one shifts. The targets_info is going
        to have the information about the items to be predicted. The targets_horizon are the horizons in the future in
        number of periods.
        :param predictors_info:
        :param shifts:
        :param targets_info:
        :param targets_horizon:
        :param period:
        :return:
        """
        list_of_dfs = []
        # We don't really need separate loops for predictors_info and targets_info but we leave it like this if
        # needed in future implementations
        for predictor in predictors_info:
            df_predictor = self.get_measure_ts(predictor.table, predictor.item_id, predictor.measures, period)
            if shifts:
                df_predictor = self.__create_shifted_columns(df_predictor, shifts, period)
            list_of_dfs.append(df_predictor)
        for target in targets_info:
            df_target = self.get_measure_ts(target.table, target.item_id, target.measures, period)
            if shifts:
                df_target = self.__create_shifted_columns(df_target, targets_horizon, period)
            list_of_dfs.append(df_target)
        return pd.concat(list_of_dfs, axis=1)
