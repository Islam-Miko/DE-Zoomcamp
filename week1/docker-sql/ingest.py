import pandas as pd
import sqlalchemy as sa
from decouple import config
import time

#VARIABLES  from envs
DATABASE_URL = config("DATABASE_URL")
CHUNK_SIZE=config("CHUNK_SIZE", cast=int)
TAXI_TABLE = "green_taxi_data"
ZONE_TABLE = "zones"

#SQLALCHEMY connection instance
engine = sa.create_engine(DATABASE_URL)

#green_tripdata table creation and ingest data

green_tripdata_header_df = pd.read_csv("green_tripdata_2019-01.csv", nrows=1).head(0)
green_tripdata_df = pd.read_csv("green_tripdata_2019-01.csv", iterator=True, chunksize=CHUNK_SIZE)
green_tripdata_header_df.to_sql(name=TAXI_TABLE, con=engine, if_exists="replace")

count = 1

start_time = time.perf_counter()
for chunk_df in green_tripdata_df:
    chunk_df.to_sql(name=TAXI_TABLE, con=engine, if_exists="append")
    print(f"{count}) Ingested chunk {CHUNK_SIZE}")
    count += 1
end_time = time.perf_counter()

print(f"Ingestion of {TAXI_TABLE}`s duration {end_time - start_time}.")



#zones table creation and ingest data
zones_header_df = pd.read_csv("taxi+_zone_lookup.csv", nrows=1).head(0)
zones_df = pd.read_csv("taxi+_zone_lookup.csv", iterator=True, chunksize=CHUNK_SIZE)

zones_header_df.to_sql(name=ZONE_TABLE, con=engine, if_exists="replace")

count = 1
start_time = time.perf_counter()
for chunk_df in zones_df:
    chunk_df.to_sql(name=ZONE_TABLE, con=engine, if_exists="append")
    print(f"{count}) Ingested chunk {CHUNK_SIZE}")
    count += 1
end_time = time.perf_counter()

print(f"Ingestion of {ZONE_TABLE}`s duration {end_time - start_time}.")
