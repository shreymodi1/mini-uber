import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime

# Import models (assuming the file has a SQLAlchemy Ride model and possibly others)
from ...rides.rides_models import Base, Ride


# -----------------------------------------------------------------------------
# Fixtures: Setup and Teardown
# -----------------------------------------------------------------------------
@pytest.fixture(scope="module")
def test_engine():
    """
    Creates an in-memory SQLite test database engine for use in tests.
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    yield engine
    # No teardown needed as in-memory DB is destroyed once connection is closed.


@pytest.fixture
def db_session(test_engine) -> Session:
    """
    Provides a scoped session for tests, rolling back any changes after each test.
    """
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


# -----------------------------------------------------------------------------
# Tests for Ride Model
# -----------------------------------------------------------------------------
def test_ride_model_creation_success(db_session: Session):
    """
    Test successful creation of a Ride model instance with valid data.
    """
    new_ride = Ride(
        start_location="Location A",
        end_location="Location B",
        status="ongoing",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db_session.add(new_ride)
    db_session.commit()
    db_session.refresh(new_ride)

    assert new_ride.id is not None, "Expected Ride ID to be set after commit."
    assert new_ride.start_location == "Location A"
    assert new_ride.end_location == "Location B"
    assert new_ride.status == "ongoing"


def test_ride_model_missing_fields(db_session: Session):
    """
    Test model creation with missing required fields to ensure integrity is enforced.
    Depending on how the model is defined (nullable or not), this may raise errors.
    """
    # Example: If start_location is not nullable, check for IntegrityError or similar.
    incomplete_ride = Ride(end_location="Location C", status="completed")
    db_session.add(incomplete_ride)

    with pytest.raises(Exception) as exc_info:
        db_session.commit()

    db_session.rollback()
    assert "IntegrityError" in str(exc_info.value) or "not null" in str(exc_info.value), (
        "Expected a database integrity error when required field is missing."
    )


def test_ride_model_default_status(db_session: Session):
    """
    Test that a default status is assigned if the model or DB sets a default
    and status is not provided.
    """
    default_ride = Ride(start_location="Location D", end_location="Location E")
    db_session.add(default_ride)
    db_session.commit()
    db_session.refresh(default_ride)

    # Adjust this assertion based on actual default set in the model.
    # For example, if default status is "pending":
    assert default_ride.status == "pending", "Expected ride to have default status 'pending'."


def test_ride_model_updating_fields(db_session: Session):
    """
    Test that updating a Ride record's fields works and the record is correctly refreshed.
    """
    ride = Ride(
        start_location="Location X",
        end_location="Location Y",
        status="ongoing",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db_session.add(ride)
    db_session.commit()
    db_session.refresh(ride)

    # Update fields
    ride.status = "completed"
    ride.end_location = "Updated Location"
    db_session.commit()
    db_session.refresh(ride)

    assert ride.status == "completed", "Expected ride status to be updated to 'completed'."
    assert ride.end_location == "Updated Location", "Expected ride end_location to be updated."


def test_ride_model_deletion(db_session: Session):
    """
    Test that a Ride record can be deleted successfully.
    """
    ride_to_delete = Ride(
        start_location="Delete Start",
        end_location="Delete End",
        status="ongoing",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db_session.add(ride_to_delete)
    db_session.commit()
    db_session.refresh(ride_to_delete)
    ride_id = ride_to_delete.id

    db_session.delete(ride_to_delete)
    db_session.commit()

    # Attempt to retrieve the deleted record
    deleted_ride = db_session.query(Ride).filter_by(id=ride_id).first()
    assert deleted_ride is None, "Expected ride record to be deleted from the database."