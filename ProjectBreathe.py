# This file contains main class for the project to analysis data, it initialize multiple data frames for later analysis

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
        self.df['pm2.5_mean'] = self.epa_pm_25_object.mean_cols
        self.df.astype({'pm2.5_mean': 'float64'}).dtypes
        self.df.reset_index()
    
    def analyse(self):
        print(self.getCorrelationBetween('smell value', 'pm2.5_mean'))

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
