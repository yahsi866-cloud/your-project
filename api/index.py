from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vehicle Challan Checker</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 800px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            text-align: center;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        
        .search-box {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }
        
        input[type="text"] {
            flex: 1;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            text-transform: uppercase;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
        }
        
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .loading {
            text-align: center;
            color: #667eea;
            display: none;
            margin: 20px 0;
        }
        
        .error {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: none;
        }
        
        .result {
            display: none;
        }
        
        .result-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        
        .info-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        
        .info-label {
            color: #666;
            font-size: 12px;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        
        .info-value {
            color: #333;
            font-size: 16px;
            font-weight: bold;
        }
        
        .section-title {
            color: #667eea;
            margin: 30px 0 15px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #e0e0e0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚗 Vehicle Challan Checker</h1>
        <p class="subtitle">Powered by GTPlay API</p>
        
        <div class="search-box">
            <input type="text" id="vehicleNo" placeholder="Enter Vehicle Number (e.g., UP61S6030)" />
            <button onclick="searchVehicle()">Search</button>
        </div>
        
        <div class="loading" id="loading">
            <p>🔍 Searching vehicle details...</p>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="result" id="result">
            <div class="result-header">
                <h2>✅ Vehicle Found Successfully</h2>
            </div>
            
            <h3 class="section-title">Basic Details</h3>
            <div class="info-grid" id="basicDetails"></div>
            
            <h3 class="section-title">Technical Details</h3>
            <div class="info-grid" id="technicalDetails"></div>
            
            <h3 class="section-title">Validity Details</h3>
            <div class="info-grid" id="validityDetails"></div>
        </div>
    </div>
    
    <script>
        async function searchVehicle() {
            const vehicleNo = document.getElementById('vehicleNo').value.trim().toUpperCase();
            
            if (!vehicleNo) {
                showError('Please enter a vehicle number');
                return;
            }
            
            // Show loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('error').style.display = 'none';
            document.getElementById('result').style.display = 'none';
            
            try {
                const response = await fetch('/api/vehicle', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `vehicle_no=${vehicleNo}`
                });
                
                const data = await response.json();
                
                document.getElementById('loading').style.display = 'none';
                
                if (data.status === true) {
                    displayResult(data.data);
                } else {
                    showError(data.message || data.error || 'Vehicle not found');
                }
            } catch (error) {
                document.getElementById('loading').style.display = 'none';
                showError('Network error. Please try again.');
            }
        }
        
        function showError(message) {
            const errorDiv = document.getElementById('error');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }
        
        function displayResult(data) {
            document.getElementById('result').style.display = 'block';
            
            // Basic Details
            const basicDetails = document.getElementById('basicDetails');
            basicDetails.innerHTML = `
                <div class="info-card">
                    <div class="info-label">Registration No</div>
                    <div class="info-value">${data.registration_no || 'N/A'}</div>
                </div>
                <div class="info-card">
                    <div class="info-label">Owner Name</div>
                    <div class="info-value">${data.owner_name || 'N/A'}</div>
                </div>
                <div class="info-card">
                    <div class="info-label">Maker Model</div>
                    <div class="info-value">${data.maker_model || 'N/A'}</div>
                </div>
                <div class="info-card">
                    <div class="info-label">Vehicle Color</div>
                    <div class="info-value">${data.vehicle_color || 'N/A'}</div>
                </div>
                <div class="info-card">
                    <div class="info-label">Fuel Type</div>
                    <div class="info-value">${data.fuel_type || 'N/A'}</div>
                </div>
                <div class="info-card">
                    <div class="info-label">Registration Date</div>
                    <div class="info-value">${data.registration_date || 'N/A'}</div>
                </div>
            `;
            
            // Technical Details
            const technicalDetails = document.getElementById('technicalDetails');
            technicalDetails.innerHTML = `
                <div class="info-card">
                    <div class="info-label">Chassis No</div>
                    <div class="info-value">${data.chassis_no || 'N/A'}</div>
                </div>
                <div class="info-card">
                    <div class="info-label">Engine No</div>
                    <div class="info-value">${data.engine_no || 'N/A'}</div>
                </div>
                <div class="info-card">
                    <div class="info-label">Seat Capacity</div>
                    <div class="info-value">${data.seat_capacity || 'N/A'}</div>
                </div>
                <div class="info-card">
                    <div class="info-label">Unload Weight</div>
                    <div class="info-value">${data.unload_weight ? data.unload_weight + ' kg' : 'N/A'}</div>
                </div>
            `;
            
            // Validity Details
            const validityDetails = document.getElementById('validityDetails');
            validityDetails.innerHTML = `
                <div class="info-card">
                    <div class="info-label">RC Status</div>
                    <div class="info-value">${data.rc_status || 'N/A'}</div>
                </div>
                <div class="info-card">
                    <div class="info-label">Fitness Upto</div>
                    <div class="info-value">${data.fitness_upto || 'N/A'}</div>
                </div>
                <div class="info-card">
                    <div class="info-label">Insurance Upto</div>
                    <div class="info-value">${data.insurance_upto || 'N/A'}</div>
                </div>
                <div class="info-card">
                    <div class="info-label">Insurance Company</div>
                    <div class="info-value">${data.insurance_company || 'N/A'}</div>
                </div>
                <div class="info-card">
                    <div class="info-label">PUC Upto</div>
                    <div class="info-value">${data.puc_upto || 'N/A'}</div>
                </div>
                <div class="info-card">
                    <div class="info-label">Registration Authority</div>
                    <div class="info-value">${data.registration_authority || 'N/A'}</div>
                </div>
            `;
        }
        
        // Allow Enter key to search
        document.getElementById('vehicleNo').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchVehicle();
            }
        });
    </script>
</body>
</html>
        '''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
