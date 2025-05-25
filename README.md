# Location Tracking System

This system allows you to track the precise location of multiple computers in real-time. It consists of a server component and client components.

## Components

### Server (location_server.py)
- Runs on a central computer
- Receives and stores location updates from clients
- Provides API endpoints to query locations

### Client (location_client.py)
- Runs on any computer you want to track
- Uses browser's geolocation API for precise location
- Sends location updates to the server

## Setup

### Server Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the server:
```bash
python location_server.py
```

The server will print its IP address. Make note of this IP as you'll need it for the clients.

### Client Setup
1. Modify the client script to use your server's IP:
```python
SERVER_IP = 'YOUR_SERVER_IP'  # Replace with your server's IP
```

2. Run the client:
```bash
python location_client.py
```

The client will open a browser window to get location permission and start sending updates.

## Usage

### Querying Locations
1. Get a specific client's location:
```
http://server_ip:5000/get_location/<client_id>
```

2. Get all client locations:
```
http://server_ip:5000/get_all_locations
```

## Features
- Accurate location using browser's geolocation API
- Real-time location updates
- Multiple client support
- Location history with timestamps
- Secure client identification using MAC addresses

## Requirements
- Python 3.10+
- Flask
- Requests library
- Web browser with geolocation support
