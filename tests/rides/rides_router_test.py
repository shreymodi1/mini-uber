import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session

from main import create_app
from config import load_config

# NOTE: We assume that the FastAPI application in main.py includes the rides router
# (from rides.rides_router) so that these endpoints are available at runtime.

@pytest.fixture
def client():
    """
    Fixture to provide a TestClient for the FastAPI app.
    """
    app = create_app()
    return TestClient(app)

@pytest.fixture
def test_db():
    """
    Fixture for providing a mock or test database session, if needed.
    This can be replaced with a real database session setup if desired.
    """
    # In a real scenario, you might set up an in-memory SQLite or a mock
    # For now, we'll just yield a MagicMock to fulfill the signature
    db_session = MagicMock(spec=Session)
    yield db_session

# -------------------------
# request_ride_endpoint
# -------------------------

def test_request_ride_success(client, test_db):
    """
    Test successful ride request with valid data.
    Expects a 200 or 201 response indicating ride creation.
    """
    request_data = {
        "rider_id": 1,
        "pickup_location": "Point A",
        "dropoff_location": "Point B"
    }
    response = client.post("/rides/request_ride", json=request_data)
    assert response.status_code in [200, 201]
    response_json = response.json()
    assert "ride_id" in response_json
    assert response_json["ride_id"] is not None

def test_request_ride_missing_data(client, test_db):
    """
    Test ride request with missing fields.
    Expects a 422 or 400 response due to invalid data.
    """
    request_data = {
        "rider_id": 1
        # Missing 'pickup_location' and 'dropoff_location'
    }
    response = client.post("/rides/request_ride", json=request_data)
    assert response.status_code in [400, 422]

@patch("rides.rides_router.rides_service.create_ride")
def test_request_ride_service_mock(mock_create_ride, client, test_db):
    """
    Test ride request mocking the rides_service.create_ride function.
    Verifies that the service layer is called with correct arguments.
    """
    mock_create_ride.return_value = {"ride_id": 101, "status": "pending"}
    request_data = {
        "rider_id": 5,
        "pickup_location": "North Gate",
        "dropoff_location": "South Station"
    }
    response = client.post("/rides/request_ride", json=request_data)
    assert response.status_code in [200, 201]
    mock_create_ride.assert_called_once_with(
        rider_id=5,
        pickup_location="North Gate",
        dropoff_location="South Station"
    )

# -------------------------
# update_ride_status_endpoint
# -------------------------

def test_update_ride_status_success(client, test_db):
    """
    Test a valid ride status update.
    Expects a 200 response and confirmation of new status.
    """
    ride_id = 123
    response = client.put(f"/rides/{ride_id}/status", json={"status": "accepted"})
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("ride_id") == ride_id
    assert response_json.get("status") == "accepted"

def test_update_ride_status_invalid_status(client, test_db):
    """
    Test ride status update with an invalid status value.
    Expects a 400 or 422 response.
    """
    ride_id = 999
    response = client.put(f"/rides/{ride_id}/status", json={"status": "unknown_status"})
    assert response.status_code in [400, 422]

@patch("rides.rides_router.rides_service.update_ride_status")
def test_update_ride_status_service_mock(mock_update_ride_status, client, test_db):
    """
    Test ride status update with a mocked rides_service.update_ride_status function.
    Verifies that the service layer is called correctly.
    """
    mock_update_ride_status.return_value = {"ride_id": 999, "status": "started"}
    response = client.put("/rides/999/status", json={"status": "started"})
    assert response.status_code == 200
    mock_update_ride_status.assert_called_once_with(999, "started")

# -------------------------
# get_ride_details_endpoint
# -------------------------

def test_get_ride_details_success(client, test_db):
    """
    Test fetching ride details for a valid ride ID.
    Expects a 200 response and valid ride detail fields in the JSON.
    """
    ride_id = 555
    response = client.get(f"/rides/{ride_id}/details")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("ride_id") == ride_id
    assert "pickup_location" in response_json
    assert "dropoff_location" in response_json
    assert "status" in response_json

def test_get_ride_details_not_found(client, test_db):
    """
    Test fetching ride details for a ride ID that does not exist.
    Expects a 404 response.
    """
    ride_id = 999999
    response = client.get(f"/rides/{ride_id}/details")
    assert response.status_code == 404

@patch("rides.rides_router.rides_service.fetch_ride")
def test_get_ride_details_service_mock(mock_fetch_ride, client, test_db):
    """
    Test the get ride details endpoint, mocking the rides_service.fetch_ride call.
    Validates correct response handling.
    """
    mock_fetch_ride.return_value = {
        "ride_id": 222,
        "pickup_location": "Location X",
        "dropoff_location": "Location Y",
        "status": "completed"
    }
    response = client.get("/rides/222/details")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["ride_id"] == 222
    assert response_json["status"] == "completed"
    mock_fetch_ride.assert_called_once_with(222)