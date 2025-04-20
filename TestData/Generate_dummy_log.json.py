import random
import json
import pytz
import datetime
from faker import Faker

faker = Faker()
Faker.seed(42)

# ---- TIMEZONES ----
timezones = [
    "UTC", "US/Eastern", "Europe/London", "Asia/Kolkata", 
    "Asia/Tokyo", "Australia/Sydney", "Europe/Berlin", "America/Los_Angeles", 
    "Africa/Johannesburg", "Asia/Dubai", "Europe/Moscow", "Pacific/Auckland"
]

# ---- MALICIOUS & LEGIT IPs ----
ips = [
    "192.168.1.1", "10.0.0.2", "172.16.0.3", "203.0.113.5", "198.51.100.7", 
    "185.220.101.23", "103.152.220.10", "45.227.253.82", "185.38.175.132", "194.147.142.0", 
    "185.100.87.202", "37.123.163.58", "192.42.116.16", "198.98.54.17", "185.220.100.252", 
    "209.141.38.71", "185.129.62.62", "193.218.118.110", "203.190.54.1", "103.15.28.5", 
    "141.98.10.91", "185.142.236.35", "103.75.201.2", "111.90.147.183", "103.55.38.6", 
    "146.70.80.184", "218.92.0.218", "218.92.0.220", "218.92.0.226", "218.92.0.228", 
    "134.209.120.69", "218.92.0.111", "218.92.0.216", "218.92.0.217", "218.92.0.219", 
    "218.92.0.221", "218.92.0.223", "218.92.0.225", "218.92.0.227", "218.92.0.229", 
    "218.92.0.230", "218.92.0.231", "218.92.0.233", "218.92.0.236", "45.148.10.67", 
    "218.92.0.103", "185.220.101.23", "103.207.38.34", "45.134.20.55", "185.107.56.231",
    "103.86.49.149", "45.83.64.1", "94.102.49.193", "193.32.126.210", "185.246.208.200", 
    "109.248.148.55", "45.66.11.10", "89.234.157.254"
]

# ---- HTTP Methods ----
requests = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]

# ---- Endpoints ----
endpoints = [
    "/login", "/admin", "/dashboard", "/api/data", "/usr/login", "/register", 
    "/auth", "/api/user", "/settings", "/profile", "/logout"
]

# ---- HTTP Status Codes ----
statuscodes = [200, 201, 400, 401, 403, 404, 500, 502, 301, 503]

# ---- User Agents ----
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "curl/7.68.0", "python-requests/2.25.1", 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)", "PostmanRuntime/7.29.0", 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4380.0 Safari/537.36", 
    "Mozilla/5.0 (Linux; Android 10; ONEPLUS A6000) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36", 
    "Mozilla/5.0 (Linux; Android 10; ONEPLUS A6000) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.116 Mobile Safari/537.36 EdgA/45.12.4.5121", 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 OPR/73.0.3856.329", 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"
]

# ---- Usernames ----
usernames = [
    "admin", "user", "root", "guest", "test", "dev", "service", "john_doe", "alice", "bob", 
    "charlie", "hacker", "james", "adam", "eve", "alex", "smith", "isabella", "david", 
    "angela", "donald", "hilary", "root", "testuser", "service_account", "webmaster", 
    "dbadmin", "johnsmith", "janedoe", "guest1", "manager"
]

# ---- Passwords (legit and malicious) ----
passwords = [
    "password123", "admin", "root", "123456", "letmein", "passw0rd", "' OR '1'='1", 
    "<script>alert(1)</script>", "admin' --", "admin' #", "x' OR 1=1 --", "root' OR '1'='1", 
    "qwerty", "123qwe", "welcome", "password", "1234abcd", "toor", "letmein123", "root123",
    "pass@123", "12345", "password1", "iloveyou", "'; DROP TABLE users; --", "<script>alert('xss')</script>",
    "admin' --", "' OR 1=1#", '" onmouseover="alert(1)"'
]

# ---- Referrers ----
referrers = [
    "https://example.com", "-", "https://google.com", "https://evil.com/phishing", 
    "https://legit-site.org", "https://unknown.tld/weird", "https://attack.com/malicious", 
    "https://secured.com", "https://someother.com", "https://evil.com/redirect", 
    "https://hacked.com/exploit", "https://bot.com/spam", "https://youtube.com", "https://facebook.com"
]

status=["success", "failed"]

# ---- TOTAL LOGS ----
num_logs = 1000

# ---- LOG FILE ----
log_file = "log.json"

# ---- GENERATE LOG ENTRY ----
def generate_log_entry():
    tz = pytz.timezone(random.choice(timezones))
    timestamp = datetime.datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S%z')

    return {
        "ip": random.choice(ips),
        "username": random.choice(usernames),
        "password": random.choice(passwords),
        "timestamp": timestamp,
        "method": random.choice(requests),
        "endpoint": random.choice(endpoints),
        "status": random.choice(statuscodes),
        "user_agent": random.choice(user_agents),
        "referrer": random.choice(referrers),
        "login_status": random.choice(status)
    }

# ---- WRITE TO JSON FILE ----
logs = [generate_log_entry() for _ in range(num_logs)]

with open(log_file, "w") as f:
    json.dump(logs, f, indent=2)

print(f"[+] {num_logs} synthetic logs written to '{log_file}' ✅")
