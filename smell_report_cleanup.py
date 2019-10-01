import pandas as pd

def cleanup(df: pd.read_csv) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df['epoch time'],unit='s')
    df['year'] = pd.DatetimeIndex(df['date']).year
    df['month'] = pd.DatetimeIndex(df['date']).month
    df['day'] = pd.DatetimeIndex(df['date']).day

    dateHoursToDaySlotMapping = map(get_part_of_day, pd.DatetimeIndex(df['date']).hour)
    dateHoursToDaySlotColumn = list(dateHoursToDaySlotMapping)

    df['dayslot'] = dateHoursToDaySlotColumn

    daySlotOneHot = pd.get_dummies(df['dayslot'])

    df = df.join(daySlotOneHot)
    #drop the slot after finish one hot encoding
    df.drop(['dayslot'], axis=1, inplace=True)

    #drop those text fileds since current it is hard to analysis texts
    df.drop(['date & time',
    'epoch time',
    'smell description',
    'additional comments',
    'symptoms'],axis=1, inplace=True)

    df.rename(columns={'skewed latitude':'lat',
                          'skewed longitude':'long'}, 
                 inplace=True)

    return df
        
    # print(df.dtypes)
    # for col in df.columns: 
    #     print(col) 

def get_part_of_day(hour):
    return (
    "isMorning" if 5 <= hour <= 11
    else
    "isAfternoon" if 12 <= hour <= 17
    else
    "isEvening" if 18 <= hour <= 22
    else
    "isNight"
    )