import tools
from os import system, name
from ProjectBreathe import ProjectBreathe
# and etc...
from bullet import VerticalPrompt, Numbers, Bullet, Check, YesNo, Input
import numpy as np
import pandas as pd
# command line parser to read flag values
import argparse
parser = argparse.ArgumentParser()

pb = None


def choose_program():
    executionChoices = ["CLI", "Graph Dashboard"]
    cli = VerticalPrompt(
        [
            Bullet("Choose program ",
                   choices=executionChoices),
        ],
        spacing=1
    )
    result = cli.launch()
    executionChoice = result[0][1]

    if (executionChoice == executionChoices[0]):
        clear()
        cli_program()
    elif (executionChoice == executionChoices[1]):
        print("Feature not complete")
        choose_program()


def cli_program():
    executionChoices = ["Show all smell report zipcodes", "exit"]
    cli = VerticalPrompt(
        [
            YesNo("Start the program "),
            Bullet("What data? ",
                   choices=executionChoices),
        ],
        spacing=1
    )
    result = cli.launch()
    executionChoice = result[1][1]

    if (executionChoice == executionChoices[0]):
        print(pb.smellReport.zipCodes)


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def test():
    smellReportLink = 'data/smell_reports.csv'
    pb = ProjectBreathe(smellReportLink)
    pb.analyse()
    # print(pb.smellReport.epa_pm_25_object.dataframe.head())

def start():
    smellReportLink = 'data/smell_reports.csv'
    pb = ProjectBreathe(smellReportLink)
    choose_program()


if __name__ == "__main__":
    parser.add_argument("-t", "--test", help="test run flag", type=tools.str2bool, nargs='?',
                        const=True, default=False,)
    args = parser.parse_args()
    isTest: bool = args.test

    if (isTest):
        test()
    else:
        start()
