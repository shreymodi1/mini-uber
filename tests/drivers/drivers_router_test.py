import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session

# -------------------------------------------------------------------------
# Relative import from the drivers_router.py file
# which contains the FastAPI router we want to test
# -------------------------------------------------------------------------
from ...drivers.drivers_router import router

# -------------------------------------------------------------------------
# Example model imports if needed (adjust as per actual usage)
# -------------------------------------------------------------------------
from ...models import Driver, Vehicle  # Adjust to actual models


@pytest.fixture
def client():
    """
    Pytest fixture to create and provide a TestClient for our FastAPI app.
    Includes the 'router' for driver-related endpoints.
    """
    app = FastAPI()
    app.include_router(router, prefix="/drivers", tags=["drivers"])
    return TestClient(app)


@pytest.fixture
def mock_db_session():
    """
    Fixture to provide a mock of the SQLAlchemy Session for database operations.
    Replace or extend as needed to simulate DB interactions.
    """
    session = MagicMock(spec=Session)
    yield session


# -------------------------------------------------------------------------
# Tests for create_driver_endpoint
# -------------------------------------------------------------------------
def test_create_driver_success(client, mock_db_session):
    """
    Test creating a new driver successfully.
    Mocks database operations and checks for a 201 status code.
    """
    # Example request data for creating a new driver
    request_data = {
        "name": "John Doe",
        "license_number": "ABC12345",
        "phone": "555-1234"
    }

    # Patch any DB calls inside create_driver_endpoint (if applicable)
    with patch("...drivers.drivers_router.get_db", return_value=mock_db_session):
        response = client.post("/drivers/create_driver", json=request_data)
        assert response.status_code == 201
        assert response.json().get("message") == "Driver created successfully"
        # Additional assertions as needed (e.g., output data, DB calls)


def test_create_driver_missing_fields(client, mock_db_session):
    """
    Test creating a driver when required fields are missing.
    Expects a 422 or 400 status code due to validation.
    """
    # Missing license_number to simulate validation error
    invalid_request_data = {
        "name": "Jane Doe",
        "phone": "555-6789"
    }

    with patch("...drivers.drivers_router.get_db", return_value=mock_db_session):
        response = client.post("/drivers/create_driver", json=invalid_request_data)
        # Status could be 422 or 400 depending on pydantic or custom validation
        assert response.status_code in [400, 422]
        # Check error details, if provided
        assert "detail" in response.json()


def test_create_driver_internal_error(client, mock_db_session):
    """
    Test creating a driver when the database operation fails internally.
    Expects a 500 status code or appropriate error response.
    """
    valid_request_data = {
        "name": "Mark Smith",
        "license_number": "XYZ98765",
        "phone": "555-9999"
    }

    # Simulate an exception from the DB layer
    mock_db_session.add.side_effect = Exception("DB Error")

    with patch("...drivers.drivers_router.get_db", return_value=mock_db_session):
        response = client.post("/drivers/create_driver", json=valid_request_data)
        assert response.status_code == 500
        assert response.json().get("detail") == "Internal server error"


# -------------------------------------------------------------------------
# Tests for update_vehicle_details_endpoint
# -------------------------------------------------------------------------
def test_update_vehicle_details_success(client, mock_db_session):
    """
    Test updating vehicle details for a driver successfully.
    Expects a 200 status code and a success response.
    """
    driver_id = 1
    request_data = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2020,
        "license_plate": "ABC-123"
    }

    # Mock the driver and vehicle retrieval to simulate existing records
    mock_driver_instance = MagicMock(spec=Driver)
    mock_driver_instance.id = driver_id
    mock_vehicle_instance = MagicMock(spec=Vehicle)
    mock_driver_instance.vehicle = mock_vehicle_instance

    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_driver_instance

    with patch("...drivers.drivers_router.get_db", return_value=mock_db_session):
        response = client.put(f"/drivers/{driver_id}/update_vehicle_details", json=request_data)
        assert response.status_code == 200
        assert response.json().get("message") == "Vehicle details updated successfully"


def test_update_vehicle_details_not_found(client, mock_db_session):
    """
    Test updating vehicle details for a driver that does not exist.
    Expects a 404 status code when the driver is not found.
    """
    driver_id = 9999
    request_data = {
        "make": "Honda",
        "model": "Civic",
        "year": 2021,
        "license_plate": "XYZ-789"
    }

    # Simulate no driver found
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = None

    with patch("...drivers.drivers_router.get_db", return_value=mock_db_session):
        response = client.put(f"/drivers/{driver_id}/update_vehicle_details", json=request_data)
        assert response.status_code == 404
        assert response.json().get("detail") == "Driver not found"


def test_update_vehicle_details_db_error(client, mock_db_session):
    """
    Test updating vehicle details when a DB error occurs.
    Expects a 500 status code or appropriate error response.
    """
    driver_id = 2
    request_data = {
        "make": "Ford",
        "model": "Focus",
        "year": 2019,
        "license_plate": "FOC-321"
    }

    # Simulate a DB error during update
    mock_driver_instance = MagicMock(spec=Driver)
    mock_driver_instance.id = driver_id
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_driver_instance
    mock_db_session.commit.side_effect = Exception("DB Commit Error")

    with patch("...drivers.drivers_router.get_db", return_value=mock_db_session):
        response = client.put(f"/drivers/{driver_id}/update_vehicle_details", json=request_data)
        assert response.status_code == 500
        assert response.json().get("detail") == "Internal server error"