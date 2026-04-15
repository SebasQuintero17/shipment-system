# Documentación del Despliegue en AWS (API de Envíos)

Esta documentación resume todos los avances realizados durante la sesión para migrar y desplegar el sistema de logística multicloud **Shipment System** en **AWS** usando Docker y ECS Fargate, conectándose a una base de datos Aurora PostgreSQL.

## 🚀 Lo que hicimos hoy

### 1. Corrección de Código y Preparación (FastAPI + SQLAlchemy)
*   Se corrigieron errores de sintaxis y duplicidades en código.
*   **`schemas.py`**: Se eliminó la duplicidad de la clase `PackageUpdate` y de las importaciones (`Optional`). Se agregó la configuración `orm_mode = True` (necesaria para mapear correctamente la BD con Pydantic v1.x/v2.x compatibilidad) a los esquemas principales.
*   **`main.py`**: Se limpiaron las importaciones duplicadas (`os`, `httpx`).
*   **`database.py`**: Se modificó la creación del motor (`create_engine`) añadiendo la directiva `connect_args={"sslmode": "require"}` para PostgreSQL, un requisito estricto de AWS Aurora RDS.

### 2. Infraestructura y Contenedores
*   **Docker & Amazon ECR (Elastic Container Registry)**:
    *   Se construyó localmente la imagen Docker (`shipment-api:latest`) de la aplicación FastAPI.
    *   Se autenticó Docker con AWS ECR usando las credenciales.
    *   Se etiquetó y publicó exitosamente la imagen en el repositorio ECR (`430695042838.dkr.ecr.us-east-2.amazonaws.com/shipment-api`).

### 3. Redes y Seguridad (AWS EC2 & RDS)
*   **Security Groups (Grupos de Seguridad)**:
    *   Creamos un Security Group dedicado para la API (`sg-0cc1c97e533cb4e70`).
    *   Modificamos el Security Group principal de Aurora (`sg-0da817f24824fc426`) añadiendo una regla Ingress para *permitir conexiones entrantes* por el puerto `5432` provenientes específicamente de los contenedores de la API.
    *   Abrimos el puerto `8000` en el grupo de seguridad de la API para permitir peticiones HTTP genéricas de salida a internet (0.0.0.0/0).
*   **Reseteo de Credenciales DB**:
    *   Aurora estaba bloqueando el acceso debido a problemas con el PAM/IAM Authentication. 
    *   Tuvimos que forzar un restablecimiento de contraseña de la DB (`Sebas3631`) desde la consola de comandos de AWS para asegurarnos que la conexión básica por contraseña fuese admitida.

### 4. Amazon ECS (Elastic Container Service) con Fargate
*   **Desestimación de App Runner**: Se intentó desplegar primero con App Runner + VPC Connector, pero la cuenta de AWS carecía de ciertas suscripciones habilitadas, así que pivoteamos hacia **ECS Fargate**.
*   **Clúster**: Creamos el clúster `shipment-cluster`.
*   **IAM Roles**: Se configuró y adjuntó el policy necesario a `ecsTaskExecutionRole` autorizando al contenedor a descargar imágenes de ECR e inyectar logs básicos hacia CloudWatch.
*   **Definición de Tareas (Task Definition)**:
    *   Generamos una capa de configuración indicando a Fargate que debe usar `0.25 vCPU` y `0.5 GB RAM`.
    *   Pasamos variables de entorno cruciales: `DATABASE_URL` y `PORT`.
    *   Se activó el registro de logs hacia **Amazon CloudWatch** (`/ecs/shipment-api`).
*   **Servicio ECS**: Se lanzó el servicio `shipment-api-service` dentro del clúster usando la Tarea predefinida y la configuración de red `awsvpc`.

---

## 🚧 ¿Qué falta por hacer? (Próximos Pasos)

A pesar de que toda la maquinaria ya existe y está vinculada, la aplicación actualmente se reinicia y aún no es accesible 100%. Esto es lo que falta corregir para finalizar el despliegue:

### 1. Resolver el problema de conexión residual en RDS Aurora
*   La API logró conectarse, y resolvió el problema del SSL (encriptación). Pero, todavía devuelve un error `PAM authentication failed` o rechazo en `pg_hba.conf`.
*   **¿Por qué pasa?** Aurora está intentando forzar inicio de sesión usando Identidad de IAM porque se configuró así al crearse la BD; o en su defecto, no reconoce la base de datos `postgres` (literal).
*   **Acción requerida:** Comprobar si debemos deshabilitar *"Autenticación de base de datos de IAM"* en el clúster RDS desde la consola de AWS, o bien asegurarnos de crear una BD inicial manual que no sea la de sistema y pasarla en el `DATABASE_URL`.

### 2. Estabilizar y correr el contenedor ECS
*   Una vez que el problema de RDS se arregla, Fargate logrará ejecutar el comando `Base.metadata.create_all(bind=engine)` de tu código en `main.py` de manera exitosa y el contenedor dejará de crashear (apagar y prender).
*   Obtendremos la **Dirección IP Pública** definitiva de parte de la tarea activa para consumo de la API.

### 3. Probar Endpoints Completos
*   Con la IP pública disponible, podremos probar los registros de *Shipment*, el CRUD normal y la orquestación a APIs Mocked.

### 4. ALERTA DE SEGURIDAD CRÍTICA ⚠️
*   A lo largo del día, en los logs o el chat **se mostraron Access Keys públicas (AKIA...) y Secret Keys** de la cuenta de AWS. 
*   **Debes ir a la Consola de IAM en AWS y desactivar/eliminar esas credenciales** inmediatamente y crear otras nuevas, de lo contrario tu cuenta corre un alto riesgo de sobrecostos por compromisos de seguridad.
