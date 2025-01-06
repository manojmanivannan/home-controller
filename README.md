# Simple Home Automation Server

This project is a simple home automation server built with FastAPI. It allows you to manage and control devices in different rooms of your home. The server provides endpoints to list, add, and toggle the state of devices.

## Features

- Add new devices to rooms
- List all devices, optionally filtered by room
- Turn on/off individual devices
- Turn off all devices in a room (TODO)
- Turn off all devices in the home (TODO)


## Getting Started

### Prerequisites

- Python 3.11.8
- Docker
- Docker Compose

### Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Server

1. Start the server using Docker Compose:
    ```sh
    docker-compose up --build
    ```

2. The server will be available at `http://localhost:8000`.

### API Endpoints

- **List Devices**
  - `GET /devices/`
  - Response: List of devices

- **Add Device**
  - `POST /devices/`
  - Request Body: `DeviceCreate`
  - Response: `DeviceRead`

- **Turn On Device**
  - `POST /turnon/`
  - Request Body: `DeviceCreate`
  - Response: `DeviceRead`

- **Turn Off Device**
  - `POST /turnoff/`
  - Request Body: `DeviceCreate`
  - Response: `DeviceRead`

- **List Rooms**
  - `GET /rooms/`
  - Response: List of rooms

- **Add Room**
  - `POST /rooms/`
  - Request Body: `RoomCreate`
  - Response: `RoomRead`

### Frontend

The frontend is a simple HTML page that displays the status of devices. It is served by an Nginx container.

1. The frontend will be available at `http://localhost:3000`.

### Logging

Logging is configured using the `logging.conf` file in the `src/common` directory. Logs are output to the console.

### Database

The project uses PostgreSQL as the database. The database schema is defined using SQLModel. Initial data is loaded from a CSV file (`src/etc/home_devices.csv`).
