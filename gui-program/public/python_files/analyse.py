#This is a modules contains multiple functions to do operations on data frame and return datas

import pandas as pd

# groupByZipCode take the dataframe and return a new dataframe grouped with 'zipcode' attribute
def groupByZipCode(df:pd.DataFrame) -> pd.DataFrame:
    dfByZipCode = df.groupby('zipcode')

    return dfByZipCode

# groupByZipCode take the dataframe and return list of all unique zipcodes
def getAllZipCodes(df:pd.DataFrame) -> list:
    groups = groupByZipCode(df).groups
    return list(groups.keys())

def customizeDateRange(df: pd.DataFrame, date_column_name:str,  start, end) -> pd.DataFrame:
    df = df[df[date_column_name] > start]
    df = df[df[date_column_name] < end]
    df = df.reset_index()
    return df