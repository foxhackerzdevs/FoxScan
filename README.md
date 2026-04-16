# 🦊 FoxScan v2.1

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

**FoxScan** is a modern reconnaissance tool built for the **initial phase of penetration testing and asset discovery**.

It automates:

* 🔍 Port scanning using Nmap
* 🌐 Service & version detection
* 📡 HTTP header analysis
* ⚠️ Security misconfiguration detection

Designed with a **performance-first mindset**, FoxScan provides meaningful insights without unnecessary complexity.

---

## ✨ Features

### ⚡ Smart Port Scanning

* Powered by Nmap
* Custom port ranges supported
* Service & version detection (`-sV`)
* Filters only active/open ports

### 🌐 Header Intelligence

* Extracts HTTP response headers
* Identifies backend technologies
* Detects exposed server details

### ⚠️ Security Insights

Detects:

* Missing `X-Frame-Options`
* Missing `X-Content-Type-Options`
* Missing `Strict-Transport-Security`
* Server version disclosure

### 📊 JSON Reporting

* Export scan results
* Machine-readable format
* Ideal for automation pipelines

### 🧵 Concurrent Execution

* Multi-threaded header scanning
* Faster execution with minimal overhead

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

#### Ubuntu / Debian

```bash
sudo apt install nmap
```

#### Fedora

```bash
sudo dnf install nmap
```

#### Windows

Download from: https://nmap.org

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

### 🔹 Export JSON Report

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
 - Missing X-Frame-Options (Clickjacking risk)
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

## 🧪 Research & Methodology

FoxScan follows real-world reconnaissance workflows:

* **Port Scanning**

  * Identifies exposed services quickly
  * Uses efficient scanning strategies

* **Service Fingerprinting**

  * Detects technologies & versions
  * Assists vulnerability assessment

* **Header Analysis**

  * Highlights insecure configurations
  * Reveals potential attack vectors

---

## 🏗 Project Structure

```
FoxScan/
├── LICENSE
├── README.md
├── foxscan.py
├── requirements.txt
└── assets/
    └── demo.gif
```

---

## 🔮 Future Scope

* 🔍 CVE lookup (NVD API integration)
* 🌐 Subdomain enumeration
* 🕷 Web crawling engine
* 📡 OS detection
* 📊 Web dashboard (UI)
* ⚡ Async scanning engine (high-performance mode)

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

## ⚠️ Disclaimer

This tool is intended strictly for:

✅ Educational purposes
✅ Ethical hacking
✅ Authorized penetration testing

❌ Unauthorized use is illegal.

The authors are **not responsible for misuse**.

---

## 📜 License

MIT License © 2026 Fox Hackerz

---

## 🦊 About Fox Hackerz

We build tools focused on:

* Cybersecurity
* Automation
* Developer systems

📌 GitHub: https://github.com/foxhackerzdevs

---

<p align="center">
  <b>🦊 Join the pack. Build. Break. Secure.</b>
</p>
