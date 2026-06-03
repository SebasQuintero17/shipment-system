from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import Any
from fastapi import Body
from .database import engine, Base, SessionLocal
from . import schemas, crud
import os
import httpx
from fastapi import APIRouter
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Shipment System API", version="3.0.0-canary")

Instrumentator().instrument(app).expose(app)

router_v2 = APIRouter(prefix="/api/v2")
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Shipment System API running", "version": "3.0.0-canary"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": "3.0.0-canary",
        "deployment": "canary",
        "deploy_date": str(date.today()),
        "features": ["canary-routing", "enhanced-tracking", "multi-region"]
    }

@router_v2.post("/packages", response_model=schemas.Package)
def create_package(package: schemas.PackageCreate, db: Session = Depends(get_db)):
    return crud.create_package(db=db, package=package)

@router_v2.get("/packages", response_model=list[schemas.Package])
def read_packages(db: Session = Depends(get_db)):
    return crud.get_packages(db)

@router_v2.get("/packages/{package_id}", response_model=schemas.Package)
def read_package(package_id: int, db: Session = Depends(get_db)):
    db_package = crud.get_package(db, package_id)
    if db_package is None:
        raise HTTPException(status_code=404, detail="Package not found")
    return db_package

@router_v2.put("/packages/{package_id}", response_model=schemas.Package)
def update_package(package_id: int, data: schemas.PackageUpdate, db: Session = Depends(get_db)):
    pkg = crud.update_package(db, package_id, data)
    if pkg is None:
        raise HTTPException(status_code=404, detail="Package not found")
    return pkg

@router_v2.delete("/packages/{package_id}")
def delete_package(package_id: int, db: Session = Depends(get_db)):
    pkg = crud.delete_package(db, package_id)
    if pkg is None:
        raise HTTPException(status_code=404, detail="Package not found")
    return {"message": "Package deleted"}

@router_v2.post("/vehicles", response_model=schemas.Vehicle)
def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    return crud.create_vehicle(db=db, vehicle=vehicle)

@router_v2.get("/vehicles", response_model=list[schemas.Vehicle])
def read_vehicles(db: Session = Depends(get_db)):
    return crud.get_vehicles(db)

@router_v2.get("/vehicles/{vehicle_id}", response_model=schemas.Vehicle)
def read_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = crud.get_vehicle(db, vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

@router_v2.put("/vehicles/{vehicle_id}", response_model=schemas.Vehicle)
def update_vehicle(vehicle_id: int, data: schemas.VehicleUpdate, db: Session = Depends(get_db)):
    veh = crud.update_vehicle(db, vehicle_id, data)
    if veh is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return veh

@router_v2.delete("/vehicles/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    veh = crud.delete_vehicle(db, vehicle_id)
    if veh is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return {"message": "Vehicle deleted"}

@router_v2.post("/shipments", response_model=schemas.Shipment)
def create_shipment(shipment: schemas.ShipmentCreate, db: Session = Depends(get_db)):
    db_shipment = crud.create_shipment(db=db, shipment=shipment)
    if db_shipment is None:
        raise HTTPException(status_code=400, detail="Invalid package_id or vehicle_id")
    return db_shipment

@router_v2.get("/shipments", response_model=list[schemas.Shipment])
def read_shipments(db: Session = Depends(get_db)):
    return crud.get_shipments(db)

@router_v2.get("/shipments/{shipment_id}", response_model=schemas.Shipment)
def read_shipment(shipment_id: int, db: Session = Depends(get_db)):
    db_shipment = crud.get_shipment(db, shipment_id)
    if db_shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return db_shipment

@router_v2.put("/shipments/{shipment_id}", response_model=schemas.Shipment)
def update_shipment(shipment_id: int, data: schemas.ShipmentUpdate, db: Session = Depends(get_db)):
    sh = crud.update_shipment(db, shipment_id, data)
    if sh is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    if sh == "invalid_package":
        raise HTTPException(status_code=400, detail="Invalid package_id")
    if sh == "invalid_vehicle":
        raise HTTPException(status_code=400, detail="Invalid vehicle_id")
    return sh

@router_v2.delete("/shipments/{shipment_id}")
def delete_shipment(shipment_id: int, db: Session = Depends(get_db)):
    shipment = crud.delete_shipment(db, shipment_id)
    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return {"message": "Shipment deleted"}

@router_v2.get("/process/{shipment_id}")
async def process_shipment(shipment_id: int, db: Session = Depends(get_db)):
    db_shipment = crud.get_shipment(db, shipment_id)
    if db_shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")

    enriched_data = {
        "shipment": {
            "id": db_shipment.id,
            "origin": db_shipment.origin,
            "destination": db_shipment.destination,
            "status": db_shipment.status
        },
        "package": {
            "id": db_shipment.package_id,
            "weight": db_shipment.package.weight,
            "description": db_shipment.package.description
        },
        "vehicle": {
            "id": db_shipment.vehicle_id,
            "plate": db_shipment.vehicle.plate,
            "capacity": db_shipment.vehicle.capacity
        },
        "canary_info": {
            "version": "3.0.0-canary",
            "enhanced_tracking": True
        }
    }

    partner_api_url = os.getenv("PARTNER_API_URL", "https://mock-api.com/tracking")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(partner_api_url, json=enriched_data, timeout=2.0)
            if response.status_code == 200:
                tracking_info = response.json()
            else:
                tracking_info = {"status": "external_error", "message": "API partner retornó error."}
    except Exception:
        tracking_info = {
            "status": "mocked",
            "location": "Central Hub",
            "note": "Aviso: API externa no disponible, datos simulados."
        }

    enriched_data["tracking"] = tracking_info
    return enriched_data

@router_v2.post("/mensaje")
async def recibir_mensaje(req: Any = Body(...), db: Session = Depends(get_db)):
    from . import models
    vehiculo = db.query(models.Vehicle).filter(models.Vehicle.status == "available").first()
    if vehiculo is None:
        vehiculo = db.query(models.Vehicle).first()
    vehiculo_dict = {
        "id": vehiculo.id,
        "plate": vehiculo.plate,
        "capacity": vehiculo.capacity,
        "status": vehiculo.status
    } if vehiculo else None

    crud.create_mensaje(db=db, elementos=req if isinstance(req, list) else [req], vehiculo_dict=vehiculo_dict or {})

    return {
        "mensaje": "Concatenación exitosa",
        "elementos": req,
        "vehiculo": vehiculo_dict
    }

@router_v2.get("/mensajes")
def ver_mensajes(db: Session = Depends(get_db)):
    return crud.get_mensajes(db)

@router_v2.post("/fetch-yecid")
async def fetch_yecid(db: Session = Depends(get_db)):
    from . import models
    yecid_url = "https://cart-api-orders-88266388657.us-central1.run.app/api/v2/mensaje"
    async with httpx.AsyncClient() as client:
        response = await client.get(yecid_url, timeout=10.0)
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="No se pudo obtener el mensaje de Yecid")
        data = response.json()

    vehiculo = db.query(models.Vehicle).filter(models.Vehicle.status == "available").first()
    if vehiculo is None:
        vehiculo = db.query(models.Vehicle).first()
    vehiculo_dict = {
        "id": vehiculo.id,
        "plate": vehiculo.plate,
        "capacity": vehiculo.capacity,
        "status": vehiculo.status
    } if vehiculo else None

    crud.create_mensaje(db=db, elementos=[data], vehiculo_dict=vehiculo_dict or {})

    return {
        "mensaje": "Mensaje de Yecid guardado exitosamente",
        "datos": data,
        "vehiculo": vehiculo_dict
    }

app.include_router(router_v2)