import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from main import create_app
from config import load_config

# Replace this import with actual model names once defined in riders_models
# For example: from riders.riders_models import Rider, RiderCreate
from riders.riders_models import (
    # Rider,  # Uncomment if you have a SQLAlchemy model named Rider
    # RiderCreate,  # Uncomment if you have a Pydantic model named RiderCreate
    RiderBase,
    Rider
)

# -------------------------------------------------------------------
# Database and FastAPI client fixtures
# -------------------------------------------------------------------
@pytest.fixture(scope="module")
def engine():
    """
    Create an in-memory SQLite engine for testing.
    """
    db_url = "sqlite:///:memory:"
    engine = create_engine(db_url, echo=False)
    yield engine
    engine.dispose()


@pytest.fixture(scope="module")
def session(engine):
    """
    Create tables and provide a Session for testing.
    """
    # If using SQLAlchemy declarative_base metadata, uncomment:
    # Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


@pytest.fixture()
def client():
    """
    Provide a TestClient instance for FastAPI endpoint tests
    (if needed).
    """
    app = create_app()
    return TestClient(app)


# -------------------------------------------------------------------
# Example Tests for Riders Models
# -------------------------------------------------------------------
def test_sqlalchemy_rider_model_creation_success(session: Session):
    """
    Test creating a SQLAlchemy Rider model instance with valid data.
    Ensures the model fields are assigned correctly.
    """
    # Uncomment and modify if Rider is a SQLAlchemy model
    """
    new_rider = Rider(
        name="Test Rider",
        phone_number="1234567890",
        payment_method="credit_card"
    )
    session.add(new_rider)
    session.commit()
    session.refresh(new_rider)

    assert new_rider.id is not None
    assert new_rider.name == "Test Rider"
    assert new_rider.phone_number == "1234567890"
    assert new_rider.payment_method == "credit_card"
    """


def test_sqlalchemy_rider_model_creation_failure_missing_fields(session: Session):
    """
    Test creating a SQLAlchemy Rider model instance with missing required fields.
    Expect an error or constraint failure.
    """
    # Uncomment and modify if Rider is a SQLAlchemy model
    """
    # Example of missing 'name'
    new_rider = Rider(
        phone_number="1234567890",
        payment_method="credit_card"
    )
    # Depending on your model constraints, this may raise an IntegrityError or similar.
    with pytest.raises(Exception):
        session.add(new_rider)
        session.commit()
    """


def test_pydantic_rider_create_model_success():
    """
    Test instantiating a Pydantic RiderCreate model with valid data.
    Ensures validation passes and fields match what was provided.
    """
    # Uncomment and modify if RiderCreate is a Pydantic model
    """
    rider_data = {
        "name": "Test Rider",
        "phone_number": "1234567890",
        "payment_method": "credit_card"
    }
    rider_create = RiderCreate(**rider_data)
    assert rider_create.name == "Test Rider"
    assert rider_create.phone_number == "1234567890"
    assert rider_create.payment_method == "credit_card"
    """


def test_pydantic_rider_create_model_failure():
    """
    Test instantiating a Pydantic RiderCreate model with invalid data.
    Ensures validation errors are raised.
    """
    # Uncomment and modify if RiderCreate is a Pydantic model
    """
    rider_data = {
        # Missing required fields, e.g., name
        "phone_number": "1234567890",
        "payment_method": "credit_card"
    }
    with pytest.raises(ValueError):
        RiderCreate(**rider_data)
    """


def test_rider_model_creation():
    # Test creating a Rider model
    rider_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone_number": "1234567890"
    }
    
    rider = Rider(**rider_data)
    assert rider.first_name == "John"
    assert rider.last_name == "Doe"
    assert rider.email == "john.doe@example.com"
    assert rider.phone_number == "1234567890"