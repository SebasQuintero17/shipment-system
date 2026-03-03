from sqlalchemy.orm import Session
from . import models, schemas


# =========================
# PACKAGES
# =========================

def create_package(db: Session, package: schemas.PackageCreate):
    db_package = models.Package(
        weight=package.weight,
        description=package.description,
        status=package.status
    )
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    return db_package


def get_packages(db: Session):
    return db.query(models.Package).all()


def get_package(db: Session, package_id: int):
    return db.query(models.Package).filter(models.Package.id == package_id).first()


def update_package(db: Session, package_id: int, data: schemas.PackageUpdate):
    pkg = get_package(db, package_id)
    if not pkg:
        return None

    if data.weight is not None:
        pkg.weight = data.weight
    if data.description is not None:
        pkg.description = data.description
    if data.status is not None:
        pkg.status = data.status

    db.commit()
    db.refresh(pkg)
    return pkg


def delete_package(db: Session, package_id: int):
    pkg = get_package(db, package_id)
    if not pkg:
        return None

    db.delete(pkg)
    db.commit()
    return pkg


# =========================
# VEHICLES
# =========================

def create_vehicle(db: Session, vehicle: schemas.VehicleCreate):
    db_vehicle = models.Vehicle(
        plate=vehicle.plate,
        capacity=vehicle.capacity,
        status=vehicle.status
    )
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


def get_vehicles(db: Session):
    return db.query(models.Vehicle).all()


def get_vehicle(db: Session, vehicle_id: int):
    return db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()


def update_vehicle(db: Session, vehicle_id: int, data: schemas.VehicleUpdate):
    veh = get_vehicle(db, vehicle_id)
    if not veh:
        return None

    if data.plate is not None:
        veh.plate = data.plate
    if data.capacity is not None:
        veh.capacity = data.capacity
    if data.status is not None:
        veh.status = data.status

    db.commit()
    db.refresh(veh)
    return veh


def delete_vehicle(db: Session, vehicle_id: int):
    veh = get_vehicle(db, vehicle_id)
    if not veh:
        return None

    db.delete(veh)
    db.commit()
    return veh


# =========================
# SHIPMENTS
# =========================

def create_shipment(db: Session, shipment: schemas.ShipmentCreate):

    package = get_package(db, shipment.package_id)
    if not package:
        return None

    vehicle = get_vehicle(db, shipment.vehicle_id)
    if not vehicle:
        return None

    db_shipment = models.Shipment(
        package_id=shipment.package_id,
        vehicle_id=shipment.vehicle_id,
        origin=shipment.origin,
        destination=shipment.destination,
        status=shipment.status
    )

    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment


def get_shipments(db: Session):
    return db.query(models.Shipment).all()


def get_shipment(db: Session, shipment_id: int):
    return db.query(models.Shipment).filter(models.Shipment.id == shipment_id).first()


def update_shipment(db: Session, shipment_id: int, data: schemas.ShipmentUpdate):
    sh = get_shipment(db, shipment_id)
    if not sh:
        return None

    if data.package_id is not None:
        pkg = get_package(db, data.package_id)
        if not pkg:
            return "invalid_package"
        sh.package_id = data.package_id

    if data.vehicle_id is not None:
        veh = get_vehicle(db, data.vehicle_id)
        if not veh:
            return "invalid_vehicle"
        sh.vehicle_id = data.vehicle_id

    if data.origin is not None:
        sh.origin = data.origin
    if data.destination is not None:
        sh.destination = data.destination
    if data.status is not None:
        sh.status = data.status

    db.commit()
    db.refresh(sh)
    return sh


def delete_shipment(db: Session, shipment_id: int):
    sh = get_shipment(db, shipment_id)
    if not sh:
        return None

    db.delete(sh)
    db.commit()
    return sh