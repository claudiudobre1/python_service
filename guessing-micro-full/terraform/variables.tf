variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "Region for GCP resources"
  type        = string
  default     = "europe-central2"
}

variable "zone" {
  description = "Zone for GCP resources"
  type        = string
  default     = "europe-central2-a"
}

variable "cluster_name" {
  description = "Name of the GKE cluster"
  type        = string
  default     = "guessing-cluster"
}

variable "repo_name" {
  description = "Artifact Registry Docker repository name"
  type        = string
  default     = "my-repo"
}
