import requests
import socket
from bs4 import BeautifulSoup
import modules.const as const

def enum(url):
    print(f"{const.CYAN}[+] ScoutKit: HTTP enumeration {url}")
    result = []
    
    try:
        response = requests.get(url, timeout=3, verify=False, allow_redirects=True)

        # Status code
        status = response.status_code
        print(f"{const.GREEN} [i] Status: {status}")

        # Headers
        server = response.headers.get('Server', 'Unknown') 
        powered_by = response.headers.get('X-Powered-By', 'Unknown')
        print(f"{const.GREEN} [i] Server: {server}")
        print(f"{const.GREEN} [i] X-Powered-By: {powered_by}")

        # Title
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else "No Title"
        print(f"{const.GREEN} [i] Title:  {title}")

        result = [
            f"\nHTTP Enumeration",
            f"--------------",
            f"[+] URL: {url}",
            f"Status: {status}",
            f"Title:  {title}",
            f"Server: {server}",
            f"X-Powered-By: {powered_by}",
        ]

    except:
        pass

    return result


def alivePorts(target):
    commonHTTPPorts = [
    80,    # HTTP
    443,   # HTTPS
    8000,  # Python http.server, Django
    8001,  # Alternate dev server
    8080,  # Common alternate HTTP port
    8089,  # Used by Splunk web interface or custom services
    8443,  # Alternate HTTPS port
    5000,  # Flask
    3000,  # React / Node.js dev
    4200,  # Angular
    5173,  # Vite
    ]
    portsAlive = []
    for port in commonHTTPPorts:
        try:
            socket.create_connection((target, port), timeout=1)
            portsAlive.append(port)
        except:
            pass
    return portsAlive
