import pytest
import random 
from app.database import Base, engine

@pytest.fixture(scope="session", autouse=True)
def clean_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# =========================
# PACKAGES
# =========================

def test_create_package():
    response = client.post("/packages", json={
        "weight": 10,
        "description": "Test package",
        "status": "pending"
    })
    assert response.status_code == 200
    assert response.json()["weight"] == 10


def test_get_packages():
    response = client.get("/packages")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_package_by_id():
    response = client.get("/packages/1")
    assert response.status_code in [200, 404]


def test_update_package():
    response = client.put("/packages/1", json={
        "weight": 20,
        "description": "Updated",
        "status": "shipped"
    })
    assert response.status_code in [200, 404]


def test_delete_package():
    response = client.delete("/packages/1")
    assert response.status_code in [200, 404]


# =========================
# VEHICLES
# =========================
def test_create_vehicle():
    response = client.post("/vehicles", json={
        "plate": "ABC123" + str(random.randint(1, 9999)),
        "capacity": 100,
        "status": "available"
    })
    assert response.status_code == 200

def test_get_vehicles():
    response = client.get("/vehicles")
    assert response.status_code == 200


def test_get_vehicle_by_id():
    response = client.get("/vehicles/1")
    assert response.status_code in [200, 404]


def test_update_vehicle():
    response = client.put("/vehicles/1", json={
        "plate": "XYZ789",
        "capacity": 200
    })
    assert response.status_code in [200, 404]


def test_delete_vehicle():
    response = client.delete("/vehicles/1")
    assert response.status_code in [200, 404]


# =========================
# SHIPMENTS
# =========================
def test_create_shipment():
    response = client.post("/shipments", json={
        "package_id": 1,
        "vehicle_id": 1,
        "origin": "Bogota",
        "destination": "Medellin",
        "status": "in_transit"
    })
    assert response.status_code in [200, 400]

def test_get_shipments():
    response = client.get("/shipments")
    assert response.status_code == 200


def test_get_shipment_by_id():
    response = client.get("/shipments/1")
    assert response.status_code in [200, 404]


def test_update_shipment():
    response = client.put("/shipments/1", json={
        "package_id": 1,
        "vehicle_id": 1,
        "destination": "Bogota"
    })
    assert response.status_code in [200, 404]


def test_delete_shipment():
    response = client.delete("/shipments/1")
    assert response.status_code in [200, 404]
    
def test_invalid_shipment_package():
    response = client.post("/shipments", json={
        "package_id": 9999,
        "vehicle_id": 1,
        "origin": "Bogota",
        "destination": "Cali",
        "status": "in_transit"
    })
    assert response.status_code == 400


def test_invalid_shipment_vehicle():
    response = client.post("/shipments", json={
        "package_id": 1,
        "vehicle_id": 9999,
        "origin": "Bogota",
        "destination": "Cali",
        "status": "in_transit"
    })
    assert response.status_code == 400


def test_update_nonexistent_package():
    response = client.put("/packages/9999", json={
        "weight": 10
    })
    assert response.status_code == 404
def test_full_vehicle_flow():
    # crear vehículo real
    response = client.post("/vehicles", json={
        "plate": "FLOW123",
        "capacity": 150,
        "status": "available"
    })
    assert response.status_code == 200
    vehicle_id = response.json()["id"]

    # actualizar vehículo existente
    response = client.put(f"/vehicles/{vehicle_id}", json={
        "capacity": 300
    })
    assert response.status_code == 200
    assert response.json()["capacity"] == 300

    # eliminar vehículo existente
    response = client.delete(f"/vehicles/{vehicle_id}")
    assert response.status_code == 200


def test_update_shipment_invalid_package_branch():
    # crear vehículo y paquete primero
    pkg = client.post("/packages", json={
        "weight": 5,
        "description": "pkg",
        "status": "pending"
    }).json()

    veh = client.post("/vehicles", json={
        "plate": "BRANCH1",
        "capacity": 100,
        "status": "available"
    }).json()

    sh = client.post("/shipments", json={
        "package_id": pkg["id"],
        "vehicle_id": veh["id"],
        "origin": "A",
        "destination": "B",
        "status": "in_transit"
    }).json()

    # ahora forzar invalid_package
    response = client.put(f"/shipments/{sh['id']}", json={
        "package_id": 9999
    })

    assert response.status_code == 400


def test_update_shipment_invalid_vehicle_branch():
    pkg = client.post("/packages", json={
        "weight": 7,
        "description": "pkg2",
        "status": "pending"
    }).json()

    veh = client.post("/vehicles", json={
        "plate": "BRANCH2",
        "capacity": 100,
        "status": "available"
    }).json()

    sh = client.post("/shipments", json={
        "package_id": pkg["id"],
        "vehicle_id": veh["id"],
        "origin": "X",
        "destination": "Y",
        "status": "in_transit"
    }).json()

    response = client.put(f"/shipments/{sh['id']}", json={
        "vehicle_id": 9999
    })

    assert response.status_code == 400