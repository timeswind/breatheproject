import numpy as np
import analyse
from EpaData import EPAPM25
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# SmellReport class initialize the datafrom from data of SmellPitts


class SmellReport(object):
    df = pd.DataFrame()
    zipcodes = []
    epa_pm_25_object: EPAPM25

    def describe(self) -> pd.DataFrame.describe:
        return self.df.describe()

    def __init__(self, dataframe):
        self.df = dataframe
        self.zipCodes = self.getZipCodes()
        self.initialize_epa_pm25_data()

    def initialize_epa_pm25_data(self):
        data_2016_filepath = 'data/EPA_PITTSBURG_PM25_2016.csv'
        data_2017_filepath = 'data/EPA_PITTSBURG_PM25_2017.csv'
        data_2018_filepath = 'data/EPA_PITTSBURG_PM25_2018.csv'

        self.epa_pm_25_object = EPAPM25(
            data_csv_path=data_2016_filepath, year=2016)
        self.epa_pm_25_object.append_data_from_csv(
            data_csv_path=data_2017_filepath, year=2017)
        self.epa_pm_25_object.append_data_from_csv(
            data_csv_path=data_2018_filepath, year=2018)
        self.pre_analyse()

    def pre_analyse(self):
        self.df = self.df.set_index(['date'])
        daily_pm25_mean_cols_by_county = self.epa_pm_25_object.daily_pm25_mean_cols_by_county
        for county in daily_pm25_mean_cols_by_county:
            self.df[county + '_daily_pm25_mean'] = daily_pm25_mean_cols_by_county[county]
            self.df.astype({county + '_daily_pm25_mean': 'float64'}).dtypes

        self.df['pa_daily_pm25_mean'] = self.epa_pm_25_object.pa_daiyly_pm25_mean_cols
        self.df.astype({'pa_daily_pm25_mean': 'float64'}).dtypes
        self.df.reset_index()

    def analyse(self):
        self.plotReportsOverMonths()
        self.analyse_corr_smell_pm25()

    def analyse_corr_smell_pm25(self):
        corr_smell_pm25_counties = {}
        for county in self.epa_pm_25_object.counties:
            corr = self.getCorrelationBetween(
                'smell value', county + '_daily_pm25_mean')
            corr_smell_pm25_counties[county] = corr
            print("The correlation bewteen smell value user reported and average pm2.5 in %s at that day is %f" % (
                county, corr))

        corr_smell_pm25 = self.getCorrelationBetween(
            'smell value', 'pa_daily_pm25_mean')

        print("The correlation bewteen smell value user reported and average pm2.5 in Pennsylvania at that day is %f" % corr_smell_pm25)
        print("** We could see there is no correlation between user reported smell value and the actualy pm2.5 level")
        for county in self.epa_pm_25_object.counties:
            sns.regplot(x=county+"_daily_pm25_mean",
                        y="smell value", data=self.df)
            plt.ylim(0,)
            plt.savefig('results/'+county+'_daily_pm25_mean.png')
            plt.close()

        sns.regplot(x="pa_daily_pm25_mean", y="smell value", data=self.df)
        plt.ylim(0,)
        plt.savefig('results/pa_daily_pm25_mean.png')
        plt.close()

    def getCorrelationBetween(self, column1, column2):
        return self.df[column1].corr(self.df[column2])

    def getZipCodes(self) -> list:
        return analyse.getAllZipCodes(self.df)

    def reportsOverMonths(self):
        return []

    def reportsOverYears(self):
        return []

    def plotReportsOverMonths(self):
        yearMonthGroups = self.df.groupby(["year", "month"])
        label = []
        no_users = []
        for key in yearMonthGroups.groups.keys():
            if not isinstance(key, list):
                label.append(str(key))
                no_users.append(yearMonthGroups.size()[key])

        index = np.arange(len(label))
        description = 'This graph shows number of reports on the SmellPitts, which is a indicator to track user activities'
        plt.rc('text', usetex=False)
        plt.bar(index, no_users)
        plt.xlabel('Month', fontsize=5)
        plt.ylabel('No of Users', fontsize=5)
        plt.xticks(index, label, fontsize=5, rotation=30)
        plt.figtext(0.99, 0.95, description,
                    horizontalalignment='right', fontsize=8)
        plt.savefig('results/reports_over_month.png')
        plt.close()