import pytest
from unittest.mock import patch, MagicMock

# Import the functions to test from the payments_service module
from ...payments.payments_service import calculate_fare, charge_rider, payout_driver


# ---------------------------------------------------------------------------
# Fixtures (if you need to set up a DB session or other state)
# ---------------------------------------------------------------------------
@pytest.fixture
def mock_db_session():
    """
    Mock database session fixture (replace with a real session if needed).
    """
    mock_session = MagicMock()
    return mock_session


# ---------------------------------------------------------------------------
# Test calculate_fare
# ---------------------------------------------------------------------------
def test_calculate_fare_valid_inputs():
    """
    Test that calculate_fare returns a valid fare amount
    given normal inputs.
    """
    fare = calculate_fare(
        pickup_location="LocationA",
        dropoff_location="LocationB",
        duration=30,   # duration in minutes
        distance=10.0  # distance in kilometers
    )
    assert fare > 0, "Fare should be greater than 0 for valid trip data"


def test_calculate_fare_zero_distance():
    """
    Test that calculate_fare handles zero distance and
    returns a minimal fare or 0.
    """
    fare = calculate_fare(
        pickup_location="LocationA",
        dropoff_location="LocationB",
        duration=20,
        distance=0.0
    )
    # Depending on business rules, fare could be minimal or 0
    assert fare >= 0, "Fare should be >= 0 for zero distance"


def test_calculate_fare_negative_values():
    """
    Test that calculate_fare raises an error or returns 0
    when duration or distance is negative.
    """
    with pytest.raises(ValueError):
        calculate_fare(
            pickup_location="LocationA",
            dropoff_location="LocationB",
            duration=-10,
            distance=5.0
        )


# ---------------------------------------------------------------------------
# Test charge_rider
# ---------------------------------------------------------------------------
@patch("...payments.payments_service.some_payment_provider_api.charge")
def test_charge_rider_success(mock_charge):
    """
    Test that charge_rider succeeds when the external payment provider
    confirms the payment.
    """
    mock_charge.return_value = {"status": "success"}
    response = charge_rider(rider_id=123, amount=50.0)
    assert response["status"] == "success", "Expected successful charge response"


@patch("...payments.payments_service.some_payment_provider_api.charge")
def test_charge_rider_insufficient_funds(mock_charge):
    """
    Test that charge_rider handles insufficient funds error
    from the payment provider.
    """
    mock_charge.return_value = {"status": "failure", "reason": "insufficient_funds"}
    response = charge_rider(rider_id=123, amount=1000.0)
    assert response["status"] == "failure", "Expected failure response for insufficient funds"
    assert response["reason"] == "insufficient_funds", "Expected 'insufficient_funds' reason"


@patch("...payments.payments_service.some_payment_provider_api.charge")
def test_charge_rider_invalid_rider(mock_charge):
    """
    Test that charge_rider raises an exception or returns a specific response
    when the rider ID is invalid.
    """
    mock_charge.side_effect = ValueError("Invalid Rider")
    with pytest.raises(ValueError, match="Invalid Rider"):
        charge_rider(rider_id=None, amount=50.0)


# ---------------------------------------------------------------------------
# Test payout_driver
# ---------------------------------------------------------------------------
@patch("...payments.payments_service.some_payment_provider_api.payout")
def test_payout_driver_success(mock_payout):
    """
    Test that payout_driver succeeds when the external payment provider
    confirms the payout.
    """
    mock_payout.return_value = {"status": "success"}
    response = payout_driver(driver_id=456, amount=75.0)
    assert response["status"] == "success", "Expected successful payout response"


@patch("...payments.payments_service.some_payment_provider_api.payout")
def test_payout_driver_invalid_driver(mock_payout):
    """
    Test that payout_driver handles invalid driver error
    from the payment provider.
    """
    mock_payout.side_effect = ValueError("Invalid Driver")
    with pytest.raises(ValueError, match="Invalid Driver"):
        payout_driver(driver_id=None, amount=50.0)


@patch("...payments.payments_service.some_payment_provider_api.payout")
def test_payout_driver_negative_amount(mock_payout):
    """
    Test that payout_driver raises an exception for negative amounts.
    """
    with pytest.raises(ValueError):
        payout_driver(driver_id=456, amount=-10.0)