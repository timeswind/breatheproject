import pandas as pd
from SmellReport import SmellReport
from pyproj import CRS, Transformer
import matplotlib.pyplot as plt

crs = CRS.from_epsg(3857)
proj = Transformer.from_crs(crs.geodetic_crs, crs)


class EJAAnalysis(object):

    # Geo-Coordinate Object that have latitude and longitude
    class Coordinate(object):
        def __init__(self, lat: float, long: float):
            self.lat = lat
            self.long = long

    # Cartesian Coordinate in 2D
    class Cartesian(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y

    # We use screenshot of the map EJA in Allegheny county
    # a1 and a2 are the origin and ending point of the retangle
    # The picture is in data folder named EJAMAP_PITTSBURG.png
    # We use these two points as offsets to plot geo-tagged smell reports
    a1 = Coordinate(lat=40.518257, long=-80.132828)
    a2 = Coordinate(lat=40.334705, long=-79.705593)

    def __init__(self, smellReport: SmellReport = None):
        if (smellReport == None):
            self.smellReport = SmellReport()
        else:
            self.smellReport = smellReport

        self.df = self.smellReport.df

    def run(self):
        # Drop the unwanted columns for this analyis
        self.df.drop(['Allegheny_daily_pm25_mean', 'Allegheny_daily_pm25_mean_binned', 'pa_daily_pm25_mean', 'pa_daily_pm25_mean_binned',
                      'date&time', 'isAfternoon', 'isEvening', 'isMorning', 'isNight', 'year', 'month', 'day', 'zipcode'], axis=1, inplace=True)

        # Project the origin into 2d plane with cartesian coordinates
        origin_in_cartesian = proj.transform(self.a1.lat, self.a1.long)
        origin_x = float(origin_in_cartesian[0])
        origin_y = float(origin_in_cartesian[1])
        self.origin = self.Cartesian(x=origin_x, y=origin_y)

        # Project the endpoint into 2d plane with cartesian coordinates
        endpoint_in_cartesian = proj.transform(self.a2.lat, self.a2.long)
        endpoint_x = float(endpoint_in_cartesian[0])
        endpoint_y = float(endpoint_in_cartesian[1])
        self.endpoint = self.Cartesian(x=endpoint_x, y=endpoint_y)

        # translate latitude and longitude for each row in smell reports into cartesian coordinates in turple format
        self.df['cartesian'] = self.smellReport.df[['lat', 'long']].apply(
            self.geodeticToCrs(offset=(self.origin.x, self.origin.y)), axis=1)

        # Seperate the coordiante into two seperate column
        new_col_list = ['cartesian x', 'cartesian y']
        for n, col in enumerate(new_col_list):
            self.df[col] = self.df['cartesian'].apply(
                lambda location: location[n])

        # discard the intermeidate data column
        self.df.drop('cartesian', axis=1, inplace=True)

        # set the boundary for the sactter plot
        minX = 0
        maxX = self.endpoint.x - self.origin.x
        minY = self.endpoint.y - self.origin.y
        maxY = 0

        # Grab the image for EJA area map
        img = plt.imread(r"data/EJAMAP_PITTSBURG.png")
        # Add the map to the plot
        fig, ax = plt.subplots()
        ax.imshow(img, extent=[minX, maxX, minY, maxY])

        # Filter the data to include reports in the map area only
        self.df = self.df[self.df['cartesian x'] > 0]
        self.df = self.df[self.df['cartesian x'] < maxX]
        self.df = self.df[self.df['cartesian y'] < 0]
        self.df = self.df[self.df['cartesian y'] > minY]

        # Draw report points in the map and save to results folder
        plt.scatter(self.df['cartesian x'], self.df['cartesian y'], s=0.1)
        plt.savefig(r'results/EJA_smell_report.png', dpi=800)
        plt.close()

    # A curry function that take the offset and return another function
    # The returned function takes in a row of panda dataframe and returned a cartesian coordinate
    def geodeticToCrs(self, offset=(0, 0)):
        def withOffset(row):
            lat = row['lat']
            long = row['long']
            rs = proj.transform(lat, long)
            x = float(rs[0]) - offset[0]
            y = float(rs[1]) - offset[1]
            return (x, y)
        return withOffset


# test = EJAAnalysis()
