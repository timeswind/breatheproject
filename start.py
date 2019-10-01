import numpy as np
import pandas as pd

from ProjectBreathe import ProjectBreathe

if __name__ == "__main__":
    smellReportLink = 'data/smell_reports.csv'

    pb = ProjectBreathe(smellReportLink)

    print(pb.smellReport.zipCodes) 