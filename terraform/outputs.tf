output "container_id" {
  description = "The ID of the created container"
  value       = docker_container.ml_classifier.id
}

output "container_name" {
  description = "The name of the created container"
  value       = docker_container.ml_classifier.name
}


output "service_url" {
  description = "URL to access the ML service"
  value       = "http://localhost:${var.host_port}"
}

output "health_check_url" {
  description = "URL for health check endpoint"
  value       = "http://localhost:${var.host_port}/health"
}

output "api_info_url" {
  description = "URL for API info endpoint"
  value       = "http://localhost:${var.host_port}/info"
}
