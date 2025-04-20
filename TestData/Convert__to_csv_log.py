import json
import csv
from datetime import datetime

# Load the JSON data
with open('log.json', 'r') as json_file:
    data = json.load(json_file)

# Step 2: Convert JSON to CSV
csv_filename = 'log.csv'
csv_headers = ['ip', 'username', 'password', 'timestamp', 'method', 'endpoint', 'status', 'user_agent', 'referrer', 'login_status']

# Writing to CSV
with open(csv_filename, 'w', newline='') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    csv_writer.writeheader()  # Write headers
    csv_writer.writerows(data)  # Write the data rows

print(f"CSV file created: {csv_filename}")

# Step 3: Convert JSON to Log File
log_filename = 'log_file.log'

with open(log_filename, 'w') as log_file:
    for entry in data:
        log_line = f"{entry['timestamp']} - {entry['ip']} - {entry['method']} {entry['endpoint']} - Status: {entry['status']} - User: {entry['username']} - Referrer: {entry['referrer']} - UA: {entry['user_agent']} -  Login_Status: {entry['login_status']}\n"
        log_file.write(log_line)

print(f"Log file created: {log_filename}")
