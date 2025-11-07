from http.server import BaseHTTPRequestHandler
import requests
import json
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))
            
            # Read POST data
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # Parse form data
            params = urllib.parse.parse_qs(post_data)
            vehicle_no = params.get('vehicle_no', [''])[0]
            
            if not vehicle_no:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {'status': False, 'error': 'vehicle_no is required'}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Call the actual API
            result = self.get_vehicle_details(vehicle_no)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {'status': False, 'error': str(e)}
            self.wfile.write(json.dumps(response).encode())
    
    def do_GET(self):
        try:
            # Parse query parameters
            from urllib.parse import urlparse, parse_qs
            query_components = parse_qs(urlparse(self.path).query)
            vehicle_no = query_components.get('vehicle_no', [''])[0]
            
            if not vehicle_no:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {'status': False, 'error': 'vehicle_no parameter is required'}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Call the actual API
            result = self.get_vehicle_details(vehicle_no)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {'status': False, 'error': str(e)}
            self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def get_vehicle_details(self, vehicle_number):
        url = "https://gtplay.in/API/vehicle_challan_info/testapi.php"
        
        # Format data
        data = f'vehicle_no={vehicle_number}'
        
        # Headers
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'okhttp/5.1.0',
            'Accept-Encoding': 'gzip',
            'Content-Length': str(len(data)),
            'Accept': 'application/json',
            'Connection': 'keep-alive'
        }
        
        try:
            response = requests.post(url, data=data, headers=headers, timeout=10)
            result = response.json()
            
            if result.get('status') == True:
                return {
                    'status': True,
                    'message': 'Vehicle found successfully',
                    'data': result.get('data', {})
                }
            else:
                return {
                    'status': False,
                    'message': result.get('error', 'Vehicle not found')
                }
                
        except requests.exceptions.RequestException as e:
            return {'status': False, 'error': f'Network error: {str(e)}'}
        except json.JSONDecodeError:
            return {'status': False, 'error': 'Invalid JSON response from API'}
        except Exception as e:
            return {'status': False, 'error': str(e)}
