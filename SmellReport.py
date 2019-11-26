import numpy as np
import analyse
import tools
from EpaData import EPAPM25
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os.path
import smell_report_cleanup
import sys
import argparse
parser = argparse.ArgumentParser()
# SmellReport class initialize the datafrom from data of SmellPitts


class SmellReport(object):
    smellReportLink = r'data/smell_reports.csv'
    df = pd.DataFrame()
    zipcodes = []
    epa_pm_25_object: EPAPM25

    def __init__(self, dataframe=None):
        parser.add_argument("-t", "--test", help="test run flag", type=tools.str2bool, nargs='?',
                            const=True, default=False,)
        parser.add_argument("-s",
                            "--startdate",
                            help="The Start Date - format YYYY-MM-DD",
                            required=False,
                            type=tools.valid_date)
        parser.add_argument("-e",
                            "--enddate",
                            help="The End Date - format YYYY-MM-DD",
                            required=False,
                            type=tools.valid_date)

        args = parser.parse_args()
        isTest: bool = args.test
        startDate: str = args.startdate
        endDate: str = args.enddate

        if (dataframe is not None):
            self.df = dataframe
        else:
            self.df = self.getInitializedSmellReportDataFrame()

        # only analyse selected date range
        # example
        # python3 SmellReport.py -s 2016-06-02 -e 2016-06-03
        if (startDate is not None and endDate is not None):
            self.df = smell_report_cleanup.customizeDateRange(self.df, startDate, endDate)

        self.zipCodes = self.getZipCodes()
        self.initialize_epa_pm25_data()

    def describe(self) -> pd.DataFrame.describe:
        return self.df.describe()

    def getInitializedSmellReportDataFrame(self) -> pd.DataFrame:
        rawSmellReport = pd.read_csv(self.smellReportLink)
        return smell_report_cleanup.cleanup(rawSmellReport)

    def initialize_epa_pm25_data(self):
        data_2016_filepath = r'data/EPA_PITTSBURG_PM25_2016.csv'
        data_2017_filepath = r'data/EPA_PITTSBURG_PM25_2017.csv'
        data_2018_filepath = r'data/EPA_PITTSBURG_PM25_2018.csv'

        self.epa_pm_25_object = EPAPM25(
            data_csv_path=data_2016_filepath, year=2016)
        self.epa_pm_25_object.append_data_from_csv(
            data_csv_path=data_2017_filepath, year=2017)
        self.epa_pm_25_object.append_data_from_csv(
            data_csv_path=data_2018_filepath, year=2018)
        self.epa_pm_25_object.analyse()
        self.pre_analyse()

    def pre_analyse(self):
        pm_25_level_labels = [1, 2, 3, 4, 5]
        self.df = self.df.set_index(['date'])

        daily_pm25_mean_cols_by_county = self.epa_pm_25_object.daily_pm25_mean_cols_by_county
        
        self.df['Allegheny_daily_pm25_mean'] = daily_pm25_mean_cols_by_county['Allegheny']
        self.df.astype({'Allegheny_daily_pm25_mean': 'float64'}).dtypes
        self.df['Allegheny_daily_pm25_mean_binned'] = pd.cut(
            self.df['Allegheny_daily_pm25_mean'], 5, labels=pm_25_level_labels)
        self.df.astype({'Allegheny_daily_pm25_mean': 'float64'}).dtypes
        self.df['Allegheny_daily_pm25_mean_binned'] = self.df['Allegheny_daily_pm25_mean_binned'].astype(
            "int8")

        self.df['pa_daily_pm25_mean'] = self.epa_pm_25_object.pa_daiyly_pm25_mean_cols
        self.df['pa_daily_pm25_mean_binned'] = pd.cut(
            self.df['pa_daily_pm25_mean'], 5, labels=pm_25_level_labels)
        self.df.astype({'pa_daily_pm25_mean': 'float64'}).dtypes
        self.df['pa_daily_pm25_mean_binned'] = self.df['pa_daily_pm25_mean_binned'].astype(
            "int8")

        self.df.reset_index()

    def run(self):
        self.plotReportsOverMonths()
        self.analyse_corr_smell_pm25()

    def analyse_corr_smell_pm25(self) -> str:

        corr_df = self.df.copy()
        corr_df = corr_df[self.df.pa_daily_pm25_mean_binned != 0]

        # normalize smell value and pm25 readings
        SmellValueNormalized = corr_df["smell value"] / \
            corr_df["smell value"].max()

        corr_df["smell value normalized"] = SmellValueNormalized
        Allegheny_Daily_PM25_mean_Normalized = corr_df["Allegheny_daily_pm25_mean"] / \
            corr_df["Allegheny_daily_pm25_mean"].max()
        corr_df["Allegheny_daily_pm25_mean_normalized"] = Allegheny_Daily_PM25_mean_Normalized

        Allegheny_corr_smell_pm25 = self.getCorrelationBetween(corr_df,
                                                               'smell value', 'Allegheny' + '_daily_pm25_mean')
        Allegheny_corr_smell_pm25_normalized = self.getCorrelationBetween(corr_df,
                                                                          'smell value normalized', 'Allegheny_daily_pm25_mean_normalized')
        print("The correlation bewteen smell value user reported and average pm2.5 in %s at that day is %f" % (
            'Allegheny', Allegheny_corr_smell_pm25))
        print("The correlation bewteen NORMALIZED smell value user reported and average pm2.5 in %s at that day is %f" % (
            'Allegheny', Allegheny_corr_smell_pm25_normalized))

        PA_corr_smell_pm25 = self.getCorrelationBetween(corr_df,
                                                        'smell value', 'pa_daily_pm25_mean')

        print("The correlation bewteen smell value user reported and average pm2.5 in Pennsylvania at that day is %f" % PA_corr_smell_pm25)
        print("** We could see there is no correlation between user reported smell value and the actualy pm2.5 level")

        sns.regplot(x="Allegheny_daily_pm25_mean_binned",
                    y="smell value", data=corr_df)
        plt.ylim(0,)
        plt.savefig(r'results/Allegheny_daily_pm25_mean_binned.png')
        plt.close()

        sns.regplot(x="Allegheny_daily_pm25_mean_normalized",
                    y="smell value normalized", data=corr_df)
        plt.ylim(0,)
        plt.savefig(r'results/Allegheny_daily_pm25_mean_normalized.png')
        plt.close()

        sns.regplot(x="pa_daily_pm25_mean_binned",
                    y="smell value", data=corr_df)
        plt.ylim(0,)
        plt.savefig(r'results/pa_daily_pm25_mean_binned.png')
        plt.close()

        return r'results/Allegheny_daily_pm25_mean_normalized.png'

    def getCorrelationBetween(self, df, column1, column2):
        return df[column1].corr(df[column2])

    def getZipCodes(self) -> list:
        return analyse.getAllZipCodes(self.df)

    def reportsOverMonths(self):
        return []

    def reportsOverYears(self):
        return []

    def plotReportsOverMonths(self) -> str:
        yearMonthGroups = self.df.groupby(["year", "month"])
        label = []
        no_users = []
        for key in yearMonthGroups.groups.keys():
            if not isinstance(key, list):
                label.append(str(key))
                no_users.append(yearMonthGroups.size()[key])

        data_folder = os.path.join("results")

        file_to_open = os.path.join(data_folder, "reports_over_month.png")

        index = np.arange(len(label))
        description = 'This graph shows number of reports on the SmellPitts, which is a indicator to track user activities'
        plt.rc('text', usetex=False)
        plt.bar(index, no_users)
        plt.xlabel('Month', fontsize=5)
        plt.ylabel('No of Users', fontsize=5)
        plt.xticks(index, label, fontsize=5, rotation=30)
        plt.figtext(0.99, 0.95, description,
                    horizontalalignment='right', fontsize=8)

        plt.savefig(os.path.join(os.getcwd(), file_to_open))
        plt.close()
        return file_to_open


if __name__ == "__main__":
    SP = SmellReport()
    SP.run()
