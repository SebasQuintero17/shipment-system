#!/bin/bash
# ============================================
# Script para conectarse a Aurora y ejecutar los SQL
# Uso: ./run_scripts.sh <RDS_ENDPOINT> <DB_USER> <DB_PASSWORD>
# ============================================

ENDPOINT=$1
USER=$2
export PGPASSWORD=$3

echo "Conectando a RDS: $ENDPOINT"

echo "----------------------------------------"
echo "1. Ejecutando creacion de tablas..."
psql -h $ENDPOINT -U $USER -d postgres -f 1_create.sql

echo "----------------------------------------"
echo "2. Insertando datos y visualizando..."
psql -h $ENDPOINT -U $USER -d postgres -f 2_insert_view.sql

echo "----------------------------------------"
echo "3. Eliminando la base de datos (tablas)..."
psql -h $ENDPOINT -U $USER -d postgres -f 3_drop.sql

echo "----------------------------------------"
echo "Ejecucion finalizada."
