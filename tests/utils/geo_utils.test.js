import { calculateDistance, estimateTime } from './utils/geo_utils';

describe('calculateDistance', () => {
    test('should calculate distance between two known coordinates', () => {
        const distance = calculateDistance(0, 0, 0, 1);
        // Roughly 111.19 km for 1 degree of longitude at the equator
        expect(distance).toBeCloseTo(111.19, 1);
    });

    test('should return 0 if both coordinates are the same', () => {
        const distance = calculateDistance(10, 20, 10, 20);
        expect(distance).toBe(0);
    });

    test('should throw an error if any parameter is not a number', () => {
        expect(() => calculateDistance('0', 0, 0, 1)).toThrow('Invalid coordinates. All parameters must be numbers.');
        expect(() => calculateDistance(0, null, 0, 1)).toThrow('Invalid coordinates. All parameters must be numbers.');
    });
});

describe('estimateTime', () => {
    test('should estimate travel time based on distance', () => {
        const distance = 100;
        // Default speed is 50 km/h, so time for 100 km is 2 hours
        const time = estimateTime(distance);
        expect(time).toBe(2);
    });

    test('should return 0 when distance is 0', () => {
        const time = estimateTime(0);
        expect(time).toBe(0);
    });

    test('should throw an error if distance is negative', () => {
        expect(() => estimateTime(-1)).toThrow('Invalid distance. Distance must be a non-negative number.');
    });

    test('should throw an error if distance is not a number', () => {
        expect(() => estimateTime('100')).toThrow('Invalid distance. Distance must be a non-negative number.');
    });
});