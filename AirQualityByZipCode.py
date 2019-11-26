import pandas as pd
from SmellReport import SmellReport
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# AirQualityByZipCode
# Zip code and user amount/location 
# We will group data point reports by zip code to generate area air quality insights based on region.
# By comparing region data to demographic statistics,
# we will find correlations between air quality and different demographic attributions.


class AirQualityByZipCode(object):
    # default smell report csv file link
    smellReportLink = r'data/smell_reports.csv'
    smellReport: SmellReport
    df: pd.DataFrame

    resultImagePath = r'results/zipcode_smellvalue_heatmap.png'

    def __init__(self, smellReport: SmellReport = None):
        if (smellReport == None):
            self.smellReport = SmellReport(dataframe=None)
        else:
            self.smellReport = smellReport

    def run(self):
        self.df = self.smellReport.df.reset_index()
        self.df = self.df.dropna()
        self.df = self.df.groupby(['smell value', 'zipcode'])['Allegheny_daily_pm25_mean'].mean()
        self.df = self.df.reset_index()
        plt.figure(figsize=(50,10))
        df_wide=self.df.pivot_table( index='smell value', columns='zipcode', values='Allegheny_daily_pm25_mean' )
        sns.heatmap(df_wide)
        plt.savefig(self.resultImagePath, dpi=300)
        plt.close()
        return self.resultImagePath
    

if __name__ == "__main__":
    test = AirQualityByZipCode()
    resultImagePath = test.run()
    print(resultImagePath)