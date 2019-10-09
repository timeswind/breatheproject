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