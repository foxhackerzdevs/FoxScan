# 🦊 FoxScan v2.2

### Automated Recon & Asset Discovery Tool

<p align="center">
  <img src="https://img.shields.io/badge/version-2.2-blue.svg">
  <img src="https://img.shields.io/badge/python-3.x-green.svg">
  <img src="https://img.shields.io/badge/license-MIT-yellow.svg">
  <img src="https://img.shields.io/badge/status-active-success.svg">
</p>

<p align="center">
  <b>Fast • Minimal • Practical Recon for Real-World Workflows</b>
</p>

---

## 🧠 Overview

**FoxScan** is a lightweight reconnaissance tool built for the **initial phase of penetration testing and asset discovery**.

It focuses on **clarity over noise**, providing structured and meaningful output instead of raw scan dumps.

---

## 🔍 Capabilities

* Port scanning via Nmap
* Optional service/version detection (`--service`)
* Smart HTTP/HTTPS detection
* HTTP header analysis
* Basic misconfiguration detection
* JSON reporting for automation pipelines

---

## ✨ Key Features

### ⚡ Smart Port Scanning

* Powered by Nmap
* Custom port ranges supported
* Filters only **open ports**
* Clean, readable output

---

### 🌐 Smart Protocol Detection

* Automatically detects HTTP vs HTTPS
* Uses port-based logic (80 → HTTP, 443 → HTTPS)
* Avoids unnecessary or failed header scans

---

### 🌐 Header Intelligence

* Extracts HTTP response headers
* Identifies backend/server exposure
* Highlights missing security headers

---

### ⚠️ Security Observations

Highlights common **misconfigurations**:

* Missing `X-Frame-Options`
* Missing `X-Content-Type-Options`
* Missing `Strict-Transport-Security`
* Missing `Content-Security-Policy`
* Server version disclosure

> ⚠️ Note: These are **observations**, not confirmed vulnerabilities.

---

### 📊 JSON Reporting

* Machine-readable structured output
* Ideal for CI/CD pipelines
* Clean automation integration

---

### 🤖 MCP / Automation Mode

FoxScan includes a minimal JSON-based interface for automation and tool integration.

Start MCP mode:

```bash
python foxscan.py --mcp
```

Example request:

```json
{"id": 1, "action": "scan", "target": "example.com"}
```

Example response:

```json
{"id": 1, "result": {...}}
```

---

### 🧵 Concurrent Execution

* Multi-threaded header scanning
* Faster recon with minimal overhead

---

## 📸 Demo

<p align="center">
  <img src="assets/demo.gif" width="800"/>
  <br>
  <em>FoxScan in action</em>
</p>

```bash
python foxscan.py example.com -p 1-1000 -o report.json
```

---

## 📦 Installation

### 1️⃣ Install Nmap

**Debian / Ubuntu**

```bash
sudo apt install nmap
```

**Fedora**

```bash
sudo dnf install nmap
```

**Windows**
Download from: [https://nmap.org/download.html](https://nmap.org/download.html)

---

### 2️⃣ Clone Repository

```bash
git clone https://github.com/foxhackerzdevs/FoxScan.git
cd FoxScan
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 💻 Usage

### 🔹 Basic Scan

```bash
python foxscan.py example.com
```

---

### 🔹 Full Port Scan

```bash
python foxscan.py example.com -p 1-65535
```

---

### 🔹 Enable Service Detection

```bash
python foxscan.py example.com --service
```

---

### 🔹 Skip Header Analysis

```bash
python foxscan.py example.com --no-headers
```

---

### 🔹 JSON Output

```bash
python foxscan.py example.com --json
```

---

### 🔹 Save Report

```bash
python foxscan.py example.com -o report.json
```

---

## 📊 Sample Output

```
[+] Starting Port Scan on: example.com

[+] Host: example.com (up)
  └─ TCP 80: Apache httpd 2.4.49

[~] HTTP Recon: http://example.com

[+] Headers:
  Server: Apache/2.4.49
  Content-Type: text/html

[!] Security Observations:
  - Server disclosed: Apache/2.4.49
  - Missing X-Frame-Options
  - Missing X-Content-Type-Options
```

---

## 📁 Project Structure

```
FoxScan/
├── foxscan.py
├── requirements.txt
├── README.md
├── LICENSE
└── assets/
    └── demo.gif
```

---

## 🧪 Methodology

FoxScan follows a practical recon workflow:

1. **Discovery** → Identify open ports
2. **Enumeration** → Detect services (optional)
3. **Analysis** → Extract HTTP headers
4. **Insight** → Highlight misconfigurations

---

## 🔮 Roadmap

* CVE lookup (NVD integration)
* Subdomain enumeration
* Web crawling module
* OS detection (Nmap integration)
* Async high-speed scanning engine
* Plugin system
* Web dashboard UI

---

## ⚠️ Disclaimer

This tool is intended strictly for:

✅ Educational purposes
✅ Ethical hacking
✅ Authorized penetration testing

❌ Unauthorized use is illegal

The authors are **not responsible for misuse**.

---

## 📜 License

MIT License © 2026 Fox Hackerz

---

## 🦊 About

Fox Hackerz builds tools focused on:

* Cybersecurity
* Automation
* Developer systems

🔗 [https://github.com/foxhackerzdevs](https://github.com/foxhackerzdevs)

---

<p align="center">
  <b>🦊 Build. Break. Secure.</b>
</p>
