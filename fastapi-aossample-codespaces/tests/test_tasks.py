from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200

def test_crud_tasks_flow():
    payload = {"title": "Comprar leche", "description": "en el súper", "completed": False, "tags": ["casa"]}
    r = client.post("/api/v1/tasks/", json=payload)
    assert r.status_code == 201
    task = r.json()

    r = client.get(f"/api/v1/tasks/{task['id']}")
    assert r.status_code == 200

    r = client.patch(f"/api/v1/tasks/{task['id']}", json={"completed": True})
    assert r.status_code == 200
    assert r.json()["completed"] is True

    r = client.get("/api/v1/tasks/?completed=true")
    assert r.status_code == 200

    r = client.delete(f"/api/v1/tasks/{task['id']}")
    assert r.status_code == 204
