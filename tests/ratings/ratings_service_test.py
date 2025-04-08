import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session

# Always import the functions under test from the service module
from ...ratings.ratings_service import (
    rate_driver,
    rate_rider,
    get_rider_rating,
    get_driver_rating
)

# Import any models as needed (this is illustrative; adjust based on your actual models)
from ...models import Ride, Rating, Driver, Rider


@pytest.fixture
def mock_db_session():
    """
    Pytest fixture that provides a mock Session object.
    This fixture can be used in tests to avoid real database interactions.
    """
    return MagicMock(spec=Session)


###############################
# rate_driver Tests
###############################

@pytest.mark.parametrize("rating_value, review_text", [
    (5, "Excellent driver!"),
    (3, "Average service")
])
def test_rate_driver_success(mock_db_session, rating_value, review_text):
    """
    Test that a valid driver rating is successfully saved and the driver's overall rating is updated.
    """
    # Arrange: Mock a ride and driver record
    mock_ride = Ride(id=1, driver_id=10, rider_id=20)
    mock_driver = Driver(id=10, overall_rating=4.0)  # hypothetical initial overall rating
    # Set up mock query results
    mock_db_session.query().filter_by().first.side_effect = [mock_ride, mock_driver]

    # Act: Rate the driver
    rate_driver(ride_id=1, rating=rating_value, review=review_text, db=mock_db_session)

    # Assert: Ensure a new Rating record is added and driver's rating is updated
    assert mock_db_session.add.called, "Expected a Rating object to be added to the session."
    assert mock_db_session.commit.called, "Expected the session to commit after adding a rating."
    # Verify that the driver's overall rating was recomputed and updated (implementation-specific check)
    update_call = mock_db_session.add.call_args[0][0]
    assert isinstance(update_call, Rating), "Should create a Rating instance."
    assert update_call.rating == rating_value, "Rating should match the provided value."
    # Check that the driver's rating was updated (this might be part of the business logic to recalc average)
    # Adjust the following check based on how your code actually updates driver rating
    mock_db_session.query().filter_by().first.assert_called()


def test_rate_driver_invalid_ride(mock_db_session):
    """
    Test that rating a driver fails if the ride does not exist.
    """
    # Arrange: The ride query should return None to simulate invalid ride
    mock_db_session.query().filter_by().first.return_value = None

    # Act & Assert: An exception or specific handling might occur if ride doesn't exist
    with pytest.raises(ValueError, match="Ride not found"):
        rate_driver(ride_id=99, rating=5, review="No ride here", db=mock_db_session)


@pytest.mark.parametrize("invalid_rating", [-1, 6])
def test_rate_driver_out_of_range(mock_db_session, invalid_rating):
    """
    Test that rating a driver fails if the rating is out of allowed range (usually 1-5).
    """
    # Arrange: Return a valid ride but attempt to save an invalid rating
    mock_ride = Ride(id=1, driver_id=10, rider_id=20)
    mock_db_session.query().filter_by().first.side_effect = [mock_ride, Driver(id=10)]

    # Act & Assert: Expect an exception or validation error
    with pytest.raises(ValueError, match="Invalid rating"):
        rate_driver(ride_id=1, rating=invalid_rating, review="Out of range", db=mock_db_session)


###############################
# rate_rider Tests
###############################

@pytest.mark.parametrize("rating_value, review_text", [
    (5, "Great passenger"),
    (2, "Could be more polite")
])
def test_rate_rider_success(mock_db_session, rating_value, review_text):
    """
    Test that a valid rider rating is successfully saved and the rider's overall rating is updated.
    """
    # Arrange: Mock a ride and rider record
    mock_ride = Ride(id=1, driver_id=10, rider_id=20)
    mock_rider = Rider(id=20, overall_rating=4.5)  # hypothetical initial overall rating
    # Set up mock query results
    mock_db_session.query().filter_by().first.side_effect = [mock_ride, mock_rider]

    # Act: Rate the rider
    rate_rider(ride_id=1, rating=rating_value, review=review_text, db=mock_db_session)

    # Assert: Check that the rating was added and committed
    assert mock_db_session.add.called, "Expected a Rating object to be added to the session."
    assert mock_db_session.commit.called, "Expected the session to commit after adding a rating."
    new_rating = mock_db_session.add.call_args[0][0]
    assert new_rating.rating == rating_value, "Rating should match the provided value."


def test_rate_rider_invalid_ride(mock_db_session):
    """
    Test that rating a rider fails if the ride cannot be found.
    """
    # Arrange: Return None for the ride
    mock_db_session.query().filter_by().first.return_value = None

    # Act & Assert: Expect an exception due to invalid ride
    with pytest.raises(ValueError, match="Ride not found"):
        rate_rider(ride_id=99, rating=5, review="Invalid ride", db=mock_db_session)


@pytest.mark.parametrize("invalid_rating", [0, 10])
def test_rate_rider_out_of_range(mock_db_session, invalid_rating):
    """
    Test that rating a rider fails if the rating is out of allowed range (e.g., 1-5).
    """
    # Arrange: Return a valid ride but use an invalid rating
    mock_ride = Ride(id=1, driver_id=10, rider_id=20)
    mock_db_session.query().filter_by().first.side_effect = [mock_ride, Rider(id=20)]

    # Act & Assert: Expect an exception due to invalid rating
    with pytest.raises(ValueError, match="Invalid rating"):
        rate_rider(ride_id=1, rating=invalid_rating, review="Out of range", db=mock_db_session)


###############################
# get_rider_rating Tests
###############################

def test_get_rider_rating_success(mock_db_session):
    """
    Test that retrieving an existing rider's overall rating succeeds.
    """
    # Arrange: Mock a rider record with a known overall rating
    mock_rider = Rider(id=20, overall_rating=4.2)
    mock_db_session.query().filter_by().first.return_value = mock_rider

    # Act
    rating = get_rider_rating(rider_id=20, db=mock_db_session)

    # Assert
    assert rating == 4.2, "Should return the correct overall rating for the rider."


def test_get_rider_rating_not_found(mock_db_session):
    """
    Test that None or an appropriate exception is returned if rider does not exist.
    """
    # Arrange: No matching rider
    mock_db_session.query().filter_by().first.return_value = None

    # Act
    rating = get_rider_rating(rider_id=999, db=mock_db_session)

    # Assert
    assert rating is None, "Expected None when rider is not found."


###############################
# get_driver_rating Tests
###############################

def test_get_driver_rating_success(mock_db_session):
    """
    Test that retrieving an existing driver's overall rating succeeds.
    """
    # Arrange: Mock a driver record
    mock_driver = Driver(id=10, overall_rating=3.8)
    mock_db_session.query().filter_by().first.return_value = mock_driver

    # Act
    rating = get_driver_rating(driver_id=10, db=mock_db_session)

    # Assert
    assert rating == 3.8, "Should return the correct overall rating for the driver."


def test_get_driver_rating_not_found(mock_db_session):
    """
    Test that None or an appropriate response is returned if the driver does not exist.
    """
    # Arrange: No matching driver
    mock_db_session.query().filter_by().first.return_value = None

    # Act
    rating = get_driver_rating(driver_id=999, db=mock_db_session)

    # Assert
    assert rating is None, "Expected None when driver is not found."