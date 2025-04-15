import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch

# Required project-level imports
from main import create_app
from config import load_config
from payments.payments_service import calculate_fare, charge_rider, payout_driver

# -----------------------------------------------------------------------------
# FIXTURES
# -----------------------------------------------------------------------------

@pytest.fixture
def client():
    """
    Create a TestClient using the FastAPI app.
    """
    app = create_app()
    return TestClient(app)


@pytest.fixture
def test_db():
    """
    Provide a test database session fixture.
    This is a placeholder for setting up an in-memory or test database.
    """
    # SETUP: Initialize connection or create in-memory DB
    session = Session()  # In real usage, pass necessary engine or config
    
    yield session
    
    # TEARDOWN: Close session/connection, remove test data, etc.
    session.close()

# -----------------------------------------------------------------------------
# TESTS FOR calculate_fare
# -----------------------------------------------------------------------------

def test_calculate_fare_valid_input():
    """
    Test calculate_fare with valid inputs.
    Ensures it returns a fare without errors.
    """
    pickup_location = (37.7749, -122.4194)  # Example: San Francisco
    dropoff_location = (37.7849, -122.4094)  # Slightly different coords
    duration = 15.0  # minutes
    distance = 3.0   # kilometers

    # ACT
    fare = calculate_fare(
        pickup_location=pickup_location,
        dropoff_location=dropoff_location,
        duration=duration,
        distance=distance
    )

    # ASSERT
    assert fare > 0, "Fare should be positive for a valid ride"


def test_calculate_fare_zero_distance():
    """
    Test calculate_fare when distance is zero.
    Depending on business logic, fare should be minimal or zero.
    """
    pickup_location = (40.7128, -74.0060)  # Example: New York
    dropoff_location = (40.7128, -74.0060)  # Same coords
    duration = 10.0
    distance = 0.0

    fare = calculate_fare(
        pickup_location=pickup_location,
        dropoff_location=dropoff_location,
        duration=duration,
        distance=distance
    )

    assert fare >= 0, "Fare should be non-negative even if distance is zero"


def test_calculate_fare_negative_distance():
    """
    Test calculate_fare with a negative distance to ensure
    it either raises an error or handles invalid input gracefully.
    """
    pickup_location = (0.0, 0.0)
    dropoff_location = (1.0, 1.0)
    duration = 10.0
    distance = -5.0

    # Depending on implementation, it may raise an error or return 0.
    # Here we demonstrate expecting an exception.
    with pytest.raises(ValueError):
        calculate_fare(
            pickup_location=pickup_location,
            dropoff_location=dropoff_location,
            duration=duration,
            distance=distance
        )

# -----------------------------------------------------------------------------
# TESTS FOR charge_rider
# -----------------------------------------------------------------------------

def test_charge_rider_success(test_db):
    """
    Test charge_rider with a valid rider ID and amount.
    Use a mock to simulate external payment provider call.
    """
    rider_id = 123
    amount = 50.0

    with patch("payments.payments_service.some_external_payment_api.charge") as mock_charge:
        # Arrange mock behavior (simulate success)
        mock_charge.return_value = {
            "status": "success",
            "transaction_id": "abc123"
        }

        # Act
        result = charge_rider(rider_id, amount)

        # Assert
        assert result["status"] == "success", "Rider charge should succeed"
        mock_charge.assert_called_once_with(rider_id, amount)


def test_charge_rider_insufficient_funds(test_db):
    """
    Test charge_rider to simulate a payment failure, e.g., insufficient funds.
    """
    rider_id = 123
    amount = 999999.99  # Excessively large to trigger insufficient funds

    with patch("payments.payments_service.some_external_payment_api.charge") as mock_charge:
        # Arrange mock behavior (simulate failure)
        mock_charge.side_effect = Exception("Insufficient funds")

        # Act & Assert
        with pytest.raises(Exception, match="Insufficient funds"):
            charge_rider(rider_id, amount)

# -----------------------------------------------------------------------------
# TESTS FOR payout_driver
# -----------------------------------------------------------------------------

def test_payout_driver_success(test_db):
    """
    Test payout_driver with a valid driver ID and amount.
    Mock the external payout system to verify a successful payout.
    """
    driver_id = 789
    amount = 75.0

    with patch("payments.payments_service.some_external_payout_api.process_payout") as mock_payout:
        # Arrange mock behavior
        mock_payout.return_value = {
            "status": "success",
            "payout_id": "payout_123"
        }

        # Act
        result = payout_driver(driver_id, amount)

        # Assert
        assert result["status"] == "success", "Driver payout should be successful"
        mock_payout.assert_called_once_with(driver_id, amount)


def test_payout_driver_invalid_driver(test_db):
    """
    Test payout_driver with an invalid or non-existent driver ID.
    Expect the code to raise an exception or return an error.
    """
    driver_id = 999999
    amount = 50.0

    with patch("payments.payments_service.some_external_payout_api.process_payout") as mock_payout:
        # Arrange mock to raise an exception for invalid driver
        mock_payout.side_effect = Exception("Driver not found")

        # Act & Assert
        with pytest.raises(Exception, match="Driver not found"):
            payout_driver(driver_id, amount)