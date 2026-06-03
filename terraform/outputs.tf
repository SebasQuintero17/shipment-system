# ============================================
# Salidas globales del proyecto
# ============================================

output "ecr_repository_url" {
  description = "URL del repositorio ECR para la imagen Docker"
  value       = module.storage.ecr_repository_url
}

output "ecs_cluster_name" {
  description = "Nombre del cluster ECS"
  value       = module.compute.ecs_cluster_name
}

output "ecs_service_name" {
  description = "Nombre del servicio ECS"
  value       = module.compute.ecs_service_name
}

output "rds_endpoint" {
  description = "Endpoint del cluster Aurora PostgreSQL"
  value       = module.storage.rds_cluster_endpoint
}

output "vpc_id" {
  description = "ID de la VPC creada"
  value       = module.network.vpc_id
}

output "bastion_public_ip" {
  description = "IP publica del Bastion Host para conexion SSH"
  value       = module.bastion.bastion_public_ip
}
