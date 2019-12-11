# This file contains main class for the project to analysis data, it initialize multiple data frames for later analysis
import analyse
import smell_report_cleanup
import numpy as np
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from SmellReport import SmellReport
from SmellPGHStatistics import SmellPGHStatistics
from EJAAnalysis import EJAAnalysis
from BreatheMeter import BreatheMeter
from AirQualityByZipCode import AirQualityByZipCode
# ProjectBreath class contains the report link and smellReport object


class ProjectBreathe(object):

    # default smell report csv file link
    smellReportLink = r'data/smell_reports.csv'
    smellReport: SmellReport = None
    smellPGHStatistics: SmellPGHStatistics
    EJAAnalysis: EJAAnalysis
    BreatheMeter: BreatheMeter

    def __init__(self, smellReportLink=None):
        # User could customize the smellReport csv file by link
        if (smellReportLink == None):
            self.smellReportLink = smellReportLink
        else:
            self.smellReportLink = self.smellReportLink

        smellReportDataFrame = self.getSmellReportDataFrame()

        # Initialize different classes for stat analyse
        self.smellReport = SmellReport(smellReportDataFrame)
        self.smellPGHStatistics = SmellPGHStatistics(self.smellReport)
        self.EJAAnalysis = EJAAnalysis(self.smellReport)
        self.BreatheMeter = BreatheMeter()
        self.AirQualityByZipCode = AirQualityByZipCode()

    # Function that return the smell report datafrome
    def getSmellReportDataFrame(self) -> pd.DataFrame:
        rawSmellReport = pd.read_csv(self.smellReportLink)
        # Clean up the smell report data entries
        smellReportDataFrame = self.cleanUp(rawSmellReport)
        return smellReportDataFrame

    def cleanUp(self, df) -> pd.DataFrame:
        return smell_report_cleanup.cleanup(df)

    # Run all analysis
    def analyse(self):
        self.smellReport.run()
        self.smellPGHStatistics.run()
        self.EJAAnalysis.run()
        self.BreatheMeter.run()
        self.AirQualityByZipCode.run()

