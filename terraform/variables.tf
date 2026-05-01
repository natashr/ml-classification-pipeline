variable "docker_image" {
  description = "Docker image to deploy"
  type        = string
  
  validation {
    condition     = can(regex("^[a-z0-9]+/[a-z0-9-]+:.+$", var.docker_image))
    error_message = "The docker_image must be in format 'username/image:tag'."
  }
}

variable "container_name" {
  description = "Name of the Docker container"
  type        = string
  default     = "ml-iris-classifier"
  
  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.container_name))
    error_message = "The container_name must contain only lowercase letters, numbers, and hyphens."
  }
}

variable "container_port" {
  description = "Port to expose the container"
  type        = number
  default     = 5001
  
  validation {
    condition     = var.container_port >= 1 && var.container_port <= 65535
    error_message = "The container_port must be between 1 and 65535."
  }
}

variable "host_port" {
  description = "Port on the host to map to container"
  type        = number
  default     = 5001
  
  validation {
    condition     = var.host_port >= 1 && var.host_port <= 65535
    error_message = "The host_port must be between 1 and 65535."
  }
}
