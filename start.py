import numpy as np
import pandas as pd

import smell_report_cleanup

smellReportLink = 'data/smell_reports.csv'

rawSmellReport = pd.read_csv(smellReportLink)

smellReport = smell_report_cleanup.cleanup(rawSmellReport)