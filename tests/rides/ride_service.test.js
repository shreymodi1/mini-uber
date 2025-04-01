import { matchDriver, updateRideStatus, broadcastLocation } from './ride_service.js';
import { findAvailableDrivers, updateRideInDB, sendNotification, publishLocationUpdate } from '../utils/ride_utils.js';

jest.mock('../utils/ride_utils.js', () => ({
  findAvailableDrivers: jest.fn(),
  updateRideInDB: jest.fn(),
  sendNotification: jest.fn(),
  publishLocationUpdate: jest.fn()
}));

describe('matchDriver', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should assign the first available driver', async () => {
    findAvailableDrivers.mockResolvedValueOnce([{ id: 'driver1', location: { lat: 10, long: 10 } }]);
    const riderLocation = { lat: 12.345, long: 67.89 };
    const result = await matchDriver(riderLocation);
    expect(findAvailableDrivers).toHaveBeenCalledTimes(1);
    expect(result).toEqual({ id: 'driver1', location: { lat: 10, long: 10 } });
  });

  test('should return null if no drivers are available', async () => {
    findAvailableDrivers.mockResolvedValueOnce([]);
    const riderLocation = { lat: 12.345, long: 67.89 };
    const result = await matchDriver(riderLocation);
    expect(findAvailableDrivers).toHaveBeenCalledTimes(1);
    expect(result).toBeNull();
  });

  test('should throw error if location is invalid', async () => {
    await expect(matchDriver({ lat: 'invalid', long: 123 })).rejects.toThrow('Invalid rider location provided');
    await expect(matchDriver({ lat: 12, long: undefined })).rejects.toThrow('Invalid rider location provided');
    await expect(matchDriver(null)).rejects.toThrow('Invalid rider location provided');
  });
});

describe('updateRideStatus', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should update ride status and send notification', async () => {
    updateRideInDB.mockResolvedValueOnce(true);
    sendNotification.mockResolvedValueOnce(true);
    const result = await updateRideStatus('ride123', 'ongoing');
    expect(updateRideInDB).toHaveBeenCalledWith('ride123', 'ongoing');
    expect(sendNotification).toHaveBeenCalledWith('ride123', 'ongoing');
    expect(result).toBe(true);
  });

  test('should throw error if parameters are missing', async () => {
    await expect(updateRideStatus('', 'ongoing')).rejects.toThrow('Invalid parameters for ride status update');
    await expect(updateRideStatus('ride123', '')).rejects.toThrow('Invalid parameters for ride status update');
  });

  test('should propagate error thrown by updateRideInDB', async () => {
    updateRideInDB.mockRejectedValueOnce(new Error('DB error'));
    await expect(updateRideStatus('ride123', 'ongoing')).rejects.toThrow('DB error');
  });
});

describe('broadcastLocation', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should broadcast location successfully', () => {
    publishLocationUpdate.mockImplementation(() => true);
    const result = broadcastLocation('ride123', 12.345, 67.89);
    expect(publishLocationUpdate).toHaveBeenCalledWith('ride123', 12.345, 67.89);
    expect(result).toBe(true);
  });

  test('should throw error if parameters are invalid', () => {
    expect(() => broadcastLocation('', 12, 34)).toThrow('Invalid parameters for location broadcast');
    expect(() => broadcastLocation('ride123', 'invalid', 34)).toThrow('Invalid parameters for location broadcast');
    expect(() => broadcastLocation('ride123', 12, null)).toThrow('Invalid parameters for location broadcast');
  });
});