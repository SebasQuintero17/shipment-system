# ============================================
# Variables del modulo de Computo
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

# --- Networking ---
variable "public_subnet_ids" {
  description = "IDs de las subnets publicas para ECS"
  type        = list(string)
}

variable "api_security_group_id" {
  description = "ID del security group de la API"
  type        = string
}

# --- Storage ---
variable "ecr_repository_url" {
  description = "URL del repositorio ECR"
  type        = string
}

# --- Base de datos ---
variable "rds_host" {
  description = "Hostname del cluster Aurora"
  type        = string
}

variable "rds_port" {
  description = "Puerto de la base de datos"
  type        = number
  default     = 5432
}

variable "rds_user" {
  description = "Usuario de la base de datos"
  type        = string
}

variable "rds_db" {
  description = "Nombre de la base de datos"
  type        = string
}

variable "rds_region" {
  description = "Region de RDS para IAM auth"
  type        = string
}

variable "use_iam_auth" {
  description = "Usar autenticacion IAM para RDS"
  type        = bool
  default     = true
}

# --- Aplicacion ---
variable "container_port" {
  description = "Puerto del contenedor"
  type        = number
  default     = 8000
}

variable "partner_api_url" {
  description = "URL de la API del partner"
  type        = string
}
