# Building Uber_lite From Scratch

Welcome to the “Uber_lite” tutorial! In this guide, we’ll build a simplified ride-hailing service (similar to Uber) using Node.js, Express, and Socket.IO. We’ll walk through creating key features:

1. Rider and Driver account creation, login  
2. Real-time location tracking (rider & driver)  
3. Ride requests, matching, and status updates  
4. Basic fare calculation and payments  
5. Trip history and receipts  

By the end, you’ll have a minimal viable product (MVP) demonstrating core ride-share functionality.

---
## 1. Project Setup

### 1.1 Prerequisites

• Node.js (>=14.x) installed  
• npm or yarn for package management  
• (Optional) Database like PostgreSQL/MongoDB for production storage; for simplicity, we’ll use an in-memory store or a lightweight JSON approach here  
• (Optional) A map or geocoding API key if you want real distance calculations  

### 1.2 Initialize the Project

1. Create a new folder for your project and navigate into it:
   ```bash
   mkdir uber_lite
   cd uber_lite
   ```

2. Initialize a Node.js project:
   ```bash
   npm init -y
   ```
   This creates a `package.json` file.

3. Install essential dependencies:
   ```bash
   npm install express socket.io
   ```
   (You can add other dependencies such as `bcrypt` for password hashing, `jsonwebtoken` for tokens, or a database driver later.)

---

## 2. Project Structure

Below is an outline of the directories and files we’ll create. The high-level idea is to keep each concern separated (auth, riders, drivers, rides, payments, realtime, utils, etc.):

```
uber_lite/
├── server.js
├── config.js
├── auth/
│   ├── auth_controller.js
│   └── auth_service.js
├── riders/
│   ├── rider_controller.js
│   └── rider_service.js
├── drivers/
│   ├── driver_controller.js
│   └── driver_service.js
├── rides/
│   ├── ride_controller.js
│   └── ride_service.js
├── payments/
│   ├── payment_controller.js
│   └── payment_service.js
├── realtime/
│   └── socket_manager.js
├── utils/
│   ├── logger.js
│   └── geo_utils.js
└── examples/
    └── basic_ride_request_demo/
        ├── demo_server.js
        ├── demo_config.js
        └── README.md
```

We’ll walk through each major section, showing minimal code snippets and explaining the logic. Feel free to expand or refactor these as needed.

---

## 3. Configuration

Create a file named `config.js`. This handles environment-based settings, such as database credentials, listening ports, and third-party API keys.

```js
// config.js

function loadConfig() {
  // In a real system, read from environment variables or .env files.
  // For demonstration, we’ll return a simple object:
  return {
    PORT: process.env.PORT || 3000,
    DB_URL: process.env.DB_URL || 'in-memory',  // or a real connection string
    PAYMENT_API_KEY: process.env.PAYMENT_API_KEY || 'demo-key',
    // ... other config as needed
  };
}

module.exports = {
  loadConfig
};
```

**Tip**: For production, consider using the `dotenv` package or a secure store like AWS Parameter Store.

---

## 4. Main Server

### 4.1 server.js

This is the heart of our Node.js application, responsible for:

• Initializing Express for API endpoints  
• Integrating Socket.IO for real-time communication  
• Hooking up our controllers (auth, riders, drivers, rides, payments)  

```js
// server.js

const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const { loadConfig } = require('./config');
const { initSocketIO } = require('./realtime/socket_manager');

// Import controllers
const authController = require('./auth/auth_controller');
const riderController = require('./riders/rider_controller');
const driverController = require('./drivers/driver_controller');
const rideController = require('./rides/ride_controller');
const paymentController = require('./payments/payment_controller');

function createServer() {
  const app = express();
  const server = http.createServer(app);
  const io = new Server(server);

  // Middleware
  app.use(express.json());

  // Routes
  app.use('/auth', authController);
  app.use('/riders', riderController);
  app.use('/drivers', driverController);
  app.use('/rides', rideController);
  app.use('/payments', paymentController);

  // Socket.IO
  initSocketIO(io);

  return server;
}

function startServer() {
  const server = createServer();
  const config = loadConfig();
  const port = config.PORT;

  server.listen(port, () => {
    console.log(`Uber_lite server is running on port ${port}`);
  });
}

if (require.main === module) {
  startServer();
}

module.exports = { createServer, startServer };
```

