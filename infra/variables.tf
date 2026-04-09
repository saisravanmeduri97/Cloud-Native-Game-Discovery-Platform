variable "project_id" {
  description = "Google Cloud project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud region"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "Primary zone for the GKE cluster"
  type        = string
  default     = "us-central1-a"
}

variable "cluster_name" {
  description = "Name of the GKE cluster"
  type        = string
  default     = "gdp-gke-cluster"
}

variable "network_name" {
  description = "VPC network name"
  type        = string
  default     = "gdp-vpc"
}

variable "subnet_name" {
  description = "Subnet name"
  type        = string
  default     = "gdp-subnet"
}

variable "subnet_cidr" {
  description = "Subnet CIDR range"
  type        = string
  default     = "10.10.0.0/20"
}

variable "pods_secondary_range_name" {
  description = "Secondary range name for pods"
  type        = string
  default     = "gdp-pods-range"
}

variable "pods_secondary_cidr" {
  description = "Secondary CIDR range for pods"
  type        = string
  default     = "10.20.0.0/16"
}

variable "services_secondary_range_name" {
  description = "Secondary range name for services"
  type        = string
  default     = "gdp-services-range"
}

variable "services_secondary_cidr" {
  description = "Secondary CIDR range for services"
  type        = string
  default     = "10.30.0.0/20"
}

variable "node_pool_name" {
  description = "Node pool name"
  type        = string
  default     = "primary-node-pool"
}

variable "node_count" {
  description = "Initial node count"
  type        = number
  default     = 2
}

variable "machine_type" {
  description = "GKE node machine type"
  type        = string
  default     = "e2-standard-2"
}

variable "disk_size_gb" {
  description = "Node disk size in GB"
  type        = number
  default     = 50
}

variable "disk_type" {
  description = "Node disk type"
  type        = string
  default     = "pd-standard"
}
