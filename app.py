from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import os, json, csv
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'json', 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ----- Define your security rule lists -----
malicious_urls = [
    'https://evil.com/phishing',
    'http://phishme.co/fake',
    'http://injected.site/sqlmap',
    'https://xss.attack.com/?src=<script>'
]
blacklisted_ips = [
    '218.92.0.218', '218.92.0.220', '218.92.0.226', '218.92.0.228',
    '134.209.120.69', '218.92.0.111', '218.92.0.216', '218.92.0.217',
    # add more from your blacklist
]
password_injection = [
    "' OR '1'='1", "'; DROP TABLE users; --", "<script>alert('xss')</script>",
    "' UNION SELECT * FROM users --"
]
unwanted_usernames = ['admin', 'root', 'test', 'guest']
# ------------------------------------------

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    ext = filename.rsplit('.', 1)[1].lower()
    data = []
    if ext == 'json':
        with open(filepath, 'r') as f:
            data = json.load(f)
    elif ext == 'csv':
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)
    else:
        return jsonify({'error': 'Unsupported file type'}), 400

    return jsonify({'data': data})

@app.route('/analyze', methods=['POST'])
def analyze_log():
    data = request.get_json(force=True)
    if not data:
        return jsonify({'error': 'No log data provided'}), 400

    try:    
        analyzed_logs = []
        failed_login_counts = {}

        for entry in data:
            if entry.get('login_status') == 'failed':
                ip = entry.get('ip')
                failed_login_counts[ip] = failed_login_counts.get(ip, 0) + 1

        for entry in data:
            severity = 'None'
            score = 0
            reasons = []

            username   = entry.get('username', '')
            endpoint   = entry.get('endpoint', '')
            login_status = entry.get('login_status', '')
            referrer   = entry.get('referrer', '')
            password   = entry.get('password', '')
            ip         = entry.get('ip', '')
            user_agent = entry.get('user_agent', '').lower()
            method     = entry.get('method', '').upper()

            if username in unwanted_usernames and endpoint in ['/login','/register','/usr/login']:
                if login_status == 'failed':
                    severity = 'Low'; score += 1; reasons.append('Unwanted username failed login')
                else:
                    severity = 'High'; score += 3; reasons.append('Unwanted username successful login')

            if referrer in malicious_urls:
                severity = 'Medium' if severity != 'High' else 'High'
                score += 2; reasons.append('Malicious referrer')

            if any(payload in password for payload in password_injection):
                severity = 'High'; score += 4; reasons.append('Password injection pattern')

            if ip in blacklisted_ips:
                severity = 'High'; score += 4; reasons.append('Blacklisted IP')

            if 'curl' in user_agent:
                if severity != 'High': severity = 'Low'
                score += 1; reasons.append('Suspicious UA: curl')

            if failed_login_counts.get(ip, 0) > 5:
                severity = 'Medium' if severity != 'High' else 'High'
                score += 3; reasons.append(f'Brute-force attempts: {failed_login_counts[ip]}')

            if method in ['PUT', 'DELETE', 'TRACE', 'CONNECT']:
                severity = 'Medium' if severity != 'High' else 'High'
                score += 2; reasons.append(f'Suspicious method: {method}')

            if severity == 'None':
                severity = 'Undefined'

            entry['severity']       = severity
            entry['priority_score'] = score
            entry['reasons']        = reasons
            analyzed_logs.append(entry)

        return jsonify({'analyzed_logs': analyzed_logs}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/result')
def results():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)
