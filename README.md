# 🚚 Shipment System

API RESTful para la gestión de envíos, paquetes y vehículos. Proyecto con integración continua, despliegue automatizado y cobertura de tests.

## 📦 Características

- CRUD de paquetes, vehículos y envíos
- Base de datos real (PostgreSQL en producción, SQLite en tests)
- Docker y docker-compose listos
- Pipelines CI/CD para pruebas y producción
- Cobertura mínima: 60% (pruebas), 85% (producción)

## 🚀 Deploy

- **Pruebas:** "https://shipment-system-71zo.onrender.com" 
- **Producción:** "https://shipment-system-prod.onrender.com"

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


## 🚦 Flujo de ramas y despliegue

- **develop**: Rama de pruebas. Todo el desarrollo y pruebas se hacen aquí. El pipeline exige cobertura mínima de 65%.
- **main**: Rama de producción. Solo se actualiza mediante Pull Request desde develop, cuando develop pasa el coverage requerido.
- Cuando develop supera el coverage, se debe crear un Pull Request manual a main. Solo se permite mergear si el pipeline pasa correctamente.

## ⚙️ Pipelines CI/CD

- `.github/workflows/ci.yml`: Pruebas automáticas en develop (cobertura ≥ 65%) y main (cobertura ≥ 60%).
- `.github/workflows/prod.yml`: Deploy a producción, cobertura ≥ 85%.

## 🔑 Variables de entorno

- `DATABASE_URL` (opcional, para producción)
- Por defecto usa SQLite en tests