**Potential Pitfalls**:

• Make sure Socket.IO is attached to the same HTTP server as Express.  
• Use JSON body-parsing middleware for POST requests.  

---

## 5. Authentication Module

### 5.1 auth_service.js

Handles the logic of creating and verifying user accounts. In a real system, this would involve hashing passwords and storing them in a database.

```js
// auth/auth_service.js

// In-memory user store for demo (replace with real DB calls)
const users = [];  // Example: [{ id, email, password, role: 'rider'|'driver' }]

function createUserAccount(userData) {
  // For a real app, hash the password (e.g., with bcrypt)
  const newUser = {
    id: users.length + 1,
    email: userData.email,
    password: userData.password,
    role: userData.role
  };
  users.push(newUser);
  return newUser;
}

function verifyCredentials(email, password) {
  const user = users.find(u => u.email === email && u.password === password);
  return user || null;
}

module.exports = {
  createUserAccount,
  verifyCredentials
};
```

### 5.2 auth_controller.js

An Express router that exposes signup, login, and logout endpoints.

```js
// auth/auth_controller.js

const express = require('express');
const router = express.Router();

const {
  createUserAccount,
  verifyCredentials
} = require('./auth_service');

// POST /auth/signup
router.post('/signup', (req, res) => {
  const { email, password, role } = req.body;
  if (!email || !password || !role) {
    return res.status(400).json({ error: 'Missing fields' });
  }
  const newUser = createUserAccount({ email, password, role });
  return res.status(201).json({ message: 'User created', user: newUser });
});

// POST /auth/login
router.post('/login', (req, res) => {
  const { email, password } = req.body;
  const user = verifyCredentials(email, password);
  if (!user) return res.status(401).json({ error: 'Invalid credentials' });

  // For demonstration, we’ll just return a dummy token
  // In production, consider JWT or session-based auth
  return res.json({
    message: 'Login successful',
    token: `dummy-token-for-user-${user.id}`
  });
});

// POST /auth/logout
router.post('/logout', (req, res) => {
  // A real app might invalidate a token here
  return res.json({ message: 'Logout successful' });
});

module.exports = router;
```

**Best Practice**: Use secure password hashing (e.g., bcrypt) and token-based authentication (JWT).

---

## 6. Rider Module

### 6.1 rider_service.js

Manages rider operations like requesting a ride, canceling, and fetching trip history.

```js
// riders/rider_service.js

const { matchDriver } = require('../rides/ride_service');

// In-memory rides data for demonstration
const rides = []; // e.g. { id, riderId, driverId, status, pickupLocation, destination }

function requestRide(riderId, pickupLocation, destination) {
  const rideId = rides.length + 1;
  const newRide = {
    id: rideId,
    riderId,
    driverId: null,
    status: 'PENDING',
    pickupLocation,
    destination
  };
  rides.push(newRide);

  // Attempt driver match
  const driver = matchDriver(pickupLocation);
  if (driver) {
    newRide.driverId = driver.id;
    newRide.status = 'DRIVER_ASSIGNED';
  }
  return newRide;
}

function cancelRide(rideId) {
  const ride = rides.find(r => r.id === parseInt(rideId));
  if (ride && ride.status === 'PENDING') {
    ride.status = 'CANCELED';
    return ride;
  }
  return null;
}

function fetchRiderHistory(riderId) {
  return rides.filter(r => r.riderId === parseInt(riderId) && r.status === 'COMPLETED');
}

module.exports = {
  requestRide,
  cancelRide,
  fetchRiderHistory
};
```

### 6.2 rider_controller.js

Express endpoints for riders.

