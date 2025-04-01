import { initiatePaymentHandler, fetchPaymentDetailsHandler } from '../payments/payment_controller.js';
import PaymentService from '../services/payment_service.js';

jest.mock('../services/payment_service.js');

describe('initiatePaymentHandler', () => {
  let mockReq;
  let mockRes;

  beforeEach(() => {
    mockReq = {
      body: {
        rideId: 'testRideId',
        fare: 25
      }
    };
    mockRes = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };
    jest.clearAllMocks();
  });

  test('should initiate payment with valid data', async () => {
    PaymentService.initiatePayment.mockResolvedValue({ transactionId: 'trxn123' });

    await initiatePaymentHandler(mockReq, mockRes);

    expect(PaymentService.initiatePayment).toHaveBeenCalledWith('testRideId', 25);
    expect(mockRes.status).toHaveBeenCalledWith(200);
    expect(mockRes.json).toHaveBeenCalledWith({
      success: true,
      data: { transactionId: 'trxn123' }
    });
  });

  test('should handle service error gracefully', async () => {
    PaymentService.initiatePayment.mockRejectedValue(new Error('Service Error'));

    await initiatePaymentHandler(mockReq, mockRes);

    expect(mockRes.status).toHaveBeenCalledWith(500);
    expect(mockRes.json).toHaveBeenCalledWith({
      success: false,
      message: 'An error occurred while initiating the payment'
    });
  });

  test('should return error response if request body is missing fare', async () => {
    mockReq.body = { rideId: 'testRideId' };

    await initiatePaymentHandler(mockReq, mockRes);

    expect(mockRes.status).toHaveBeenCalledWith(500);
    expect(mockRes.json).toHaveBeenCalledWith({
      success: false,
      message: 'An error occurred while initiating the payment'
    });
  });
});

describe('fetchPaymentDetailsHandler', () => {
  let mockReq;
  let mockRes;

  beforeEach(() => {
    mockReq = {
      params: {
        rideId: 'testRideId'
      }
    };
    mockRes = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };
    jest.clearAllMocks();
  });

  test('should fetch payment details with valid rideId', async () => {
    PaymentService.getPaymentDetails.mockResolvedValue({ transactionId: 'trxn123', amount: 25 });

    await fetchPaymentDetailsHandler(mockReq, mockRes);

    expect(PaymentService.getPaymentDetails).toHaveBeenCalledWith('testRideId');
    expect(mockRes.status).toHaveBeenCalledWith(200);
    expect(mockRes.json).toHaveBeenCalledWith({
      success: true,
      data: { transactionId: 'trxn123', amount: 25 }
    });
  });

  test('should handle service error gracefully', async () => {
    PaymentService.getPaymentDetails.mockRejectedValue(new Error('Service Error'));

    await fetchPaymentDetailsHandler(mockReq, mockRes);

    expect(mockRes.status).toHaveBeenCalledWith(500);
    expect(mockRes.json).toHaveBeenCalledWith({
      success: false,
      message: 'An error occurred while retrieving payment details'
    });
  });

  test('should return error response if rideId is missing', async () => {
    mockReq.params = {};

    await fetchPaymentDetailsHandler(mockReq, mockRes);

    expect(mockRes.status).toHaveBeenCalledWith(500);
    expect(mockRes.json).toHaveBeenCalledWith({
      success: false,
      message: 'An error occurred while retrieving payment details'
    });
  });
});