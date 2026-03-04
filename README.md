# 🚚 Shipment System

API RESTful para la gestión de envíos, paquetes y vehículos. Proyecto con integración continua, despliegue automatizado y cobertura de tests.

## 📦 Características

- CRUD de paquetes, vehículos y envíos
- Base de datos real (PostgreSQL en producción, SQLite en tests)
- Docker y docker-compose listos
- Pipelines CI/CD para pruebas y producción
- Cobertura mínima: 60% (pruebas), 85% (producción)

## 🚀 Deploy

- **Pruebas:** [URL de pruebas]
- **Producción:** [URL de producción]

## 🛠️ Instalación local

```bash
git clone https://github.com/SebasQuintero17/shipment-system.git
cd shipment-system
python -m venv venv
venv\Scripts\activate  # En Windows
pip install -r requirements.txt
```

## 🐳 Docker

```bash
docker compose up
```

## 🧪 Tests y cobertura

```bash
pytest --cov=app
```

## ⚙️ Pipelines CI/CD

- `.github/workflows/ci.yml`: Pruebas automáticas, cobertura ≥ 60%
- `.github/workflows/prod.yml`: Deploy a producción, cobertura ≥ 85%

## 🔑 Variables de entorno

- `DATABASE_URL` (opcional, para producción)
- Por defecto usa SQLite en tests

