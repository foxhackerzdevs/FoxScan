#!/usr/bin/env python3

import shlex
import nmap
import requests
import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor

VERSION = "2.0"

# =========================
# BANNER
# =========================
def generate_banner():
    return r'''
  _____ _____  ______   ____    _    _   _ 
 |  ___/ _ \ \/ / ___| / ___|  / \  | \ | |
 | |_ | | | \  /\___ \| |     / _ \ |  \| |
 |  _|| |_| /  \ ___) | |___ / ___ \| |\  |
 |_|   \___/_/\_\____/ \____/_/   \_\_| \_|
                                          
        FoxScan v2.0 - Recon Tool
    '''

# =========================
# ARGUMENT PARSER
# =========================
def parse_args():
    parser = argparse.ArgumentParser(description="FoxScan v2.0 - Recon Tool")
    parser.add_argument("target", help="Target IP or domain")
    parser.add_argument("-p", "--ports", default="1-1000", help="Port range (default: 1-1000)")
    parser.add_argument("-t", "--timeout", type=int, default=5, help="Request timeout")
    parser.add_argument("--no-headers", action="store_true", help="Skip header scan")
    parser.add_argument("-o", "--output", help="Save output to JSON file")
    return parser.parse_args()

# =========================
# PORT SCAN
# =========================
def scan_target(target, ports):
    print(f"[+] Starting Port Scan on: {target}")
    
    try:
        nm = nmap.PortScanner()
    except Exception as e:
        print(f"[-] Nmap error: {e}")
        return {}

    try:
        safe_ports = shlex.quote(ports)
        nm.scan(target, arguments=f"-p {safe_ports} -sV --open")
    except Exception as e:
        print(f"[-] Scan failed: {e}")
        return {}

    results = {}

    for host in nm.all_hosts():
        results[host] = {
            "state": nm[host].state(),
            "protocols": {}
        }

        for proto in nm[host].all_protocols():
            results[host]["protocols"][proto] = {}

            for port in sorted(nm[host][proto].keys()):
                service = nm[host][proto][port]
                results[host]["protocols"][proto][port] = {
                    "state": service["state"],
                    "name": service.get("name", ""),
                    "product": service.get("product", ""),
                    "version": service.get("version", "")
                }

                print(f"{host}:{port} -> {service['state']} ({service.get('product', '')})")

    return results

# =========================
# HEADER ANALYSIS
# =========================
def analyze_headers(headers):
    issues = []

    if "X-Frame-Options" not in headers:
        issues.append("Missing X-Frame-Options (Clickjacking risk)")

    if "X-Content-Type-Options" not in headers:
        issues.append("Missing X-Content-Type-Options")

    if "Server" in headers:
        issues.append(f"Server disclosed: {headers['Server']}")

    return issues

# =========================
# HEADER CHECK
# =========================
def check_headers(url, timeout):
    print(f"\n[*] Checking Headers: {url}")

    if not url.startswith("http"):
        url = "http://" + url

    try:
        response = requests.get(url, timeout=timeout)
        headers = dict(response.headers)

        for k, v in headers.items():
            print(f"{k}: {v}")

        issues = analyze_headers(headers)

        if issues:
            print("\n[!] Potential Issues:")
            for issue in issues:
                print(f" - {issue}")

        return {
            "headers": headers,
            "issues": issues
        }

    except Exception as e:
        print(f"[-] Header check failed: {e}")
        return {}

# =========================
# SAVE REPORT
# =========================
def save_report(data, filename):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"\n[+] Report saved to {filename}")
    except Exception as e:
        print(f"[-] Could not save report: {e}")

# =========================
# MAIN
# =========================
def main():
    print(generate_banner())

    args = parse_args()
    final_data = {
        "target": args.target,
        "version": VERSION
    }

    # Port Scan
    port_data = scan_target(args.target, args.ports)
    final_data["port_scan"] = port_data

    # Header Scan (Threaded)
    if not args.no_headers:
        with ThreadPoolExecutor(max_workers=2) as executor:
            future = executor.submit(check_headers, args.target, args.timeout)
            header_data = future.result()
            final_data["headers"] = header_data

    # Save Output
    if args.output:
        save_report(final_data, args.output)

# =========================
# ENTRY
# =========================
if __name__ == "__main__":
    main()