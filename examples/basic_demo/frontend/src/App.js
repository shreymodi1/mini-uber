import React, { useState } from 'react';
import axios from 'axios';

/**
 * App component serves as the core React component for this demo.
 * It contains basic forms for creating drivers, riders, and rides,
 * and integrates with Flask routes via Axios requests.
 */
function App() {
  // State for driver inputs
  const [driverData, setDriverData] = useState({ name: '', vehicle: '' });
  // State for rider inputs
  const [riderData, setRiderData] = useState({ name: '' });
  // State for ride inputs
  const [rideData, setRideData] = useState({ driverId: '', riderId: '' });

  /**
   * Updates driverData state on input change.
   * @param {Event} e
   */
  const handleDriverChange = (e) => {
    setDriverData({
      ...driverData,
      [e.target.name]: e.target.value,
    });
  };

  /**
   * Submits new driver to the Flask backend.
   * @param {Event} e
   */
  const handleDriverSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/drivers', driverData);
      setDriverData({ name: '', vehicle: '' });
      // Handle success (e.g., show confirmation, refresh data, etc.)
    } catch (error) {
      // Handle error (e.g., show error message)
    }
  };

  /**
   * Updates riderData state on input change.
   * @param {Event} e
   */
  const handleRiderChange = (e) => {
    setRiderData({
      ...riderData,
      [e.target.name]: e.target.value,
    });
  };

  /**
   * Submits new rider to the Flask backend.
   * @param {Event} e
   */
  const handleRiderSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/riders', riderData);
      setRiderData({ name: '' });
      // Handle success
    } catch (error) {
      // Handle error
    }
  };

  /**
   * Updates rideData state on input change.
   * @param {Event} e
   */
  const handleRideChange = (e) => {
    setRideData({
      ...rideData,
      [e.target.name]: e.target.value,
    });
  };

  /**
   * Submits new ride to the Flask backend.
   * @param {Event} e
   */
  const handleRideSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/rides', rideData);
      setRideData({ driverId: '', riderId: '' });
      // Handle success
    } catch (error) {
      // Handle error
    }
  };

  return (
    <div>
      <h1>Basic Demo</h1>

      {/* Driver Form */}
      <form onSubmit={handleDriverSubmit}>
        <h2>Create Driver</h2>
        <div>
          <label htmlFor="driverName">Name: </label>
          <input
            id="driverName"
            name="name"
            type="text"
            value={driverData.name}
            onChange={handleDriverChange}
            required
          />
        </div>
        <div>
          <label htmlFor="driverVehicle">Vehicle: </label>
          <input
            id="driverVehicle"
            name="vehicle"
            type="text"
            value={driverData.vehicle}
            onChange={handleDriverChange}
            required
          />
        </div>
        <button type="submit">Add Driver</button>
      </form>

      {/* Rider Form */}
      <form onSubmit={handleRiderSubmit}>
        <h2>Create Rider</h2>
        <div>
          <label htmlFor="riderName">Name: </label>
          <input
            id="riderName"
            name="name"
            type="text"
            value={riderData.name}
            onChange={handleRiderChange}
            required
          />
        </div>
        <button type="submit">Add Rider</button>
      </form>

      {/* Ride Form */}
      <form onSubmit={handleRideSubmit}>
        <h2>Create Ride</h2>
        <div>
          <label htmlFor="driverId">Driver ID: </label>
          <input
            id="driverId"
            name="driverId"
            type="text"
            value={rideData.driverId}
            onChange={handleRideChange}
            required
          />
        </div>
        <div>
          <label htmlFor="riderId">Rider ID: </label>
          <input
            id="riderId"
            name="riderId"
            type="text"
            value={rideData.riderId}
            onChange={handleRideChange}
            required
          />
        </div>
        <button type="submit">Create Ride</button>
      </form>
    </div>
  );
}

export default App;