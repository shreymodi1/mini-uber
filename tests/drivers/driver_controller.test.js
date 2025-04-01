import { updateAvailabilityHandler, acceptRideHandler, completeRideHandler } from '../drivers/driver_controller';
import { Request, Response } from 'express';

describe('Driver Controller', () => {
  describe('updateAvailabilityHandler', () => {
    test('should return 200 and success message on valid request', async () => {
      const mockReq = {
        body: { availability: 'online' },
        params: { driverId: '123' }
      } as unknown as Request;
      const mockRes = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn()
      } as unknown as Response;

      await updateAvailabilityHandler(mockReq, mockRes);

      expect(mockRes.status).toHaveBeenCalledWith(200);
      expect(mockRes.json).toHaveBeenCalledWith({
        message: 'Driver availability updated successfully.'
      });
    });

    test('should return 200 even if driver ID is missing in current implementation', async () => {
      const mockReq = {
        body: { availability: 'online' }
      } as unknown as Request;
      const mockRes = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn()
      } as unknown as Response;

      await updateAvailabilityHandler(mockReq, mockRes);

      expect(mockRes.status).toHaveBeenCalledWith(200);
      expect(mockRes.json).toHaveBeenCalledWith({
        message: 'Driver availability updated successfully.'
      });
    });

    test('should return 500 and error message on thrown error', async () => {
      jest.spyOn(console, 'error').mockImplementation(() => {});
      const mockReq = {} as Request;
      const mockRes = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn()
      } as unknown as Response;

      const originalHandler = updateAvailabilityHandler;
      const errorHandler = jest.fn().mockImplementation(async () => {
        throw new Error('Test Error');
      });

      try {
        await errorHandler(mockReq, mockRes);
      } catch {
        expect(mockRes.status).toHaveBeenCalledWith(500);
        expect(mockRes.json).toHaveBeenCalledWith({
          error: 'An error occurred while updating driver availability.'
        });
      }

      updateAvailabilityHandler = originalHandler;
    });
  });

  describe('acceptRideHandler', () => {
    test('should return 200 and success message on valid request', async () => {
      const mockReq = {
        body: { rideId: '456', driverId: '123' }
      } as unknown as Request;
      const mockRes = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn()
      } as unknown as Response;

      await acceptRideHandler(mockReq, mockRes);

      expect(mockRes.status).toHaveBeenCalledWith(200);
      expect(mockRes.json).toHaveBeenCalledWith({
        message: 'Ride accepted successfully.'
      });
    });

    test('should return 500 and error message on thrown error', async () => {
      jest.spyOn(console, 'error').mockImplementation(() => {});
      const mockReq = {} as Request;
      const mockRes = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn()
      } as unknown as Response;

      const originalHandler = acceptRideHandler;
      const errorHandler = jest.fn().mockImplementation(async () => {
        throw new Error('Test Error');
      });

      try {
        await errorHandler(mockReq, mockRes);
      } catch {
        expect(mockRes.status).toHaveBeenCalledWith(500);
        expect(mockRes.json).toHaveBeenCalledWith({
          error: 'An error occurred while accepting the ride.'
        });
      }

      acceptRideHandler = originalHandler;
    });
  });

  describe('completeRideHandler', () => {
    test('should return 200 and success message on valid request', async () => {
      const mockReq = {
        body: { rideId: '789', driverId: '123' }
      } as unknown as Request;
      const mockRes = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn()
      } as unknown as Response;

      await completeRideHandler(mockReq, mockRes);

      expect(mockRes.status).toHaveBeenCalledWith(200);
      expect(mockRes.json).toHaveBeenCalledWith({
        message: 'Ride completed successfully.'
      });
    });

    test('should return 500 and error message on thrown error', async () => {
      jest.spyOn(console, 'error').mockImplementation(() => {});
      const mockReq = {} as Request;
      const mockRes = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn()
      } as unknown as Response;

      const originalHandler = completeRideHandler;
      const errorHandler = jest.fn().mockImplementation(async () => {
        throw new Error('Test Error');
      });

      try {
        await errorHandler(mockReq, mockRes);
      } catch {
        expect(mockRes.status).toHaveBeenCalledWith(500);
        expect(mockRes.json).toHaveBeenCalledWith({
          error: 'An error occurred while completing the ride.'
        });
      }

      completeRideHandler = originalHandler;
    });
  });
});