from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float)
    description = Column(String)
    status = Column(String)


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    plate = Column(String, unique=True)
    capacity = Column(Float)
    status = Column(String)


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    package_id = Column(Integer, ForeignKey("packages.id"))
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    origin = Column(String)
    destination = Column(String)
    status = Column(String)

    package = relationship("Package")
    vehicle = relationship("Vehicle")