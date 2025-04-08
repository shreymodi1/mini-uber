import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

# Import the Rider model (adjust the actual model name if it's different)
from ...models import Rider

# Import the functions to test from the riders_service module
from ...riders.riders_service import create_rider, fetch_rider


@pytest.fixture
def mock_db_session():
    """
    Fixture to create a mock database session for each test.
    """
    return MagicMock(spec=Session)


@pytest.mark.parametrize(
    "name, phone_number, payment_method",
    [
        ("John Doe", "1234567890", "credit_card"),
        ("Jane Smith", "0987654321", "cash"),
    ],
)
def test_create_rider_success(mock_db_session, name, phone_number, payment_method):
    """
    Test that create_rider successfully creates a rider
    with valid input and calls the necessary DB methods.
    """
    # Call the function under test
    rider = create_rider(name, phone_number, payment_method, db_session=mock_db_session)

    # Assertions to ensure Rider object is created correctly
    assert rider.name == name
    assert rider.phone_number == phone_number
    assert rider.payment_method == payment_method

    # Check DB session calls
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(rider)


def test_create_rider_missing_name(mock_db_session):
    """
    Test that create_rider raises ValueError (or similar) 
    when the name parameter is missing or invalid.
    """
    with pytest.raises(ValueError):
        create_rider(name=None, phone_number="1234567890", payment_method="credit_card", db_session=mock_db_session)


@patch("...riders.riders_service.Rider")  # Mock the Rider class itself if needed
def test_create_rider_db_error(mock_rider_class, mock_db_session):
    """
    Test that create_rider handles a database error by rolling back
    and re-raising the exception (or returning an appropriate error).
    """
    # Simulate an exception when adding to the session
    mock_db_session.add.side_effect = Exception("DB error")

    with pytest.raises(Exception, match="DB error"):
        create_rider("John Doe", "1234567890", "credit_card", db_session=mock_db_session)

    # Ensure rollback was called on exception
    mock_db_session.rollback.assert_called_once()


def test_fetch_rider_success(mock_db_session):
    """
    Test that fetch_rider returns the correct Rider object
    when the record exists in the database.
    """
    # Mock a Rider object
    mock_rider = Rider(id=1, name="John Doe", phone_number="1234567890", payment_method="credit_card")

    # Configure the query to return the mock_rider
    mock_db_session.query.return_value.get.return_value = mock_rider

    # Call the function
    fetched_rider = fetch_rider(rider_id=1, db_session=mock_db_session)

    # Verify the returned rider matches
    assert fetched_rider == mock_rider
    mock_db_session.query.assert_called_once()


def test_fetch_rider_not_found(mock_db_session):
    """
    Test that fetch_rider returns None (or handles properly)
    when the rider does not exist in the database.
    """
    # Configure the query to return None
    mock_db_session.query.return_value.get.return_value = None

    # Call the function
    fetched_rider = fetch_rider(rider_id=999, db_session=mock_db_session)

    # Verify the function returns None
    assert fetched_rider is None
    mock_db_session.query.assert_called_once()