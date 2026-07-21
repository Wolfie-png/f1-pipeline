import pandas as pd
import os
from sqlalchemy import create_engine

def get_engine():
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'wolfie')
    password = os.getenv('DB_PASSWORD', 'secret_password_here')
    db = os.getenv('DB_NAME', 'f1_data')


    return create_engine(
        f'postgresql+psycopg2://{user}:{password}@{host}:5432/{db}'
    )
    


def load_laps(clean_laps):
    engine = get_engine()

    clean_laps.to_sql(
        name='laps', #table name
        con=engine, 
        if_exists='replace', #drop any existing tables and replace it
        index=False
    )

    print(f"Loaded {len(clean_laps)} laps into PostgreSQL")



if __name__ == "__main__":
    from extractor.extract import extract_session
    from transformer.transform import transform_laps

    raw = extract_session(2023, 'Bahrain', 'R')
    clean = transform_laps(raw)
    load_laps(clean)