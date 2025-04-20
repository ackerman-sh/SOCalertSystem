# 🔒 SOC Alert Prioritization System

A lightweight Flask-powered tool to prioritize and analyze Security Operation Center (SOC) alerts using rule-based scoring, severity levels, and export capabilities.

---

## 🚀 Overview

The **SOC Alert Prioritization System** allows security analysts to upload, process, and analyze server logs for suspicious or malicious behavior. The system applies rule-based checks to assign severity, calculate priority scores, and display actionable insights.

---

## 🌐 Features

- ✅ Upload `.json` or `.csv` server logs
- ⚖️ Analyze logs using rule-based detection (e.g., XSS, brute force, SQLi)
- 🔹 Assigns:
  - Severity levels (`Low`, `Medium`, `High`, `Critical`)
  - Numerical priority scores (0-100)
  - Specific reasons for alert
- 🔍 Filters:
  - By severity
  - By priority score (ascending/descending)
  - By reason tags
- 📄 Export filtered logs to CSV or JSON
- 🌐 Responsive frontend using HTML, CSS, JavaScript

---

## 📊 Folder Structure

```
SOCAlertSystem/
|
|├— app.py                 # Flask backend application
|├— install.sh             # Auto setup for virtual environment and dependencies
|├— requirements.txt       # Python dependencies
|├— templates/             # Frontend HTML templates
|   |
|   |├— index.html         # Upload interface
|   └— results.html       # Filter + Export view
|├— uploads/               # Temporarily stores uploaded files
|└— TestData/              # Sample log files and scripts
    |
    |├— BlackListIp.txt       # Sample blacklist IPs
    |├— Convert__to_csv_log.py # Tool to convert logs
    |├— Generate_dummy_log.json.py # Dummy log generator
    |├— log.csv
    |├— log_file.log
    └— log.json
```

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ackerman-sh/SOCAlertSystem.git
cd SOCAlertSystem
```

### 2. Run Setup Script
```bash
bash install.sh
```
This will:
- Create `myenv` virtual environment
- Activate it
- Install all dependencies from `requirements.txt`

---

## 🔍 Usage

### Run the Flask App
```bash
source myenv/bin/activate
python app.py
```
Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Upload & Analyze
1. Upload a `.csv` or `.json` log file
2. System analyzes each entry for attack patterns
3. Results shown in a dynamic table with filters
4. Export results as `.csv` or `.json`

---

## 🔒 Security Rule Engine

Each log is checked against multiple patterns, such as:
- SQL Injection payloads
- Brute force attempts from IPs
- Suspicious user agents or referers
- Blacklisted IPs
- XSS or JS-based injection strings

Each detection increases the severity and score.

---

## 📓 Requirements

See `requirements.txt` for full list.

Key libraries:
- Flask
- Pandas
- NumPy
- Flask-CORS
- Faker (optional for dummy logs)

---

## 💾 Export Options

- Choose format from dropdown: `CSV` or `JSON`
- Click **Export** to download filtered result

---


## 💡 Roadmap Ideas

- [ ] API endpoints for log ingestion
- [ ] Auth mode for multi-user SOCs
- [ ] Visualization dashboard (Geo/IP heatmaps)
- [ ] Integration with SIEM tools

