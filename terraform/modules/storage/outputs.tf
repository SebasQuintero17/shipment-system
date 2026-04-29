# ============================================
# Salidas del modulo de Almacenamiento
# ============================================

output "ecr_repository_url" {
  description = "URL del repositorio ECR"
  value       = aws_ecr_repository.api.repository_url
}

output "ecr_repository_arn" {
  description = "ARN del repositorio ECR"
  value       = aws_ecr_repository.api.arn
}

output "rds_cluster_endpoint" {
  description = "Endpoint del cluster Aurora PostgreSQL"
  value       = aws_rds_cluster.aurora.endpoint
}

output "rds_cluster_reader_endpoint" {
  description = "Endpoint de lectura del cluster Aurora"
  value       = aws_rds_cluster.aurora.reader_endpoint
}

output "rds_cluster_id" {
  description = "ID del cluster Aurora"
  value       = aws_rds_cluster.aurora.id
}
