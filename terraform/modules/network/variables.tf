# ============================================
# Variables del modulo de Red
# ============================================

variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
}

variable "environment" {
  description = "Entorno de despliegue"
  type        = string
}

variable "aws_region" {
  description = "Region de AWS"
  type        = string
}

variable "container_port" {
  description = "Puerto del contenedor de la API"
  type        = number
  default     = 8000
}
