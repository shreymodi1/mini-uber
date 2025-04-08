import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Import the SQLAlchemy Base (if defined) and models from the drivers_models module
from ...drivers.drivers_models import Base, Driver, Vehicle

# -----------------------------------------------------------------------------------
# FIXTURES
# -----------------------------------------------------------------------------------

@pytest.fixture(scope="module")
def test_engine():
    """
    Create an in-memory SQLite database engine for testing.
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="function")
def db_session(test_engine) -> Session:
    """
    Create a new database session for each test and tear it down afterward.
    """
    connection = test_engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# -----------------------------------------------------------------------------------
# TESTS FOR DRIVER MODEL
# -----------------------------------------------------------------------------------

def test_create_driver_success(db_session: Session):
    """
    Test creating a Driver instance with valid data and ensuring
    it is properly persisted to the database.
    """
    new_driver = Driver(name="John Doe", license_number="ABC12345")
    db_session.add(new_driver)
    db_session.commit()
    db_session.refresh(new_driver)

    assert new_driver.id is not None, "Driver ID should be set after commit."
    assert new_driver.name == "John Doe", "Driver name should match the input."
    assert new_driver.license_number == "ABC12345", "Driver license number should match the input."


def test_create_driver_missing_name(db_session: Session):
    """
    Test creating a Driver with missing required field (e.g., name).
    This should fail if 'name' is a non-nullable column or validated.
    """
    driver = Driver(name=None, license_number="XYZ9876")
    
    db_session.add(driver)
    with pytest.raises(Exception):
        # Expecting an IntegrityError or similar if 'name' is a required field
        db_session.commit()


# -----------------------------------------------------------------------------------
# TESTS FOR VEHICLE MODEL
# -----------------------------------------------------------------------------------

def test_create_vehicle_success(db_session: Session):
    """
    Test creating a Vehicle instance with valid data.
    Ensures the vehicle is saved to the database.
    """
    # Create a driver first to satisfy foreign key constraints if necessary
    driver = Driver(name="Jane Doe", license_number="DEF6789")
    db_session.add(driver)
    db_session.commit()
    db_session.refresh(driver)

    new_vehicle = Vehicle(model="Test Model", license_plate="XYZ-1234", driver_id=driver.id)
    db_session.add(new_vehicle)
    db_session.commit()
    db_session.refresh(new_vehicle)

    assert new_vehicle.id is not None, "Vehicle ID should be set after commit."
    assert new_vehicle.driver_id == driver.id, "Driver ID should match the associated driver."


def test_create_vehicle_missing_model(db_session: Session):
    """
    Test creating a Vehicle with a missing required field (e.g., model).
    This should fail if 'model' is a non-nullable column or validated.
    """
    # Create a driver
    driver = Driver(name="Sam Smith", license_number="GHI5432")
    db_session.add(driver)
    db_session.commit()
    db_session.refresh(driver)

    vehicle = Vehicle(model=None, license_plate="NO-MODL", driver_id=driver.id)
    db_session.add(vehicle)
    with pytest.raises(Exception):
        # Expecting an IntegrityError or similar if 'model' is a required field
        db_session.commit()


def test_vehicle_driver_relationship(db_session: Session):
    """
    Test that the relationship between Vehicle and Driver is set up correctly.
    """
    driver = Driver(name="Alex Johnson", license_number="LMN1122")
    db_session.add(driver)
    db_session.commit()
    db_session.refresh(driver)

    vehicle = Vehicle(model="Relationship Test", license_plate="RLT-123", driver_id=driver.id)
    db_session.add(vehicle)
    db_session.commit()
    db_session.refresh(vehicle)

    # Access the driver through the relationship
    assert vehicle.driver is not None, "Vehicle should have an associated driver."
    assert vehicle.driver.name == "Alex Johnson", "Vehicle's driver name should match."
    assert vehicle.driver.license_number == "LMN1122", "License number should match the driver's."