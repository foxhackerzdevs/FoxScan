#!/usr/bin/env python3

import shlex
import nmap
import requests
import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor

VERSION = "2.1"

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

        FoxScan v2.1 - Recon Tool
    '''

# =========================
# ARGUMENT PARSER
# =========================
def parse_args():
    parser = argparse.ArgumentParser(description="FoxScan v2.1 - Recon Tool")

    parser.add_argument("target", help="Target IP or domain")
    parser.add_argument("-p", "--ports", default="1-1000",
                        help="Port range (default: 1-1000)")
    parser.add_argument("-t", "--timeout", type=int, default=5,
                        help="Request timeout (default: 5)")
    parser.add_argument("--no-headers", action="store_true",
                        help="Skip header scan")
    parser.add_argument("-o", "--output",
                        help="Save output to JSON file")

    return parser.parse_args()

# =========================
# PORT SCAN
# =========================
def scan_target(target, ports):
    print(f"[+] Starting Port Scan on: {target}")

    try:
        nm = nmap.PortScanner()
    except Exception as e:
        print(f"[-] Nmap not found or error: {e}")
        return {}

    try:
        safe_ports = shlex.quote(ports)
        nm.scan(hosts=target, arguments=f"-p {safe_ports} -sV --open")
    except Exception as e:
        print(f"[-] Scan failed: {e}")
        return {}

    results = {}

    for host in nm.all_hosts():
        print(f"\n[+] Host: {host} ({nm[host].state()})")

        results[host] = {
            "state": nm[host].state(),
            "protocols": {}
        }

        for proto in nm[host].all_protocols():
            results[host]["protocols"][proto] = {}

            for port in sorted(nm[host][proto].keys()):
                service = nm[host][proto][port]

                port_info = {
                    "state": service["state"],
                    "name": service.get("name", ""),
                    "product": service.get("product", ""),
                    "version": service.get("version", "")
                }

                results[host]["protocols"][proto][port] = port_info

                print(f"  └─ {proto.upper()} {port}: {service['state']} "
                      f"{service.get('product', '')} {service.get('version', '')}")

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

    if "Strict-Transport-Security" not in headers:
        issues.append("Missing HSTS (HTTPS not enforced)")

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

        print("\n[+] Response Headers:")
        for k, v in headers.items():
            print(f"  {k}: {v}")

        issues = analyze_headers(headers)

        if issues:
            print("\n[!] Potential Issues:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("\n[+] No obvious header issues found")

        return {
            "headers": headers,
            "issues": issues
        }

    except requests.exceptions.RequestException as e:
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
            final_data["headers"] = future.result()

    # Save Output
    if args.output:
        save_report(final_data, args.output)

# =========================
# ENTRY
# =========================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        sys.exit(1)
