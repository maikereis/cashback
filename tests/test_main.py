# async bug: "ValueError: set_wakeup_fd only works in main thread"
import pytest

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture
def get_token():
    response = client.post(
        "/token",
        headers={
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "",
            "username": "johndoe",
            "password": "secret",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_request_new_token():
    response = client.post(
        "/token",
        headers={
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "",
            "username": "johndoe",
            "password": "secret",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response.status_code == 200


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"CashBack API": "Hello World!"}


def test_calculate_cashback(get_token):
    response = client.post(
        "/api/cashback/",
        headers={
            "accept": "application/json",
            "Authorization": f"Bearer {get_token}",
        },
        json={
            "sold_at": "2021-11-15 18:54:40",
            "customer": {"customer_name": "string", "customer_cpf": 0},
            "total": 0,
            "products": [],
        }
    )
    assert response.status_code == 200
    assert response.json()=={
            "sold_at": "2021-11-15T18:54:40",
            "customer": {"customer_name": "string", "customer_cpf": 0},
            "total": 0,
            "products": [],
        }
