import os
from typing import Dict, Optional

DEMO_CONFIG: Dict[str, Optional[str]] = {}


def load_demo_config() -> None:
    """
    Loads or mocks environment variables for the Flask server.
    
    This function reads relevant environment variables and stores them in the
    global DEMO_CONFIG dictionary. If certain variables are not present, it
    assigns default values.
    
    TODO: Expand or modify this function to load additional variables required
    by the Flask server.
    """
    # Use os.getenv with defaults to mock or provide fallback values
    DEMO_CONFIG['FLASK_ENV'] = os.getenv('FLASK_ENV', 'development')
    DEMO_CONFIG['UBER_LITE_API_URL'] = os.getenv('UBER_LITE_API_URL', 'http://localhost:8000')


def get_uber_lite_api_url() -> str:
    """
    Returns the base URL (http://localhost:8000) of the FastAPI app.

    :return: The base URL string.
    """
    # Fetch the URL from DEMO_CONFIG or use default
    return DEMO_CONFIG.get('UBER_LITE_API_URL', 'http://localhost:8000')