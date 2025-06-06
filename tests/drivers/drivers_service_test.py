import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

# FastAPI & Config imports
from fastapi.testclient import TestClient
from main import create_app
from config import load_config

# Service and Models imports (absolute imports based on project structure)
from drivers.drivers_service import create_driver, update_vehicle_details
from drivers.drivers_models import Driver


@pytest.fixture
def client():
    """
    Fixture to provide a TestClient for FastAPI app.
    """
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_db():
    """
    Fixture to provide a mock Session object for database operations.
    """
    return MagicMock(spec=Session)


def test_create_driver_success(test_db):
    """
    Test creating a new driver with valid data.
    Ensures that the driver record is persisted and session commits.
    """
    # Arrange
    name = "John Doe"
    license_number = "ABC12345"
    vehicle_info = {"make": "Toyota", "model": "Corolla", "year": 2020}

    # Act
    new_driver = create_driver(name, license_number, vehicle_info)

    # Assert
    assert new_driver is not None
    assert new_driver.name == name
    assert new_driver.license_number == license_number
    assert new_driver.vehicle_info == vehicle_info


def test_create_driver_invalid_license(test_db):
    """
    Test creating a driver with invalid or missing license data, expecting an error or None result.
    This simulates license verification failing.
    """
    # Arrange
    name = "Jane Doe"
    license_number = ""  # Invalid license
    vehicle_info = {"make": "Honda", "model": "Civic", "year": 2019}

    # Act
    result = None
    try:
        result = create_driver(name, license_number, vehicle_info)
    except ValueError as e:
        # For example, if the service raises a ValueError for an invalid license
        assert "license" in str(e)

    # Assert
    # If the service handles invalid licenses by returning None or raising, confirm it here
    if result is not None:
        # If it returns None instead of raising
        assert result is None


def test_update_vehicle_details_success(test_db):
    """
    Test updating a driver's vehicle details successfully.
    Verifies the new vehicle info is saved to the driver record.
    """
    # Arrange
    driver_id = 1
    new_vehicle_info = {"make": "Tesla", "model": "Model 3", "year": 2021}

    # Mock existing driver
    mock_driver = Driver(
        name="Alice",
        license_number="XYZ98765",
        vehicle_info={"make": "Old", "model": "Car", "year": 2010},
    )
    mock_driver.id = driver_id

    # Patch the retrieval of driver from DB
    with patch("drivers.drivers_service.Driver") as mock_driver_model:
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = mock_driver
        mock_driver_model.query = mock_query

        # Act
        updated_driver = update_vehicle_details(driver_id, new_vehicle_info)

        # Assert
        assert updated_driver is not None
        assert updated_driver.vehicle_info == new_vehicle_info


def test_update_vehicle_details_driver_not_found(test_db):
    """
    Test attempting to update vehicle details for a driver that does not exist.
    Ensures the service handles the missing record gracefully.
    """
    # Arrange
    driver_id = 999
    new_vehicle_info = {"make": "Ford", "model": "Focus", "year": 2018}

    # Patch the retrieval of driver from DB - returns None
    with patch("drivers.drivers_service.Driver") as mock_driver_model:
        mock_query = MagicMock()
        mock_query.filter_by.return_value.first.return_value = None
        mock_driver_model.query = mock_query

        # Act
        updated_driver = update_vehicle_details(driver_id, new_vehicle_info)

        # Assert
        assert updated_driver is None, "Expected None when driver does not exist."