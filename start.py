import numpy as np
import pandas as pd

from ProjectBreathe import ProjectBreathe
import smell_report_cleanup

smellReportLink = 'data/smell_reports.csv'

pb = ProjectBreathe(smellReportLink)

print(pb.smellReport.zipCodes)
# print(analyse.getAllZipCodes(smellReport))
# analyse.groupByZipCode(smellReport)