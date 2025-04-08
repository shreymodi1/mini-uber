import logging
from typing import Optional

logger = logging.getLogger(__name__)


def rate_driver(ride_id: int, rating: float, review: Optional[str] = None) -> None:
    """
    Saves a new driver rating and updates overall rating.

    :param ride_id: The unique ID of the ride.
    :param rating: Numeric rating for the driver (1-5).
    :param review: Optional text review for the driver.
    :raises ValueError: If the rating is out of the valid range.
    """
    if rating < 1 or rating > 5:
        logger.error("Invalid driver rating: %f", rating)
        raise ValueError("Rating must be between 1 and 5.")

    # TODO: Implement DB logic to save the driver rating
    # TODO: Fetch/update the driver's overall rating
    # TODO: Log the action for audit
    logger.debug("Received driver rating for ride_id=%d, rating=%f", ride_id, rating)


def rate_rider(ride_id: int, rating: float, review: Optional[str] = None) -> None:
    """
    Saves a new rider rating and updates overall rating.

    :param ride_id: The unique ID of the ride.
    :param rating: Numeric rating for the rider (1-5).
    :param review: Optional text review for the rider.
    :raises ValueError: If the rating is out of the valid range.
    """
    if rating < 1 or rating > 5:
        logger.error("Invalid rider rating: %f", rating)
        raise ValueError("Rating must be between 1 and 5.")

    # TODO: Implement DB logic to save the rider rating
    # TODO: Fetch/update the rider's overall rating
    # TODO: Log the action for audit
    logger.debug("Received rider rating for ride_id=%d, rating=%f", ride_id, rating)


def get_rider_rating(rider_id: int) -> float:
    """
    Returns the overall rating for a given rider.

    :param rider_id: The unique ID of the rider.
    :return: The rider's overall rating as a float.
    """
    # TODO: Implement DB logic to retrieve the rider's overall rating
    # TODO: Handle case if rider is not found or rating does not exist
    logger.debug("Retrieving rider rating for rider_id=%d", rider_id)
    raise NotImplementedError("get_rider_rating is not yet implemented.")


def get_driver_rating(driver_id: int) -> float:
    """
    Returns the overall rating for a given driver.

    :param driver_id: The unique ID of the driver.
    :return: The driver's overall rating as a float.
    """
    # TODO: Implement DB logic to retrieve the driver's overall rating
    # TODO: Handle case if driver is not found or rating does not exist
    logger.debug("Retrieving driver rating for driver_id=%d", driver_id)
    raise NotImplementedError("get_driver_rating is not yet implemented.")