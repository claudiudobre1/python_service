terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
  required_version = ">= 1.3.0"
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# Enable required APIs
resource "google_project_service" "container" {
  project = var.project_id
  service = "container.googleapis.com"
}

resource "google_project_service" "artifact" {
  project = var.project_id
  service = "artifactregistry.googleapis.com"
}

resource "google_project_service" "iam" {
  project = var.project_id
  service = "iam.googleapis.com"
}

# Artifact Registry (DOCKER repository)
resource "google_artifact_registry_repository" "repo" {
  depends_on = [
    google_project_service.artifact
  ]

  project       = var.project_id
  location      = var.region
  repository_id = var.repo_name
  description   = "Docker repo pentru aplicația Flask"
  format        = "DOCKER"
}

# GKE Cluster
resource "google_container_cluster" "primary" {
  depends_on = [
    google_project_service.container
  ]

  project  = var.project_id
  name     = var.cluster_name
  location = var.zone

  remove_default_node_pool = true
  initial_node_count       = 1
}

# Node pool
resource "google_container_node_pool" "primary_nodes" {
  depends_on = [
    google_container_cluster.primary
  ]

  cluster  = google_container_cluster.primary.name
  name     = "primary-node-pool"
  location = var.zone

  node_count = 2

  lifecycle {
    ignore_changes = [
      node_config[0].resource_labels,
      node_config[0].kubelet_config,
      node_config[0].labels,
      node_config[0].tags
    ]
  }

  node_config {
    machine_type = "e2-medium"

    oauth_scopes = [
      "https://www.googleapis.com/auth/devstorage.read_write",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]
  }
}
