from fastapi.testclient import TestClient
from main import app

# A fake browser that talks to your app directly
client = TestClient(app)


def test_root_works():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_valid_message_returns_a_prediction():
    response = client.post("/predict", json={"message": "Hello, are we still meeting tomorrow?"})
    assert response.status_code == 200

    data = response.json()
    assert data["prediction"] in ("spam", "ham")


def test_empty_message_is_rejected():
    response = client.post("/predict", json={"message": ""})
    # 400 or 422 both mean "your input was invalid"
    assert response.status_code in (400, 422)


def test_missing_message_is_rejected():
    response = client.post("/predict", json={})
    assert response.status_code == 422