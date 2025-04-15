import os
import pytest

# Importing the functions under test from the project's root-level config module
from config import load_config, get_database_url

@pytest.fixture
def clear_env_vars(monkeypatch):
    """
    Fixture to clear specific environment variables before each test to avoid side effects.
    """
    vars_to_clear = [
        "DATABASE_URL",  # Example env var name for the DB connection URL
        "SOME_OTHER_CONFIG"  # Example of any other config-related env var that might be used
    ]
    for var in vars_to_clear:
        monkeypatch.delenv(var, raising=False)
    yield


def test_load_config_reads_env_vars(monkeypatch, clear_env_vars):
    """
    Test that load_config() correctly reads and returns important
    configuration data from environment variables.
    """
    # Arrange
    monkeypatch.setenv("SOME_OTHER_CONFIG", "TestValue")

    # Act
    config_values = load_config()

    # Assert
    assert "SOME_OTHER_CONFIG" in config_values, "Expected config to include 'SOME_OTHER_CONFIG'"
    assert config_values["SOME_OTHER_CONFIG"] == "TestValue", "Expected 'SOME_OTHER_CONFIG' to match env var"


def test_load_config_env_var_not_set_returns_default(clear_env_vars):
    """
    Test that load_config() returns default or fallback values
    when certain environment variables are not set.
    """
    # Act
    config_values = load_config()

    # Assert
    # Adjust the assertion based on how 'load_config' handles missing env vars
    assert "SOME_OTHER_CONFIG" not in config_values or config_values["SOME_OTHER_CONFIG"] is None, (
        "Expected fallback behavior for missing 'SOME_OTHER_CONFIG'"
    )


def test_get_database_url_with_env(monkeypatch, clear_env_vars):
    """
    Test get_database_url() returns the correct database URL
    when DATABASE_URL environment variable is set.
    """
    # Arrange
    db_url = "postgresql://test_user:test_pass@localhost:5432/test_db"
    monkeypatch.setenv("DATABASE_URL", db_url)

    # Act
    result = get_database_url()

    # Assert
    assert result == db_url, "Expected get_database_url() to return the environment-specified DB URL"


def test_get_database_url_no_env_raises_or_fallback(clear_env_vars):
    """
    Test behavior of get_database_url() when DATABASE_URL is not set.
    Depending on implementation, it might raise an error or return a default/fallback.
    """
    # Act / Assert
    # Modify the test based on the actual behavior. Example if it raises an exception:
    with pytest.raises(Exception) as exc_info:
        _ = get_database_url()
    assert "not set" in str(exc_info.value), "Expected exception when DATABASE_URL is missing"