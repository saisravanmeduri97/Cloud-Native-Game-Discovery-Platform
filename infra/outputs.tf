output "cluster_name" {
  value = google_container_cluster.primary.name
}

output "cluster_location" {
  value = google_container_cluster.primary.location
}

output "cluster_endpoint" {
  value = google_container_cluster.primary.endpoint
}

output "network_name" {
  value = google_compute_network.vpc.name
}

output "subnetwork_name" {
  value = google_compute_subnetwork.subnet.name
}

output "node_service_account_email" {
  value = google_service_account.gke_nodes.email
}
