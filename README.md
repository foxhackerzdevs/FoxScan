# 🦊 FoxScan v2.0  
### Automated Reconnaissance & Asset Discovery Tool  

<p align="center">
  <img src="https://img.shields.io/badge/version-2.0-blue.svg">
  <img src="https://img.shields.io/badge/python-3.x-green.svg">
  <img src="https://img.shields.io/badge/license-MIT-yellow.svg">
  <img src="https://img.shields.io/badge/status-active-success.svg">
</p>

<p align="center">
  <b>Fast • Lightweight • Practical Recon Tool for Security Enthusiasts</b>
</p>

---

## 🧠 Overview

**FoxScan** is a modern reconnaissance tool built for the **initial phase of penetration testing**.

It automates:
- 🔍 Port scanning using Nmap  
- 🌐 Service & version detection  
- 📡 HTTP header extraction  
- ⚠️ Basic security misconfiguration detection  

Designed with **simplicity + power**, FoxScan delivers meaningful insights without unnecessary complexity.

---

## ✨ Features

### ⚡ Smart Port Scanning
- Powered by Nmap
- Custom port ranges supported
- Service & version detection (`-sV`)

### 🌐 Header Intelligence
- Extracts HTTP response headers
- Identifies backend technologies
- Reveals server configurations

### ⚠️ Security Insights
Detects:
- Missing `X-Frame-Options`
- Missing `X-Content-Type-Options`
- Server version exposure

### 📊 JSON Reporting
- Export scan results
- Machine-readable format
- Useful for automation & pipelines

### 🧵 Concurrent Execution
- Faster header checks using threading

---

## 📸 Demo

<p align="center">
  <img src="assets/demo.gif" width="800"/>
  <br>
  <em>FoxScan v2.0 in action</em>
</p>

```bash
python foxscan.py example.com -p 1-1000 -o report.json
````

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

Download from: [https://nmap.org](https://nmap.org)

---

### 2️⃣ Clone the Repository

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

### 🔹 Custom Ports

```bash
python foxscan.py example.com -p 1-65535
```

### 🔹 Skip Headers

```bash
python foxscan.py example.com --no-headers
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
 - Missing X-Frame-Options (Clickjacking risk)
```

---

## 📁 JSON Output

```json
{
  "target": "example.com",
  "version": "2.0",
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

## 🧪 Research Notes

FoxScan follows real-world reconnaissance principles:

* **Port Scanning**

  * Identifies exposed services quickly
  * Uses optimized scanning techniques

* **Fingerprinting**

  * Detects server technologies
  * Assists in vulnerability mapping

* **Header Analysis**

  * Highlights insecure configurations
  * Reveals attack surface indicators

---

## 🏗 Project Structure

```
FoxScan/
├── LICENSE
├── README.md
├── assets
│   └── demo.gif
├── foxscan.py
└── requirements.txt
```

---

## 🔮 Future Scope

* 🔍 CVE lookup integration (NVD API)
* 🌐 Subdomain enumeration
* 🕷 Web crawling
* 📡 OS detection
* 📊 Web dashboard (UI)
* ⚡ Parallel port scanning engine

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch
3. Make changes
4. Submit a pull request

---

## ⚠️ Disclaimer

This tool is intended for:

✅ Educational purposes
✅ Ethical hacking
✅ Authorized penetration testing

❌ Unauthorized usage is illegal.

The authors are **not responsible for misuse**.

---

## 📜 License

MIT License © 2026 Fox Hackerz

---

## 🦊 About Fox Hackerz

We build tools focused on:

* Cybersecurity
* Automation
* Developer tools

📌 GitHub: [https://github.com/foxhackerzdevs](https://github.com/foxhackerzdevs)

---

<p align="center">
  <b>🦊 Join the pack. Build. Break. Secure.</b>
</p>
