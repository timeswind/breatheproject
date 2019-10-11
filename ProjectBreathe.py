# This file contains main class for the project to analysis data, it initialize multiple data frames for later analysis

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import smell_report_cleanup
import analyse

from EpaData import EPAPM25


# SmellReport class initialize the datafrom from data of SmellPitts

class SmellReport:
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
        self.analyse()

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
        corr_smell_pm25_counties = {}
        for county in self.epa_pm_25_object.counties:
            corr = self.getCorrelationBetween('smell value', county + '_daily_pm25_mean')
            corr_smell_pm25_counties[county] = corr
            print("The correlation bewteen smell value user reported and average pm2.5 in %s at that day is %f" % (county, corr))

        corr_smell_pm25 = self.getCorrelationBetween('smell value', 'pa_daily_pm25_mean')

        print("The correlation bewteen smell value user reported and average pm2.5 in Pennsylvania at that day is %f" % corr_smell_pm25)
        # print(self.df.head())
        #sns.regplot(x="pa_daily_pm25_mean", y="smell value", data=self.df)
        #plt.ylim(0,)
        #plt.show()

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
        plt.bar(index, no_users)
        plt.xlabel('Month', fontsize=5)
        plt.ylabel('No of Users', fontsize=5)
        plt.xticks(index, label, fontsize=5, rotation=30)
        plt.show()

# ProjectBreath class contains the report link and smellReport object.


class ProjectBreathe:

    smellReportLink = ''
    smellReport: SmellReport = None

    def __init__(self, smellReportLink):

        self.smellReportLink = smellReportLink
        rawSmellReport = pd.read_csv(self.smellReportLink)
        smellReportDataFrame = smell_report_cleanup.cleanup(rawSmellReport)
        self.smellReport = SmellReport(smellReportDataFrame)

    def cleanUp(self, df) -> pd.DataFrame:
        return smell_report_cleanup.cleanup(df)
