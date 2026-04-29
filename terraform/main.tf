# ============================================
# Configuracion principal - llama a los modulos
# ============================================

# --- Modulo de Red (VPC, Subnets, Security Groups) ---
module "network" {
  source = "./modules/network"

  project_name   = var.project_name
  environment    = var.environment
  aws_region     = var.aws_region
  container_port = var.container_port
}

# --- Modulo de Almacenamiento (ECR, RDS Aurora) ---
module "storage" {
  source = "./modules/storage"

  project_name = var.project_name
  environment  = var.environment
  aws_region   = var.aws_region

  # Networking
  vpc_id                = module.network.vpc_id
  private_subnet_ids    = module.network.public_subnet_ids
  rds_security_group_id = module.network.rds_security_group_id

  # Base de datos
  db_username = var.db_username
  db_password = var.db_password
  db_name     = var.db_name
}

# --- Modulo de Computo (ECS Fargate) ---
module "compute" {
  source = "./modules/compute"

  project_name = var.project_name
  environment  = var.environment
  aws_region   = var.aws_region

  # Networking
  public_subnet_ids     = module.network.public_subnet_ids
  api_security_group_id = module.network.api_security_group_id

  # Storage
  ecr_repository_url = module.storage.ecr_repository_url

  # Base de datos
  rds_host     = module.storage.rds_cluster_endpoint
  rds_port     = 5432
  rds_user     = var.db_username
  rds_db       = var.db_name
  rds_region   = var.aws_region
  use_iam_auth = true

  # Aplicacion
  container_port  = var.container_port
  partner_api_url = var.partner_api_url
}
