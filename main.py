from modules import port_scan
import os
import argparse
parser = argparse.ArgumentParser(prog='ScoutKit',
                                 description="Toolkit for recon of CTF, boxes or pentest"
                                 )
parser.add_argument('target')
args = parser.parse_args()
def main(target):
    target_dir = f"results/{target}"
    os.makedirs(target_dir, exist_ok=True)

    # Port scanning
    ports = port_scan.scan(target)
    with open(f"{target_dir}/ports.txt", "w") as f:
        f.write("\n".join(ports))
if __name__ == "__main__":
    target_ip = "10.10.10.10"
    if args.target:
        target_ip = args.target()
    else:
        target_ip = input("Target IP or hostname")
        
    main(target_ip)