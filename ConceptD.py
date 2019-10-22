import pandas as pd
import SmellReport as SmellReport


# Concept D
# Zip code and user amount/location 
# We will group data point reports by zip code to generate area air quality insights based on region.
# By comparing region data to demographic statistics,
# we will find correlations between air quality and different demographic attributions.


class ConceptD(object):
    smellReport: SmellReport

    def __init__(self):
        self.smellReport = SmellReport()

    def __init__(self, smellReport: SmellReport):
        self.smellReport = smellReport

    def begin(self):
        return None
    