## 🦊 FoxScan v2.1

### Automated Reconnaissance & Asset Discovery Tool

<p align="center">
  <img src="https://img.shields.io/badge/version-2.1-blue.svg">
  <img src="https://img.shields.io/badge/python-3.x-green.svg">
  <img src="https://img.shields.io/badge/license-MIT-yellow.svg">
  <img src="https://img.shields.io/badge/status-active-success.svg">
</p>

<p align="center">
  <b>Fast • Lightweight • Practical Recon Tool for Security Engineers</b>
</p>

---

## 🧠 Overview

**FoxScan** is a lightweight reconnaissance tool designed for the **initial phase of penetration testing and asset discovery**.

It focuses on delivering **clear, structured insights** rather than raw scan output.

### 🔍 What it does

* Port scanning via **Nmap**
* Service & version detection
* HTTP header analysis
* Basic misconfiguration detection
* JSON report generation for automation

---

## ✨ Features

### ⚡ Smart Port Scanning

* Powered by Nmap (`-sV`)
* Custom port ranges
* Shows only open/active ports
* Clean structured output (not cluttered CLI dump)

### 🌐 Header Intelligence

* Extracts HTTP headers
* Identifies backend/server exposure
* Detects missing security headers

### ⚠️ Security Insights

Detects common issues like:

* Missing `X-Frame-Options`
* Missing `X-Content-Type-Options`
* Missing `Strict-Transport-Security`
* Missing `Content-Security-Policy`
* Server version disclosure

### 📊 JSON Reporting

* Machine-readable output
* Pipeline-friendly
* Easy integration with other tools

### 🧵 Concurrent Execution

* Multi-threaded header scanning
* Faster recon without heavy resource usage

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

**Ubuntu / Debian**

```bash
sudo apt install nmap
```

**Fedora**

```bash
sudo dnf install nmap
```

**Windows**
Download: [https://nmap.org/download.html](https://nmap.org/download.html)

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

### 🔹 Full Port Range

```bash
python foxscan.py example.com -p 1-65535
```

### 🔹 Skip Header Analysis

```bash
python foxscan.py example.com --no-headers
```

### 🔹 JSON Output (Automation Mode)

```bash
python foxscan.py example.com --json
```

### 🔹 Save Report

```bash
python foxscan.py example.com -o report.json
```

---

## 📊 Example Output

```
[+] Starting Port Scan on: example.com

example.com:80 -> open (Apache httpd)

[*] Checking Headers: http://example.com

Server: Apache/2.4.49
Content-Type: text/html

[!] Potential Issues:
 - Server disclosed: Apache/2.4.49
 - Missing X-Frame-Options
```

---

## 📁 JSON Output (Sample)

```json
{
  "target": "example.com",
  "version": "2.1",
  "port_scan": {
    "example.com": {
      "state": "up",
      "protocols": {
        "tcp": {
          "80": {
            "state": "open",
            "name": "http",
            "product": "Apache",
            "version": "2.4.49"
          }
        }
      }
    }
  }
}
```

---

## 🧪 Methodology

FoxScan follows a **real-world recon workflow**:

1. **Discovery** → Identify open ports
2. **Enumeration** → Detect services & versions
3. **Analysis** → Extract headers & configs
4. **Insight** → Highlight potential weaknesses

---

## 🏗 Project Structure

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

## 🔮 Roadmap

* 🔍 CVE lookup (NVD API integration)
* 🌐 Subdomain enumeration
* 🕷 Web crawler module
* 📡 OS detection (Nmap integration)
* 📊 Web UI dashboard
* ⚡ Async scanning engine
* 🔌 Plugin system (major upgrade)

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch
3. Commit changes
4. Open a Pull Request

---

## ⚠️ Disclaimer

This tool is intended for:

* ✅ Educational use
* ✅ Authorized security testing

Unauthorized use is illegal.
The authors are not responsible for misuse.

---

## 📜 License

MIT License © 2026 Fox Hackerz

---

## 🦊 About

**Fox Hackerz** builds tools focused on:

* Cybersecurity
* Automation
* Developer tooling

🔗 [https://github.com/foxhackerzdevs](https://github.com/foxhackerzdevs)

---

<p align="center">
  <b>🦊 Build simple tools that actually get used.</b>
</p>
