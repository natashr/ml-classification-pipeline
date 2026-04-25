terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  # Connect to Docker Desktop
  host = "npipe:////./pipe/docker_engine"
}

# Variable for the Docker image
variable "docker_image" {
  description = "Docker image to deploy"
  type        = string
  default     = "your-username/ml-iris-classifier:latest"
}

variable "container_name" {
  description = "Name of the Docker container"
  type        = string
  default     = "ml-iris-classifier"
}

variable "container_port" {
  description = "Port to expose the container"
  type        = number
  default     = 5000
}

variable "host_port" {
  description = "Port on the host to map to container"
  type        = number
  default     = 5000
}

# Pull the latest Docker image
resource "docker_image" "ml_classifier" {
  name         = var.docker_image
  keep_locally = false
}

# Create and run the Docker container
resource "docker_container" "ml_classifier" {
  name  = var.container_name
  image = docker_image.ml_classifier.image_id
  
  ports {
    internal = var.container_port
    external = var.host_port
  }

  restart = "unless-stopped"

  # Environment variables
  env = [
    "PORT=${var.container_port}"
  ]

  # Health check
  healthcheck {
    test     = ["CMD", "curl", "-f", "http://localhost:${var.container_port}/health"]
    interval = "30s"
    timeout  = "10s"
    retries  = 3
  }
}

# Output the container details
output "container_id" {
  description = "The ID of the created container"
  value       = docker_container.ml_classifier.id
}

output "container_name" {
  description = "The name of the created container"
  value       = docker_container.ml_classifier.name
}

output "container_ip" {
  description = "The IP address of the container"
  value       = docker_container.ml_classifier.ip_address
}

output "service_url" {
  description = "URL to access the ML service"
  value       = "http://localhost:${var.host_port}"
}
