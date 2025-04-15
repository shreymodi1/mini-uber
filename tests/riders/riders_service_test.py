import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session

# Required imports based on project structure
from config import load_config
from main import create_app
from riders.riders_service import create_rider, fetch_rider
from riders.riders_models import Rider


@pytest.fixture
def mock_db_session():
    """
    Fixture to provide a mock SQLAlchemy session for testing database interactions.
    """
    return MagicMock(spec=Session)


def test_create_rider_success(mock_db_session):
    """
    Test that create_rider successfully persists a new rider with valid data.
    Expects:
        - The returned Rider object to match the input data.
        - Session add() and commit() are called to persist the record.
    """
    # Arrange
    # Patch where the Session is used inside riders_service
    with patch("riders.riders_service.Session", return_value=mock_db_session):
        mock_db_session.add.return_value = None
        mock_db_session.commit.return_value = None

        # Act
        created_rider = create_rider(name="John Doe", phone_number="1234567890", payment_method="CreditCard")

        # Assert
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        assert created_rider is not None
        assert created_rider.name == "John Doe"
        assert created_rider.phone_number == "1234567890"
        assert created_rider.payment_method == "CreditCard"


def test_create_rider_error_invalid_phone(mock_db_session):
    """
    Test that create_rider handles an invalid phone number scenario (e.g. empty or malformed).
    Expects:
        - Some form of error to be raised or handled when phone_number is invalid.
        - Session should not commit changes if invalid data is provided.
    """
    with patch("riders.riders_service.Session", return_value=mock_db_session):
        mock_db_session.add.return_value = None

        # In a real scenario, the service might raise a ValueError or custom exception for invalid phone numbers.
        # Here we demonstrate expecting an exception. Adjust as needed for your actual implementation.
        with pytest.raises(ValueError):
            create_rider(name="Jane Doe", phone_number="", payment_method="CreditCard")

        mock_db_session.add.assert_not_called()
        mock_db_session.commit.assert_not_called()


def test_fetch_rider_success(mock_db_session):
    """
    Test that fetch_rider returns the correct rider object when the rider exists.
    Expects:
        - The returned Rider object to have the same attributes as stored in the mock.
    """
    with patch("riders.riders_service.Session", return_value=mock_db_session):
        # Mock a rider object that would be returned from the DB
        mock_rider = Rider(name="Alice", phone_number="9876543210", payment_method="PayPal")

        query_mock = mock_db_session.query.return_value
        filter_mock = query_mock.filter_by.return_value
        filter_mock.first.return_value = mock_rider

        # Act
        rider = fetch_rider(rider_id=1)

        # Assert
        assert rider is mock_rider, "Expected the fetched rider to match the mocked instance"
        mock_db_session.query.assert_called_once()
        filter_mock.first.assert_called_once()


def test_fetch_rider_not_found(mock_db_session):
    """
    Test that fetch_rider returns None (or an equivalent behavior) when no rider is found.
    Expects:
        - None or a valid 'not found' response if the rider does not exist.
    """
    with patch("riders.riders_service.Session", return_value=mock_db_session):
        # Rider does not exist, so .first() returns None
        query_mock = mock_db_session.query.return_value
        filter_mock = query_mock.filter_by.return_value
        filter_mock.first.return_value = None

        # Act
        rider = fetch_rider(rider_id=999)

        # Assert
        assert rider is None, "Expected None when the rider does not exist"
        mock_db_session.query.assert_called_once()
        filter_mock.first.assert_called_once()