from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from decouple import config

GCP_STORAGE = config("GCP_STORAGE")


@task()
def load_dataset_from_link(link: str)-> pd.DataFrame:
    """
    Task to load dataset from link.
    Returns dataset as pandas.DataFrame
    """
    df = pd.read_csv(link)
    return df

@task(log_prints=True)
def clean(dataframe: pd.DataFrame)-> pd.DataFrame:
    """
    Transforms dataframe correcting fields types.
    """
    #NOTE 
    #tpep_* for - yellow taxi datasets
    #lpep_* for - green taxi datasets
    dataframe["tpep_pickup_datetime"] = pd.to_datetime(dataframe["tpep_pickup_datetime"])
    dataframe["tpep_dropoff_datetime"] = pd.to_datetime(dataframe["tpep_dropoff_datetime"])
    print(f"rows: {len(dataframe)}")
    return dataframe

    
@task()
def store_on_local(dataframe: pd.DataFrame, color: str, dataset_filename: str)-> Path:
    """
    Stores given dataframe on local FileSystem.
    """
    store_path = Path(
        f"data/{color}/{dataset_filename}.parquet"
    )
    #dataframe.to_parquet(store_path, compression="gzip")
    return store_path

@task()
def store_on_cloud(path: Path)-> None:
    """
    Stores given dataframe on cloud Bucket.
    """
    bucket = GcsBucket.load(GCP_STORAGE)
    bucket.upload_from_path(
        from_path=path,
        to_path=path
    )


@flow()
def etl_web_to_gcp(
    color: str,
    year: int,
    month: int
)-> None:
    """
    Flow to load dataset to GCP storage
    """
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_link = (
        f"https://github.com/DataTalksClub/nyc-tlc-data/r"
        f"eleases/download/{color}/{dataset_file}.csv.gz"
    )
    df = load_dataset_from_link(dataset_link)
    df = clean(df)
    path = store_on_local(df, color, dataset_file)
    store_on_cloud(path)


@flow()
def main_flow_web_to_gcp(
    color: str,
    year: int,
    months: list[int]
):
    """
    Main flow that starts subflows `etl_web_to_gcp`
    """
    for month in months:
        etl_web_to_gcp(color, year, month)

if __name__ == "__main__":
    main_flow_web_to_gcp("yellow", 2019, [2])
