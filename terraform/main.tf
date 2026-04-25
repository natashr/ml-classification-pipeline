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

