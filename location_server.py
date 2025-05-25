from flask import Flask, request, jsonify
import socket
import threading
import time

app = Flask(__name__)

# Store locations by client ID
client_locations = {}

@app.route('/update_location', methods=['POST'])
def update_location():
    try:
        data = request.json
        client_id = data.get('client_id')
        if not client_id:
            return jsonify({'error': 'Client ID required'}), 400
            
        location = {
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'accuracy': data.get('accuracy'),
            'timestamp': time.time()
        }
        
        client_locations[client_id] = location
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/get_location/<client_id>', methods=['GET'])
def get_location(client_id):
    if client_id in client_locations:
        return jsonify(client_locations[client_id]), 200
    return jsonify({'error': 'Client not found'}), 404

@app.route('/get_all_locations', methods=['GET'])
def get_all_locations():
    return jsonify(client_locations), 200

if __name__ == '__main__':
    # Get server IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    server_ip = s.getsockname()[0]
    s.close()
    
    print(f"Server running at http://{server_ip}:5000")
    print("Use this IP in the client script")
    app.run(host='0.0.0.0', port=5000)
