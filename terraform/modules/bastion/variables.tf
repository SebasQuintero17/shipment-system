variable "vpc_id" {
  description = "ID de la VPC donde se desplegara el Bastion Host"
  type        = string
}

variable "subnet_id" {
  description = "ID de la subnet publica donde se ubicara el Bastion Host"
  type        = string
}

variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
}

variable "environment" {
  description = "Entorno (dev, prod, etc.)"
  type        = string
}

variable "bastion_security_group_id" {
  description = "ID del Security Group para el Bastion Host"
  type        = string
}
