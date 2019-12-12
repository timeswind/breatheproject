import pandas as pd
from SmellReport import SmellReport
from pyproj import CRS, Transformer
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import matplotlib.patches as mpatches


crs = CRS.from_epsg(3857)
proj = Transformer.from_crs(crs.geodetic_crs, crs)


class EJAAnalysis(object):
    resultImagePath = r"results/EJA_smell_report.png"
    resultImagePathKey = r"results/EJA_smell_report"
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
    a1 = Coordinate(lat=40.552488, long=-80.117494)
    a2 = Coordinate(lat=40.285871, long=-79.725970)

    def __init__(self, smellReport: SmellReport = None):
        if (smellReport == None):
            self.smellReport = SmellReport()
        else:
            self.smellReport = smellReport

        self.df = self.smellReport.df

    def run(self):
        # Drop the unwanted columns for this analyis
        df = self.df
        df = df.reset_index()
        df = df[['year', 'lat', 'long']]
        # sort the dataframe
        df.sort_values(by=['year'])
        # set the index to be this and don't drop
        df.set_index(keys=['year'], drop=False,inplace=True)
        # get a list of names
        years=df['year'].unique().tolist()
        # now we can perform a lookup on a 'view' of the dataframe
        
        analyseDataframe = df
        print(analyseDataframe)
        # now you can query all 'joes'

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

        # set the boundary for the sactter plot
        minX = 0
        maxX = self.endpoint.x - self.origin.x
        minY = self.endpoint.y - self.origin.y
        maxY = 0

        # translate latitude and longitude for each row in smell reports into cartesian coordinates in turple format
        analyseDataframe['cartesian'] = analyseDataframe[['lat', 'long']].apply(self.geodeticToCrs(offset=(self.origin.x, self.origin.y)), axis=1)

        # Seperate the coordiante into two seperate column
        new_col_list = ['cartesian x', 'cartesian y']
        for n, col in enumerate(new_col_list):
            analyseDataframe[col] = analyseDataframe['cartesian'].apply(
                lambda location: location[n])

        # discard the intermeidate data column
        analyseDataframe.drop('cartesian', axis=1, inplace=True)


        # Grab the image for EJA area map
        img = plt.imread(r"data/EJAMAP_PITTSBURG.png")
        # Add the map to the plot
        fig, ax = plt.subplots()
        ax.imshow(img, extent=[minX, maxX, minY, maxY])

        # Filter the data to include reports in the map area only
        analyseDataframe = analyseDataframe[analyseDataframe['cartesian x'] > 0]
        analyseDataframe = analyseDataframe[analyseDataframe['cartesian x'] < maxX]
        analyseDataframe = analyseDataframe[analyseDataframe['cartesian y'] < 0]
        analyseDataframe = analyseDataframe[analyseDataframe['cartesian y'] > minY]

        # Draw report points in the map and save to results folder
        colors = cm.rainbow(np.linspace(0, 1, len(years)))
        recs = []
        for year, c in zip(years, colors):
            year_analyseDataframe = analyseDataframe.loc[analyseDataframe.year==year]
            plt.scatter(year_analyseDataframe['cartesian x'], year_analyseDataframe['cartesian y'], s=0.1, color=c, alpha=0.5)
            recs.append(mpatches.Rectangle((0,0),1,1,fc=c))
            
        plt.legend(recs,years,loc=4)
        plt.savefig(self.resultImagePath, dpi=800)
        plt.close()

        for year, c in zip(years, colors):
            # Grab the image for EJA area map
            img = plt.imread(r"data/EJAMAP_PITTSBURG.png")
            # Add the map to the plot
            fig, ax = plt.subplots()
            ax.imshow(img, extent=[minX, maxX, minY, maxY])
            year_analyseDataframe = analyseDataframe.loc[analyseDataframe.year==year]
            plt.scatter(year_analyseDataframe['cartesian x'], year_analyseDataframe['cartesian y'], s=0.1, color=c, alpha=0.5)
            recs.append(mpatches.Rectangle((0,0),1,1,fc=c))
            plt.legend(recs,years,loc=4)
            plt.savefig(self.resultImagePathKey + '_' + str(year) + '.png', dpi=800)
            plt.close()

        return self.resultImagePath

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


if __name__ == "__main__":
    # Run the test as a single file by 'python3 EJAAnalysis.py', get the results in the results folder
    test = EJAAnalysis()
    resultImagePath = test.run()
    print(resultImagePath)
