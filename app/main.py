from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, Base, SessionLocal
from . import schemas, crud

# ===============================
# Crear aplicación
# ===============================
app = FastAPI()

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# ===============================
# Dependency para base de datos
# ===============================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===============================
# Root
# ===============================
@app.get("/")
def root():
    return {"message": "Shipment System API running"}

# =====================================================
# ===================== PACKAGES ======================
# =====================================================

@app.post("/packages", response_model=schemas.Package)
def create_package(package: schemas.PackageCreate, db: Session = Depends(get_db)):
    return crud.create_package(db=db, package=package)

@app.get("/packages", response_model=list[schemas.Package])
def read_packages(db: Session = Depends(get_db)):
    return crud.get_packages(db)

@app.get("/packages/{package_id}", response_model=schemas.Package)
def read_package(package_id: int, db: Session = Depends(get_db)):
    db_package = crud.get_package(db, package_id)
    if db_package is None:
        raise HTTPException(status_code=404, detail="Package not found")
    return db_package

@app.put("/packages/{package_id}", response_model=schemas.Package)
def update_package(package_id: int, data: schemas.PackageUpdate, db: Session = Depends(get_db)):
    pkg = crud.update_package(db, package_id, data)
    if pkg is None:
        raise HTTPException(status_code=404, detail="Package not found")
    return pkg

@app.delete("/packages/{package_id}")
def delete_package(package_id: int, db: Session = Depends(get_db)):
    pkg = crud.delete_package(db, package_id)
    if pkg is None:
        raise HTTPException(status_code=404, detail="Package not found")
    return {"message": "Package deleted"}

# =====================================================
# ===================== VEHICLES ======================
# =====================================================

@app.post("/vehicles", response_model=schemas.Vehicle)
def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    return crud.create_vehicle(db=db, vehicle=vehicle)

@app.get("/vehicles", response_model=list[schemas.Vehicle])
def read_vehicles(db: Session = Depends(get_db)):
    return crud.get_vehicles(db)

@app.get("/vehicles/{vehicle_id}", response_model=schemas.Vehicle)
def read_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = crud.get_vehicle(db, vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

@app.put("/vehicles/{vehicle_id}", response_model=schemas.Vehicle)
def update_vehicle(vehicle_id: int, data: schemas.VehicleUpdate, db: Session = Depends(get_db)):
    veh = crud.update_vehicle(db, vehicle_id, data)
    if veh is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return veh

@app.delete("/vehicles/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    veh = crud.delete_vehicle(db, vehicle_id)
    if veh is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return {"message": "Vehicle deleted"}

# =====================================================
# ===================== SHIPMENTS =====================
# =====================================================

@app.post("/shipments", response_model=schemas.Shipment)
def create_shipment(shipment: schemas.ShipmentCreate, db: Session = Depends(get_db)):
    db_shipment = crud.create_shipment(db=db, shipment=shipment)
    if db_shipment is None:
        raise HTTPException(status_code=400, detail="Invalid package_id or vehicle_id")
    return db_shipment

@app.get("/shipments", response_model=list[schemas.Shipment])
def read_shipments(db: Session = Depends(get_db)):
    return crud.get_shipments(db)

@app.get("/shipments/{shipment_id}", response_model=schemas.Shipment)
def read_shipment(shipment_id: int, db: Session = Depends(get_db)):
    db_shipment = crud.get_shipment(db, shipment_id)
    if db_shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return db_shipment

@app.put("/shipments/{shipment_id}", response_model=schemas.Shipment)
def update_shipment(shipment_id: int, data: schemas.ShipmentUpdate, db: Session = Depends(get_db)):
    sh = crud.update_shipment(db, shipment_id, data)
    if sh is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    if sh == "invalid_package":
        raise HTTPException(status_code=400, detail="Invalid package_id")
    if sh == "invalid_vehicle":
        raise HTTPException(status_code=400, detail="Invalid vehicle_id")
    return sh

@app.delete("/shipments/{shipment_id}")
def delete_shipment(shipment_id: int, db: Session = Depends(get_db)):
    shipment = crud.delete_shipment(db, shipment_id)
    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return {"message": "Shipment deleted"}