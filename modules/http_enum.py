import requests
import socket
from bs4 import BeautifulSoup

def enum(ip):
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

            # Headers
            server = response.headers.get('Server', 'Unknown') 
            powered_by = response.headers.get('X-Powered-By', 'Unknown')

            # Title
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string.strip() if soup.title else "No Title"

            result = [
                f"[+] URL: {url}",
                f"--------------",
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
    commonHTTPPorts = [80, 443, 8080, 8089]
    portsAlive = []
    try:
        for port in commonHTTPPorts:
            socket.create_connection((target, port), timeout=1)
            portsAlive.append(port)
    except:
        pass
    
    return portsAlive
