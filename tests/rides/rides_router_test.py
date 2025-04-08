import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Router import from the rides module
from ...rides.rides_router import router

# Example model import (if needed for mocking or validation)
from ...models import Ride


@pytest.fixture(scope="module")
def test_app():
    """
    Fixture to create a FastAPI test application and include the rides router
    """
    app = FastAPI()
    app.include_router(router, prefix="/rides")
    yield app


@pytest.fixture
def client(test_app):
    """
    Fixture to create a test client for making HTTP requests
    """
    with TestClient(test_app) as c:
        yield c


@pytest.fixture
def mock_db_session():
    """
    Fixture to provide a mock or test DB session
    Replace or extend with actual DB session logic or mock if necessary
    """
    # Could mock methods like session.query, session.add, session.commit, etc.
    class MockSession:
        def add(self, obj):
            pass

        def commit(self):
            pass

        def refresh(self, obj):
            pass

        def close(self):
            pass

    return MockSession()


# -------------------------
# TESTS FOR request_ride_endpoint
# -------------------------
def test_request_ride_success(client, mock_db_session):
    """
    Test successful ride request with valid pickup and dropoff data
    """
    payload = {"pickup": "Location A", "dropoff": "Location B"}
    response = client.post("/rides/", json=payload)

    # Assert the endpoint returns HTTP 201 or 200 on success (assuming 201 is used for creation)
    assert response.status_code == 201
    assert response.json()["pickup"] == payload["pickup"]
    assert response.json()["dropoff"] == payload["dropoff"]
    assert "ride_id" in response.json()


def test_request_ride_missing_data(client, mock_db_session):
    """
    Test request ride endpoint with missing pickup or dropoff data
    to verify it returns a bad request error
    """
    payload = {"pickup": "Location A"}  # Missing dropoff
    response = client.post("/rides/", json=payload)

    # Expecting a 422 or 400 for validation error
    assert response.status_code in [400, 422]


def test_request_ride_invalid_data(client, mock_db_session):
    """
    Test request ride endpoint with invalid data (e.g., empty strings)
    """
    payload = {"pickup": "", "dropoff": ""}
    response = client.post("/rides/", json=payload)

    # Expecting a validation error
    assert response.status_code in [400, 422]


# -------------------------
# TESTS FOR update_ride_status_endpoint
# -------------------------
def test_update_ride_status_success(client, mock_db_session):
    """
    Test successfully updating ride status
    """
    # First create a new ride
    create_payload = {"pickup": "Location A", "dropoff": "Location B"}
    create_response = client.post("/rides/", json=create_payload)
    ride_id = create_response.json()["ride_id"]

    # Update status
    update_payload = {"status": "started"}
    update_response = client.put(f"/rides/{ride_id}/status", json=update_payload)

    assert update_response.status_code == 200
    assert update_response.json()["status"] == "started"


def test_update_ride_status_invalid_status(client, mock_db_session):
    """
    Test updating ride status with an invalid status value
    """
    # Create a new ride
    create_payload = {"pickup": "Location A", "dropoff": "Location B"}
    create_response = client.post("/rides/", json=create_payload)
    ride_id = create_response.json()["ride_id"]

    # Attempt to update with invalid status
    update_payload = {"status": "flying"}  # Not a valid ride status
    update_response = client.put(f"/rides/{ride_id}/status", json=update_payload)

    # Expecting a 400 or 422 for invalid status
    assert update_response.status_code in [400, 422]


def test_update_ride_status_ride_not_found(client, mock_db_session):
    """
    Test updating status for a ride that does not exist
    """
    update_payload = {"status": "completed"}
    response = client.put("/rides/999999/status", json=update_payload)  # Non-existent ride_id

    # Expecting 404 if ride is not found
    assert response.status_code == 404


# -------------------------
# TESTS FOR get_ride_details_endpoint
# -------------------------
def test_get_ride_details_success(client, mock_db_session):
    """
    Test fetching existing ride details
    """
    # Create a new ride
    create_payload = {"pickup": "Location A", "dropoff": "Location B"}
    create_response = client.post("/rides/", json=create_payload)
    ride_id = create_response.json()["ride_id"]

    # Fetch details
    response = client.get(f"/rides/{ride_id}")

    assert response.status_code == 200
    assert "pickup" in response.json()
    assert response.json()["pickup"] == "Location A"


def test_get_ride_details_not_found(client, mock_db_session):
    """
    Test fetching ride details for a non-existent ride
    """
    response = client.get("/rides/999999")

    # Expecting 404 for non-existent ride
    assert response.status_code == 404