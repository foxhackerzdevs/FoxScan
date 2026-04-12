# 🦊 FoxScan v1.0
**Automated Reconnaissance & Asset Discovery Tool**

Developed by **Fox Hackerz** ([@foxhackerzdevs](https://github.com/foxhackerzdevs))

---

## 🛠 Description
FoxScan is a lightweight, modular reconnaissance tool designed for the initial phase of a penetration test. It automates the process of identifying active hosts, scanning for open ports, and extracting critical HTTP header information to identify server technologies.

## 🚀 Key Features
- **Fast Port Discovery**: Scans common ports to identify attack surfaces quickly.
- **Service Fingerprinting**: Grabs HTTP response headers to identify CMS, server versions, and security configurations.
- **Minimal Dependencies**: Built with Python for portability and ease of use.
- **Clean Output**: Structured terminal output for easy analysis.

## 📦 Installation

1. **Prerequisites**: Ensure you have [Nmap](https://nmap.org) installed on your system.
2. **Clone the Repo**:
   ```bash
   git clone https://github.com/foxhackerzdevs/FoxScan.git
   cd FoxScan
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

Run the script against a target domain or IP address:
```bash
python foxscan.py <target_ip_or_domain>
```

## 🛡 Disclaimer
This tool is for **educational and ethical security testing purposes only**. Unauthorized scanning of targets without prior consent is illegal. The Fox Hackerz team is not responsible for any misuse of this tool.

---

**Join the pack.** Follow us for more security tools. 🦊