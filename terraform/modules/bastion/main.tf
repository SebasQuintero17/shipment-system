# ============================================
# Modulo de Bastion Host (Servicio 4)
# ============================================


# Obtener la ultima AMI de Amazon Linux 2023
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

# Crear una llave SSH (par de claves) en AWS para acceder al Bastion
resource "tls_private_key" "bastion_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "bastion_key_pair" {
  key_name   = "${var.project_name}-bastion-key"
  public_key = tls_private_key.bastion_key.public_key_openssh
}

# Guardar la llave privada localmente para que el usuario pueda usarla
resource "local_file" "private_key" {
  content         = tls_private_key.bastion_key.private_key_pem
  filename        = "${path.root}/${var.project_name}-bastion.pem"
  file_permission = "0400"
}

# Instancia EC2 (Bastion Host)
resource "aws_instance" "bastion" {
  ami                         = data.aws_ami.amazon_linux.id
  instance_type               = "t2.micro" # Capa gratuita
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [var.bastion_security_group_id]
  key_name                    = aws_key_pair.bastion_key_pair.key_name
  associate_public_ip_address = true

  # Script para instalar el cliente de PostgreSQL
  user_data = <<-EOF
              #!/bin/bash
              dnf update -y
              dnf install -y postgresql15
              EOF

  tags = {
    Name        = "${var.project_name}-bastion-host"
    Environment = var.environment
  }
}
