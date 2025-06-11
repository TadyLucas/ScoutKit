import subprocess
import modules.const as const
import re

def bruteForce(url):
    try:
        wordlist = "modules/wordlists/common.txt"
        result = []

        # Files
        print(f"{const.CYAN}[+] ScoutKit: Bruteforcing files on webserver {url}{const.RESET}")
        cmd = [
            "gobuster", "dir",
            "-u", url,
            "-w", wordlist,
            "-x", "php,html,txt,js",
            "-t", "50",
            "--no-error",
            "--status-codes", "200,204,301,302,307,403",
            "--status-codes-blacklist", "",
        ]
        resultFiles = subprocess.run(cmd, capture_output=True, text=True)
        result.append(printRes(resultFiles.stdout))
        
        # Dirs
        print(f"{const.CYAN}[+] ScoutKit: Bruteforcing files on webserver {url}{const.RESET}")
        cmd = [
            "gobuster", "dir",
            "-u", url,
            "-w", wordlist,
            "-t", "50",
            "--no-error",
            "--status-codes", "200,204,301,302,307,403",
            "--status-codes-blacklist", "",
        ]

        resultDirs = subprocess.run(cmd, capture_output=True, text=True)
        result.append(printRes(resultDirs.stdout.strip().splitlines()))

    except:
        print(f"{const.RED}[x] Bruteforce failed{const.RESET}")


def printRes(output):
    result = []
    pattern = re.compile(r'^\s*(\/[\w\.\-\_/]+)\s+\(Status:\s*(\d{3})\)')

    # Split by lines here
    lines = output.split('\n')

    for line in lines:
        print("output: " + line)
        line = line.strip()
        if not line:
            continue

        match = pattern.search(line)
        if match:
            path, status = match.groups()
            print(f"{const.GREEN}[i] Found: {path} [Status: {status}]")
            result.append(f"[i] Found: {path} [Status: {status}]")

    return result

