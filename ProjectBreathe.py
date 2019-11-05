# This file contains main class for the project to analysis data, it initialize multiple data frames for later analysis
import analyse
import smell_report_cleanup
import numpy as np
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from SmellReport import SmellReport
from ConceptC import ConceptC
from EJAAnalysis import EJAAnalysis

# ProjectBreath class contains the report link and smellReport object


class ProjectBreathe(object):

    # default smell report csv file link
    smellReportLink = 'data/smell_reports.csv'
    smellReport: SmellReport = None
    conceptC: ConceptC
    EJAAnalysis: EJAAnalysis

    def __init__(self, smellReportLink):
        self.smellReportLink = smellReportLink
        smellReportDataFrame = self.getSmellReportDataFrame()
        self.smellReport = SmellReport(smellReportDataFrame)
        self.conceptC = ConceptC(self.smellReport)
        self.EJAAnalysis = EJAAnalysis(self.smellReport)

    def getSmellReportDataFrame(self) -> pd.DataFrame:
        rawSmellReport = pd.read_csv(self.smellReportLink)
        smellReportDataFrame = smell_report_cleanup.cleanup(rawSmellReport)
        return smellReportDataFrame

    def cleanUp(self, df) -> pd.DataFrame:
        return smell_report_cleanup.cleanup(df)

    def analyse(self):
        self.smellReport.analyse()
        self.conceptC.run()
        self.EJAAnalysis.run()
