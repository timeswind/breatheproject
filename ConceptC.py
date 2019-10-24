import pandas as pd
import SmellReport as SmellReport


# Concept C
# Smell PGH Statistics
# We will generate a graph to analyze the smell value over time.
# This will give us an idea of how the air quality changed in that particular area over the years.
# We will using Python program that will help us project all the data in a graphical scenario.
# the path of demonstrating the air quality to others will be user-friendly to the public.
class ConceptC(object):
    smellReport: SmellReport

    def __init__(self):
        self.smellReport = SmellReport()

    def __init__(self, smellReport: SmellReport):
        self.smellReport = smellReport

    def run(self):
        return None

    def averageSmellValuePerDay(self) -> pd.DataFrame:
        
        return None
    