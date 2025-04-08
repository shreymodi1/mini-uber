import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Relative import from the main project structure
from ...ratings.ratings_router import router
from ...models import YourModel  # Replace with actual model(s) as needed


@pytest.fixture(scope="module")
def test_app():
    """
    Create a temporary FastAPI application instance with the ratings router included.
    This fixture runs once per test module.
    """
    app = FastAPI()
    app.include_router(router, prefix="/ratings", tags=["ratings"])
    yield app


@pytest.fixture(scope="module")
def client(test_app):
    """
    Provides a TestClient for making requests to the FastAPI test app.
    """
    return TestClient(test_app)


@pytest.fixture
def db_session():
    """
    Mock or provide a test database session.
    If using an actual database, set up and tear down test data here.
    """
    # In a real scenario, you'd create a special session or mock session.
    # This is a placeholder for demonstration.
    session = Session(bind=None)  # Provide a real engine or mock here if needed
    yield session
    # Teardown logic if needed (e.g., close connections, drop test data, etc.)


class TestRateDriverEndpoint:
    """
    Tests for the rate_driver_endpoint function.
    """

    def test_rate_driver_success(self, client: TestClient, db_session: Session):
        """
        Test successful rating of a driver by providing valid ride_id, rating, and review.
        Expect a 200/201 status code and confirmation of the rating being saved.
        """
        payload = {
            "ride_id": 1,
            "rating": 5,
            "review": "Great driver!"
        }
        response = client.post("/ratings/driver", json=payload)
        assert response.status_code in [200, 201], "Expected a successful response status code."
        data = response.json()
        assert "message" in data, "Expected a 'message' key in the response."
        # Additional assertions depending on the stored data

    def test_rate_driver_invalid_ride_id(self, client: TestClient, db_session: Session):
        """
        Test rating of a driver with an invalid ride_id.
        Expect an error response (e.g. 400 or 404).
        """
        payload = {
            "ride_id": -999,
            "rating": 4,
            "review": "Attempted to rate with invalid ride_id."
        }
        response = client.post("/ratings/driver", json=payload)
        assert response.status_code == 400 or response.status_code == 404, (
            "Expected a 400 or 404 status code for invalid ride_id."
        )


class TestRateRiderEndpoint:
    """
    Tests for the rate_rider_endpoint function.
    """

    def test_rate_rider_success(self, client: TestClient, db_session: Session):
        """
        Test successful rating of a rider by providing valid ride_id, rating, and review.
        Expect a 200/201 status code and confirmation of the rating being saved.
        """
        payload = {
            "ride_id": 2,
            "rating": 4,
            "review": "Polite rider."
        }
        response = client.post("/ratings/rider", json=payload)
        assert response.status_code in [200, 201], "Expected a successful response status code."
        data = response.json()
        assert "message" in data, "Expected a 'message' key in the response."
        # Additional assertions depending on the stored data

    def test_rate_rider_invalid_ride_id(self, client: TestClient, db_session: Session):
        """
        Test rating of a rider with an invalid ride_id.
        Expect an error response (e.g. 400 or 404).
        """
        payload = {
            "ride_id": -1,
            "rating": 3,
            "review": "Invalid ride_id test."
        }
        response = client.post("/ratings/rider", json=payload)
        assert response.status_code == 400 or response.status_code == 404, (
            "Expected a 400 or 404 status code for invalid ride_id."
        )


class TestGetRiderRatingEndpoint:
    """
    Tests for the get_rider_rating_endpoint function.
    """

    def test_get_rider_rating_success(self, client: TestClient, db_session: Session):
        """
        Test retrieving rider's average rating with a valid rider_id.
        Expect a 200 status code and a valid rating float or integer.
        """
        rider_id = 10
        response = client.get(f"/ratings/rider/{rider_id}")
        assert response.status_code == 200, "Expected a successful response status code."
        data = response.json()
        assert "average_rating" in data, "Expected an 'average_rating' key in the response."
        # Further assertions, like checking numeric range, could be added here

    def test_get_rider_rating_not_found(self, client: TestClient, db_session: Session):
        """
        Test retrieving rider's average rating with a non-existent rider_id.
        Expect a 404 response code or appropriate error response.
        """
        rider_id = 999999
        response = client.get(f"/ratings/rider/{rider_id}")
        assert response.status_code == 404, "Expected a 404 status code for non-existent rider_id."


class TestGetDriverRatingEndpoint:
    """
    Tests for the get_driver_rating_endpoint function.
    """

    def test_get_driver_rating_success(self, client: TestClient, db_session: Session):
        """
        Test retrieving driver's average rating with a valid driver_id.
        Expect a 200 status code and a valid rating float or integer.
        """
        driver_id = 20
        response = client.get(f"/ratings/driver/{driver_id}")
        assert response.status_code == 200, "Expected a successful response status code."
        data = response.json()
        assert "average_rating" in data, "Expected an 'average_rating' key in the response."

    def test_get_driver_rating_not_found(self, client: TestClient, db_session: Session):
        """
        Test retrieving driver's average rating with a non-existent driver_id.
        Expect a 404 response code or appropriate error response.
        """
        driver_id = 999999
        response = client.get(f"/ratings/driver/{driver_id}")
        assert response.status_code == 404, "Expected a 404 status code for non-existent driver_id."