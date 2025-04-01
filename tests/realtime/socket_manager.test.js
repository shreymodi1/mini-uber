import { Server } from 'socket.io';
import { initSocketIO, onDriverLocationUpdate, onRideStatusChange } from '../realtime/socket_manager';

jest.mock('socket.io', () => {
    const emitMock = jest.fn();
    const serverMock = jest.fn().mockImplementation(() => ({
        emit: emitMock
    }));
    return {
        Server: serverMock,
        __esModule: true
    };
});

describe('Socket Manager', () => {
    let consoleErrorSpy;
    let mockServer;

    beforeEach(() => {
        consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
        mockServer = {};
        jest.clearAllMocks();
    });

    afterEach(() => {
        consoleErrorSpy.mockRestore();
    });

    describe('initSocketIO', () => {
        test('should initialize socket.io with the given server', () => {
            initSocketIO(mockServer);
            expect(Server).toHaveBeenCalledWith(mockServer, {
                cors: { origin: '*', methods: ['GET', 'POST'] }
            });
        });

        test('should log error if socket.io initialization fails', () => {
            Server.mockImplementationOnce(() => {
                throw new Error('Failed to init');
            });
            initSocketIO(mockServer);
            expect(consoleErrorSpy).toHaveBeenCalledWith('Error initializing Socket.IO:', expect.any(Error));
        });
    });

    describe('onDriverLocationUpdate', () => {
        test('should log error if socket.io is not initialized', () => {
            onDriverLocationUpdate('driver123', { lat: 10, lng: 20 });
            expect(consoleErrorSpy).toHaveBeenCalledWith('Socket.IO not initialized');
        });

        test('should log error if driverId or location is missing', () => {
            initSocketIO(mockServer);
            onDriverLocationUpdate(null, { lat: 10, lng: 20 });
            onDriverLocationUpdate('driver123', null);
            expect(consoleErrorSpy).toHaveBeenCalledTimes(2);
            expect(consoleErrorSpy).toHaveBeenCalledWith('Invalid driverId or location');
        });

        test('should broadcast new driver location for valid inputs', () => {
            initSocketIO(mockServer);
            onDriverLocationUpdate('driver123', { lat: 10, lng: 20 });
            const serverInstance = Server.mock.results[0].value;
            expect(serverInstance.emit).toHaveBeenCalledWith('driverLocationUpdate', {
                driverId: 'driver123',
                location: { lat: 10, lng: 20 }
            });
        });
    });

    describe('onRideStatusChange', () => {
        test('should log error if socket.io is not initialized', () => {
            onRideStatusChange('ride123', 'in_progress');
            expect(consoleErrorSpy).toHaveBeenCalledWith('Socket.IO not initialized');
        });

        test('should log error if rideId or status is missing', () => {
            initSocketIO(mockServer);
            onRideStatusChange(null, 'in_progress');
            onRideStatusChange('ride123', null);
            expect(consoleErrorSpy).toHaveBeenCalledTimes(2);
            expect(consoleErrorSpy).toHaveBeenCalledWith('Invalid rideId or status');
        });

        test('should broadcast ride status change for valid inputs', () => {
            initSocketIO(mockServer);
            onRideStatusChange('ride123', 'completed');
            const serverInstance = Server.mock.results[0].value;
            expect(serverInstance.emit).toHaveBeenCalledWith('rideStatusChange', {
                rideId: 'ride123',
                status: 'completed'
            });
        });
    });
});