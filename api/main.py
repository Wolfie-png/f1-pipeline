from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import pandas as pd
import os

app = FastAPI(title="F1 Telemetry API")

import os
from sqlalchemy import create_engine

def get_engine():
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'wolfie')
    password = os.getenv('DB_PASSWORD', 'password')
    db = os.getenv('DB_NAME', 'f1data')
    return create_engine(f'postgresql://{user}:{password}@{host}:5432/{db}')


class Lap(BaseModel):
    Driver: str
    LapNumber: int
    LapTime: float
    Compound: str
    TyreLife: int

@app.get('/')
def root():
    return {"message": "F1 Telemetry API is running"}


import numpy as np

@app.get("/laps")
def get_all_laps():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM laps", engine)
    df = df.replace({np.nan: None, np.inf: None, -np.inf: None})
    return df.to_dict(orient='records')

@app.get('/laps/{driver}')
def get_driver_laps(driver: str):
    engine = get_engine()
    df = pd.read_sql(text("SELECT * FROM laps WHERE \"Driver\" = :driver"),
                     engine, params={"driver": driver.upper()})
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No laps found for the driver: {driver}")
    df = df.replace({np.nan: None, np.inf: None, -np.inf: None})
    return df.to_dict(orient='records')


@app.get("/fastest-lap")
def get_fastest_lap():
    engine = get_engine()
    df = pd.read_sql(
        "SELECT * FROM laps ORDER BY \"LapTime\" ASC LIMIT 1",
        engine
    )
    return df.to_dict(orient='records')[0]

@app.get("/laps/{driver}/best")
def get_driver_best_lap(driver: str):
    engine = get_engine()
    df = pd.read_sql(
        text("""
            SELECT * FROM laps 
            WHERE \"Driver\" = :driver 
            ORDER BY \"LapTime\" ASC 
            LIMIT 1
        """),
        engine,
        params={"driver": driver.upper()}
    )
    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No laps found for driver {driver}"
        )
    return df.to_dict(orient='records')[0]

@app.get("/compounds")
def get_compounds():
    engine = get_engine()
    df = pd.read_sql(
        """
        SELECT \"Compound\", 
               COUNT(*) as lap_count,
               ROUND(AVG(\"LapTime\")::numeric, 3) as avg_lap_time,
               ROUND(MIN(\"LapTime\")::numeric, 3) as fastest_lap
        FROM laps 
        GROUP BY \"Compound\"
        ORDER BY avg_lap_time ASC
        """,
        engine
    )
    return df.to_dict(orient='records')