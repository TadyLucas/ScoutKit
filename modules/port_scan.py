import subprocess
import modules.const as const

def scan(target):
    print(f"{const.CYAN}[+] ScoutKit: Scanning ports and OS")

    cmd = ["nmap", "-sS","-sV", "-O", "-p-", "--min-rate", "1000", "--min-parallelism", "100","-T4", "-Pn", "-n",target]
    
    results = subprocess.run(
        cmd,
        capture_output=True, text=True
    )

    nmap_info = []

    # Parse output line by line
    lines = results.stdout.splitlines()

    nmap_info.append("Port scan\n-------------\n")

    # Collect open ports
    for line in lines:
        if "/tcp" in line and "open" in line:
            nmap_info.append(line.strip())
            print(f"{const.GREEN} [i] Port: {line.strip()}")

    # Simple way to extract OS info section (lines starting with "OS details" or "OS detection")
    for i, line in enumerate(lines):
        if line.startswith("OS details") or line.startswith("OS detection") or line.startswith("Running:"):
            nmap_info.append(line.strip())
            print(f"{const.GREEN} [i] OS:{line.strip()}")
            break

    
    return nmap_info


