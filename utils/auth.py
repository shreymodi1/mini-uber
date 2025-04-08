import datetime
from typing import Dict, Any

import jwt

# TODO: Replace this with a secure key storage mechanism or environment variable
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_jwt(user_id: str) -> str:
    """
    Generates a JWT with user claims.

    Args:
        user_id (str): The unique identifier of the user.

    Returns:
        str: The generated JWT token.
    """
    # TODO: Add additional claims as needed
    expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": user_id,
        "exp": expiry
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_jwt(token: str) -> Dict[str, Any]:
    """
    Validates and decodes a JWT.

    Args:
        token (str): The JWT to verify.

    Returns:
        Dict[str, Any]: The decoded token payload.

    Raises:
        ValueError: If the token has expired or is invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError as e:
        raise ValueError("Token has expired.") from e
    except jwt.InvalidTokenError as e:
        raise ValueError("Invalid token.") from e