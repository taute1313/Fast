from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_crud_flow():
    payload = {"name": "Laptop", "description": "Ultrabook", "price": 999.0, "tags": ["tech"]}
    r = client.post("/api/v1/items/", json=payload)
    assert r.status_code == 201
    item = r.json()

    r = client.get(f"/api/v1/items/{item['id']}")
    assert r.status_code == 200

    r = client.patch(f"/api/v1/items/{item['id']}", json={"price": 1099.0})
    assert r.status_code == 200
    assert r.json()["price"] == 1099.0

    r = client.get("/api/v1/items/?skip=0&limit=10")
    assert r.status_code == 200
    assert len(r.json()) >= 1

    r = client.delete(f"/api/v1/items/{item['id']}")
    assert r.status_code == 204
