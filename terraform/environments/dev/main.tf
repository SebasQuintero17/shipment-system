# ============================================
# Entorno de Desarrollo (Dev)
# ============================================

module "dev" {
  source = "../../"

  aws_region   = "us-east-2"
  project_name = "shipment-system"
  environment  = "dev"

  db_username = "postgres"
  db_password = var.db_password
  db_name     = "postgres"

  container_port  = 8000
  partner_api_url = "https://cart-api-orders-88266388657.us-central1.run.app/api/v2/mensaje"
}

variable "db_password" {
  description = "Contrasena de la base de datos Aurora PostgreSQL"
  type        = string
  sensitive   = true
}

# --- Salidas del entorno dev ---
output "ecr_repository_url" {
  value = module.dev.ecr_repository_url
}

output "ecs_cluster_name" {
  value = module.dev.ecs_cluster_name
}

output "rds_endpoint" {
  value = module.dev.rds_endpoint
}
