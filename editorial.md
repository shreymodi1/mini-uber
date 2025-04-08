# Building Uber_lite: A Minimal Viable Rideshare App

Welcome to this hands-on tutorial for building a simplified rideshare application — **Uber_lite**. We’ll guide you through creating a minimal viable product (MVP) from scratch using Python’s FastAPI framework, Pydantic for data validation, (optionally) SQLAlchemy for data persistence, and a Flask + React demo to showcase how the API can be consumed. Follow these steps to set up the core features of a rideshare platform, including rider/driver onboarding, ride matching, payments, and ratings.

## Overview

This MVP includes the following features:
1. Rider sign-up, onboarding, and profile management  
2. Driver registration, onboarding, vehicle management  
3. Ride request creation, matching to available drivers  
4. Real-time ride status updates and location tracking  
5. Payment processing (basic fare calculation, driver payouts)  
6. Rating and feedback system (rider rates driver, driver rates rider)

We’ll also provide an example folder with a Flask application that calls the FastAPI endpoints (using `requests` or `httpx`) and a basic React frontend demonstrating a simple user interface flow.

---

## 1. Project Structure

We’ll create the following directory layout with one main FastAPI app and several modules:

```
uber_lite/
├── main.py
├── config.py
├── requirements.txt
├── riders/
│   ├── riders_router.py
│   ├── riders_service.py
│   └── riders_models.py
├── drivers/
│   ├── drivers_router.py
│   ├── drivers_service.py
│   └── drivers_models.py
├── rides/
│   ├── rides_router.py
│   ├── rides_service.py
│   └── rides_models.py
├── payments/
│   ├── payments_router.py
│   ├── payments_service.py
│   └── payments_models.py
├── ratings/
│   ├── ratings_router.py
│   ├── ratings_service.py
│   └── ratings_models.py
├── utils/
│   ├── logger.py
│   ├── auth.py
│   └── geolocation.py
└── examples/
    └── basic_demo/
        ├── demo_api.py
        ├── demo_app.py
        ├── demo_config.py
        ├── README.md
        └── frontend/
            ├── package.json
            ├── public/
            │   └── index.html
            └── src/
                ├── App.js
                └── index.js
```

Below is a step-by-step guide to building each piece. Feel free to adapt or modify for your environment and exact needs.

---

## 2. Prerequisites

- Python 3.8+  
- A virtual environment tool (e.g., `venv`, `conda`) or dependency manager like Poetry  
- Node.js (14.x or above) for the React frontend  
- A database (Postgres, MySQL, or even SQLite for local development)  
- Optionally, SQLAlchemy if you want to use an ORM for database access

---

## 3. Initial Setup

### Step 3.1: Create Your Project Directories

Create a folder named `uber_lite` (or your preferred name) and subdirectories as shown above.

```bash
mkdir uber_lite
cd uber_lite

mkdir riders drivers rides payments ratings utils examples
cd examples && mkdir basic_demo && cd basic_demo
mkdir frontend
touch demo_api.py demo_app.py demo_config.py README.md
cd ..
cd ..
```

### Step 3.2: Initialize a Virtual Environment & Install Dependencies

Within `uber_lite`, create and activate a virtual environment, then install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install fastapi uvicorn pydantic
# Optional: pip install sqlalchemy psycopg2  # For PostgreSQL
pip install requests httpx Flask
# For demonstration or if you want extra swagger doc features
pip install python-multipart
```

Then create a `requirements.txt` file:

```bash
echo "fastapi
uvicorn
pydantic
requests
httpx
Flask
# optional for DB
sqlalchemy
psycopg2
" > requirements.txt
```

---

## 4. Configuration

Create a file named `config.py` that handles environment variables and database connections:

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

def load_config():
    # In real usage, you might load from a .env file or environment variables
    return {
        "DB_URL": os.getenv("DB_URL", "sqlite:///./uber_lite.db"),
        "SECRET_KEY": os.getenv("SECRET_KEY", "supersecret"),
    }

def get_database_url():
    config = load_config()
    return config["DB_URL"]
```

> **Pitfall:** Make sure to keep sensitive secrets (API keys, tokens) outside of source control or load them from environment-specific files.

---

## 5. Main Application

### Step 5.1: Create `main.py`

`main.py` will define and launch our FastAPI app, mounting each of our feature routers:

