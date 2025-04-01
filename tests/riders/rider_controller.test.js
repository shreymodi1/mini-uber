import { requestRideHandler, cancelRideHandler, getRideHistoryHandler } from '../../riders/rider_controller';

describe('requestRideHandler', () => {
  let mockReq;
  let mockRes;

  beforeEach(() => {
    mockReq = {
      body: {},
      params: {},
      query: {},
      user: { id: 'rider123' }
    };
    mockRes = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };
  });

  test('should return 200 with a success message when ride is requested successfully', async () => {
    await requestRideHandler(mockReq, mockRes);
    expect(mockRes.status).toHaveBeenCalledWith(200);
    expect(mockRes.json).toHaveBeenCalledWith({
      success: true,
      message: 'Ride requested successfully'
    });
  });

  test('should return 500 on unexpected error', async () => {
    const errorMock = new Error('Simulated error');
    // @ts-ignore
    requestRideHandler.__Rewire__ && requestRideHandler.__Rewire__('someInternalFunction', () => {
      throw errorMock;
    });

    await requestRideHandler(mockReq, mockRes);
    expect(mockRes.status).toHaveBeenCalledWith(500);
    expect(mockRes.json).toHaveBeenCalledWith({
      success: false,
      error: 'Internal Server Error'
    });
  });
});

describe('cancelRideHandler', () => {
  let mockReq;
  let mockRes;

  beforeEach(() => {
    mockReq = {
      body: {},
      params: {},
      query: {},
      user: { id: 'rider123' }
    };
    mockRes = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };
  });

  test('should return 200 with a success message when ride is canceled successfully', async () => {
    await cancelRideHandler(mockReq, mockRes);
    expect(mockRes.status).toHaveBeenCalledWith(200);
    expect(mockRes.json).toHaveBeenCalledWith({
      success: true,
      message: 'Ride canceled successfully'
    });
  });

  test('should return 500 on unexpected error', async () => {
    const errorMock = new Error('Simulated error');
    // @ts-ignore
    cancelRideHandler.__Rewire__ && cancelRideHandler.__Rewire__('someInternalFunction', () => {
      throw errorMock;
    });

    await cancelRideHandler(mockReq, mockRes);
    expect(mockRes.status).toHaveBeenCalledWith(500);
    expect(mockRes.json).toHaveBeenCalledWith({
      success: false,
      error: 'Internal Server Error'
    });
  });
});

describe('getRideHistoryHandler', () => {
  let mockReq;
  let mockRes;

  beforeEach(() => {
    mockReq = {
      body: {},
      params: {},
      query: {},
      user: { id: 'rider123' }
    };
    mockRes = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };
  });

  test('should return 200 with an empty data array when no ride history is found', async () => {
    await getRideHistoryHandler(mockReq, mockRes);
    expect(mockRes.status).toHaveBeenCalledWith(200);
    expect(mockRes.json).toHaveBeenCalledWith({
      success: true,
      data: []
    });
  });

  test('should return 500 on unexpected error', async () => {
    const errorMock = new Error('Simulated error');
    // @ts-ignore
    getRideHistoryHandler.__Rewire__ && getRideHistoryHandler.__Rewire__('someInternalFunction', () => {
      throw errorMock;
    });

    await getRideHistoryHandler(mockReq, mockRes);
    expect(mockRes.status).toHaveBeenCalledWith(500);
    expect(mockRes.json).toHaveBeenCalledWith({
      success: false,
      error: 'Internal Server Error'
    });
  });
});