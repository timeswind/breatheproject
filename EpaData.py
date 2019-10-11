import pandas as pd


class EPAdata(object):
    year: int
    dataframe: pd.DataFrame
    # initlaize data by csv file

    def __init__(self, data_csv_path: str):
        self.__init__(data_csv_path=str, year=0)

    # initialize data by csv file and corronsponding year
    def __init__(self, data_csv_path: str, year: int):
        self.year = year
        self.dataframe = pd.read_csv(data_csv_path)

    def append_data_from_csv(self, data_csv_path: str, year: int):
        new_csv = pd.read_csv(data_csv_path)
        frames = [self.dataframe, new_csv]
        self.dataframe = pd.concat(frames, sort=False)

    def analyse(self):

        return None

    def cleanup(self):
        raise NotImplementedError


class EPAPM25(EPAdata):
        # initlaize data by csv file

    def __init__(self, data_csv_path: str):
        self.__init__(str, 0)

    # initialize data by csv file and corronsponding year
    def __init__(self, data_csv_path: str, year: int):
        super().__init__(data_csv_path, year)
        self.cleanup()
        self.analyse()

    def cleanup(self):
        dates = pd.to_datetime(self.dataframe['Date'])
        self.dataframe['date'] = pd.DatetimeIndex(dates).date
        self.dataframe.drop(['Date'], axis=1, inplace=True)
        # self.dataframe = self.dataframe.rename(columns={"Date": "date"})

    def analyse(self):
        self.get_mean_cols_group_by_date()
        return None
    # calculate average pm2.5 readings for each date
    def get_mean_cols_group_by_date(self):
        self.mean_cols = self.dataframe.groupby(['date'])['Daily Mean PM2.5 Concentration'].mean()
