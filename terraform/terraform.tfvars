# ============================================
# Valores de variables para el entorno dev
# NOTA: No subir este archivo a Git si contiene secretos
# ============================================

aws_region   = "us-east-2"
project_name = "shipment-system"
environment  = "dev"

db_username = "postgres"
db_name     = "postgres"

# La contrasena se pasa por variable de entorno o por CLI:
# terraform plan -var="db_password=TU_PASSWORD"

container_port  = 8000
partner_api_url = "https://cart-api-orders-88266388657.us-central1.run.app/api/v2/mensaje"
