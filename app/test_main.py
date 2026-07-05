from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "uptime" in response.json()

def test_predict_no_model():
    response = client.post("/predict", json={"features": [1.0, 2.0, 3.0]})
    # 503 expected when model.pkl not present
    assert response.status_code == 503
