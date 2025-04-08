import math

def calculate_distance(coord1: tuple[float, float], coord2: tuple[float, float]) -> float:
    """
    Returns the distance between two coordinates using the Haversine formula.

    Args:
        coord1: A tuple (latitude, longitude) in decimal degrees.
        coord2: A tuple (latitude, longitude) in decimal degrees.

    Returns:
        The distance in kilometers.

    Raises:
        ValueError: If the input coordinates are invalid or improperly structured.
    """
    if (
        not isinstance(coord1, tuple) or
        not isinstance(coord2, tuple) or
        len(coord1) != 2 or
        len(coord2) != 2
    ):
        raise ValueError("Coordinates must be tuples of the form (latitude, longitude).")

    # TODO: Evaluate a more robust method for coordinate validation if needed.
    # Convert latitude and longitude from degrees to radians
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = (math.sin(dlat / 2) ** 2) + (
        math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    radius_earth_km = 6371.0

    distance = radius_earth_km * c
    return distance

def estimate_travel_time(coord1: tuple[float, float], coord2: tuple[float, float]) -> float:
    """
    Returns an estimated time in hours to travel between two coordinates.
    Uses a simple average speed assumption for estimation.

    Args:
        coord1: A tuple (latitude, longitude) in decimal degrees.
        coord2: A tuple (latitude, longitude) in decimal degrees.

    Returns:
        The estimated travel time in hours.

    Raises:
        ValueError: If the input coordinates are invalid or improperly structured.
    """
    # TODO: Update logic with dynamic speed or route data for more accurate estimations.
    distance_km = calculate_distance(coord1, coord2)

    # Simple assumption: average speed (in km/h)
    average_speed_kmh = 80.0

    if average_speed_kmh <= 0:
        raise ValueError("Average speed must be greater than zero.")

    travel_time_hours = distance_km / average_speed_kmh
    return travel_time_hours