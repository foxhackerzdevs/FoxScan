#!/usr/bin/env python3

import nmap
import requests
import argparse
import json
import sys

VERSION = "2.2"

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

        FoxScan v2.2 - Recon Tool
    '''

# =========================
# ARGUMENT PARSER
# =========================
def parse_args():
    parser = argparse.ArgumentParser(description="FoxScan v2.2 - Recon Tool")

    parser.add_argument("target", help="Target IP or domain")
    parser.add_argument("-p", "--ports", default="1-1000",
                        help="Port range (default: 1-1000)")
    parser.add_argument("-t", "--timeout", type=int, default=5,
                        help="Request timeout")
    parser.add_argument("--no-headers", action="store_true",
                        help="Skip header scan")
    parser.add_argument("--service", action="store_true",
                        help="Enable service/version detection")
    parser.add_argument("-o", "--output",
                        help="Save JSON report")
    parser.add_argument("--json", action="store_true",
                        help="Pure JSON output")
    parser.add_argument("--mcp", action="store_true",
                        help="Enable MCP mode")

    return parser.parse_args()

# =========================
# PORT SCAN
# =========================
def scan_target(target, ports, service=False, silent=False):
    if not silent:
        print(f"[+] Starting Port Scan on: {target}")

    try:
        nm = nmap.PortScanner()
    except nmap.PortScannerError:
        print("[-] Nmap not found. Please install it.")
        sys.exit(1)

    scan_args = f"-p {ports} -T4 --host-timeout 30s"
    if service:
        scan_args += " -sV"

    try:
        nm.scan(hosts=target, arguments=scan_args)
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
                service_data = nm[host][proto][port]

                if service_data["state"] != "open":
                    continue

                port_info = {
                    "state": service_data["state"],
                    "name": service_data.get("name", ""),
                    "product": service_data.get("product", ""),
                    "version": service_data.get("version", "")
                }

                results[host]["protocols"][proto][port] = port_info

                if not silent:
                    print(f"  └─ {proto.upper()} {port} "
                          f"[{port_info['name']}] "
                          f"{port_info['product']} {port_info['version']}")

    return results

# =========================
# EXTRACT OPEN PORTS
# =========================
def extract_open_ports(scan_data):
    ports = set()
    for host in scan_data.values():
        for proto in host.get("protocols", {}).values():
            for port, data in proto.items():
                if data["state"] == "open":
                    ports.add(port)
    return ports

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
    if not silent:
        print(f"\n[~] HTTP Recon: {url}")

    try:
        headers = {"User-Agent": "FoxScan/2.2"}
        response = requests.get(url, timeout=timeout, headers=headers)

        hdrs = dict(response.headers)
        issues = analyze_headers(hdrs)

        if not silent:
            print("\n[+] Headers:")
            for k, v in hdrs.items():
                print(f"  {k}: {v}")

            if issues:
                print("\n[!] Security Observations:")
                for i in issues:
                    print(f"  - {i}")
            else:
                print("\n[+] No issues found")

        return {
            "headers": hdrs,
            "issues": issues,
            "status_code": response.status_code
        }

    except requests.exceptions.RequestException as e:
        if not silent:
            print(f"[-] Header check failed: {e}")
        return {"error": str(e)}

# =========================
# MCP MODE
# =========================
def mcp_mode():
    for line in sys.stdin:
        try:
            req = json.loads(line.strip())

            req_id = req.get("id")
            action = req.get("action")
            target = req.get("target")

            if not target:
                result = {"error": "Missing target"}

            elif action == "scan":
                result = scan_target(target, "1-1000", silent=True)

            elif action == "headers":
                result = check_headers(target, 5, silent=True)

            else:
                result = {"error": "Unknown action"}

            print(json.dumps({
                "id": req_id,
                "result": result
            }))
            sys.stdout.flush()

        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

# =========================
# MAIN
# =========================
def main():
    args = parse_args()

    if args.mcp:
        mcp_mode()
        return

    print(generate_banner())

    silent = args.json

    final_data = {
        "target": args.target,
        "version": VERSION
    }

    # Port Scan
    port_data = scan_target(
        args.target,
        args.ports,
        args.service,
        silent
    )
    final_data["port_scan"] = port_data

    # Header Detection
    if not args.no_headers:
        open_ports = extract_open_ports(port_data)

        common_http_ports = [80, 443, 8080, 8000, 8888, 3000]
        url = None

        for p in common_http_ports:
            if p in open_ports:
                scheme = "https" if p == 443 else "http"
                url = f"{scheme}://{args.target}:{p}" if p not in [80, 443] else f"{scheme}://{args.target}"
                break

        if url:
            final_data["headers"] = check_headers(url, args.timeout, silent)
        else:
            final_data["headers"] = {"info": "No HTTP service detected"}

    final_data["status"] = "ok" if port_data else "failed"

    if args.output:
        with open(args.output, "w") as f:
            json.dump(final_data, f, indent=4)
        print(f"\n[+] Report saved to {args.output}")

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