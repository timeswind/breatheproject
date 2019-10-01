import pandas as pd

def cleanup(df: pd.read_csv):
    df["date"] = pd.to_datetime(df['epoch time'],unit='s')
    #drop those text fileds since current it is hard to analysis texts
    df.drop(['date & time',
    'epoch time',
    'smell description',
    'additional comments',
    'symptoms'],axis=1, inplace=True)

    df.rename(columns={'skewed latitude':'lat',
                          'skewed longitude':'long'}, 
                 inplace=True)

    print(df.head())
        
    # print(df.dtypes)
    # for col in df.columns: 
    #     print(col) 