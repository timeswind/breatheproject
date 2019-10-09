#This file contains main class for the project to analysis data, it initialize multiple data frames for later analysis

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import smell_report_cleanup
import analyse

# SmellReport class initialize the datafrom from data of SmellPitts
class SmellReport:
    df = pd.DataFrame()
    zipcodes = []

    def describe(self)->pd.DataFrame.describe:
        return self.df.describe()

    def __init__(self, dataframe):
        self.df = dataframe
        self.zipCodes = self.getZipCodes()

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
        
#ProjectBreath class contains the report link and smellReport object.
class ProjectBreathe:

    smellReportLink = ''
    smellReport:SmellReport = None

    def __init__(self, smellReportLink):

        self.smellReportLink = smellReportLink
        rawSmellReport = pd.read_csv(self.smellReportLink)
        smellReportDataFrame = smell_report_cleanup.cleanup(rawSmellReport)
        self.smellReport = SmellReport(smellReportDataFrame)
    
    def cleanUp(self, df) -> pd.DataFrame:
        return smell_report_cleanup.cleanup(df)
