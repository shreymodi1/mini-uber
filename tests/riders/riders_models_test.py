import pytest
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# ------------------------------------------------------------------
# Necessary relative imports for the models and base
# Adjust these imports based on your actual file structure and names
# ------------------------------------------------------------------
from ...models import Base  # SQLAlchemy Base for metadata creation
from ...riders.riders_models import Rider, RiderCreate  # Example models to test


# ------------------------------------------------------------------
# Fixtures for setting up and tearing down an in-memory test database
# ------------------------------------------------------------------
@pytest.fixture(scope="module")
def db_engine():
    """
    Creates an in-memory SQLite engine for testing.
    This runs once per test session module.
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    Provides a fresh database session for each test.
    Rolls back transactions between tests to keep them isolated.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = TestSession()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# ------------------------------------------------------------------
# Pydantic Model Tests (RiderCreate example)
# ------------------------------------------------------------------
def test_rider_create_model_valid_data():
    """
    Test that a RiderCreate Pydantic model
    is valid when correct data is provided.
    """
    valid_data = {
        "name": "John Doe",
        "age": 30
    }
    rider = RiderCreate(**valid_data)
    assert rider.name == "John Doe"
    assert rider.age == 30


def test_rider_create_model_missing_name():
    """
    Test that a ValidationError is raised
    when 'name' is missing from RiderCreate data.
    """
    invalid_data = {
        "age": 25
    }
    with pytest.raises(ValidationError):
        RiderCreate(**invalid_data)


def test_rider_create_model_invalid_age():
    """
    Test that a ValidationError is raised when 'age' has an invalid value.
    For example, negative ages might be disallowed.
    Adjust the expected behavior based on your model validation.
    """
    invalid_data = {
        "name": "Jane Doe",
        "age": -5
    }
    with pytest.raises(ValidationError):
        RiderCreate(**invalid_data)


# ------------------------------------------------------------------
# SQLAlchemy Model Tests (Rider example)
# ------------------------------------------------------------------
def test_rider_model_persistence(db_session: Session):
    """
    Test that a Rider SQLAlchemy model instance can be
    persisted and retrieved from the database.
    """
    new_rider = Rider(name="Alice", age=28)
    db_session.add(new_rider)
    db_session.commit()
    db_session.refresh(new_rider)

    assert new_rider.id is not None, "Rider ID should be auto-generated"
    assert new_rider.name == "Alice"
    assert new_rider.age == 28


def test_rider_model_update(db_session: Session):
    """
    Test updating an existing Rider's attributes.
    """
    rider = Rider(name="Bob", age=40)
    db_session.add(rider)
    db_session.commit()
    db_session.refresh(rider)

    # Update the rider's name and age
    rider.name = "Bob Updated"
    rider.age = 41
    db_session.commit()
    db_session.refresh(rider)

    assert rider.name == "Bob Updated"
    assert rider.age == 41


def test_rider_model_delete(db_session: Session):
    """
    Test that a Rider can be deleted from the database
    and is no longer retrievable.
    """
    rider_to_delete = Rider(name="Temp Rider", age=22)
    db_session.add(rider_to_delete)
    db_session.commit()
    db_session.refresh(rider_to_delete)

    # Delete the rider
    db_session.delete(rider_to_delete)
    db_session.commit()

    # Attempt to retrieve the deleted rider
    deleted_rider = db_session.query(Rider).filter_by(id=rider_to_delete.id).first()
    assert deleted_rider is None, "Deleted rider should not be found in the database"