import subprocess

def scan(target):
    print(f"[+] ScoutKit: Scanning ports on {target}")
    results = subprocess.run(
        ["nmap", "-p-", "--min-rate", "1000", "-T4", target],
        capture_output=True, text=True
    )
    open_ports = []
    for line in results.stdout.splitlines():
        if "/tcp" in line and "open" in line:
            open_ports.append(line.strip())
    return open_ports