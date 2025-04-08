import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import FastAPI

# Adjust the relative import based on your project's structure:
# Assuming main.py is one level above the tests directory:
from ..main import create_app, run_app

@pytest.fixture
def test_app():
    """
    Fixture to create and return a FastAPI test application instance.
    """
    return create_app()

def test_create_app_instance(test_app):
    """
    Test that create_app() returns a valid FastAPI application instance.
    """
    assert isinstance(test_app, FastAPI), "create_app should return a FastAPI instance."

def test_app_docs_endpoint(test_app):
    """
    Test that the FastAPI application's /docs endpoint is accessible.
    """
    client = TestClient(test_app)
    response = client.get("/docs")
    assert response.status_code == 200, "Expected /docs to return an HTTP 200 status."

@patch("..main.uvicorn.run")
def test_run_app_success(mock_uvicorn_run):
    """
    Test that run_app() invokes uvicorn.run with appropriate parameters.
    """
    run_app()
    mock_uvicorn_run.assert_called_once(), (
        "uvicorn.run should be called exactly once by run_app."
    )