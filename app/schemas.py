from pydantic import BaseModel
from typing import Optional

class PackageBase(BaseModel):
	weight: float
	description: str
	status: str

class PackageCreate(PackageBase):
	pass



class Package(PackageBase):
	id: int

	class Config:
		orm_mode = True

class PackageUpdate(BaseModel):
	weight: float | None = None
	description: str | None = None
	status: str | None = None

	class Config:
		orm_mode = True

class VehicleBase(BaseModel):
	plate: str
	capacity: float
	status: str

class VehicleCreate(VehicleBase):
	pass

class VehicleUpdate(BaseModel):
	plate: str | None = None
	capacity: float | None = None
	status: str | None = None

class Vehicle(VehicleBase):
	id: int

	class Config:
		orm_mode = True

class ShipmentBase(BaseModel):
	package_id: int
	vehicle_id: int
	origin: str
	destination: str
	status: str

class ShipmentCreate(ShipmentBase):
	pass

class ShipmentUpdate(BaseModel):
	package_id: int | None = None
	vehicle_id: int | None = None
	origin: str | None = None
	destination: str | None = None
	status: str | None = None

class Shipment(ShipmentBase):
	id: int
	package: Optional[Package]
	vehicle: Optional[Vehicle]

	class Config:
		orm_mode = True