```js
// riders/rider_controller.js

const express = require('express');
const router = express.Router();

const {
  requestRide,
  cancelRide,
  fetchRiderHistory
} = require('./rider_service');

// POST /riders/request
router.post('/request', (req, res) => {
  const { riderId, pickupLocation, destination } = req.body;
  if (!riderId || !pickupLocation || !destination) {
    return res.status(400).json({ error: 'Missing fields' });
  }
  const ride = requestRide(riderId, pickupLocation, destination);
  return res.json(ride);
});

// POST /riders/cancel
router.post('/cancel', (req, res) => {
  const { rideId } = req.body;
  const result = cancelRide(rideId);
  if (!result) {
    return res.status(400).json({ error: 'Cannot cancel this ride' });
  }
  return res.json(result);
});

// GET /riders/history/:riderId
router.get('/history/:riderId', (req, res) => {
  const { riderId } = req.params;
  const history = fetchRiderHistory(riderId);
  return res.json(history);
});

module.exports = router;
```

---

## 7. Driver Module

### 7.1 driver_service.js

Manages drivers’ availability, accepting rides, and completing them.

```js
// drivers/driver_service.js

// In-memory driver data
const drivers = []; // e.g. { id, isAvailable, location }

function setDriverAvailability(driverId, status) {
  let driver = drivers.find(d => d.id === parseInt(driverId));
  if (!driver) {
    driver = { id: parseInt(driverId), isAvailable: false, location: null };
    drivers.push(driver);
  }
  driver.isAvailable = status === 'online';
  return driver;
}

function acceptRide(driverId, ride) {
  ride.driverId = parseInt(driverId);
  ride.status = 'ONGOING';
  // Mark driver as unavailable
  const driver = drivers.find(d => d.id === parseInt(driverId));
  if (driver) {
    driver.isAvailable = false;
  }
  return ride;
}

function completeRide(ride) {
  ride.status = 'COMPLETED';
  // Payment logic can be triggered here
  return ride;
}

module.exports = {
  setDriverAvailability,
  acceptRide,
  completeRide,
  drivers
};
```

### 7.2 driver_controller.js

```js
// drivers/driver_controller.js

const express = require('express');
const router = express.Router();

const { setDriverAvailability, acceptRide, completeRide, drivers } = require('./driver_service');
const { rides } = require('../riders/rider_service'); // or separate store

// POST /drivers/availability
router.post('/availability', (req, res) => {
  const { driverId, status } = req.body;
  const driver = setDriverAvailability(driverId, status);
  return res.json(driver);
});

// POST /drivers/accept
router.post('/accept', (req, res) => {
  const { driverId, rideId } = req.body;
  const ride = rides.find(r => r.id === parseInt(rideId));
  if (!ride || ride.status !== 'PENDING' && ride.status !== 'DRIVER_ASSIGNED') {
    return res.status(400).json({ error: 'Ride not available for acceptance' });
  }
  const updatedRide = acceptRide(driverId, ride);
  return res.json(updatedRide);
});

// POST /drivers/complete
router.post('/complete', (req, res) => {
  const { rideId } = req.body;
  const ride = rides.find(r => r.id === parseInt(rideId));
  if (!ride || ride.status !== 'ONGOING') {
    return res.status(400).json({ error: 'Ride not in progress' });
  }
  const completed = completeRide(ride);
  return res.json(completed);
});

module.exports = router;
```

---

## 8. Rides Module

While the rider and driver services contain some ride logic, we’ll keep ride status updates and matching logic in a central place.

### 8.1 ride_service.js

```js
// rides/ride_service.js

const { drivers } = require('../drivers/driver_service');

// Stub for distance-based driver matching
function matchDriver(riderLocation) {
  // In a real system, compute distance from each driver’s location
  // For the MVP, pick the first "available" driver
  const availableDriver = drivers.find(d => d.isAvailable === true);
  return availableDriver || null;
}

function updateRideStatus(ride, status) {
  ride.status = status;
  // Possibly emit a socket event with real-time updates
  return ride;
}

function broadcastLocation(ride, lat, long) {
  // This is where you'd use Socket.IO to emit new location data
  // For this MVP, just log it
  console.log(`Ride ${ride.id} location updated to lat=${lat}, long=${long}`);
  return { rideId: ride.id, lat, long };
}

module.exports = {
  matchDriver,
  updateRideStatus,
  broadcastLocation
};
```

### 8.2 ride_controller.js

