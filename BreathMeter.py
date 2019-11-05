import pandas as pd


class BreathMeter(object):
    default_csv_path = 'data/annual_aqi_by_cbsa_2016.csv'

    def __init__(self):
        self.df = pd.read_csv(self.default_csv_path)
        self.calculateRank()
    
    def calculateRank(self):
        self.df['pct_rank'] = self.df['Days PM2.5'].rank(pct=True)

    def cities(self):
        return self.df['CBSA'].unique()

    def export(self):
        export_df = self.df[['CBSA', 'pct_rank']]
        export_df.to_csv('results/Breath_Meter_2016.csv', index = None, header=True)


#Run as a single file, generate the Breath Meter results in the resutls folder
BM = BreathMeter()
BM.export()