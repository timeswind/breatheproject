import pandas as pd
from SmellReport import SmellReport
from pyproj import CRS, Transformer
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

        rs = proj.transform(self.a1.lat, self.a1.long)
        x = float(rs[0])
        y = float(rs[1])
        self.origin = self.Cartesian(x=x, y=y)
        self.df['cartesian coordinate'] = self.smellReport.df[['lat', 'long']].apply(
            self.geodeticToCrs(offset=(self.origin.x, self.origin.y)), axis=1)
        print(self.smellReport.df.head(100))

    def convertCoordinatesInSmellReport(self):
        # coordinateToCartesianMapping = map(
        # geodeticToCrs, df[''])
        # dateHoursToDaySlotColumn = list(dateHoursToDaySlotMapping)
        return None

    def geodeticToCrs(self, offset= (0,0)):
        def withOffset(row):
            lat = row['lat']
            long = row['long']
            rs = proj.transform(lat, long)
            x = float(rs[0]) - offset[0]
            y = float(rs[1]) - offset[1]
            return (x, y)
        return withOffset


test = EJAAnalysis()
