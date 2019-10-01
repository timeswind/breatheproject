import pandas as pd


def groupByZipCode(df:pd.DataFrame) -> pd.DataFrame:
    dfByZipCode = df.groupby('zipcode')

    return dfByZipCode

def getAllZipCodes(df:pd.DataFrame) -> pd.DataFrame:
    groups = groupByZipCode(df).groups
    return list(groups.keys())