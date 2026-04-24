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

    # MCP / automation mode
    parser.add_argument("--json", action="store_true",
                        help="Output pure JSON (no logs)")

    return parser.parse_args()

# =========================
# PORT SCAN
# =========================
def scan_target(target, ports, silent=False):
    if not silent:
        print(f"[+] Starting Port Scan on: {target}")

    try:
        nm = nmap.PortScanner()
    except Exception as e:
        if not silent:
            print(f"[-] Nmap not found: {e}")
        return {}

    try:
        safe_ports = shlex.quote(ports)
        nm.scan(hosts=target, arguments=f"-p {safe_ports} -sV --open")
    except Exception as e:
        if not silent:
            print(f"[-] Scan failed: {e}")
        return {}

    results = {}

    for host in nm.all_hosts():
        results[host] = {
            "state": nm[host].state(),
            "protocols": {}
        }

        if not silent:
            print(f"\n[+] Host: {host} ({nm[host].state()})")

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

                if not silent:
                    print(f"  └─ {proto.upper()} {port}: {service['state']} "
                          f"{service.get('product','')} {service.get('version','')}")

    return results

# =========================
# HEADER ANALYSIS
# =========================
def analyze_headers(headers):
    issues = []

    if "X-Frame-Options" not in headers:
        issues.append("Missing X-Frame-Options")

    if "X-Content-Type-Options" not in headers:
        issues.append("Missing X-Content-Type-Options")

    if "Strict-Transport-Security" not in headers:
        issues.append("Missing HSTS")

    if "Content-Security-Policy" not in headers:
        issues.append("Missing CSP")

    if "Server" in headers:
        issues.append(f"Server disclosed: {headers['Server']}")

    return issues

# =========================
# HEADER CHECK
# =========================
def check_headers(url, timeout, silent=False):
    if not url.startswith("http"):
        url = "http://" + url

    if not silent:
        print(f"\n[*] Checking Headers: {url}")

    try:
        response = requests.get(url, timeout=timeout)
        headers = dict(response.headers)

        issues = analyze_headers(headers)

        if not silent:
            print("\n[+] Headers:")
            for k, v in headers.items():
                print(f"  {k}: {v}")

            if issues:
                print("\n[!] Issues:")
                for i in issues:
                    print(f"  - {i}")
            else:
                print("\n[+] No issues found")

        return {
            "headers": headers,
            "issues": issues,
            "status_code": response.status_code
        }

    except requests.exceptions.RequestException as e:
        if not silent:
            print(f"[-] Header check failed: {e}")
        return {"error": str(e)}

# =========================
# SAVE REPORT
# =========================
def save_report(data, filename):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"\n[+] Report saved to {filename}")
    except Exception as e:
        print(f"[-] Save failed: {e}")

# =========================
# MCP SERVER MODE (basic)
# =========================
def mcp_mode():
    """
    Minimal MCP-style loop (stdin/stdout JSON RPC-like)
    """
    for line in sys.stdin:
        try:
            req = json.loads(line.strip())
            action = req.get("action")
            target = req.get("target")

            if action == "scan":
                result = scan_target(target, "1-1000", silent=True)
            elif action == "headers":
                result = check_headers(target, 5, silent=True)
            else:
                result = {"error": "Unknown action"}

            print(json.dumps({"result": result}))
            sys.stdout.flush()

        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

# =========================
# MAIN
# =========================
def main():
    if "--mcp" in sys.argv:
        mcp_mode()
        return

    print(generate_banner())

    args = parse_args()
    silent = args.json

    final_data = {
        "target": args.target,
        "version": VERSION
    }

    # Port Scan
    final_data["port_scan"] = scan_target(
        args.target,
        args.ports,
        silent=silent
    )

    # Header Scan
    if not args.no_headers:
        with ThreadPoolExecutor(max_workers=2) as executor:
            future = executor.submit(
                check_headers,
                args.target,
                args.timeout,
                silent
            )
            final_data["headers"] = future.result()

    # Output handling
    if args.output:
        save_report(final_data, args.output)

    if args.json:
        print(json.dumps(final_data, indent=2))

# =========================
# ENTRY
# =========================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted")
        sys.exit(1)