```js
// rides/ride_controller.js

const express = require('express');
const router = express.Router();

const { rides } = require('../riders/rider_service'); // in-memory rides
const { updateRideStatus, broadcastLocation } = require('./ride_service');

// GET /rides/status/:rideId
router.get('/status/:rideId', (req, res) => {
  const { rideId } = req.params;
  const ride = rides.find(r => r.id === parseInt(rideId));
  if (!ride) return res.status(404).json({ error: 'Ride not found' });
  return res.json({ status: ride.status });
});

// POST /rides/location
router.post('/location', (req, res) => {
  const { rideId, lat, long } = req.body;
  const ride = rides.find(r => r.id === parseInt(rideId));
  if (!ride) return res.status(404).json({ error: 'Ride not found' });
  const locationUpdate = broadcastLocation(ride, lat, long);
  return res.json(locationUpdate);
});

module.exports = router;
```

---

## 9. Payments Module

### 9.1 payment_service.js

```js
// payments/payment_service.js

function calculateFare(distance, time) {
  // Very naive approach: base fare + per km + per minute
  const baseFare = 2.00;
  const costPerKm = 1.00;
  const costPerMin = 0.50;
  return baseFare + (costPerKm * distance) + (costPerMin * time);
}

function processPayment(riderId, driverId, amount) {
  // In a real app, integrate with a payment gateway
  console.log(`Charging rider ${riderId} $${amount}`);
  console.log(`Paying driver ${driverId} minus fees`);
  return {
    paymentId: `pay_${Date.now()}`,
    amount,
    riderId,
    driverId,
    status: 'COMPLETED'
  };
}

function getPaymentDetails(rideId) {
  // Return dummy data for now
  return {
    rideId,
    paymentId: `pay_demo_${rideId}`,
    amount: 10.0,
    status: 'COMPLETED'
  };
}

module.exports = {
  calculateFare,
  processPayment,
  getPaymentDetails
};
```

### 9.2 payment_controller.js

```js
// payments/payment_controller.js

const express = require('express');
const router = express.Router();

const {
  calculateFare,
  processPayment,
  getPaymentDetails
} = require('./payment_service');

const { rides } = require('../riders/rider_service');

// POST /payments/initiate
router.post('/initiate', (req, res) => {
  const { rideId, distance, time } = req.body;
  const ride = rides.find(r => r.id === parseInt(rideId));
  if (!ride || ride.status !== 'COMPLETED') {
    return res.status(400).json({ error: 'Ride not completed or not found' });
  }
  const fare = calculateFare(distance, time);
  const paymentReceipt = processPayment(ride.riderId, ride.driverId, fare);
  return res.json(paymentReceipt);
});

// GET /payments/details/:rideId
router.get('/details/:rideId', (req, res) => {
  const { rideId } = req.params;
  const details = getPaymentDetails(rideId);
  return res.json(details);
});

module.exports = router;
```

---

## 10. Real-Time Module

### 10.1 socket_manager.js

Sets up Socket.IO events for location updates, ride status changes, etc.

```js
// realtime/socket_manager.js

function initSocketIO(io) {
  io.on('connection', (socket) => {
    console.log('Client connected via Socket.IO');

    socket.on('driverLocation', (data) => {
      const { driverId, location } = data;
      console.log(`Driver ${driverId} location:`, location);
      // Broadcast to relevant riders, or store location, etc.
      io.emit('driverLocationUpdate', data);
    });

    socket.on('rideStatusChange', (data) => {
      const { rideId, status } = data;
      console.log(`Ride ${rideId} status updated to ${status}`);
      io.emit('rideStatusUpdate', data);
    });

    socket.on('disconnect', () => {
      console.log('Client disconnected');
    });
  });
}

function onDriverLocationUpdate(driverId, location) {
  // In a real system, you might do: io.emit(...)
  console.log('onDriverLocationUpdate called');
}

function onRideStatusChange(rideId, status) {
  // In a real system, you might do: io.emit(...)
  console.log('onRideStatusChange called');
}

module.exports = {
  initSocketIO,
  onDriverLocationUpdate,
  onRideStatusChange
};
```

---

## 11. Utilities

### 11.1 logger.js

