from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_default_rate_endpoint():
    response = client.get("/kpi/default_rate")
    assert response.status_code == 200
    data = response.json()
    assert "default_rate" in data
    assert isinstance(data["default_rate"], (int, float))


def test_average_loan_amount_endpoint():
    response = client.get("/kpi/average_loan_amount")
    assert response.status_code == 200
    data = response.json()
    assert "average_loan_amount" in data
    assert isinstance(data["average_loan_amount"], (int, float))


def test_average_interest_rate_endpoint():
    response = client.get("/kpi/average_interest_rate")
    assert response.status_code == 200
    data = response.json()
    assert "average_interest_rate" in data
    assert isinstance(data["average_interest_rate"], (int, float))
