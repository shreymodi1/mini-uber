import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Import from project root based on provided structure
from config import load_config
from main import create_app
from rides.rides_service import create_ride, assign_driver_to_ride, update_ride_status
from rides.rides_models import Ride


@pytest.fixture(scope="module")
def client():
    """
    Fixture to initialize the FastAPI application and return a test client.
    """
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_db():
    """
    Fixture to provide a mocked database session or in-memory DB for testing.
    """
    # You would typically set up an in-memory SQLite DB or a mock Session here.
    # For demonstration, we'll return a MagicMock to stand in for a Session.
    return MagicMock(spec=Session)


def test_create_ride_success(test_db):
    """
    Test that create_ride successfully creates a new ride record when valid inputs are provided.
    """
    # Arrange
    rider_id = 123
    pickup_location = {"lat": 40.7128, "lng": -74.0060}
    dropoff_location = {"lat": 40.73061, "lng": -73.935242}

    # Mock the database call to create and save a new ride
    test_db.add = MagicMock()
    test_db.commit = MagicMock()

    # Act
    new_ride = create_ride(rider_id, pickup_location, dropoff_location)

    # Assert
    assert isinstance(new_ride, Ride)
    assert new_ride.rider_id == rider_id
    assert new_ride.pickup_location == pickup_location
    assert new_ride.dropoff_location == dropoff_location
    test_db.add.assert_called_once()
    test_db.commit.assert_called_once()


def test_create_ride_failure_invalid_rider(test_db):
    """
    Test that create_ride raises an exception or handles errors when the rider_id is invalid.
    For demonstration, we assume an invalid rider_id < 0 triggers a ValueError.
    """
    # Arrange
    invalid_rider_id = -1
    pickup_location = {"lat": 40.7128, "lng": -74.0060}
    dropoff_location = {"lat": 40.73061, "lng": -73.935242}

    # Act & Assert
    with pytest.raises(ValueError):
        create_ride(invalid_rider_id, pickup_location, dropoff_location)


@patch("rides.rides_service.fetch_rider")
def test_create_ride_failure_rider_not_found(mock_fetch_rider, test_db):
    """
    Test that create_ride handles the scenario where the rider cannot be found in the database.
    """
    # Arrange
    mock_fetch_rider.return_value = None  # Rider not found
    rider_id = 999
    pickup_location = {"lat": 40.7128, "lng": -74.0060}
    dropoff_location = {"lat": 40.73061, "lng": -73.935242}

    # Act & Assert
    with pytest.raises(RuntimeError, match="Rider not found"):
        create_ride(rider_id, pickup_location, dropoff_location)


def test_assign_driver_to_ride_success(test_db):
    """
    Test that assign_driver_to_ride assigns an available driver to an existing ride successfully.
    """
    # Arrange
    ride_id = 10
    mock_ride = MagicMock(spec=Ride)
    mock_ride.id = ride_id
    mock_ride.driver_id = None
    test_db.query.return_value.filter_by.return_value.first.return_value = mock_ride

    # Mock a simple "available driver" finding mechanism
    available_driver_id = 101

    def mock_find_driver(*args, **kwargs):
        return available_driver_id

    # Patch the part of the service that finds an available driver
    with patch("rides.rides_service.assign_driver_to_ride.find_available_driver", new=mock_find_driver):
        # Act
        updated_ride = assign_driver_to_ride(ride_id)

    # Assert
    assert updated_ride.driver_id == available_driver_id
    test_db.commit.assert_called_once()


@patch("rides.rides_service.assign_driver_to_ride.find_available_driver", return_value=None)
def test_assign_driver_to_ride_no_available_driver(mock_find_driver, test_db):
    """
    Test that assign_driver_to_ride handles the case where no drivers are available.
    """
    # Arrange
    ride_id = 11
    mock_ride = MagicMock(spec=Ride)
    mock_ride.id = ride_id
    mock_ride.driver_id = None
    test_db.query.return_value.filter_by.return_value.first.return_value = mock_ride

    # Act
    updated_ride = assign_driver_to_ride(ride_id)

    # Assert
    # If no driver is assigned, we expect driver_id to remain None.
    assert updated_ride.driver_id is None


def test_assign_driver_to_ride_ride_not_found(test_db):
    """
    Test that assign_driver_to_ride handles the case when the ride does not exist.
    """
    # Arrange
    ride_id = 999
    test_db.query.return_value.filter_by.return_value.first.return_value = None  # Ride not found

    # Act & Assert
    with pytest.raises(RuntimeError, match="Ride not found"):
        assign_driver_to_ride(ride_id)


def test_update_ride_status_success(test_db):
    """
    Test that update_ride_status successfully updates the ride status when provided valid ride_id and status.
    """
    # Arrange
    ride_id = 20
    new_status = "in-progress"
    mock_ride = MagicMock(spec=Ride)
    mock_ride.id = ride_id
    mock_ride.status = "requested"
    test_db.query.return_value.filter_by.return_value.first.return_value = mock_ride

    # Act
    updated_ride = update_ride_status(ride_id, new_status)

    # Assert
    assert updated_ride.status == new_status
    test_db.commit.assert_called_once()


def test_update_ride_status_invalid_ride(test_db):
    """
    Test that update_ride_status raises an error when the ride does not exist in the database.
    """
    # Arrange
    ride_id = 9999
    new_status = "canceled"
    test_db.query.return_value.filter_by.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(RuntimeError, match="Ride not found"):
        update_ride_status(ride_id, new_status)


def test_update_ride_status_invalid_status(test_db):
    """
    Test that update_ride_status handles invalid status strings appropriately.
    For demonstration, we assume an invalid status triggers a ValueError.
    """
    # Arrange
    ride_id = 30
    invalid_status = "invalid-status"
    mock_ride = MagicMock(spec=Ride)
    mock_ride.id = ride_id
    mock_ride.status = "requested"
    test_db.query.return_value.filter_by.return_value.first.return_value = mock_ride

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid ride status"):
        update_ride_status(ride_id, invalid_status)