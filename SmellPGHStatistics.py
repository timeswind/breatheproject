import pandas as pd
from SmellReport import SmellReport
import math
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# Concept C
# Smell PGH Statistics
# We will generate a graph to analyze the smell value over time.
# This will give us an idea of how the air quality changed in that particular area over the years.
# We will using Python program that will help us project all the data in a graphical scenario.
# the path of demonstrating the air quality to others will be user-friendly to the public.


class SmellPGHStatistics(object):
    smellReport: SmellReport
    df: pd.DataFrame

    def __init__(self, smellReport: SmellReport = None):
        if (smellReport == None):
            self.smellReport = SmellReport()
        else:
            self.smellReport = smellReport

    def run(self):
        self.df = self.smellReport.df.drop(['lat', 'long', 'zipcode', 'year', 'month', 'day',
                                            'isAfternoon', 'isEvening', 'isMorning', 'isNight'], axis=1, inplace=False)
        self.df = self.df.groupby('date').mean()
        self.df = self.df[self.df['pa_daily_pm25_mean_binned'] != 0]
        # Group the PM2.5 Readings into 6 different category with Boundary value we get from EPA site
        cut_bounds = [0, 50, 100, 150, 200, 300, 500]
        bounds_labels = ['Good', 'Moderate', 'Unhealthy for Sensitive Groups',
                         'Unhealthy', 'Very Unhealthy', 'Hazardous']
        bucketted_allegheny_daily_pm25_mean = pd.cut(
            self.df["Allegheny_daily_pm25_mean"], bins=cut_bounds, labels=bounds_labels)
        self.df["bucketted_allegheny_daily_pm25_mean"] = bucketted_allegheny_daily_pm25_mean
        self.df = self.df.reset_index()
        self.df["smell value"] = self.df["smell value"] / \
            self.df["smell value"].max()

        self.df["Allegheny_daily_pm25_mean"] = self.df["Allegheny_daily_pm25_mean"] / \
            self.df["Allegheny_daily_pm25_mean"].max()

        self.plot()
        return None

    def plot(self):
        my_dpi = 100
        plt.figure(figsize=(8000/my_dpi, 800/my_dpi), dpi=my_dpi)
        plt.plot('date', 'smell value', data=self.df, marker='o', markerfacecolor='blue',
                 markersize=1, color='yellow', linewidth=1, label="Smell Value Normalized")
        plt.plot('date', 'Allegheny_daily_pm25_mean', data=self.df, marker='o', markerfacecolor='yellow',
                 markersize=1, color='skyblue', linewidth=1, label="Allegheny_daily_pm25_mean_normalized")
        plt.legend()
        plt.savefig(
            r'results/compare_bewteen_smell_value_and_pm25_history_line.png')
        plt.close()

# test only
SPS = SmellPGHStatistics()
SPS.run()
