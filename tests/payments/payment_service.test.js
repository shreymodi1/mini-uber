import { calculateFare, processPayment, getPaymentDetails } from '../payments/payment_service';
import { db } from '../db';
import { externalPaymentGateway } from '../payment_gateway';

jest.mock('../db');
jest.mock('../payment_gateway');

describe('calculateFare', () => {
    test('should calculate fare correctly with valid inputs', () => {
        const distance = 10;
        const time = 10;
        const fare = calculateFare(distance, time);
        expect(fare).toBe(30);
    });

    test('should return base fare for zero distance and time', () => {
        const fare = calculateFare(0, 0);
        expect(fare).toBe(5);
    });

    test('should handle negative values without throwing an error', () => {
        const distance = -5;
        const time = -10;
        const fare = calculateFare(distance, time);
        expect(typeof fare).toBe('number');
    });
});

describe('processPayment', () => {
    afterEach(() => {
        jest.clearAllMocks();
    });

    test('should process payment successfully', async () => {
        externalPaymentGateway.charge.mockResolvedValueOnce(true);
        externalPaymentGateway.credit.mockResolvedValueOnce(true);
        db.insertTransaction.mockResolvedValueOnce(true);

        const riderId = 'rider123';
        const driverId = 'driver456';
        const amount = 100;

        const result = await processPayment(riderId, driverId, amount);

        expect(externalPaymentGateway.charge).toHaveBeenCalledWith(riderId, amount);
        expect(externalPaymentGateway.credit).toHaveBeenCalledWith(driverId, 80);
        expect(db.insertTransaction).toHaveBeenCalled();
        expect(result.success).toBe(true);
        expect(result.transaction.driverAmount).toBe(80);
    });

    test('should throw error if charging rider fails', async () => {
        externalPaymentGateway.charge.mockRejectedValueOnce(new Error('Charge failed'));

        await expect(
            processPayment('rider123', 'driver456', 100)
        ).rejects.toThrow('Failed to process payment.');
    });

    test('should throw error if crediting driver fails', async () => {
        externalPaymentGateway.charge.mockResolvedValueOnce(true);
        externalPaymentGateway.credit.mockRejectedValueOnce(new Error('Credit failed'));

        await expect(
            processPayment('rider123', 'driver456', 100)
        ).rejects.toThrow('Failed to process payment.');
    });

    test('should throw error if inserting transaction into DB fails', async () => {
        externalPaymentGateway.charge.mockResolvedValueOnce(true);
        externalPaymentGateway.credit.mockResolvedValueOnce(true);
        db.insertTransaction.mockRejectedValueOnce(new Error('DB error'));

        await expect(
            processPayment('rider123', 'driver456', 100)
        ).rejects.toThrow('Failed to process payment.');
    });
});

describe('getPaymentDetails', () => {
    afterEach(() => {
        jest.clearAllMocks();
    });

    test('should return transaction details if found', async () => {
        const mockTransaction = { id: 'tx123', riderId: 'rider123' };
        db.findTransactionByRideId.mockResolvedValueOnce(mockTransaction);

        const result = await getPaymentDetails('ride123');
        expect(db.findTransactionByRideId).toHaveBeenCalledWith('ride123');
        expect(result).toEqual(mockTransaction);
    });

    test('should return null if transaction not found', async () => {
        db.findTransactionByRideId.mockResolvedValueOnce(null);
        const result = await getPaymentDetails('rideNotFound');
        expect(result).toBeNull();
    });

    test('should throw error if DB fails', async () => {
        db.findTransactionByRideId.mockRejectedValueOnce(new Error('DB failure'));

        await expect(
            getPaymentDetails('rideError')
        ).rejects.toThrow('Failed to retrieve payment details.');
    });
});