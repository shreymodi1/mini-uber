import express from 'express';
import http from 'http';
import { Server } from 'socket.io';

/**
 * Initializes and configures the demo Express server with Socket.IO.
 * Sets up basic routes and error handling.
 * @param {number} [appPort=3000] - The port on which the server should listen
 * @returns {void}
 */
export function initDemoServer(appPort = 3000) {
    try {
        const app = express();
        const server = http.createServer(app);
        const io = new Server(server, {
            cors: {
                origin: '*'
            }
        });

        app.use(express.json());

        // TODO: Implement additional middleware and production-level configurations

        /**
         * Basic health check endpoint
         */
        app.get('/', (req, res) => {
            res.status(200).send('Demo server is running');
        });

        // TODO: Implement actual endpoints for ride logic

        // Socket.IO connection handling
        io.on('connection', (socket) => {
            console.log(`Client connected: ${socket.id}`);

            // TODO: Implement socket events for ride request and updates

            socket.on('disconnect', () => {
                console.log(`Client disconnected: ${socket.id}`);
            });
        });

        server.listen(appPort, () => {
            console.log(`Demo server listening on port ${appPort}`);
        });
    } catch (error) {
        console.error('Failed to initialize demo server:', error);
        process.exit(1);
    }
}

/**
 * Simulates a full ride flow: rider requests a ride, driver accepts, and ride completes.
 * Demonstration uses mock data only.
 * @returns {void}
 */
export function demoRideFlow() {
    try {
        // TODO: Fetch or create mock rider and driver data
        const mockRider = { id: 'rider123', name: 'Test Rider' };
        const mockDriver = { id: 'driver456', name: 'Test Driver' };

        // Request phase
        console.log(`Rider ${mockRider.name} requests a ride`);
        // TODO: Emit 'rideRequested' event via Socket.IO

        // Accept phase
        console.log(`Driver ${mockDriver.name} accepts the ride`);
        // TODO: Emit 'rideAccepted' event via Socket.IO

        // Completion phase
        console.log(`Ride completed for rider ${mockRider.name}`);
        // TODO: Emit 'rideCompleted' event via Socket.IO

        // TODO: Implement additional logic or database actions
    } catch (error) {
        console.error('Error in demoRideFlow:', error);
    }
}