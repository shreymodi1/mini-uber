import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

# Import the functions to test from the drivers_service module
from ...drivers.drivers_service import create_driver, update_vehicle_details
# Import your database models if needed (example below)
# from ...models import Driver

@pytest.fixture
def mock_session():
    """
    Pytest fixture to provide a mocked SQLAlchemy session.
    This fixture could be replaced with a real test database or an in-memory DB.
    """
    return MagicMock(spec=Session)

@pytest.fixture
def driver_data():
    """
    Fixture providing standard valid driver data.
    """
    return {
        "name": "John Doe",
        "license_number": "ABC123456",
        "vehicle_info": {
            "make": "Toyota",
            "model": "Camry",
            "year": 2020
        }
    }

@pytest.fixture
def setup_teardown_db():
    """
    Optional setup/teardown fixture if you want to do additional work
    before tests and cleanup afterwards.
    """
    # Setup code here
    yield
    # Teardown code here

# -----------------
# create_driver Tests
# -----------------

def test_create_driver_success(mock_session, driver_data, setup_teardown_db):
    """
    Test creating a driver successfully. Expect the function to commit changes
    to the DB and return the new driver record without error.
    """
    # Arrange
    mock_session.commit.return_value = None  # No errors on commit

    # Act
    new_driver = create_driver(
        name=driver_data["name"],
        license_number=driver_data["license_number"],
        vehicle_info=driver_data["vehicle_info"]
    )

    # Assert
    mock_session.add.assert_called_once()   # Check if driver was 'added' to session
    mock_session.commit.assert_called_once()  # Check if the session commit was called
    assert new_driver is not None
    assert new_driver.name == driver_data["name"]
    assert new_driver.license_number == driver_data["license_number"]
    assert new_driver.vehicle_info == driver_data["vehicle_info"]

def test_create_driver_invalid_license(mock_session, driver_data, setup_teardown_db):
    """
    Test creating a driver with invalid license. Expect an exception or error raised.
    """
    # Arrange
    driver_data["license_number"] = ""  # Empty or invalid license

    # Act & Assert
    with pytest.raises(ValueError):
        create_driver(
            name=driver_data["name"],
            license_number=driver_data["license_number"],
            vehicle_info=driver_data["vehicle_info"]
        )

    # Ensure session was not committed for invalid data
    mock_session.commit.assert_not_called()

# -------------------------
# update_vehicle_details Tests
# -------------------------

def test_update_vehicle_details_success(mock_session, driver_data, setup_teardown_db):
    """
    Test updating vehicle details of an existing driver. Expect the DB to commit
    the changes and return the updated driver.
    """
    # Arrange
    mock_driver = MagicMock()
    mock_driver.id = 123
    mock_driver.vehicle_info = {}
    mock_session.query.return_value.filter_by.return_value.first.return_value = mock_driver

    updated_vehicle_info = {
        "make": "Honda",
        "model": "Civic",
        "year": 2021
    }

    # Act
    updated_driver = update_vehicle_details(
        driver_id=mock_driver.id,
        vehicle_info=updated_vehicle_info
    )

    # Assert
    mock_session.commit.assert_called_once()  # Check if changes were committed
    assert updated_driver is not None
    assert updated_driver.vehicle_info == updated_vehicle_info

def test_update_vehicle_details_not_found(mock_session, driver_data, setup_teardown_db):
    """
    Test updating vehicle details with a driver_id that doesn't exist. Expect an exception or error.
    """
    # Arrange
    mock_session.query.return_value.filter_by.return_value.first.return_value = None

    updated_vehicle_info = {
        "make": "Tesla",
        "model": "Model 3",
        "year": 2022
    }

    # Act & Assert
    with pytest.raises(ValueError):
        update_vehicle_details(
            driver_id=999,
            vehicle_info=updated_vehicle_info
        )

    # Ensure session was not committed when driver not found
    mock_session.commit.assert_not_called()