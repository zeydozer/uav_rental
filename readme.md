# UAV Rental Project

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technologies Used](#technologies-used)
3. [Installation](#installation)
4. [Usage](#usage)
5. [API Endpoints](#api-endpoints)

## Project Overview

The UAV Rental project is a web application designed to facilitate the rental of Unmanned Aerial Vehicles (UAVs). It provides functionalities for user registration and login, UAV management, rental management, and more.

## Technologies Used

- **Python**
- **Django**
- **Django REST Framework**
- **PostgreSQL**
- **Docker**

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd uav_rental
   ```

2. **Build and run the Docker container:**
   ```bash
   docker compose up -d
   ```

## Usage

You can access the Django admin panel at `http://127.0.0.1:8000/admin/`. <br>
Superuser username is **root** and password is **root**.

You can access the Adminer panel at `http://127.0.0.1:8080/`. <br>
All information is **postgres**, database name is **uav_rental**.

## API Endpoints

### User Management

- **Register a new user:**
  ```
  POST /api/register
  ```
  **Parameters:**
  - `username` (string)
  - `password` (string)
  - `email` (string)

- **Login a user and get a JWT token:**
  ```
  POST /api/login
  ```
  **Parameters:**
  - `username` (string)
  - `password` (string)
  - `email` (string) (optional)

**List all users:**
  ```
  GET /api/users
  ```

To authenticate, include the JWT token in the `Authorization` header as follows:
```
Authorization: Bearer <your_token>
```

### UAV Management

- **List all UAVs:**
  ```
  GET /api/uavs
  ```

- **Create a new UAV:**
  ```
  POST /api/uavs
  ```
  **Parameters:**
  - `brand` (string)
  - `model` (string)
  - `weight` (float)
  - `category` (string)

- **Retrieve a specific UAV:**
  ```
  GET /api/uavs/{id}
  ```

- **Update a specific UAV:**
  ```
  PUT /api/uavs/{id}
  ```
  **Parameters:**
  - `brand` (string)
  - `model` (string)
  - `weight` (float)
  - `category` (string)

- **Delete a specific UAV:**
  ```
  DELETE /api/uavs/{id}
  ```

- **Create a new UAV rental:**
  ```
  POST /api/uavs/{id}/rent
  ```
  **Parameters:**
  - `start_date` (datetime)
  - `end_date` (datetime)

### Rental Management

- **List all rentals:**
  ```
  GET /api/rentals
  ```

- **Retrieve a specific rental:**
  ```
  GET /api/rentals/{id}
  ```

- **Update a specific rental:**
  ```
  PUT /api/rentals/{id}
  ```
  **Parameters:**
  - `uav_id` (integer)
  - `renting_member_id` (integer)
  - `start_date` (datetime)
  - `end_date` (datetime)

- **Delete a specific rental:**
  ```
  DELETE /api/rentals/{id}
  ```