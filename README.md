# ScoutKit

ScoutKit is a modular, extensible network and web reconnaissance framework designed to automate the initial phases of penetration testing and Capture The Flag (CTF) challenges like Hack The Box (HTB). It helps you quickly discover open ports, identify services, enumerate web applications, and organize your findings — all in one place.

---

## Features

- **Fast Port Scanning**  
  Uses `nmap` to discover open TCP ports with customizable speed settings.

- **Web Enumeration**  
  Automatically probes common web ports (80, 443, 8080), fetches HTTP status codes, page titles, and detects basic web technologies.

- **Modular Design**  
  Easily extend functionality by adding new modules (e.g., SMB, FTP enumeration) without changing core logic.

- **Organized Output**  
  Saves all recon data into structured directories for each target, making follow-up analysis easier.

- **Extensible Framework**  
  Designed with scalability in mind to add screenshotting, CMS detection, subdomain enumeration, and more.

---

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/TadyLucas/ScoutKit.git
    cd ScoutKit
    ```

2. Install Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Ensure `nmap` is installed and accessible from your terminal.

---

## Usage

Run the main script and enter the target IP or hostname:

```bash
python3 main.py
