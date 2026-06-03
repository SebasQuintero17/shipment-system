# ============================================
# Salidas del modulo de Red
# ============================================

output "vpc_id" {
  description = "ID de la VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs de las subnets publicas"
  value       = [aws_subnet.public_a.id, aws_subnet.public_b.id]
}

output "api_security_group_id" {
  description = "ID del security group de la API"
  value       = aws_security_group.api.id
}

output "rds_security_group_id" {
  description = "ID del security group de RDS"
  value       = aws_security_group.rds.id
}

output "bastion_security_group_id" {
  description = "ID del security group del Bastion"
  value       = aws_security_group.bastion.id
}
