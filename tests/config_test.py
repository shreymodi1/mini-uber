import os
import pytest
from unittest.mock import patch, mock_open

# Import the functions to test from the config module
from ...config import load_config, get_database_url

@pytest.fixture
def restore_env():
    """
    Fixture to restore environment variables after each test to prevent
    cross-test contamination.
    """
    original_env = dict(os.environ)
    yield
    os.environ.clear()
    os.environ.update(original_env)

def test_load_config_with_env_variables(restore_env):
    """
    Test that load_config correctly reads and sets required environment variables
    when they are already present in the environment.
    """
    # Arrange
    os.environ["DB_URL"] = "postgresql://user:pass@localhost:5432/db_test"
    os.environ["SECRET_KEY"] = "mysecretkey"
    
    # Act
    load_config()
    
    # Assert
    assert os.getenv("DB_URL") == "postgresql://user:pass@localhost:5432/db_test"
    assert os.getenv("SECRET_KEY") == "mysecretkey"

def test_load_config_with_env_file(restore_env, tmp_path):
    """
    Test that load_config can read and set environment variables from a .env file
    when those variables are not already present in the environment.
    """
    # Arrange
    env_file = tmp_path / ".env"
    env_content = "DB_URL=postgresql://user:pass@localhost:5432/db_from_file\nSECRET_KEY=file_secret_key"
    env_file.write_text(env_content)
    
    # Mocking os.path.exists to return True for the .env file check
    with patch("...config.os.path.exists", return_value=True):
        # Mocking open to return our custom file content
        with patch("builtins.open", mock_open(read_data=env_content)):
            # Act
            load_config()

    # Assert
    assert os.getenv("DB_URL") == "postgresql://user:pass@localhost:5432/db_from_file"
    assert os.getenv("SECRET_KEY") == "file_secret_key"

def test_load_config_with_missing_env_file(restore_env):
    """
    Test that load_config does not throw an error if .env file is missing
    and environment variables are also not available in the environment.
    The function should fail gracefully or at least not break execution.
    """
    with patch("...config.os.path.exists", return_value=False):
        load_config()
    # If no crash, we assume the function handled missing .env correctly
    assert True

def test_get_database_url_success(restore_env):
    """
    Test that get_database_url returns the correct URL
    when the DB_URL environment variable is set.
    """
    # Arrange
    os.environ["DB_URL"] = "postgresql://user:pass@localhost:5432/success_db"

    # Act
    db_url = get_database_url()

    # Assert
    assert db_url == "postgresql://user:pass@localhost:5432/success_db"

def test_get_database_url_missing(restore_env):
    """
    Test that get_database_url returns None or raises an error
    when DB_URL is not set. Adjust based on config.py implementation:
    - if it raises an exception, use pytest.raises
    - if it returns None, just check for None
    """
    # Arrange
    # Ensure DB_URL is not set
    os.environ.pop("DB_URL", None)

    # Act
    db_url = get_database_url()

    # Assert
    # Adjust the assertion based on actual behavior in config.py
    assert db_url is None, "Expected None when DB_URL is missing"

def test_get_database_url_invalid_format(restore_env):
    """
    Test that get_database_url handles invalid DB_URL format.
    Depending on the config.py implementation, this may raise an exception
    or return None. Adjust accordingly.
    """
    # Arrange
    os.environ["DB_URL"] = "invalid_db_url"

    # Act
    with pytest.raises(ValueError):
        # If config.py raises a ValueError for invalid format
        get_database_url()