import pandas as pd

import smell_report_cleanup
import analyse

class SmellReport:
    df = pd.DataFrame()
    zipcodes = []

    def __init__(self, dataframe):
        self.df = dataframe
        self.zipCodes = self.getZipCodes()

    def getZipCodes(self) -> list:
        return analyse.getAllZipCodes(self.df)

class ProjectBreathe:

    smellReportLink = ''
    smellReport = None

    def __init__(self, smellReportLink):
        self.smellReportLink = smellReportLink
        rawSmellReport = pd.read_csv(self.smellReportLink)
        smellReportDataFrame = smell_report_cleanup.cleanup(rawSmellReport)
        self.smellReport = SmellReport(smellReportDataFrame)
    
    def cleanUp(self, df) -> pd.DataFrame:
        return smell_report_cleanup.cleanup(df)
