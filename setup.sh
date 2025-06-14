#!/bin/bash
set -e

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "[*] Updating package list..."
sudo apt update -qq > /dev/null 2>&1

if ! command_exists nmap; then
    echo "[*] Installing nmap..."
    sudo apt install -y -qq nmap > /dev/null 2>&1
else
    echo "[*] nmap already installed."
fi

if ! command_exists gobuster; then
    echo "[*] Installing gobuster..."
    sudo apt install -y -qq gobuster > /dev/null 2>&1
else
    echo "[*] gobuster already installed."
fi

if ! command_exists whatweb; then
    echo "[*] Installing whatweb..."
    sudo apt install -y -qq whatweb > /dev/null 2>&1
else
    echo "[*] whatweb already installed."
fi

if ! command_exists rustc || ! command_exists cargo; then
    echo "[*] Installing Rust..."
    sudo apt install -y -qq rustc cargo > /dev/null 2>&1
else
    echo "[*] Rust already installed."
fi

# Install python3-venv if not present
if ! dpkg -s python3-venv > /dev/null 2>&1; then
    echo "[*] Installing python3-venv..."
    sudo apt install -y -qq python3-venv > /dev/null 2>&1
else
    echo "[*] python3-venv already installed."
fi

# Setup Python virtual environment and install dependencies from requirements.txt
if [ -f requirements.txt ]; then
    echo "[*] Setting up Python virtual environment..."
    python3 -m venv venv
    echo "[*] Activating virtual environment and installing Python packages..."
    # Activate venv and install, suppress pip output except errors
    source venv/bin/activate
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt > /dev/null 2>&1
    deactivate
    echo "[*] Python packages installed in virtual environment."
else
    echo "[*] requirements.txt not found, skipping Python package installation."
fi

echo "[*] Setup complete!"
