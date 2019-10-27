import pandas as pd


class EPAdata(object):
    year: int
    dataframe: pd.DataFrame
    # initlaize data by csv file

    # initialize data by csv file and corronsponding year
    def __init__(self, data_csv_path: str, year: int = 0):
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
    counties = list()

    # initialize data by csv file and corronsponding year
    def __init__(self, data_csv_path: str, year: int = 0):
        super().__init__(data_csv_path, year)
        self.cleanup()

    def append_data_from_csv(self, data_csv_path: str, year: int):
        new_EPAPM25 = EPAPM25(data_csv_path, year)
        new_frames = new_EPAPM25.dataframe
        frames = [self.dataframe, new_frames]
        self.dataframe = pd.concat(frames, sort=False)

    def cleanup(self):
        dates = pd.to_datetime(self.dataframe['Date'])
        self.dataframe['date'] = pd.DatetimeIndex(dates).date
        self.dataframe.drop(['Date'], axis=1, inplace=True)
        # self.dataframe = self.dataframe.rename(columns={"Date": "date"})

    def analyse(self):
        self.get_mean_cols_group_by('date')
        return None
    # calculate average pm2.5 readings for each date

    def get_mean_cols_group_by(self, column: str):
        counties = self.dataframe['COUNTY'].unique()
        self.daily_pm25_mean_cols_by_county = {}
        for county in counties:
            self.counties.append(county)
            filterByCounty = self.dataframe[self.dataframe['COUNTY']==county]
            self.daily_pm25_mean_cols_by_county[county] = filterByCounty.groupby(
            [column])['Daily Mean PM2.5 Concentration'].mean()
            
        self.pa_daiyly_pm25_mean_cols = self.dataframe.groupby(
            [column])['Daily Mean PM2.5 Concentration'].mean()