```python
# main.py
from fastapi import FastAPI
import uvicorn

# Import your routers
from riders.riders_router import router as riders_router
from drivers.drivers_router import router as drivers_router
from rides.rides_router import router as rides_router
from payments.payments_router import router as payments_router
from ratings.ratings_router import router as ratings_router

def create_app():
    app = FastAPI(title="Uber_lite API", version="0.1.0")
    # Include our feature routers
    app.include_router(riders_router, prefix="/riders", tags=["riders"])
    app.include_router(drivers_router, prefix="/drivers", tags=["drivers"])
    app.include_router(rides_router, prefix="/rides", tags=["rides"])
    app.include_router(payments_router, prefix="/payments", tags=["payments"])
    app.include_router(ratings_router, prefix="/ratings", tags=["ratings"])
    return app

def run_app():
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run_app()
```

You may run the server with:
```bash
python main.py
```
Or with uvicorn directly:
```bash
uvicorn main:create_app --reload
```

---

## 6. Riders Module

### Step 6.1: Models

In `riders/riders_models.py`, define Pydantic or SQLAlchemy models. For simplicity, let’s do a Pydantic model:

```python
# riders_models.py
from pydantic import BaseModel, Field
from typing import Optional

class RiderCreate(BaseModel):
    name: str
    phone_number: str
    payment_method: str

class Rider(BaseModel):
    rider_id: int
    name: str
    phone_number: str
    payment_method: str
```

> **Note:** If using SQLAlchemy, create a `Base` and define a Rider entity with columns for `id`, `name`, etc.

### Step 6.2: Service

`riders/riders_service.py` handles the business logic:

```python
# riders_service.py
from typing import Optional
from .riders_models import RiderCreate, Rider

# Fake in-memory store for demonstration
FAKE_RIDERS_DB = {}
RIDER_COUNTER = 1

def create_rider(name: str, phone_number: str, payment_method: str) -> Rider:
    global RIDER_COUNTER
    rider_id = RIDER_COUNTER
    RIDER_COUNTER += 1

    rider = Rider(rider_id=rider_id, name=name,
                  phone_number=phone_number,
                  payment_method=payment_method)
    FAKE_RIDERS_DB[rider_id] = rider
    return rider

def fetch_rider(rider_id: int) -> Optional[Rider]:
    return FAKE_RIDERS_DB.get(rider_id)
```

### Step 6.3: Router

Create a router in `riders_router.py`:

```python
# riders_router.py
from fastapi import APIRouter, HTTPException
from .riders_models import RiderCreate, Rider
from .riders_service import create_rider, fetch_rider

router = APIRouter()

@router.post("/", response_model=Rider)
def create_rider_endpoint(rider_data: RiderCreate):
    rider = create_rider(
        name=rider_data.name,
        phone_number=rider_data.phone_number,
        payment_method=rider_data.payment_method
    )
    return rider

@router.get("/{rider_id}", response_model=Rider)
def get_rider_profile_endpoint(rider_id: int):
    rider = fetch_rider(rider_id)
    if not rider:
        raise HTTPException(status_code=404, detail="Rider not found")
    return rider
```

---

## 7. Drivers Module

### Step 7.1: Models
```python
# drivers_models.py
from pydantic import BaseModel

class DriverCreate(BaseModel):
    name: str
    license_number: str
    vehicle_info: str

class Driver(BaseModel):
    driver_id: int
    name: str
    license_number: str
    vehicle_info: str
```

### Step 7.2: Service
```python
# drivers_service.py
FAKE_DRIVERS_DB = {}
DRIVER_COUNTER = 1

def create_driver(name: str, license_number: str, vehicle_info: str):
    global DRIVER_COUNTER
    driver_id = DRIVER_COUNTER
    DRIVER_COUNTER += 1

    driver = {
        "driver_id": driver_id,
        "name": name,
        "license_number": license_number,
        "vehicle_info": vehicle_info
    }
    FAKE_DRIVERS_DB[driver_id] = driver
    return driver

def update_vehicle_details(driver_id: int, vehicle_info: str):
    driver = FAKE_DRIVERS_DB.get(driver_id)
    if driver:
        driver["vehicle_info"] = vehicle_info
        FAKE_DRIVERS_DB[driver_id] = driver
    return driver
```

### Step 7.3: Router
```python
# drivers_router.py
from fastapi import APIRouter, HTTPException
from .drivers_service import create_driver, update_vehicle_details
from .drivers_models import DriverCreate

router = APIRouter()

@router.post("/")
def create_driver_endpoint(driver_data: DriverCreate):
    new_driver = create_driver(
        name=driver_data.name,
        license_number=driver_data.license_number,
        vehicle_info=driver_data.vehicle_info
    )
    return new_driver

@router.put("/{driver_id}")
def update_vehicle_details_endpoint(driver_id: int, vehicle_info: str):
    driver = update_vehicle_details(driver_id, vehicle_info)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver
```

