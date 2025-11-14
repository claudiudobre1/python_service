output "cluster_name" {
  value = google_container_cluster.primary.name
}

output "cluster_endpoint" {
  value = google_container_cluster.primary.endpoint
}

output "artifact_repo" {
  value = google_artifact_registry_repository.repo.repository_id
}
