import { createRide, cancelExistingRide, getRiderTrips } from '../db/rider_repository.js';
import { requestRide, cancelRide, fetchRiderHistory } from './rider_service.js';

jest.mock('../db/rider_repository.js', () => ({
  createRide: jest.fn(),
  cancelExistingRide: jest.fn(),
  getRiderTrips: jest.fn(),
}));

describe('rider_service', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('requestRide', () => {
    it('should create a ride with provided parameters', async () => {
      const riderId = 'rider123';
      const pickupLocation = { lat: 10, lng: 20 };
      const destination = { lat: 30, lng: 40 };
      const mockRide = {
        riderId,
        pickupLocation,
        destination,
        status: 'REQUESTED',
        createdAt: new Date(),
      };
      createRide.mockResolvedValue(mockRide);

      const result = await requestRide(riderId, pickupLocation, destination);

      expect(createRide).toHaveBeenCalledWith(expect.objectContaining({
        riderId,
        pickupLocation,
        destination,
        status: 'REQUESTED',
      }));
      expect(result).toEqual(mockRide);
    });

    it('should throw an error if ride creation fails', async () => {
      createRide.mockRejectedValue(new Error('DB error'));

      await expect(requestRide('rider123', {}, {})).rejects.toThrow('Failed to request ride: DB error');
    });
  });

  describe('cancelRide', () => {
    it('should return true when ride is successfully canceled', async () => {
      cancelExistingRide.mockResolvedValue(true);

      const result = await cancelRide('ride123');

      expect(cancelExistingRide).toHaveBeenCalledWith('ride123');
      expect(result).toBe(true);
    });

    it('should throw an error if cancellation fails', async () => {
      cancelExistingRide.mockRejectedValue(new Error('Cancel error'));

      await expect(cancelRide('ride123')).rejects.toThrow('Failed to cancel ride: Cancel error');
    });
  });

  describe('fetchRiderHistory', () => {
    it('should return an array of completed trips', async () => {
      const mockTrips = [
        { rideId: 'ride1', status: 'COMPLETED' },
        { rideId: 'ride2', status: 'COMPLETED' },
      ];
      getRiderTrips.mockResolvedValue(mockTrips);

      const result = await fetchRiderHistory('rider123');

      expect(getRiderTrips).toHaveBeenCalledWith('rider123');
      expect(result).toEqual(mockTrips);
    });

    it('should throw an error if fetching history fails', async () => {
      getRiderTrips.mockRejectedValue(new Error('History error'));

      await expect(fetchRiderHistory('rider123')).rejects.toThrow('Failed to fetch rider history: History error');
    });
  });
});