---

## 8. Rides Module

### Step 8.1: Models
```python
# rides_models.py
from pydantic import BaseModel
from typing import Optional

class RideCreate(BaseModel):
    rider_id: int
    pickup_location: str
    dropoff_location: str

class Ride(BaseModel):
    ride_id: int
    rider_id: int
    driver_id: Optional[int]
    pickup_location: str
    dropoff_location: str
    status: str
```

### Step 8.2: Service
```python
# rides_service.py
FAKE_RIDES_DB = {}
RIDE_COUNTER = 1

def create_ride(rider_id: int, pickup_location: str, dropoff_location: str):
    global RIDE_COUNTER
    ride_id = RIDE_COUNTER
    RIDE_COUNTER += 1

    ride = {
        "ride_id": ride_id,
        "rider_id": rider_id,
        "driver_id": None,
        "pickup_location": pickup_location,
        "dropoff_location": dropoff_location,
        "status": "requested"
    }
    FAKE_RIDES_DB[ride_id] = ride
    return ride

def assign_driver_to_ride(ride_id: int):
    # Simplified logic: pick any available driver if needed
    # For now we’ll just pick a random ID or skip actual matching
    ride = FAKE_RIDES_DB.get(ride_id)
    if ride:
        # Example: Hardcode driver_id = 1 for now
        ride["driver_id"] = 1
        ride["status"] = "accepted"
    return ride

def update_ride_status(ride_id: int, new_status: str):
    ride = FAKE_RIDES_DB.get(ride_id)
    if ride:
        ride["status"] = new_status
        FAKE_RIDES_DB[ride_id] = ride
    return ride
```

### Step 8.3: Router
```python
# rides_router.py
from fastapi import APIRouter, HTTPException
from .rides_models import RideCreate
from .rides_service import create_ride, assign_driver_to_ride, update_ride_status

router = APIRouter()

@router.post("/request_ride")
def request_ride_endpoint(request_data: RideCreate):
    ride = create_ride(
        rider_id=request_data.rider_id,
        pickup_location=request_data.pickup_location,
        dropoff_location=request_data.dropoff_location
    )
    return ride

@router.post("/assign_driver/{ride_id}")
def assign_driver_endpoint(ride_id: int):
    ride = assign_driver_to_ride(ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    return ride

@router.put("/{ride_id}/status")
def update_ride_status_endpoint(ride_id: int, status: str):
    ride = update_ride_status(ride_id, status)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    return ride
```

---

## 9. Payments Module

### Step 9.1: Models
```python
# payments_models.py
from pydantic import BaseModel

class Payment(BaseModel):
    ride_id: int
    amount: float
    status: str
```

### Step 9.2: Service
```python
# payments_service.py
import random

def calculate_fare(pickup_location, dropoff_location, duration=None, distance=None):
    # Simplified formula or a random baseline
    return round(random.uniform(5.0, 20.0), 2)

def charge_rider(rider_id, amount):
    # In real scenario, call a payment gateway
    return {"rider_id": rider_id, "charged_amount": amount, "status": "success"}

def payout_driver(driver_id, amount):
    # Simulate driver payout
    return {"driver_id": driver_id, "payout_amount": amount, "status": "payout_sent"}
```

### Step 9.3: Router
```python
# payments_router.py
from fastapi import APIRouter, HTTPException
from .payments_service import calculate_fare, charge_rider, payout_driver

router = APIRouter()

@router.get("/calculate_fare/{ride_id}")
def calculate_fare_endpoint(ride_id: int):
    # For demonstration, pass dummy data
    fare = calculate_fare("pickup", "dropoff")
    return {"ride_id": ride_id, "fare": fare}

@router.post("/process_payment/{ride_id}")
def process_payment_endpoint(ride_id: int):
    # Hardcoding or retrieving the rider/driver details from DB is needed in real usage
    result = charge_rider(rider_id=1, amount=10.0)
    return result

@router.post("/driver_payout/{ride_id}")
def disburse_driver_payment_endpoint(ride_id: int):
    # Hardcoding the driver ID for demonstration
    result = payout_driver(driver_id=1, amount=8.0)
    return result
```

---

## 10. Ratings Module

### Step 10.1: Models
```python
# ratings_models.py
from pydantic import BaseModel

class Rating(BaseModel):
    user_id: int
    rating: float
    review: str
```

