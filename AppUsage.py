
from SmellReport import SmellReport

if __name__ == "__main__":
    # Run the test as a single file, generate the Breath Meter results in the resutls folder
    SR = SmellReport()
    filePath = SR.plotReportsOverMonths()
    print(filePath)