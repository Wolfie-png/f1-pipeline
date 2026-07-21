import pytest 
import pandas as pd
import numpy as np
from transformer.transform import transform_laps


#sample data to be passed in every test
@pytest.fixture
def sample_raw_laps():
    return pd.DataFrame({
        #Drivers column
        'Driver': ['VER', 'HAM', 'LEC', 'VER', 'HAM'],

        #LapNumer column
        'LapNumber': [1, 1, 1, 2, 2],

        #Laptime column
        'LapTime': [
            pd.Timedelta(seconds=95.5),
            pd.Timedelta(seconds=96.2),
            pd.Timedelta(seconds=97.1),
            None,#null data for removal of null test
            pd.Timedelta(seconds=200.0)# removal of outlier test
            ],



            'Sector1Time': [
                pd.Timedelta(seconds=28.1),
                pd.Timedelta(seconds=28.5),
                pd.Timedelta(seconds=29.0),
                None,
                pd.Timedelta(seconds=60.0),
            ],

            'Sector2Time': [
                pd.Timedelta(seconds=35.2),
                pd.Timedelta(seconds=35.8),
                pd.Timedelta(seconds=36.1),
                None,
                pd.Timedelta(seconds=80.0),
            ],


            'Sector3Time': [
                pd.Timedelta(seconds=32.2),
                pd.Timedelta(seconds=31.9),
                pd.Timedelta(seconds=32.0),
                None,
                pd.Timedelta(seconds=60.0),
            ],

            'Compound': ['SOFT', 'MEDIUM', 'HARD', 'SOFT', 'MEDIUM'],
            'TyreLife': [1, 1, 1, 2, 2],
            'FreshTyre': [True, True, True, False, False],
            'Stint': [1, 1, 1, 1, 1],
            'SpeedI1': [290.0, 288.0, 285.0, 291.0, 287.0],
            'SpeedI2': [295.0, 293.0, 290.0, 296.0, 292.0],
            'SpeedFL': [310.0, 308.0, 305.0, 311.0, 307.0],
            'SpeedST': [320.0, 318.0, 315.0, 321.0, 317.0],
            'IsPersonalBest': [True, False, False, False, False]
            
    })


#**************TEST 1: REMOVAL OF NULL LABS****************
def test_null_laps_removed(sample_raw_laps):
    result = transform_laps(sample_raw_laps)
    assert result['LapTime'].isnull().sum() == 0

#**************TEST 2: REMOVAL OF OUTLIER LABS****************
def test_outlier_laps_removed(sample_raw_laps):
    result = transform_laps(sample_raw_laps)
    fastest = result['LapTime'].min()
    assert result['LapTime'].max() <= fastest * 1.1

#**************TEST 3: LAPTIMES AND SECTOR TIMES WENT FROM TIMEDELTA --> FLOAT DATATYPE****************
def test_sector_times_is_float(sample_raw_laps):
    result = transform_laps(sample_raw_laps)
    assert result['LapTime'].dtype == float
    assert result['Sector1Time'].dtype == float
    assert result['Sector2Time'].dtype == float
    assert result['Sector3Time'].dtype == float

#**************TEST 4: CHECK DATATPES FOR THE REMAINING COLUMNS****************
def test_dt_remaining_columns(sample_raw_laps):
    result = transform_laps(sample_raw_laps)
    assert result['LapNumber'].dtype == int
    assert result['TyreLife'].dtype == int
    assert result['Driver'].dtype == object  
    assert result['Compound'].dtype == object

