import * as RideController from '../../rides/ride_controller';
import { getRideStatusHandler, updateRideLocationHandler } from '../../rides/ride_controller';

describe('getRideStatusHandler', () => {
  test('should return the current status of a ride successfully', async () => {
    const req = {
      params: { rideId: '123' },
      query: { rideId: '123' }
    };
    const res = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };

    await getRideStatusHandler(req, res);

    expect(res.status).toHaveBeenCalledWith(200);
    expect(res.json).toHaveBeenCalledWith({ status: 'Pending' });
  });

  test('should handle errors and return 500 status', async () => {
    const req = {
      params: { rideId: '123' },
      query: { rideId: '123' }
    };
    const res = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };

    const originalImplementation = RideController.getRideStatusHandler;
    const error = new Error('Mocked error');

    jest.spyOn(console, 'error').mockImplementation(() => {});
    jest.spyOn(RideController, 'getRideStatusHandler').mockImplementation(async () => { throw error; });

    await getRideStatusHandler(req, res);

    expect(res.status).toHaveBeenCalledWith(500);
    expect(res.json).toHaveBeenCalledWith({ error: 'Failed to retrieve ride status' });

    jest.spyOn(console, 'error').mockRestore();
    jest.spyOn(RideController, 'getRideStatusHandler').mockImplementation(originalImplementation);
  });
});

describe('updateRideLocationHandler', () => {
  test('should update ride location successfully', async () => {
    const req = {
      params: { rideId: '123' },
      query: { rideId: '123' },
      body: { latitude: 40.7128, longitude: -74.0060 }
    };
    const res = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };

    await updateRideLocationHandler(req, res);

    expect(res.status).toHaveBeenCalledWith(200);
    expect(res.json).toHaveBeenCalledWith({ message: 'Location updated successfully' });
  });

  test('should handle errors and return 500 status', async () => {
    const req = {
      params: { rideId: '123' },
      query: { rideId: '123' },
      body: { latitude: 40.7128, longitude: -74.0060 }
    };
    const res = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };

    const originalImplementation = RideController.updateRideLocationHandler;
    const error = new Error('Mocked error');

    jest.spyOn(console, 'error').mockImplementation(() => {});
    jest.spyOn(RideController, 'updateRideLocationHandler').mockImplementation(async () => { throw error; });

    await updateRideLocationHandler(req, res);

    expect(res.status).toHaveBeenCalledWith(500);
    expect(res.json).toHaveBeenCalledWith({ error: 'Failed to update ride location' });

    jest.spyOn(console, 'error').mockRestore();
    jest.spyOn(RideController, 'updateRideLocationHandler').mockImplementation(originalImplementation);
  });
});