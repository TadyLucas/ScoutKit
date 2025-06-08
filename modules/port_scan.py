import subprocess
import socket

def scan(target):
    print(f"[+] ScoutKit: Scanning ports and OS on {target}")

    results = subprocess.run(
        ["nmap", "-sV", "-O", "-p", "0-10000", "--min-rate", "1000", "-T4", target],
        capture_output=True, text=True
    )

    nmap_info = []

    # Parse output line by line
    lines = results.stdout.splitlines()

    # Collect open ports
    for line in lines:
        if "/tcp" in line and "open" in line:
            nmap_info.append(line.strip())

    # Simple way to extract OS info section (lines starting with "OS details" or "OS detection")
    for i, line in enumerate(lines):
        if line.startswith("OS details") or line.startswith("OS detection") or line.startswith("Running:"):
            nmap_info.append(line.strip())
            break

    
    return nmap_info


