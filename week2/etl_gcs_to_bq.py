
from prefect import flow, task
from pathlib import Path
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
import pandas as pd

from decouple import config

GCP_STORAGE = config("GCP_STORAGE")
GCP_CREDENTIALS = config("GCP_CREDENTIALS")
TABLE_NAME = config("TABLE_NAME")
PROJECT_ID = config("PROJECT_ID")

def generate_path(
    color: str,
    year: int,
    month: int
)-> Path:
    """
    Generate path to .parquet file inside main `data` dir.
    """
    return f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"

def get_dataframe_length(dataframe: pd.DataFrame)-> int:
    """
    Return length of dataframe
    """
    return len(dataframe)

@task()
def extract_from_gcs(
    color: str, 
    year: int,
    month: int
) -> Path:
    """
    Flow extracts dataset from GCS
    """
    dataset_path = generate_path(color, year, month)
    gcs_bucket = GcsBucket.load(GCP_STORAGE)
    gcs_bucket.get_directory(from_path=dataset_path, local_path=".")
    return dataset_path


@task(log_prints=True)
def get_dataframe(path: Path)-> pd.DataFrame:
    dataframe = pd.read_parquet(path)
    return dataframe

@task()
def write_to_bq(dataframe: pd.DataFrame)-> None:
    """
    Writes to BigQuery
    """
    gcp_credentials_block = GcpCredentials.load(GCP_CREDENTIALS)

    dataframe.to_gbq(
        destination_table=TABLE_NAME,
        project_id=PROJECT_ID,
        chunksize=100_000,
        if_exists="append",
        credentials=gcp_credentials_block.get_credentials_from_service_account()
    )

@flow(log_prints=True)
def etl_gcs_to_bq(
    color: str, 
    year: int,
    month: int
)-> int:
    """
    Flow to load dataset from GCP storage to BigQuery.
    Returns row size of dataset
    """

    path = extract_from_gcs(color, year, month)
    dataframe = get_dataframe(path)
    write_to_bq(dataframe)
    length = get_dataframe_length(dataframe)
    return length


@flow(log_prints=True)
def main_flow(
    color: str,
    year: int,
    months: list[int]
):
    """
    Main flow that starts subflows `etl_gcs_to_bq`
    """
    total_row = 0
    for month in months:
        length = etl_gcs_to_bq(
            color,
            year,
            month
        )
        total_row += length
    print(f"{total_row} rows are processed!")

if __name__ == "__main__":
    main_flow(
        "green",
        2020,
        [2, 3]
    )