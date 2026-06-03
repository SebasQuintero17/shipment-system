output "bastion_public_ip" {
  description = "IP publica del Bastion Host para conectarse por SSH"
  value       = aws_instance.bastion.public_ip
}


