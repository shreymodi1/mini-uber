import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic import ValidationError

# Import the models from the main project
# Adjust imports based on your actual model names/classes
from ...ratings.ratings_models import Rating, RatingCreate, RatingUpdate  # Example imports
from ...models import Base  # Replace with your actual Base or metadata import

# --------------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------------

@pytest.fixture(scope="module")
def test_engine():
    """
    Fixture to create a new in-memory SQLite database engine for testing.
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="module")
def test_db_session(test_engine):
    """
    Fixture to create a new session for each test function.
    It uses the test_engine fixture's in-memory database.
    """
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def valid_rating_data():
    """
    Provides valid rating data for Pydantic model testing.
    """
    return {
        "user_id": 1,
        "value": 5,
        "comment": "Great product!"
    }


# --------------------------------------------------------------------------------
# Pydantic Model Tests
# --------------------------------------------------------------------------------

def test_ratingcreate_model_valid(valid_rating_data):
    """
    Test that the RatingCreate Pydantic model successfully
    creates an instance with valid data.
    """
    rating_create = RatingCreate(**valid_rating_data)
    assert rating_create.user_id == valid_rating_data["user_id"]
    assert rating_create.value == valid_rating_data["value"]
    assert rating_create.comment == valid_rating_data["comment"]


def test_ratingcreate_model_invalid_value(valid_rating_data):
    """
    Test that the RatingCreate Pydantic model raises a ValidationError
    when the rating value is invalid (e.g., below 1 or above a certain limit).
    Adjust the condition to match your model constraints.
    """
    invalid_data = valid_rating_data.copy()
    invalid_data["value"] = 999  # Example of an invalid rating

    with pytest.raises(ValidationError):
        RatingCreate(**invalid_data)


def test_ratingupdate_model_valid():
    """
    Test that the RatingUpdate model allows partial updates
    and can create a valid instance with optional fields.
    """
    updates = {"value": 3, "comment": "Updated comment"}
    rating_update = RatingUpdate(**updates)
    assert rating_update.value == 3
    assert rating_update.comment == "Updated comment"


# --------------------------------------------------------------------------------
# SQLAlchemy Model Tests
# --------------------------------------------------------------------------------

def test_create_rating_in_db(test_db_session: Session):
    """
    Test creating a new Rating record in the database.
    Checks if the record is persisted correctly.
    """
    rating = Rating(user_id=2, value=4, comment="Nice experience")
    test_db_session.add(rating)
    test_db_session.commit()
    test_db_session.refresh(rating)

    assert rating.id is not None
    assert rating.user_id == 2
    assert rating.value == 4
    assert rating.comment == "Nice experience"


def test_read_rating_from_db(test_db_session: Session):
    """
    Test reading a Rating record from the database 
    after creation to ensure it's retrievable.
    """
    # Create a new rating
    new_rating = Rating(user_id=3, value=5, comment="Excellent!")
    test_db_session.add(new_rating)
    test_db_session.commit()
    test_db_session.refresh(new_rating)

    # Now retrieve it
    stored_rating = test_db_session.query(Rating).filter_by(id=new_rating.id).first()
    assert stored_rating is not None
    assert stored_rating.id == new_rating.id
    assert stored_rating.user_id == 3
    assert stored_rating.value == 5
    assert stored_rating.comment == "Excellent!"


def test_update_rating_in_db(test_db_session: Session):
    """
    Test updating an existing Rating record in the database.
    """
    # Create and commit a new rating
    rating = Rating(user_id=4, value=2, comment="Test comment")
    test_db_session.add(rating)
    test_db_session.commit()
    test_db_session.refresh(rating)

    # Update the rating
    rating.value = 3
    rating.comment = "Updated comment"
    test_db_session.commit()
    test_db_session.refresh(rating)

    assert rating.value == 3
    assert rating.comment == "Updated comment"


def test_delete_rating_in_db(test_db_session: Session):
    """
    Test deleting a Rating record from the database.
    Verifies the record no longer exists after deletion.
    """
    # Create and commit a new rating
    rating = Rating(user_id=5, value=1, comment="Will be deleted")
    test_db_session.add(rating)
    test_db_session.commit()
    test_db_session.refresh(rating)

    # Delete the rating
    test_db_session.delete(rating)
    test_db_session.commit()

    # Verify it no longer exists
    deleted = test_db_session.query(Rating).filter_by(id=rating.id).first()
    assert deleted is None