import subprocess
import modules.const as const
import re

def bruteForce(url):
    try:
        wordlist = "modules/wordlists/common.txt"
        result = []

        # Files
        print(f"{const.CYAN}[+] ScoutKit: Bruteforcing files on webserver{const.RESET}")
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
        result.append(printRes(resultFiles.stdout.strip()))
        
        # Dirs
        print(f"{const.CYAN}[+] ScoutKit: Bruteforcing files on webserver{const.RESET}")
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
        result.append(printRes(resultDirs.stdout.strip()))

    except:
        print(f"{const.RED}[x] Bruteforce failed{const.RESET}")

def printRes(output):
    result = []
    for line in output:
        match = re.search(r'(/[\w\-/\.]+)\s+\(Status:\s+(\d+)', line)
        if match:
            path, status = match.groups()
            print(f" {const.GREEN}[i] Found: {path} [Status: {status}]")
            result.append(f"[i] Found: {path} [Status: {status}]")