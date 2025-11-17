terraform {
  backend "gcs" {
    bucket = "INLOCUIESTE_CU_BUCKETUL_TAU"
    prefix = "terraform/state"
  }
}
