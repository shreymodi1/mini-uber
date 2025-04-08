import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Import the router you want to test
from ...riders.riders_router import router
# Import any necessary models if needed
from ...models import YourModel

@pytest.fixture
def test_app():
    """
    Create and configure a new FastAPI app instance with the riders router included.
    This fixture will be used by the TestClient fixture below.
    """
    app = FastAPI()
    app.include_router(router, prefix="/riders", tags=["riders"])
    return app

@pytest.fixture
def client(test_app):
    """
    Returns a TestClient instance for making requests to the 'test_app' fixture.
    """
    return TestClient(test_app)

@pytest.fixture
def db_session():
    """
    Setup a database session fixture. Here you could create an in-memory database or
    mock database interactions as needed. For now, this is a placeholder.
    """
    session = Session(bind=None)  # Replace 'None' with an actual testing engine if needed
    yield session
    session.close()

# ------------------------- Tests for create_rider_endpoint -------------------------

def test_create_rider_endpoint_success(client, db_session):
    """
    Test creating a new rider with valid data.
    Expect a 201 status code and a response containing newly created rider details.
    """
    new_rider_data = {
        "name": "Test Rider",
        "email": "test@example.com",
        "phone": "1234567890"
    }
    response = client.post("/riders/create_rider", json=new_rider_data)
    assert response.status_code == 201
    response_json = response.json()
    assert response_json["name"] == "Test Rider"
    assert response_json["email"] == "test@example.com"
    assert "id" in response_json  # Assuming the created rider has an ID returned

def test_create_rider_endpoint_error_missing_fields(client, db_session):
    """
    Test creating a new rider with missing required fields.
    Expect a 422 or 400 error depending on your validation/exception handling strategy.
    """
    incomplete_data = {
        # Intentionally missing some required fields like 'email' or 'phone'
        "name": "Rider Without Email"
    }
    response = client.post("/riders/create_rider", json=incomplete_data)
    assert response.status_code in [400, 422]

# ------------------------- Tests for get_rider_profile_endpoint -------------------------

def test_get_rider_profile_endpoint_success(client, db_session):
    """
    Test retrieving a rider profile by valid rider_id.
    Expect a 200 status code and correct rider profile data.
    """
    # Insert a test rider into the DB or mock it.
    test_rider_id = 1

    # Example: If your endpoint is /riders/{rider_id}
    response = client.get(f"/riders/{test_rider_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == test_rider_id
    assert "email" in response_json
    assert "name" in response_json

def test_get_rider_profile_endpoint_not_found(client, db_session):
    """
    Test retrieving a rider profile with an invalid rider_id or one that doesn't exist.
    Expect a 404 status code to indicate the rider was not found.
    """
    non_existent_rider_id = 9999
    response = client.get(f"/riders/{non_existent_rider_id}")
    assert response.status_code == 404