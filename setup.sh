#!/bin/bash
set -e

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "[*] Updating package list..."
sudo apt update -qq > /dev/null 2>&1

for pkg in nmap gobuster whatweb python3-venv; do
    if ! command_exists $pkg && ! dpkg -s $pkg > /dev/null 2>&1; then
        echo "[*] Installing $pkg..."
        sudo apt install -y -qq $pkg > /dev/null 2>&1
    else
        echo "[*] $pkg already installed."
    fi
done

# Setup Python virtual environment and install dependencies from requirements.txt
if [ -f requirements.txt ]; then
    echo "[*] Setting up Python virtual environment..."
    python3 -m venv venv
    echo "[*] Activating virtual environment and installing Python packages..."
    source venv/bin/activate
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt > /dev/null 2>&1
    deactivate
    echo "[*] Python packages installed in virtual environment."
else
    echo "[*] requirements.txt not found, skipping Python package installation."
fi

# Create the launcher script
echo "[*] Creating scoutkit launcher..."

sudo tee /usr/local/bin/scoutkit > /dev/null <<'EOF'
#!/bin/bash
cd /opt/scoutkit || { echo "ScoutKit directory not found!"; exit 1; }
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found. Please run the setup script first."
    exit 1
fi
python3 main.py "$@"
deactivate
EOF

sudo chmod +x /usr/local/bin/scoutkit

echo "[*] Setup complete! You can now run 'scoutkit' from anywhere."