### Step 10.2: Service
```python
# ratings_service.py
# Simple in-memory store for demonstration
DRIVER_RATINGS = {}
RIDER_RATINGS = {}

def rate_driver(ride_id: int, rating: float, review: str):
    # In a real scenario, link with `ride_id` and `driver_id`
    DRIVER_RATINGS.setdefault(1, []).append(rating)
    return rating

def rate_rider(ride_id: int, rating: float, review: str):
    # Simplify to rider_id=1 for demonstration
    RIDER_RATINGS.setdefault(1, []).append(rating)
    return rating

def get_driver_rating(driver_id: int):
    ratings = DRIVER_RATINGS.get(driver_id, [])
    if ratings:
        return sum(ratings) / len(ratings)
    return 0

def get_rider_rating(rider_id: int):
    ratings = RIDER_RATINGS.get(rider_id, [])
    if ratings:
        return sum(ratings) / len(ratings)
    return 0
```

### Step 10.3: Router
```python
# ratings_router.py
from fastapi import APIRouter, HTTPException
from .ratings_service import rate_driver, rate_rider, get_rider_rating, get_driver_rating

router = APIRouter()

@router.post("/driver/{ride_id}")
def rate_driver_endpoint(ride_id: int, rating: float, review: str):
    res = rate_driver(ride_id, rating, review)
    return {"status": "driver rated", "rating": res}

@router.post("/rider/{ride_id}")
def rate_rider_endpoint(ride_id: int, rating: float, review: str):
    res = rate_rider(ride_id, rating, review)
    return {"status": "rider rated", "rating": res}

@router.get("/rider_rating/{rider_id}")
def get_rider_rating_endpoint(rider_id: int):
    rating = get_rider_rating(rider_id)
    return {"rider_id": rider_id, "rating": rating}

@router.get("/driver_rating/{driver_id}")
def get_driver_rating_endpoint(driver_id: int):
    rating = get_driver_rating(driver_id)
    return {"driver_id": driver_id, "rating": rating}
```

---

## 11. Utilities Module

Create `logger.py`, `auth.py`, `geolocation.py` as placeholders. For brevity:

```python
# logger.py
def log_debug(message: str):
    print(f"[DEBUG] {message}")

def log_info(message: str):
    print(f"[INFO] {message}")

def log_error(message: str):
    print(f"[ERROR] {message}")
```

```python
# auth.py
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "something"

def create_jwt(user_id: int):
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_jwt(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
```

```python
# geolocation.py
import math

def calculate_distance(coord1, coord2):
    # Dummy calculation using Euclidean distance
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def estimate_travel_time(coord1, coord2):
    distance = calculate_distance(coord1, coord2)
    # Assume average speed ~ 1 distance unit/minute
    return distance
```

---

## 12. Example: Flask + React Integration

### Step 12.1: Flask Demo

Inside `examples/basic_demo`, create `demo_api.py` to show how to call the FastAPI endpoints:

```python
# demo_api.py
import requests

UBER_LITE_BASE_URL = "http://localhost:8000"

def create_rider(name, phone_number, payment_method):
    url = f"{UBER_LITE_BASE_URL}/riders/"
    payload = {
        "name": name,
        "phone_number": phone_number,
        "payment_method": payment_method
    }
    response = requests.post(url, json=payload)
    return response.json()

def create_driver(name, license_number, vehicle_info):
    url = f"{UBER_LITE_BASE_URL}/drivers/"
    payload = {
        "name": name,
        "license_number": license_number,
        "vehicle_info": vehicle_info
    }
    response = requests.post(url, json=payload)
    return response.json()

def request_ride(rider_id, pickup, dropoff):
    url = f"{UBER_LITE_BASE_URL}/rides/request_ride"
    payload = {
        "rider_id": rider_id,
        "pickup_location": pickup,
        "dropoff_location": dropoff
    }
    response = requests.post(url, json=payload)
    return response.json()

def calculate_fare(ride_id):
    url = f"{UBER_LITE_BASE_URL}/payments/calculate_fare/{ride_id}"
    response = requests.get(url)
    return response.json()

def process_payment(ride_id):
    url = f"{UBER_LITE_BASE_URL}/payments/process_payment/{ride_id}"
    response = requests.post(url)
    return response.json()
```

Create `demo_app.py` for the Flask server:

```python
# demo_app.py
from flask import Flask, request, jsonify
import demo_api

def create_flask_app():
    app = Flask(__name__)

    @app.route("/demo/create_rider", methods=["POST"])
    def create_rider():
        data = request.json
        result = demo_api.create_rider(data["name"], data["phone_number"], data["payment_method"])
        return jsonify(result)

    @app.route("/demo/request_ride", methods=["POST"])
    def create_ride():
        data = request.json
        result = demo_api.request_ride(data["rider_id"], data["pickup"], data["dropoff"])
        return jsonify(result)

    # Add more endpoints as needed: create_driver, calculate_fare, etc.

    return app

def run_demo_app():
    app = create_flask_app()
    app.run(port=5000, debug=True)

if __name__ == "__main__":
    run_demo_app()
```

