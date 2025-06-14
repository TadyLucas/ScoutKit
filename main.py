from modules import port_scan, core, http_enum, whatWeb, dir_bruteforce, subdomain_bruteforce
import os
import argparse
import sys
import time
import modules.const as const

parser = argparse.ArgumentParser(prog='ScoutKit',
                                 description="Toolkit for recon of CTF, boxes or pentest"
                                 )
parser.add_argument('target')
args = parser.parse_args()

def fullRecon(target): 
    # Start timer
    start = time.perf_counter()

    # Print banner
    core.printBanner()

    result = []

    #Create base dir
    output_dir = f"results/"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{target}.txt")

    #If file exists remove it
    if os.path.isfile(output_file):
        os.remove(output_file)

    # Port scanning
    scannedPorts = port_scan.scan(target)
    result.append(scannedPorts)
    
    httpPorts = http_enum.alivePorts(target)
    if httpPorts:
        for port in httpPorts:
            scheme = "https" if port == 443 else "http"
            url = f"{scheme}://{target}:{port}"

            # # Http recon
            httpEnumResults = http_enum.enum(url)
            if httpEnumResults:
                result.append(httpEnumResults)
    
            # # Whatweb recon
            whatWebRes = whatWeb.enum(url)
            if whatWebRes:
                result.append(whatWebRes)

            # # Dir bruteforce
            bruteForce = dir_bruteforce.bruteForce(url)
            if bruteForce:
                result.append(bruteForce)

            subdomains = subdomain_bruteforce.enumerate(url)
            if subdomains:
                result.append(subdomains)
    else:
        print(f"{const.RED}[x] No web available{const.RESET}")

    
            

    with open(f"{output_file}", "w") as f:
        for res in result:
            if isinstance(res, list):
                for item in res:
                    if isinstance(item, list):
                        for subItem in item:
                            f.write(str(subItem) + "\n")
                    else:
                        f.write(str(item) + "\n")

            else:
                print(res)
                f.write(str(res) + "\n")

    end = time.perf_counter()
    duration = end - start
    minutes = int(duration // 60)
    seconds = int(duration % 60)

    print(f"Recon completed in {const.RED + str(minutes) + const.RESET}m and {const.RED + str(seconds) + const.RESET}s")


if __name__ == "__main__":
    target_ip = "10.10.10.10"
    if args.target:
        target_ip = args.target
    else:
        target_ip = input("Target IP or hostname")

    # if not core.validate(target_ip) :
    #     sys.exit("[x] Target ip address is in wrong format. Try again e.g. 10.10.12.11")
    
    if not core.isHostAlive(target_ip):
        sys.exit("[x] Cannot reach the host")
        
    fullRecon(target_ip)