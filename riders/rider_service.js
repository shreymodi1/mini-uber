import { createRide, cancelExistingRide, getRiderTrips } from '../db/rider_repository.js';

/**
 * Initiates ride creation, triggers driver match
 * @param {string} riderId - Unique ID of the rider
 * @param {Object} pickupLocation - Coordinates or address for pickup
 * @param {Object} destination - Coordinates or address for destination
 * @returns {Promise<Object>} Ride information
 */
export async function requestRide(riderId, pickupLocation, destination) {
    try {
        // TODO: Validate rider existence before creating ride
        // TODO: Implement driver matching logic
        const newRideData = {
            riderId,
            pickupLocation,
            destination,
            status: 'REQUESTED',
            createdAt: new Date()
        };
        const ride = await createRide(newRideData);
        return ride;
    } catch (error) {
        // TODO: Add proper error logging
        throw new Error(`Failed to request ride: ${error.message}`);
    }
}

/**
 * Cancels an ongoing or pending ride, notifies driver if matched
 * @param {string} rideId - Unique ID of the ride
 * @returns {Promise<boolean>} Cancellation success status
 */
export async function cancelRide(rideId) {
    try {
        // TODO: Validate ride ownership for the rider
        const success = await cancelExistingRide(rideId);
        return success;
    } catch (error) {
        // TODO: Add proper error logging
        throw new Error(`Failed to cancel ride: ${error.message}`);
    }
}

/**
 * Retrieves completed trip records from DB
 * @param {string} riderId - Unique ID of the rider
 * @returns {Promise<Array>} List of completed trips
 */
export async function fetchRiderHistory(riderId) {
    try {
        // TODO: Validate rider existence before fetching history
        const history = await getRiderTrips(riderId);
        return history;
    } catch (error) {
        // TODO: Add proper error logging
        throw new Error(`Failed to fetch rider history: ${error.message}`);
    }
}