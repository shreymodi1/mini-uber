/**
 * Calculates the approximate distance between two latitude/longitude coordinates using the Haversine formula.
 * @param {number} lat1 - Latitude of the first coordinate
 * @param {number} lon1 - Longitude of the first coordinate
 * @param {number} lat2 - Latitude of the second coordinate
 * @param {number} lon2 - Longitude of the second coordinate
 * @returns {number} - Distance in kilometers
 * @throws {Error} If any of the input parameters are invalid
 */
export function calculateDistance(lat1, lon1, lat2, lon2) {
    // TODO: Adjust formula/constants as needed for project-specific requirements
    if (
        typeof lat1 !== 'number' ||
        typeof lon1 !== 'number' ||
        typeof lat2 !== 'number' ||
        typeof lon2 !== 'number'
    ) {
        throw new Error('Invalid coordinates. All parameters must be numbers.');
    }

    const toRadians = (value) => (value * Math.PI) / 180;
    const earthRadius = 6371; // Earth's radius in kilometers

    const dLat = toRadians(lat2 - lat1);
    const dLon = toRadians(lon2 - lon1);
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(toRadians(lat1)) * Math.cos(toRadians(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const distance = earthRadius * c;

    return distance;
}

/**
 * Estimates travel time based on distance and a default average speed.
 * @param {number} distance - The distance in kilometers
 * @returns {number} - Estimated travel time in hours
 * @throws {Error} If the distance parameter is invalid
 */
export function estimateTime(distance) {
    // TODO: Adjust average speed as needed for project-specific requirements
    if (typeof distance !== 'number' || distance < 0) {
        throw new Error('Invalid distance. Distance must be a non-negative number.');
    }

    const averageSpeed = 50; // Default average speed in km/h
    const travelTime = distance / averageSpeed;

    return travelTime;
}