# ============================================
# Variables globales del proyecto
# ============================================

variable "aws_region" {
  description = "Region de AWS donde se despliegan los recursos"
  type        = string
  default     = "us-east-2"
}

variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
  default     = "shipment-system"
}

variable "environment" {
  description = "Entorno de despliegue (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "db_username" {
  description = "Usuario de la base de datos Aurora PostgreSQL"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "Contrasena de la base de datos Aurora PostgreSQL"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "Nombre de la base de datos"
  type        = string
  default     = "postgres"
}

variable "container_port" {
  description = "Puerto del contenedor de la API"
  type        = number
  default     = 8000
}

variable "partner_api_url" {
  description = "URL de la API del partner para orquestacion multicloud"
  type        = string
  default     = "https://cart-api-orders-88266388657.us-central1.run.app/api/v2/mensaje"
}
