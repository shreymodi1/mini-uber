import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import create_app
from riders.riders_service import create_rider, fetch_rider


@pytest.fixture
def client():
    """
    Fixture to initialize the FastAPI test client using the main.py create_app function.
    """
    app = create_app()
    return TestClient(app)


@pytest.fixture
def mock_create_rider(mocker):
    """
    Fixture to mock out the create_rider service call to prevent actual DB interaction.
    """
    return mocker.patch("riders.riders_service.create_rider")


@pytest.fixture
def mock_fetch_rider(mocker):
    """
    Fixture to mock out the fetch_rider service call to prevent actual DB interaction.
    """
    return mocker.patch("riders.riders_service.fetch_rider")


def test_create_rider_endpoint_success(client, mock_create_rider):
    """
    Test the rider creation endpoint with valid data.
    Expects 201 status and a success response structure.
    """
    # Arrange
    mock_create_rider.return_value = {
        "id": 1,
        "name": "John Doe",
        "phone_number": "1234567890",
        "payment_method": "credit_card"
    }
    request_data = {
        "name": "John Doe",
        "phone_number": "1234567890",
        "payment_method": "credit_card"
    }

    # Act
    response = client.post("/riders", json=request_data)

    # Assert
    assert response.status_code == 201
    assert response.json()["id"] == 1
    mock_create_rider.assert_called_once_with(
        name="John Doe",
        phone_number="1234567890",
        payment_method="credit_card"
    )


def test_create_rider_endpoint_bad_request(client, mock_create_rider):
    """
    Test the rider creation endpoint with incomplete data.
    Expects a 422 (Unprocessable Entity) or 400 (Bad Request) for invalid payload.
    """
    request_data = {
        # 'name' is missing
        "phone_number": "1234567890",
        "payment_method": "credit_card"
    }

    response = client.post("/riders", json=request_data)

    # The endpoint should validate input and return 422 or similar
    assert response.status_code in [400, 422]
    mock_create_rider.assert_not_called()


def test_get_rider_profile_endpoint_success(client, mock_fetch_rider):
    """
    Test the get rider profile endpoint with an existing rider ID.
    Expects 200 status and correct rider data in the response.
    """
    mock_fetch_rider.return_value = {
        "id": 2,
        "name": "Jane Roe",
        "phone_number": "0987654321",
        "payment_method": "paypal"
    }
    rider_id = 2

    response = client.get(f"/riders/{rider_id}")

    assert response.status_code == 200
    assert response.json()["id"] == 2
    assert response.json()["name"] == "Jane Roe"
    mock_fetch_rider.assert_called_once_with(rider_id=2)


def test_get_rider_profile_endpoint_not_found(client, mock_fetch_rider):
    """
    Test the get rider profile endpoint with a non-existent rider ID.
    Expects 404 status when the rider is not found.
    """
    mock_fetch_rider.return_value = None
    rider_id = 999  # Non-existent rider ID for testing

    response = client.get(f"/riders/{rider_id}")

    assert response.status_code == 404
    mock_fetch_rider.assert_called_once_with(rider_id=999)