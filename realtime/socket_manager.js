import { Server } from 'socket.io';

let io;

/**
 * Binds Socket.IO to the Express server instance
 * @param {Object} server - The Express server instance
 * @returns {void}
 */
export function initSocketIO(server) {
    try {
        io = new Server(server, {
            cors: {
                origin: '*',
                methods: ['GET', 'POST']
            }
        });
        // TODO: Add specific event listeners here if needed
    } catch (error) {
        console.error('Error initializing Socket.IO:', error);
    }
}

/**
 * Broadcasts new driver location to relevant riders
 * @param {string} driverId - The ID of the driver
 * @param {{ lat: number, lng: number }} location - The current location of the driver
 * @returns {void}
 */
export function onDriverLocationUpdate(driverId, location) {
    if (!io) {
        console.error('Socket.IO not initialized');
        return;
    }
    if (!driverId || !location) {
        console.error('Invalid driverId or location');
        return;
    }
    try {
        // TODO: Add logic to identify which riders to broadcast the driver's location to
        io.emit('driverLocationUpdate', { driverId, location });
    } catch (error) {
        console.error('Error broadcasting driver location update:', error);
    }
}

/**
 * Pushes ride status changes to rider & driver clients
 * @param {string} rideId - The ID of the ride
 * @param {string} status - The new status of the ride
 * @returns {void}
 */
export function onRideStatusChange(rideId, status) {
    if (!io) {
        console.error('Socket.IO not initialized');
        return;
    }
    if (!rideId || !status) {
        console.error('Invalid rideId or status');
        return;
    }
    try {
        // TODO: Implement logic to broadcast ride status changes to relevant clients only
        io.emit('rideStatusChange', { rideId, status });
    } catch (error) {
        console.error('Error broadcasting ride status change:', error);
    }
}