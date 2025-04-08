import os
import logging
from typing import Optional
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def load_config() -> None:
    """
    Reads environment variables or a .env file for application configuration.

    Raises:
        Exception: If an error occurs during loading of environment variables.
    """
    try:
        load_dotenv()
        # TODO: Handle production vs. development configurations
    except Exception as e:
        logger.error("Failed to load configuration: %s", e)
        raise

def get_database_url() -> str:
    """
    Returns a valid SQLAlchemy database URL based on environment variables.

    Raises:
        ValueError: If the DATABASE_URL environment variable is missing.

    Returns:
        str: The database URL.
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL is not configured in the environment.")
    return database_url