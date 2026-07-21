import pandas as pd

def transform_laps(raw_laps):
    """This function handles cleaning of data so eveytime
    its called it return a dataframe is clean and ready"""

    columns_needed = ['Driver',
        'LapNumber',
        'LapTime',
        'Sector1Time',
        'Sector2Time', 
        'Sector3Time',
        'Compound',
        'TyreLife',
        'FreshTyre',
        'Stint',
        'SpeedI1',
        'SpeedI2',
        'SpeedFL',
        'SpeedST',
        'IsPersonalBest']

    df = raw_laps[columns_needed].copy()
    #converting timedelta columns into total seconds for example:
    #1 minute, 22 seconds, and 400 milliseconds --> 82.4 seconds
    time_columns = ['LapTime', 'Sector1Time', 'Sector2Time', 'Sector3Time']

    for col in time_columns:
        df[col] = df[col].dt.total_seconds()
    #remove null rows from laptime colunm
    df = df.dropna(subset=['LapTime'])

    #get the fastest lap
    fastest = df['LapTime'].min()

    #remove any lap that is faster than the fastest lap by 110%
    df = df[df['LapTime'] <= fastest * 1.1]

    #Fix DataT Types
    df['LapNumber'] = df['LapNumber'].astype(int)
    df['TyreLife'] = df['TyreLife'].astype(int)
    df['Stint'] = df['Stint'].astype(int)
    df['FreshTyre'] = df['FreshTyre'].astype(bool)
    df['IsPersonalBest'] = df['IsPersonalBest'].astype(bool)
    df['Compound'] = df['Compound'].astype(str)
    df['Driver'] = df['Driver'].astype(str)


    #Reset the index
    df = df.reset_index(drop=True)

    return df


