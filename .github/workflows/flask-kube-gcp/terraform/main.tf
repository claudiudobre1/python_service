provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_artifact_registry_repository" "repo" {
  location       = var.region
  repository_id  = var.repo_name
  description    = "Docker repo pentru aplicația Flask"
  format         = "DOCKER"
}

resource "google_container_cluster" "primary" {
  name               = var.cluster_name
  location           = var.zone
  remove_default_node_pool = true
  initial_node_count = 1
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "node-pool"
  cluster    = google_container_cluster.primary.name
  location   = var.zone
  node_count = 2

  node_config {
    machine_type = "e2-medium"
  }
}
