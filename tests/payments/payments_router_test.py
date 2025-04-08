import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session

# Import your FastAPI router from the main code
from ...payments.payments_router import router


@pytest.fixture(scope="module")
def test_app():
    """
    Creates a FastAPI app for testing by including the payments router.
    """
    app = FastAPI()
    app.include_router(router, prefix="/payments", tags=["payments"])
    return app


@pytest.fixture(scope="module")
def client(test_app):
    """
    Provides a test client for sending requests to the FastAPI app.
    """
    with TestClient(test_app) as c:
        yield c


@pytest.fixture
def mock_db_session():
    """
    Provides a mock database session to avoid making real database calls.
    """
    # You can customize the MagicMock or patch specific methods if needed.
    return MagicMock(spec=Session)


# -----------------------------
# calculate_fare_endpoint Tests
# -----------------------------

def test_calculate_fare_success(client, mock_db_session):
    """
    Test that calculate_fare_endpoint returns an estimated or final fare
    for a valid ride_id.
    """
    ride_id = 123

    # Optionally, patch any function inside payments_router that queries the DB
    # or external services to prevent real calls.
    with patch("...payments.payments_router.some_db_method", return_value={"fare": 15.5}):
        response = client.get(f"/payments/fare/{ride_id}")
        assert response.status_code == 200
        json_data = response.json()
        assert "fare" in json_data
        assert json_data["fare"] == 15.5


def test_calculate_fare_invalid_ride(client, mock_db_session):
    """
    Test that calculate_fare_endpoint returns an error when the ride_id is invalid.
    """
    invalid_ride_id = 999

    # Mock a DB lookup that returns None or raises an exception
    with patch("...payments.payments_router.some_db_method", return_value=None):
        response = client.get(f"/payments/fare/{invalid_ride_id}")
        assert response.status_code == 404
        json_data = response.json()
        assert json_data.get("detail") == "Ride not found"


# -----------------------------------
# process_payment_endpoint Tests
# -----------------------------------

def test_process_payment_success(client, mock_db_session):
    """
    Test that process_payment_endpoint successfully charges the rider for a valid ride.
    """
    ride_id = 321

    # Mock the DB and external payment gateway call
    with patch("...payments.payments_router.charge_rider_payment", return_value=True):
        response = client.post(f"/payments/pay/{ride_id}")
        assert response.status_code == 200
        json_data = response.json()
        assert json_data.get("message") == "Payment processed successfully"


def test_process_payment_failure(client, mock_db_session):
    """
    Test that process_payment_endpoint returns an error if payment fails.
    """
    ride_id = 321

    # Mock the payment gateway to simulate an error
    with patch("...payments.payments_router.charge_rider_payment", side_effect=Exception("Payment failed")):
        response = client.post(f"/payments/pay/{ride_id}")
        assert response.status_code == 400
        json_data = response.json()
        assert json_data.get("detail") == "Payment failed"


# -----------------------------------------
# disburse_driver_payment_endpoint Tests
# -----------------------------------------

def test_disburse_driver_payment_success(client, mock_db_session):
    """
    Test that disburse_driver_payment_endpoint successfully disburses payment to the driver
    for a completed ride.
    """
    ride_id = 456

    # Mock the DB and external transaction call
    with patch("...payments.payments_router.pay_driver", return_value=True):
        response = client.post(f"/payments/disburse/{ride_id}")
        assert response.status_code == 200
        json_data = response.json()
        assert json_data.get("message") == "Driver payment disbursed"


def test_disburse_driver_payment_for_non_completed_ride(client, mock_db_session):
    """
    Test that disburse_driver_payment_endpoint returns an error if the ride is not completed.
    """
    ride_id = 456

    # Mock a scenario where the ride is not completed
    with patch("...payments.payments_router.pay_driver", side_effect=ValueError("Ride not completed")):
        response = client.post(f"/payments/disburse/{ride_id}")
        assert response.status_code == 400
        json_data = response.json()
        assert json_data.get("detail") == "Ride not completed"