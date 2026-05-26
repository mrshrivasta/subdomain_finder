# 🌐 Subdomain Finder

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Dashboard-black?style=for-the-badge&logo=flask)
![Cybersecurity](https://img.shields.io/badge/Cybersecurity-Educational-red?style=for-the-badge)
![DNS](https://img.shields.io/badge/DNS-Enumeration-success?style=for-the-badge)
![Open Source](https://img.shields.io/badge/Open%20Source-GitHub-181717?style=for-the-badge&logo=github)
![Educational](https://img.shields.io/badge/Use-Educational-orange?style=for-the-badge)

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=24&pause=1000&color=1A6FD4&center=true&vCenter=true&width=1000&lines=Subdomain+Finder+%7C+Educational+Tool;DNS+Enumeration+Dashboard;Cybersecurity+Inspired+Project;Built+Using+Python+%2B+Flask;Real-Time+Subdomain+Discovery;Bug+Bounty+Learning+Project" />

### ⚡ Advanced Subdomain Enumeration Tool Built Using Python + Flask

### 🔥 DNS Enumeration • HTTP Probing • Real-Time Dashboard • Export System

</div>

---

# 📌 Overview

Subdomain Finder is a modern educational subdomain enumeration tool built using:

- Python
- Flask
- dnspython
- requests
- multithreading

The project allows users to discover subdomains of a target domain using DNS brute-force techniques.

This tool includes:

✅ Real-time scanning  
✅ Web dashboard  
✅ DNS enumeration  
✅ HTTP probing  
✅ CSV/JSON export  
✅ Progress tracking  
✅ Multi-threaded scanning  
✅ Live activity logs  
✅ Custom wordlists  
✅ Bug bounty learning features  

---

# ⚠ LEGAL DISCLAIMER

```txt
Educational and research use ONLY.

ONLY scan domains:
- you own
- or have explicit written authorization to test

Unauthorized scanning may violate:
- CFAA (United States)
- Computer Misuse Act 1990 (United Kingdom)
- Information Technology Act 2000 (India)

The author assumes ZERO liability for misuse.
```

---

# 🚀 Features

# 🌐 DNS Enumeration

- DNS brute-force enumeration
- A record resolution
- CNAME resolution
- MX resolution
- Socket fallback support
- Multi-threaded DNS lookups
- Concurrent scanning engine

---

# ⚡ Real-Time Dashboard

- Modern Flask dashboard
- Live scan progress
- Real-time activity feed
- Dynamic progress bar
- Animated UI
- Responsive layout
- Mobile-friendly interface

---

# 🔍 HTTP Probing

- HTTP probing
- HTTPS probing
- HTTP status detection
- Server banner detection
- Website title extraction
- Redirect handling

---

# 📦 Export Features

- Export CSV
- Export JSON
- Copy discovered subdomains
- Downloadable reports

---

# 📊 Statistics

- Checked subdomains counter
- Found subdomains counter
- Completion percentage
- Scan duration tracking
- Thread count display

---

# 🧠 Advanced Features

- Built-in wordlist
- Custom wordlist support
- Thread customization
- Timeout customization
- Event streaming
- SSE live updates
- Background concurrent workers

---

# 🎨 UI Features

- Modern cybersecurity-style dashboard
- Smooth animations
- Progress bars
- Activity logs
- Responsive design
- Clean minimal interface
- Interactive controls

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend |
| Flask | Web framework |
| dnspython | DNS enumeration |
| requests | HTTP probing |
| HTML5 | Frontend |
| CSS3 | Styling |
| JavaScript | Real-time UI |
| SSE | Live event streaming |

---

# 📥 Installation Guide

# 🐍 Step 1 — Install Python

Download Python:

🔗 https://www.python.org/downloads/

### IMPORTANT

During installation:

✅ Enable:

```txt
Add Python to PATH
```

---

# 📦 Step 2 — Install Required Packages

Open:

```txt
Command Prompt
```

Run:

```bash
pip install flask dnspython requests
```

---

# 📂 Step 3 — Clone Repository

```bash
git clone https://github.com/mrshrivasta/subdomain_finder.git
```

---

# 📁 Step 4 — Open Folder

```bash
cd subdomain_finder
```

---

# 🚀 Step 5 — Run Web Dashboard

```bash
python subdomain_finder.py --web
```

---

# 🌐 Step 6 — Open In Browser

```txt
http://localhost:5000
```

---

# 🛑 Stop Server

Press:

```txt
CTRL + C
```

inside terminal.

---

# ⚡ Quick Start

```bash
pip install flask dnspython requests
python subdomain_finder.py --web
```

---

# 🖥️ CLI Usage

# Basic Scan

```bash
python subdomain_finder.py --domain example.com
```

---

# Web Dashboard

```bash
python subdomain_finder.py --web
```

---

# Custom Wordlist

```bash
python subdomain_finder.py --domain example.com --wordlist words.txt
```

---

# Export CSV

```bash
python subdomain_finder.py --domain example.com --csv output.csv
```

---

# Export JSON

```bash
python subdomain_finder.py --domain example.com --json output.json
```

---

# Full Example

```bash
python subdomain_finder.py --domain example.com --workers 100 --timeout 3 --csv results.csv --json results.json
```

---

# 📡 Web Dashboard Features

# 🖥️ Dashboard

- Live scan progress
- Real-time updates
- Live result table
- Dynamic logs

---

# 📊 Progress Monitoring

- Completion %
- Real-time counters
- Elapsed scan time
- Scan status indicators

---

# 🔍 Results Table

- Subdomain hostname
- IP addresses
- CNAME records
- HTTP status codes
- Server headers
- Website titles

---

# 📜 Activity Logs

- Live scan logs
- Discovery logs
- Export logs
- Status updates

---

# ⚡ API System

The project includes real-time server-sent event streaming for dashboard updates. :contentReference[oaicite:0]{index=0}

---

# 🧠 Built-In Wordlist

Includes:

- common subdomains
- API endpoints
- admin panels
- cloud services
- mail services
- staging environments
- developer infrastructure
- monitoring systems

Examples:

```txt
www
api
mail
dev
staging
admin
dashboard
vpn
cdn
assets
beta
test
```

---

# 📊 Example Scan Output

```txt
✓ api.example.com
✓ mail.example.com
✓ dev.example.com
✓ staging.example.com
```

---

# 🌐 SEO Keywords

Subdomain Finder, DNS Enumeration Tool, Subdomain Scanner, Python Subdomain Finder, Flask Cybersecurity Project, DNS Brute Force Tool, Educational Ethical Hacking Tool, Bug Bounty Tool, Subdomain Enumeration Dashboard, Flask Security Dashboard, Python DNS Scanner, Real-Time Enumeration Tool, Cybersecurity Dashboard, Network Security Project

---

# 📂 Project Architecture

```txt
subdomain_finder.py
│
├── DNS Resolver
├── HTTP Probe Engine
├── Concurrent Scanner
├── SSE Event Streaming
├── Flask Backend
├── Dashboard Frontend
├── Export System
├── Activity Logging
└── Wordlist Engine
```

---

# ⚡ Why This Project?

Most beginner projects are:

- Calculator
- Weather app
- To-do app

This project demonstrates:

✅ Networking  
✅ DNS enumeration  
✅ Flask backend development  
✅ Real-time dashboards  
✅ Multithreading  
✅ HTTP probing  
✅ Security tooling concepts  
✅ Event streaming  
✅ Cybersecurity-inspired engineering  

---

# 🔥 Real-Time Features

The dashboard updates live using:

```txt
Server-Sent Events (SSE)
```

This enables:

- real-time progress
- live discovered subdomains
- instant UI updates
- streaming scan results

---

# ⚠ Educational Purpose

This project is intended for:

- cybersecurity education
- networking learning
- DNS research
- Flask dashboard practice
- bug bounty learning
- ethical hacking education

---

# 🔒 Security Notice

```txt
DO NOT:
- scan government systems
- scan random companies
- perform unauthorized testing
- misuse this project

ONLY test domains you own or have permission to assess.
```

---

# 🛠️ Troubleshooting

# ❌ pip not recognized

Run:

```bash
python -m pip install flask dnspython requests
```

---

# ❌ Python not recognized

Reinstall Python and enable:

```txt
Add Python to PATH
```

---

# ❌ Flask module not found

Run:

```bash
pip install flask
```

---

# ❌ dnspython module not found

Run:

```bash
pip install dnspython
```

---

# ❌ requests module not found

Run:

```bash
pip install requests
```

---

# ❌ Port 5000 already in use

Change:

```python
app.run(port=5000)
```

to:

```python
app.run(port=5050)
```

---

# ❌ Slow scanning

Increase worker count:

```bash
--workers 100
```

---

# 📈 Performance Notes

- Multi-threaded scanning
- Fast DNS enumeration
- Optimized concurrent workers
- Lightweight backend
- Real-time streaming
- Efficient UI rendering

---

# 🧠 Learning Concepts

This project helps learn:

- DNS systems
- HTTP protocols
- Flask development
- multithreading
- event streaming
- cybersecurity basics
- network reconnaissance
- dashboard engineering

---

# 🚀 Future Improvements

- DNS record expansion
- Async scanning
- WebSocket support
- Better fingerprinting
- Screenshot capture
- IPv6 support
- WHOIS integration
- Dark mode
- Graph visualization
- Docker support

---

# 🤝 Contributing

Pull requests are welcome.

To contribute:

1. Fork repository
2. Create branch
3. Commit changes
4. Push updates
5. Open pull request

---

# ⭐ Support

If you like this project:

⭐ Star the repository  
🍴 Fork the repository  
📢 Share the project  

---

# 👨‍💻 Author

# Karanam Shrivasta

### 🌐 GitHub

:contentReference[oaicite:1]{index=1}

### 💼 LinkedIn

:contentReference[oaicite:2]{index=2}

---

# 📜 License

MIT License

---

# 🔥 Fun Fact

This advanced real-time cybersecurity-inspired dashboard runs from:

```txt
One Python file.
```

---

<div align="center">

# 🌐 Subdomain Finder

### ⚡ Real-Time DNS Enumeration Dashboard

### 🚀 Built With Python + Flask

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=20&pause=1000&color=1A6FD4&center=true&vCenter=true&width=800&lines=Made+By+Karanam+Shrivasta;Educational+Cybersecurity+Project;DNS+Enumeration+Dashboard;Python+%2B+Flask+Security+Tool" />

</div>