Create an optional `demo_config.py`:

```python
# demo_config.py
import os

def load_demo_config():
    return {
        "FASTAPI_URL": os.getenv("UBER_LITE_BASE_URL", "http://localhost:8000")
    }

def get_uber_lite_api_url():
    config = load_demo_config()
    return config["FASTAPI_URL"]
```

### Step 12.2: React Frontend (Optional Demo)

In `examples/basic_demo/frontend/`, you could initialize a React app (e.g. with `create-react-app`). For demonstration:

• `package.json`:

```json
{
  "name": "uber_lite_demo_frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^17.0.0",
    "react-dom": "^17.0.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  }
}
```

• `public/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Uber_lite Demo</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
```

• `src/index.js`:

```javascript
import React from "react";
import ReactDOM from "react-dom";
import App from "./App";

ReactDOM.render(<App />, document.getElementById("root"));
```

• `src/App.js` (a basic form to create a rider and request a ride, for instance):

```javascript
import React, { useState } from 'react';

function App() {
  const [riderName, setRiderName] = useState("");
  const [riderPhone, setRiderPhone] = useState("");
  const [pickup, setPickup] = useState("");
  const [dropoff, setDropoff] = useState("");
  const [result, setResult] = useState("");

  const createRider = async () => {
    const res = await fetch("http://localhost:5000/demo/create_rider", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        name: riderName,
        phone_number: riderPhone,
        payment_method: "credit_card"
      })
    });
    const data = await res.json();
    setResult(JSON.stringify(data));
  };

  const requestRide = async () => {
    // Hardcode rider_id=1 in this example
    const res = await fetch("http://localhost:5000/demo/request_ride", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        rider_id: 1,
        pickup,
        dropoff
      })
    });
    const data = await res.json();
    setResult(JSON.stringify(data));
  };

  return (
    <div>
      <h1>Uber_lite Demo</h1>
      
      <h2>Create Rider</h2>
      <input placeholder="Rider Name" value={riderName} onChange={(e) => setRiderName(e.target.value)} />
      <input placeholder="Phone" value={riderPhone} onChange={(e) => setRiderPhone(e.target.value)} />
      <button onClick={createRider}>Create Rider</button>

      <h2>Request Ride</h2>
      <input placeholder="Pickup Location" value={pickup} onChange={(e) => setPickup(e.target.value)} />
      <input placeholder="Dropoff Location" value={dropoff} onChange={(e) => setDropoff(e.target.value)} />
      <button onClick={requestRide}>Request Ride</button>
      
      <h3>Response:</h3>
      <pre>{result}</pre>
    </div>
  );
}

export default App;
```

> **Tip:** The React app calls the Flask server at `localhost:5000`, which in turn calls the FastAPI service at `localhost:8000`.

### Step 12.3: Running the Example

1. In one terminal, run the FastAPI server:
   ```bash
   uvicorn main:create_app --reload
   ```
2. In another terminal, run the Flask server:
   ```bash
   cd examples/basic_demo
   python demo_app.py
   ```
3. (Optional) In a third terminal, run the React frontend:
   ```bash
   cd examples/basic_demo/frontend
   npm install
   npm start
   ```
4. Navigate to http://localhost:3000 to view the React demo UI.

---

## 13. Next Steps & Best Practices

• **Persisting Data** – The above code uses in-memory dictionaries. For a real application, integrate with SQLAlchemy or a database driver.  
• **Security and Authentication** – The `utils/auth.py` file is just a placeholder. You’ll want robust user authentication, possibly OAuth2 with JWT.  
• **Validation and Error Handling** – Expand your Pydantic models, add more custom validations. Return consistent error responses.  
• **Logging & Monitoring** – Use structured logs (e.g., `logging` library), and consider monitoring tools for production.  
• **Scalability** – Host behind a production server (e.g., Gunicorn + Uvicorn workers) and load balance.  

> **Potential Pitfall:** Don’t rely on in-memory data for real-world scenarios. A server restart wipes data, and concurrency across multiple processes can cause data issues.

---

## Conclusion

You’ve now built a simplified version of a rideshare app—complete with rider/driver onboarding, real-time ride request matching, payment processing, and ratings—demonstrated in a basic Flask + React integration. This MVP structure should serve as a foundation for further enhancements, such as advanced geolocation, robust data persistence, and production-level security.

Feel free to explore the code, expand with additional features, or adapt it to your preferred Python frameworks. Happy coding with Uber_lite!