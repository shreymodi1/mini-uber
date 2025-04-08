import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session

# Import the functions to be tested from the rides_service file
from ...rides.rides_service import create_ride, assign_driver_to_ride, update_ride_status

# Import models if needed
from ...models import Ride, Driver


@pytest.fixture
def mock_db_session():
    """
    Provides a mocked database session for testing.
    Replace MagicMock() with an actual test session if you want to integrate with the real DB.
    """
    return MagicMock(spec=Session)


@pytest.fixture
def sample_ride_data():
    """
    Provides sample data for creating a ride.
    """
    return {
        "rider_id": 1,
        "pickup_location": "Location A",
        "dropoff_location": "Location B"
    }


@pytest.fixture
def sample_ride_in_db():
    """
    Provides a mock Ride object that might represent an existing ride in the database.
    """
    mock_ride = MagicMock(spec=Ride)
    mock_ride.id = 123
    mock_ride.rider_id = 1
    mock_ride.pickup_location = "Location A"
    mock_ride.dropoff_location = "Location B"
    mock_ride.status = "created"
    return mock_ride


@pytest.mark.parametrize("pickup, dropoff", [
    # Test with valid pickup and dropoff
    ("Location A", "Location B"),
    # Test with minimal necessary locations
    ("", "Exact Spot"),
])
def test_create_ride_success(mock_db_session, pickup, dropoff):
    """
    Test that create_ride successfully creates a ride when called with valid data.
    The function should insert a new ride record into the database.
    """
    # Arrange
    rider_id = 1

    # Act
    new_ride = create_ride(rider_id, pickup, dropoff, db_session=mock_db_session)

    # Assert
    # Ensure a ride object is returned
    assert new_ride is not None
    # Check that the ride has the correct attributes
    assert new_ride.rider_id == rider_id
    assert new_ride.pickup_location == pickup
    assert new_ride.dropoff_location == dropoff
    # Verify that the DB session's add/commit was called
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()


def test_create_ride_missing_location(mock_db_session):
    """
    Test that create_ride raises an exception when required locations are missing.
    """
    # Arrange
    rider_id = 1
    invalid_pickup = None
    invalid_dropoff = ""

    # Act & Assert
    with pytest.raises(ValueError):
        create_ride(rider_id, invalid_pickup, "Valid Dropoff", db_session=mock_db_session)

    with pytest.raises(ValueError):
        create_ride(rider_id, "Valid Pickup", invalid_dropoff, db_session=mock_db_session)


@patch("...rides.rides_service.get_available_driver")
def test_assign_driver_to_ride_success(mock_get_driver, mock_db_session, sample_ride_in_db):
    """
    Test that assign_driver_to_ride assigns an available driver to an existing ride.
    It should update the ride's status and driver_id.
    """
    # Arrange
    mock_driver = MagicMock(spec=Driver)
    mock_driver.id = 10
    mock_get_driver.return_value = mock_driver

    # Mock DB session behavior for getting a ride
    mock_db_session.query.return_value.get.return_value = sample_ride_in_db

    # Act
    updated_ride = assign_driver_to_ride(sample_ride_in_db.id, db_session=mock_db_session)

    # Assert
    assert updated_ride.driver_id == mock_driver.id
    assert updated_ride.status == "assigned"
    mock_db_session.commit.assert_called_once()


@patch("...rides.rides_service.get_available_driver")
def test_assign_driver_to_ride_no_drivers(mock_get_driver, mock_db_session, sample_ride_in_db):
    """
    Test that assign_driver_to_ride handles the scenario where no drivers are available.
    It should raise an exception or return None (depending on your logic).
    """
    # Arrange
    mock_get_driver.return_value = None
    mock_db_session.query.return_value.get.return_value = sample_ride_in_db

    # Act & Assert
    with pytest.raises(RuntimeError):
        assign_driver_to_ride(sample_ride_in_db.id, db_session=mock_db_session)


def test_assign_driver_to_ride_ride_not_found(mock_db_session):
    """
    Test that assign_driver_to_ride raises an exception if the ride does not exist.
    """
    # Arrange
    non_existent_ride_id = 999
    mock_db_session.query.return_value.get.return_value = None

    # Act & Assert
    with pytest.raises(ValueError):
        assign_driver_to_ride(non_existent_ride_id, db_session=mock_db_session)


@pytest.mark.parametrize("new_status", [
    "in_progress",
    "completed",
    "canceled"
])
def test_update_ride_status_success(mock_db_session, sample_ride_in_db, new_status):
    """
    Test that update_ride_status successfully updates a ride's status
    when called with a valid status.
    """
    # Arrange
    mock_db_session.query.return_value.get.return_value = sample_ride_in_db

    # Act
    updated_ride = update_ride_status(sample_ride_in_db.id, new_status, db_session=mock_db_session)

    # Assert
    assert updated_ride.status == new_status
    mock_db_session.commit.assert_called_once()


def test_update_ride_status_invalid_status(mock_db_session, sample_ride_in_db):
    """
    Test that update_ride_status raises an exception if an invalid status is provided.
    """
    # Arrange
    mock_db_session.query.return_value.get.return_value = sample_ride_in_db
    invalid_status = "not_a_valid_status"

    # Act & Assert
    with pytest.raises(ValueError):
        update_ride_status(sample_ride_in_db.id, invalid_status, db_session=mock_db_session)


def test_update_ride_status_not_found(mock_db_session):
    """
    Test that update_ride_status raises an exception if the ride does not exist.
    """
    # Arrange
    ride_id = 999
    new_status = "in_progress"
    mock_db_session.query.return_value.get.return_value = None

    # Act & Assert
    with pytest.raises(ValueError):
        update_ride_status(ride_id, new_status, db_session=mock_db_session)