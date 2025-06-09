from modules import port_scan, core, http_enum
import os
import argparse
import sys
import requests

parser = argparse.ArgumentParser(prog='ScoutKit',
                                 description="Toolkit for recon of CTF, boxes or pentest"
                                 )
parser.add_argument('target')
args = parser.parse_args()

def fullRecon(target):    
    result = []

    #Create base dir
    output_dir = f"results/"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{target}.txt")

    #If file exists remove it
    if os.path.isfile(output_file):
        os.remove(output_file)

    # Port scanning
    ports = port_scan.scan(target)
    result.append(core.modifyOutput("\n".join(ports), "Port scan"))

    # Http recon
    httpEnumResults = http_enum.enum(target)
    if httpEnumResults:
        result.append(httpEnumResults)

    with open(f"{output_file}", "w") as f:
        for res in result:
            if isinstance(res, list):
                for item in res:
                    for subItem in item:
                        f.write(str(subItem) + "\n")
            else:
                f.write(str(res) + "\n")


if __name__ == "__main__":
    target_ip = "10.10.10.10"
    if args.target:
        target_ip = args.target
    else:
        target_ip = input("Target IP or hostname")

    if not core.validate(target_ip) :
        sys.exit("[x] Target ip address is in wrong format. Try again e.g. 10.10.12.11")
    
    if not core.isHostAlive(target_ip):
        sys.exit("[x] Cannot reach the host")
        
    fullRecon(target_ip)