```js
// utils/logger.js

function logDebug(message) {
  console.debug(`[DEBUG] ${message}`);
}

function logInfo(message) {
  console.info(`[INFO] ${message}`);
}

function logError(message) {
  console.error(`[ERROR] ${message}`);
}

module.exports = {
  logDebug,
  logInfo,
  logError
};
```

### 11.2 geo_utils.js

```js
// utils/geo_utils.js

function calculateDistance(lat1, lon1, lat2, lon2) {
  // Simplified Haversine or a placeholder
  return Math.random() * 10; // Return a random distance
}

function estimateTime(distance) {
  // Example: average speed = 40 km/h => time in hours
  // Convert hours to minutes if needed
  return distance / 40; 
}

module.exports = {
  calculateDistance,
  estimateTime
};
```

---

## 12. Example: Basic Ride Request Demo

In `examples/basic_ride_request_demo/`, we’ll create a small script that starts our server and simulates a basic ride flow with mock data.

### 12.1 demo_config.js

```js
// examples/basic_ride_request_demo/demo_config.js

function loadDemoConfig() {
  // Mock environment variables or override some defaults if needed
  return {
    PORT: 4000  // Hardcode a different port for the demo
  };
}

module.exports = { loadDemoConfig };
```

### 12.2 demo_server.js

```js
// examples/basic_ride_request_demo/demo_server.js

const { createServer } = require('../../server');
const { loadConfig } = require('../../config');
const { loadDemoConfig } = require('./demo_config');

function initDemoServer() {
  const demoConfig = loadDemoConfig();
  const globalConfig = loadConfig();

  // Merge or override as appropriate
  globalConfig.PORT = demoConfig.PORT;
  
  // Create the server
  const server = createServer();
  server.listen(globalConfig.PORT, () => {
    console.log(`Demo server running on port ${globalConfig.PORT}`);
    demoRideFlow();
  });
}

function demoRideFlow() {
  console.log('Simulating a rider requesting a ride, a driver accepting, and completing...');

  // In a real test, call HTTP endpoints or use a test framework like jest/supertest
  console.log('1) Rider signs up, logs in, and requests a ride...');
  console.log('2) Driver goes online, accepts ride...');
  console.log('3) Ride is completed, payment is processed...');
  console.log('All steps can be automated with fetch/axios for a real test.');
}

if (require.main === module) {
  initDemoServer();
}

module.exports = { initDemoServer, demoRideFlow };
```

### 12.3 README.md

Explain how to install dependencies, run the demo, and simulate ride requests.

```markdown
# Basic Ride Request Demo

## Setup
1. Install project dependencies from the root directory:
   ```bash
   npm install
   ```
2. Navigate to the `examples/basic_ride_request_demo` folder.

## Running the Demo
```bash
node demo_server.js
```

By default, this starts the Demo server on port 4000.  
Use tools like Postman, curl, or a browser to test endpoints (e.g., /auth/signup, /riders/request, /drivers/accept, etc.).
```

---

## 13. Running the Full MVP

1. Install dependencies:
   ```bash
   npm install
   ```
2. Start the main server:
   ```bash
   node server.js
   ```
   or
   ```bash
   npm start
   ```
3. Use an API testing tool to create users (rider/driver), set driver availability, request a ride, accept it, and complete it.  
4. (Optional) Start the demo server from `examples/basic_ride_request_demo`.

---

## 14. Next Steps & Expansion

• Replace in-memory stores with a real database (MongoDB, PostgreSQL, etc.).  
• Implement secure password hashing (bcrypt), JWT authentication, and proper session management.  
• Integrate real geocoding and distance calculation (like Google Maps or OpenStreetMap).  
• Use a payment gateway (Stripe, PayPal, etc.) for actual transactions.  
• Refine real-time updates (location, ride status) via Socket.IO channels/rooms.  

---

## Conclusion

You’ve now built a minimal version of an “Uber-like” service from scratch, demonstrating:

• User authentication (signup, login, logout)  
• Driver availability and real-time location updates  
• Request/accept/cancel/complete ride workflow  
• Fare calculation and payment logic  
• Real-time communication using Socket.IO  

This MVP framework can serve as a starting point for more complex production features: robust security, scalability, and integration with third-party APIs. Happy coding!