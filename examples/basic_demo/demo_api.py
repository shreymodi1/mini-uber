import requests
from requests.exceptions import RequestException

API_BASE_URL = "http://localhost:8000"


def create_rider(name: str, phone_number: str, payment_method: str) -> dict:
    """
    Sends a POST request to create a new rider.

    Args:
        name (str): The rider's name.
        phone_number (str): The rider's phone number.
        payment_method (str): The rider's preferred payment method.

    Returns:
        dict: A dictionary containing the rider data or an error message.
    """
    try:
        payload = {
            "name": name,
            "phone_number": phone_number,
            "payment_method": payment_method
        }
        response = requests.post(f"{API_BASE_URL}/riders", json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        # TODO: Implement more robust error handling.
        return {"error": str(e)}


def create_driver(name: str, license_number: str, vehicle_info: str) -> dict:
    """
    Sends a POST request to create a new driver.

    Args:
        name (str): The driver's name.
        license_number (str): The driver's license number.
        vehicle_info (str): Information about the driver's vehicle.

    Returns:
        dict: A dictionary containing the driver data or an error message.
    """
    try:
        payload = {
            "name": name,
            "license_number": license_number,
            "vehicle_info": vehicle_info
        }
        response = requests.post(f"{API_BASE_URL}/drivers", json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        # TODO: Implement more robust error handling.
        return {"error": str(e)}


def request_ride(rider_id: int, pickup: str, dropoff: str) -> dict:
    """
    Sends a POST request to request a ride.

    Args:
        rider_id (int): The ID of the rider.
        pickup (str): The pickup location.
        dropoff (str): The dropoff location.

    Returns:
        dict: A dictionary containing ride request details or an error message.
    """
    try:
        payload = {
            "rider_id": rider_id,
            "pickup": pickup,
            "dropoff": dropoff
        }
        response = requests.post(f"{API_BASE_URL}/rides/request_ride", json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        # TODO: Implement more robust error handling.
        return {"error": str(e)}


def calculate_fare(ride_id: int) -> dict:
    """
    Sends a request to calculate the fare for a given ride.

    Args:
        ride_id (int): The ID of the ride.

    Returns:
        dict: A dictionary containing fare details or an error message.
    """
    try:
        # Using GET request by default. Switch to POST if needed.
        response = requests.get(f"{API_BASE_URL}/payments/calculate_fare", params={"ride_id": ride_id}, timeout=5)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        # TODO: Implement more robust error handling.
        return {"error": str(e)}


def process_payment(ride_id: int) -> dict:
    """
    Sends a POST request to process payment for a given ride.

    Args:
        ride_id (int): The ID of the ride.

    Returns:
        dict: A dictionary containing payment confirmation or an error message.
    """
    try:
        payload = {"ride_id": ride_id}
        response = requests.post(f"{API_BASE_URL}/payments/process_payment", json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        # TODO: Implement more robust error handling.
        return {"error": str(e)}