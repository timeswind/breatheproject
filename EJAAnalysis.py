import pandas as pd
from SmellReport import SmellReport
from pyproj import CRS, Transformer
import matplotlib.pyplot as plt

crs = CRS.from_epsg(3857)
proj = Transformer.from_crs(crs.geodetic_crs, crs)


class EJAAnalysis(object):
    class Coordinate(object):
        def __init__(self, lat: float, long: float):
            self.lat = lat
            self.long = long

    class Cartesian(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y

    a1 = Coordinate(lat=40.518257, long=-80.132828)
    a2 = Coordinate(lat=40.334705, long=-79.705593)

    def __init__(self, smellReport: SmellReport = None):
        if (smellReport == None):
            self.smellReport = SmellReport()
        else:
            self.smellReport = smellReport

        self.df = self.smellReport.df
        self.df.drop(['Allegheny_daily_pm25_mean', 'Allegheny_daily_pm25_mean_binned', 'pa_daily_pm25_mean', 'pa_daily_pm25_mean_binned',
                      'date&time', 'isAfternoon', 'isEvening', 'isMorning', 'isNight', 'year', 'month', 'day', 'zipcode'], axis=1, inplace=True)

        a1rs = proj.transform(self.a1.lat, self.a1.long)
        a1x = float(a1rs[0])
        a1y = float(a1rs[1])
        self.origin = self.Cartesian(x=a1x, y=a1y)

        a2rs = proj.transform(self.a2.lat, self.a2.long)
        a2x = float(a2rs[0])
        a2y = float(a2rs[1])
        self.endpoint = self.Cartesian(x=a2x, y=a2y)

        self.df['cartesian'] = self.smellReport.df[['lat', 'long']].apply(
            self.geodeticToCrs(offset=(self.origin.x, self.origin.y)), axis=1)

        new_col_list = ['cartesian x', 'cartesian y']
        for n, col in enumerate(new_col_list):
            self.df[col] = self.df['cartesian'].apply(
                lambda location: location[n])

        self.df.drop('cartesian', axis=1, inplace=True)
        # print(self.smellReport.df.head(100))

        minX = 0
        maxX = self.endpoint.x - self.origin.x
        minY = self.endpoint.y - self.origin.y
        maxY = 0

        img = plt.imread(r"data/EJAMAP_PITTSBURG.png")
        fig, ax = plt.subplots()
        ax.imshow(img, extent=[minX, maxX, minY, maxY])

        self.df = self.df[self.df['cartesian x'] > 0]
        self.df = self.df[self.df['cartesian x'] < maxX]
        self.df = self.df[self.df['cartesian y'] < 0]
        self.df = self.df[self.df['cartesian y'] > minY]


        plt.scatter(self.df['cartesian x'], self.df['cartesian y'],s = 0.1)
        plt.savefig(r'results/EJA_smell_report.png', dpi=800)
        plt.close()

    def convertCoordinatesInSmellReport(self):
        # coordinateToCartesianMapping = map(
        # geodeticToCrs, df[''])
        # dateHoursToDaySlotColumn = list(dateHoursToDaySlotMapping)
        return None

    def geodeticToCrs(self, offset=(0, 0)):
        def withOffset(row):
            lat = row['lat']
            long = row['long']
            rs = proj.transform(lat, long)
            x = float(rs[0]) - offset[0]
            y = float(rs[1]) - offset[1]
            return (x, y)
        return withOffset


test = EJAAnalysis()
