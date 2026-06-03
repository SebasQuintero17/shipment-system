#!/bin/bash
# ============================================
# Script para eliminar toda la infraestructura
# ============================================

echo "Iniciando la destruccion de la infraestructura..."
cd "$(dirname "$0")"

# Ejecuta terraform destroy
terraform destroy -auto-approve

echo "Destruccion completada. AWS ya no facturara por estos recursos."
