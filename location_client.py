import socket
import requests
import json
import time
from uuid import getnode

class LocationClient:
    def __init__(self, server_ip, update_interval=30):
        self.server_ip = server_ip
        self.update_interval = update_interval
        self.client_id = hex(getnode())  # Get unique MAC address as client ID
        self.running = False

    def get_browser_location(self):
        """Get location using browser's geolocation API"""
        try:
            # Create a simple HTML page to get location
            html_content = """
            <script>
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(
                        function(position) {
                            const data = {
                                latitude: position.coords.latitude,
                                longitude: position.coords.longitude,
                                accuracy: position.coords.accuracy
                            };
                            // Send data back to Python via localhost
                            fetch('http://localhost:8000/location', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify(data)
                            });
                        },
                        function() {
                            console.log('Location access denied');
                        }
                    );
                }
            </script>
            """
            
            # Start a simple HTTP server to serve the HTML and receive location
            from http.server import HTTPServer, BaseHTTPRequestHandler
            
            class LocationHandler(BaseHTTPRequestHandler):
                def do_GET(self):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(html_content.encode())
                
                def do_POST(self):
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    location_data = json.loads(post_data)
                    self.server.location_data = location_data
                    self.send_response(200)
                    self.end_headers()
            
            self.server = HTTPServer(('localhost', 8000), LocationHandler)
            self.server.location_data = None
            
            # Start the server in a separate thread
            server_thread = threading.Thread(target=self.server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            
            # Open browser to get location
            import webbrowser
            webbrowser.open('http://localhost:8000')
            
            # Wait for location data
            max_attempts = 10
            attempts = 0
            while not self.server.location_data and attempts < max_attempts:
                time.sleep(1)
                attempts += 1
            
            return self.server.location_data
            
        except Exception as e:
            print(f"Error getting browser location: {str(e)}")
            return None

    def send_location_to_server(self, location_data):
        """Send location data to the server"""
        try:
            data = {
                'client_id': self.client_id,
                'latitude': location_data['latitude'],
                'longitude': location_data['longitude'],
                'accuracy': location_data['accuracy']
            }
            
            response = requests.post(
                f'http://{self.server_ip}:5000/update_location',
                json=data
            )
            
            if response.status_code == 200:
                print("Location successfully sent to server")
            else:
                print(f"Error sending location: {response.text}")
                
        except Exception as e:
            print(f"Error sending location to server: {str(e)}")

    def start_tracking(self):
        """Start tracking location and sending updates"""
        self.running = True
        while self.running:
            location = self.get_browser_location()
            if location:
                self.send_location_to_server(location)
            time.sleep(self.update_interval)

    def stop_tracking(self):
        """Stop tracking location"""
        self.running = False
        if hasattr(self, 'server'):
            self.server.shutdown()

if __name__ == '__main__':
    # Replace with your server's IP address
    SERVER_IP = 'YOUR_SERVER_IP'
    
    client = LocationClient(SERVER_IP)
    client.start_tracking()
