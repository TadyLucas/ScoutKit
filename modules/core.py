from ipaddress import ip_address
from ping3 import ping
import socket

def validate(ip):
    try:
        if ip_address(ip):
            return True
        else:
            return False
    except:
        return False


def printBanner():
    from rich.console import Console
    import pyfiglet

    console = Console()
    banner = pyfiglet.figlet_format("ScoutKit")
    console.print(banner, style="bold cyan")


def isHostAlive(ip):
    response = ping(ip, timeout=1)
    
    if response is not None:
        return True
    else:
        for port in [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389]:
            try:
                with socket.create_connection((ip, port), timeout=1):
                    return True
            except:
                pass
    return False

