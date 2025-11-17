terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.80"
    }
  }
}

provider "google" {
  project = "INLOCUIESTE_CU_PROIECTUL_TAU"
  region  = "europe-central2"
  zone    = "europe-central2-a"
}
