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
        self.dataframe = pd.concat(frames)


class EPAPM25(EPAdata):
        # initlaize data by csv file
    def __init__(self, data_csv_path: str):
        super().__init__(str)

    # initialize data by csv file and corronsponding year
    def __init__(self, data_csv_path: str, year: int):
        super().__init__(data_csv_path, year)