import logging
from typing import Optional

logger = logging.getLogger(__name__)


def create_rider(name: str, phone_number: str, payment_method: str) -> dict:
    """
    Persists a new rider record in the database.
    
    :param name: Full name of the rider
    :param phone_number: The rider's phone number
    :param payment_method: Selected payment method for the rider
    :return: A dictionary representing the newly created rider
    :raises ValueError: If required parameters are invalid
    :raises Exception: For any other unexpected database or application errors
    """
    if not name or not phone_number or not payment_method:
        raise ValueError("Invalid input. 'name', 'phone_number' and 'payment_method' are required.")
    
    try:
        # TODO: Implement actual database logic to persist the rider
        # Example: session.add(rider_record); session.commit()
        new_rider = {
            "id": 1,  # Placeholder ID
            "name": name,
            "phone_number": phone_number,
            "payment_method": payment_method
        }
        logger.info("Rider created successfully.")
        return new_rider
    except Exception as e:
        logger.error("Error creating rider: %s", str(e))
        raise


def fetch_rider(rider_id: int) -> Optional[dict]:
    """
    Retrieves a rider record from the database by rider_id.
    
    :param rider_id: The unique identifier of the rider
    :return: A dictionary representing the rider if found, otherwise None
    :raises ValueError: If the rider_id is invalid
    :raises Exception: For any other unexpected database or application errors
    """
    if rider_id <= 0:
        raise ValueError("Invalid 'rider_id'. It must be a positive integer.")
    
    try:
        # TODO: Implement actual database logic to fetch the rider
        # Example: rider = session.query(Rider).filter_by(id=rider_id).first()
        # return rider.as_dict() if rider else None
        example_rider = {
            "id": rider_id,
            "name": "John Doe",
            "phone_number": "123-456-7890",
            "payment_method": "Credit Card"
        }
        # Placeholder logic
        return example_rider if rider_id == 1 else None
    except Exception as e:
        logger.error("Error fetching rider with ID %d: %s", rider_id, str(e))
        raise