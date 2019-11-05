import pandas as pd

# The breath meter of the breatje project https://breatheproject.org/breathe-meter/


class BreatheMeter(object):

    # Default csv file link from EPA for annual_aqi_by_cbsa 2016
    default_csv_path = r'data/annual_aqi_by_cbsa_2016.csv'

    def __init__(self, csv_file_link=None):

        # user could initialize the class by customize data source of csv file link
        if (csv_file_link == None):
            self.df = pd.read_csv(self.default_csv_path)
        else:
            self.df = pd.read_csv(csv_file_link)
        self.calculateRank()

    def run(self):
        self.export()

    # Rank the row by 'Days PM2.5' column value
    def calculateRank(self):
        self.df['pct_rank'] = self.df['Days PM2.5'].rank(pct=True)

    # Get all cities
    def cities(self):
        return self.df['CBSA'].unique()


    # Export the resulting datafram into csv file
    def export(self):
        export_df = self.df[['CBSA', 'pct_rank']]
        export_df.to_csv('results/Breath_Meter_2016.csv',
                         index=None, header=True)


# Run the test as a single file, generate the Breath Meter results in the resutls folder
# BM = BreatheMeter()
# BM.run()
