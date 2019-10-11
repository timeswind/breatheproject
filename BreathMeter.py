import pandas as pd


class BreathMeter(object):
    default_csv_path = 'data/annual_aqi_by_cbsa_2018.csv'

    def __init__(self, withEpaAnnualAqiByCbsaCsvFilepath: str):
        if (str):
            self.df = pd.read_csv(str)
        else:
            self.df = pd.read_csv(self.default_csv_path)
