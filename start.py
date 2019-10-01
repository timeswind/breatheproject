import numpy as np
import pandas as pd
from os import system, name 

from bullet import VerticalPrompt, Numbers, Bullet, Check, YesNo, Input # and etc...

from ProjectBreathe import ProjectBreathe

pb = None

def choose_program():
    executionChoices = ["CLI", "Graph Dashboard"]
    cli = VerticalPrompt(
    [
        Bullet("Choose program ",
              choices = executionChoices),
    ],
    spacing = 1
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
              choices = executionChoices),
    ],
    spacing = 1
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

if __name__ == "__main__":
    smellReportLink = 'data/smell_reports.csv'
    pb = ProjectBreathe(smellReportLink)

    choose_program()
