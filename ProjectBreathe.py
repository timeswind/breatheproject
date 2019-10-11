# This file contains main class for the project to analysis data, it initialize multiple data frames for later analysis
import analyse
import smell_report_cleanup
import numpy as np
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from SmellReport import SmellReport

# ProjectBreath class contains the report link and smellReport object.
class ProjectBreathe(object):

    smellReportLink = ''
    smellReport: SmellReport = None

    def __init__(self, smellReportLink):

        self.smellReportLink = smellReportLink
        rawSmellReport = pd.read_csv(self.smellReportLink)
        smellReportDataFrame = smell_report_cleanup.cleanup(rawSmellReport)
        self.smellReport = SmellReport(smellReportDataFrame)

    def cleanUp(self, df) -> pd.DataFrame:
        return smell_report_cleanup.cleanup(df)

    def analyse(self):
        self.smellReport.analyse()
