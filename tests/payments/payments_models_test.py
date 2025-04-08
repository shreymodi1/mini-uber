import pytest
from pydantic import ValidationError
from ...payments.payments_models import PaymentRecord, FareLog, PayoutDetail

# -----------------------------------------------------------------------------------
# These tests cover basic validation and instantiation logic for the payment models.
# Tests include both success scenarios (valid data) and error scenarios (invalid data).
# -----------------------------------------------------------------------------------

@pytest.fixture
def setup_teardown():
    """
    Fixture for setting up resources before tests and cleaning up afterwards.
    In a real-world scenario, this could initialize a test database session
    or set up other necessary test resources.
    """
    # Setup phase: (e.g., connect to an in-memory DB, mock services, etc.)
    yield
    # Teardown phase: (e.g., close DB connections, clean up mock objects, etc.)


# -----------------------------------------------------------------------------------
# PaymentRecord Model Tests
# -----------------------------------------------------------------------------------

def test_create_payment_record_success(setup_teardown):
    """
    Test creating a PaymentRecord with all required fields and valid data.
    Expect: Success with no errors.
    """
    payment = PaymentRecord(
        id=1,
        amount=100.00,
        currency="USD",
        status="completed",
        created_at="2023-10-10T10:00:00Z",
        updated_at="2023-10-10T10:05:00Z"
    )
    assert payment.id == 1
    assert payment.amount == 100.00
    assert payment.currency == "USD"
    assert payment.status == "completed"


def test_create_payment_record_missing_required_field(setup_teardown):
    """
    Test creating a PaymentRecord with a missing required field.
    Expect: Raises ValidationError.
    """
    with pytest.raises(ValidationError) as exc_info:
        PaymentRecord(
            # 'amount' is missing
            id=1,
            currency="USD",
            status="completed",
            created_at="2023-10-10T10:00:00Z",
            updated_at="2023-10-10T10:05:00Z"
        )
    assert "field required" in str(exc_info.value)


def test_create_payment_record_invalid_amount(setup_teardown):
    """
    Test creating a PaymentRecord with an invalid amount (e.g., negative).
    Expect: Raises ValidationError.
    """
    with pytest.raises(ValidationError) as exc_info:
        PaymentRecord(
            id=1,
            amount=-50.00,  # Invalid negative value
            currency="USD",
            status="completed",
            created_at="2023-10-10T10:00:00Z",
            updated_at="2023-10-10T10:05:00Z"
        )
    assert "ensure this value is greater than or equal to 0" in str(exc_info.value)


# -----------------------------------------------------------------------------------
# FareLog Model Tests
# -----------------------------------------------------------------------------------

def test_create_fare_log_success(setup_teardown):
    """
    Test creating a FareLog with valid data.
    Expect: Success with correct field assignments.
    """
    fare_log = FareLog(
        id=1,
        distance=12.5,
        cost=30.00,
        created_at="2023-10-10T09:00:00Z"
    )
    assert fare_log.id == 1
    assert fare_log.distance == 12.5
    assert fare_log.cost == 30.00


def test_create_fare_log_missing_required_field(setup_teardown):
    """
    Test creating a FareLog with a missing required field.
    Expect: Raises ValidationError due to missing 'distance'.
    """
    with pytest.raises(ValidationError) as exc_info:
        FareLog(
            id=2,
            cost=25.00,
            created_at="2023-10-10T09:30:00Z"
        )
    assert "field required" in str(exc_info.value)


def test_create_fare_log_negative_distance(setup_teardown):
    """
    Test creating a FareLog with a negative distance.
    Expect: Raises ValidationError if the model disallows negative distances.
    """
    with pytest.raises(ValidationError) as exc_info:
        FareLog(
            id=3,
            distance=-5.0,
            cost=10.00,
            created_at="2023-10-10T09:45:00Z"
        )
    assert "ensure this value is greater than or equal to 0" in str(exc_info.value)


# -----------------------------------------------------------------------------------
# PayoutDetail Model Tests
# -----------------------------------------------------------------------------------

def test_create_payout_detail_success(setup_teardown):
    """
    Test creating a PayoutDetail with valid data.
    Expect: Success with all fields correctly assigned.
    """
    payout = PayoutDetail(
        id=1,
        user_id=101,
        amount=150.00,
        method="bank_transfer",
        status="pending",
        created_at="2023-10-10T11:00:00Z"
    )
    assert payout.id == 1
    assert payout.user_id == 101
    assert payout.amount == 150.00
    assert payout.method == "bank_transfer"
    assert payout.status == "pending"


def test_create_payout_detail_missing_required_field(setup_teardown):
    """
    Test creating a PayoutDetail with a missing required field.
    Expect: Raises ValidationError for missing 'method'.
    """
    with pytest.raises(ValidationError) as exc_info:
        PayoutDetail(
            id=2,
            user_id=102,
            amount=200.00,
            status="pending",
            created_at="2023-10-10T11:15:00Z"
        )
    assert "field required" in str(exc_info.value)


def test_create_payout_detail_negative_amount(setup_teardown):
    """
    Test creating a PayoutDetail with a negative amount.
    Expect: Raises ValidationError for invalid amount.
    """
    with pytest.raises(ValidationError) as exc_info:
        PayoutDetail(
            id=3,
            user_id=103,
            amount=-50.00,
            method="paypal",
            status="failed",
            created_at="2023-10-10T11:30:00Z"
        )
    assert "ensure this value is greater than or equal to 0" in str(exc_info.value)