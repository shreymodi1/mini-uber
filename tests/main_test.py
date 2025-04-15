import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
from sqlalchemy.orm import Session

from config import load_config
from main import create_app, run_app

@pytest.fixture
def client():
    """
    Fixture to create a TestClient for our FastAPI app.
    This is used to test API endpoints without running a live server.
    """
    app = create_app()
    return TestClient(app)

def test_create_app_instance():
    """
    Test that create_app returns a valid FastAPI application instance.
    """
    app = create_app()
    assert isinstance(app, FastAPI), "create_app should return a FastAPI instance"

def test_riders_router_included(client):
    """
    Test that the /riders route is included in the application.
    We expect a non-404 status code (likely 422 if no body is provided).
    """
    response = client.post("/riders", json={})
    assert response.status_code != 404, "Expected /riders endpoint to be included in the app"

def test_drivers_router_included(client):
    """
    Test that the /drivers route is included in the application.
    We expect a non-404 status code (likely 422 if no body is provided).
    """
    response = client.post("/drivers", json={})
    assert response.status_code != 404, "Expected /drivers endpoint to be included in the app"

def test_rides_router_included(client):
    """
    Test that the /rides route is included in the application.
    We expect a non-404 status code (likely 422 if no body is provided).
    """
    response = client.post("/rides/request_ride", json={})
    assert response.status_code != 404, "Expected /rides endpoint to be included in the app"

def test_payments_router_included(client):
    """
    Test that the /payments route is included in the application.
    We expect a non-404 status code (likely 422 if no body is provided).
    """
    response = client.post("/payments/process_payment", json={})
    assert response.status_code != 404, "Expected /payments endpoint to be included in the app"

def test_run_app():
    """
    Test that run_app calls uvicorn.run (or does not crash).
    We mock uvicorn.run to ensure it is invoked correctly.
    """
    with patch("uvicorn.run") as mock_run:
        run_app()  # This function is optional, so we just ensure it doesn't crash or raise.
        mock_run.assert_called_once(), "run_app should call uvicorn.run exactly once"