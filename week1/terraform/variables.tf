locals {
  data_lake_bucket = "zoomcamp_gcp_bucket"
}

variable "project" {
  description = "Enter your GCP project ID"
}

variable "region" {
    description = "Enter your project region"
    default = "me-west1"
}

variable "storage_class" {
  default = "STANDARD"
  description = "Enter storage_class for bucket"
}


variable "BQ_DATASET" {
  description = "Enter BQ id"
  type = string
  default = "zoomcamp_de_bq"
}
