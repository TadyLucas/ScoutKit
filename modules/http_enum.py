import requests
import socket
from bs4 import BeautifulSoup

def enum(ip):
    print(f"[+] ScoutKit: HTTP enumeration {ip}")
    allResults = []
    res = alivePorts(ip)
    if not res:
        return False
    
    for port in res:
        scheme = "https" if port == 443 else "http"
        url = f"{scheme}://{ip}:{port}"

        
        try:
            response = requests.get(url, timeout=3, verify=False, allow_redirects=True)

            # Status code
            status = response.status_code
            print(f" [i] Status: {status}")

            # Headers
            server = response.headers.get('Server', 'Unknown') 
            powered_by = response.headers.get('X-Powered-By', 'Unknown')
            print(f" [i] Server: {server}")
            print(f" [i] X-Powered-By: {powered_by}")

            # Title
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string.strip() if soup.title else "No Title"
            print(f" [i] Title:  {title}")

            result = [
                f"\n HTTP Enumeration",
                f"--------------",
                f"[+] URL: {url}",
                f"Status: {status}",
                f"Title:  {title}",
                f"Server: {server}",
                f"X-Powered-By: {powered_by}",
            ]
            allResults.append(result)

        except:
            pass
    return allResults


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
