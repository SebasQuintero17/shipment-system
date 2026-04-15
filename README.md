# 🚚 Shipment System

API RESTful para la gestión de envíos, paquetes y vehículos. Proyecto con integración continua, despliegue automatizado, cobertura de tests y **Arquitectura Multicloud**.

## 📦 Características

- CRUD completo de paquetes, vehículos y envíos.
- Base de datos real y separada (PostgreSQL en producción en GCP, SQLite en tests).
- Docker y docker-compose configurados nativamente.
- Pipelines CI/CD en GitHub Actions para pruebas y pases a producción.
- **Orquestación Multicloud**: Integración de servicios distribuidos en AWS y GCP enriqueciendo cargas útiles de JSON.

## 🌍 Arquitectura Multicloud y Flujo de Orquestación

Este ecosistema ha evolucionado a una estructura multicloud donde las APIs interactúan y enriquecen mensajes.

```mermaid
graph TD
    Client([💻 Cliente]) --> API[🚀 API Principal Shipment (GCP Cloud Run)]
    API --> DB[(📦 PostgreSQL Cloud SQL)]
    API -- Enruta Shipment + Vehicle --> AWS[☁️ API Santiago AWS EKS / API Gateway]
    API -- Enruta Shipment + Vehicle --> GCP[☁️ API Yecid GCP Cloud Run]
    
    classDef gcp fill:#E3F2FD,stroke:#1565C0,stroke-width:2px;
    classDef aws fill:#FFF3E0,stroke:#E65100,stroke-width:2px;
    
    class API,DB,GCP gcp;
    class AWS aws;
```

### ✅ Proceso de Enriquecimiento (Endpoint `/api/v2/process/{id}`)
Al llamar este endpoint, no solo se obtiene el recurso, sino que se fabrica un mensaje escalable:
1. `{"shipment": {...}}` (Extraído de BD).
2. Se une: `{"shipment": {...}, "vehicle": {...}}` (Agregación interna).
3. Se consume una API de un compañero en otra nube (AWS/GCP), y se adosa la data externa: 
`{"shipment": {...}, "vehicle": {...}, "tracking": {...}}`

## 🚀 Deploy

- **Pruebas:** "https://shipment-system-71zo.onrender.com" 
- **Producción (GCP):** *Pendiente de URL Cloud Run...*

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

## ⚙️ Pipelines CI/CD

- `.github/workflows/ci.yml`: Pruebas automáticas en develop (cobertura ≥ 65%) y main (cobertura ≥ 60%).
- `.github/workflows/prod.yml`: Deploy automatizado a GCP Cloud Run y Artifact Registry.

## 🔑 Variables de entorno principales

- `DATABASE_URL`: URI de la base de datos (PostgreSQL en Google Cloud).
- `PARTNER_API_URL`: (Opcional) URL destino en donde se procesa la orquestación (P. ej., API de Santiago en AWS).
