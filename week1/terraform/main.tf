terraform {
  required_version = ">= 1.0"
  backend "local" {}

}

provider "google" {
    project = var.project
    region = var.region
}

resource "google_storage_bucket" "data-lake-bucket" {
  
  name = "${local.data_lake_bucket}_miko_${var.project}"
  location = var.region
  storage_class = var.storage_class
  uniform_bucket_level_access = true
  force_destroy =  true

}

resource "google_bigquery_dataset" "dataset" {
    dataset_id = var.BQ_DATASET
    project = var.project
    location = var.region
  
}