# Despliegue de Infraestructura con Terraform

Este directorio contiene el codigo de Infraestructura como Codigo (IaC) modular para desplegar el Shipment System en AWS.
Cumple con el despliegue de 4 servicios: VPC (Red), ECS Fargate (Computo), Aurora PostgreSQL (Base de datos), y EC2 Bastion Host (Acceso SSH).

## Requisitos
- Terraform instalado
- AWS CLI configurado

## 1. Despliegue
Para desplegar la infraestructura completa, ejecuta:
```bash
cd terraform
terraform init
terraform apply -auto-approve -var="db_password=TuPasswordSeguro123"
```
Al finalizar, Terraform mostrara en pantalla:
- `bastion_public_ip`: La IP para conectarte por SSH.
- `rds_endpoint`: El endpoint de la base de datos.
- `ecs_service_name`: El nombre del servicio de la API.

## 2. Conectarse a la Base de Datos vía SSH
AWS Aurora es un servicio administrado, por lo que el acceso seguro se realiza mediante un Servidor de Salto (Bastion Host) en EC2.

1. Al aplicar Terraform, se genero automaticamente un archivo de clave privada llamado `shipment-system-bastion.pem`.
2. Sube la carpeta `scripts_db` al Bastion Host:
```bash
scp -i shipment-system-bastion.pem -r ../scripts_db ec2-user@<BASTION_PUBLIC_IP>:~/
```
3. Conectate por SSH al Bastion:
```bash
ssh -i shipment-system-bastion.pem ec2-user@<BASTION_PUBLIC_IP>
```
4. Corre los scripts de la base de datos:
```bash
cd scripts_db
chmod +x run_scripts.sh
./run_scripts.sh <RDS_ENDPOINT> postgres TuPasswordSeguro123
```

## 3. Eliminacion de la Infraestructura
Para no incurrir en costos adicionales despues de la sustentacion, usa el script de destruccion:
```bash
./destroy.sh
```
O manualmente:
```bash
terraform destroy -auto-approve -var="db_password=TuPasswordSeguro123"
```
