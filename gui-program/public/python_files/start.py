import tools
from os import system, name
from ProjectBreathe import ProjectBreathe
# and etc...
import numpy as np
import pandas as pd
# command line parser to read flag values
import argparse
parser = argparse.ArgumentParser()
pb = None


def test():
    smellReportLink = 'data/smell_reports.csv'
    pb = ProjectBreathe(smellReportLink)
    pb.analyse()
    print('** Check results folder to view graphs of: correlation bewteen reported smell value and PM2.5 data records in different regions in PA')
    print('The user reports over month')
    # print(pb.smellReport.epa_pm_25_object.dataframe.head())


def start():
    smellReportLink = 'data/smell_reports.csv'
    pb = ProjectBreathe(smellReportLink)
    pb.analyse()
    print('** Check results folder to view graphs of: correlation bewteen reported smell value and PM2.5 data records in different regions in PA')
    print('The user reports over month')


if __name__ == "__main__":
    parser.add_argument("-t", "--test", help="test run flag", type=tools.str2bool, nargs='?',
                        const=True, default=False,)
    parser.add_argument("-s",
                        "--startdate",
                        help="The Start Date - format YYYY-MM-DD",
                        required=False,
                        type=tools.valid_date)
    parser.add_argument("-e",
                        "--enddate",
                        help="The End Date - format YYYY-MM-DD",
                        required=False,
                        type=tools.valid_date)

    args = parser.parse_args()
    isTest: bool = args.test
    startDate: str = args.startdate
    endDate: str = args.enddate

    if (isTest):
        test()
    else:
        start()
