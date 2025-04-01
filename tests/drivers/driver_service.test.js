import db from "../database/connection.js";
import { setDriverAvailability, acceptRide, completeRide } from "../drivers/driver_service.js";

jest.mock("../database/connection.js", () => ({
    query: jest.fn()
}));

describe("setDriverAvailability", () => {
    beforeEach(() => {
        db.query.mockClear();
    });

    test("should update the driver's availability if both driverId and status are provided", async () => {
        db.query.mockResolvedValueOnce({});
        await expect(setDriverAvailability("driver123", "available")).resolves.toBeUndefined();
        expect(db.query).toHaveBeenCalledWith(
            expect.any(String),
            expect.arrayContaining(["available", "driver123"])
        );
    });

    test("should throw an error if driverId is missing", async () => {
        await expect(setDriverAvailability("", "available")).rejects.toThrow(
            "Driver ID and status are required."
        );
        expect(db.query).not.toHaveBeenCalled();
    });

    test("should throw an error if status is missing", async () => {
        await expect(setDriverAvailability("driver123", "")).rejects.toThrow(
            "Driver ID and status are required."
        );
        expect(db.query).not.toHaveBeenCalled();
    });

    test("should propagate error if db query fails", async () => {
        db.query.mockRejectedValueOnce(new Error("DB Error"));
        await expect(setDriverAvailability("driver123", "available")).rejects.toThrow(
            "Failed to set driver availability: DB Error"
        );
    });
});

describe("acceptRide", () => {
    beforeEach(() => {
        db.query.mockClear();
    });

    test("should accept the ride when both driverId and rideId are provided", async () => {
        db.query.mockResolvedValueOnce({});
        await expect(acceptRide("driver123", "ride456")).resolves.toBeUndefined();
        expect(db.query).toHaveBeenCalledWith(
            expect.any(String),
            expect.arrayContaining(["driver123", "ride456"])
        );
    });

    test("should throw an error if driverId is missing", async () => {
        await expect(acceptRide("", "ride456")).rejects.toThrow(
            "Driver ID and ride ID are required."
        );
        expect(db.query).not.toHaveBeenCalled();
    });

    test("should throw an error if rideId is missing", async () => {
        await expect(acceptRide("driver123", "")).rejects.toThrow(
            "Driver ID and ride ID are required."
        );
        expect(db.query).not.toHaveBeenCalled();
    });

    test("should propagate error if db query fails", async () => {
        db.query.mockRejectedValueOnce(new Error("DB Error"));
        await expect(acceptRide("driver123", "ride456")).rejects.toThrow(
            "Failed to accept ride: DB Error"
        );
    });
});

describe("completeRide", () => {
    beforeEach(() => {
        db.query.mockClear();
    });

    test("should complete the ride if rideId is provided", async () => {
        db.query.mockResolvedValueOnce({});
        await expect(completeRide("ride456")).resolves.toBeUndefined();
        expect(db.query).toHaveBeenCalledWith(
            expect.any(String),
            expect.arrayContaining(["ride456"])
        );
    });

    test("should throw an error if rideId is missing", async () => {
        await expect(completeRide("")).rejects.toThrow("Ride ID is required.");
        expect(db.query).not.toHaveBeenCalled();
    });

    test("should propagate error if db query fails", async () => {
        db.query.mockRejectedValueOnce(new Error("DB Error"));
        await expect(completeRide("ride456")).rejects.toThrow(
            "Failed to complete ride: DB Error"
        );
    });
});