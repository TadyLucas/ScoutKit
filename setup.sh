#!/bin/bash
set -e

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "[*] Updating package list..."
sudo apt update -qq > /dev/null 2>&1

for pkg in nmap gobuster whatweb rustc cargo python3-venv; do
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

INSTALL_DIR="/opt/scoutkit"
LAUNCHER="/usr/local/bin/scoutkit"

echo "[*] Building ScoutKit Rust project..."
cd "$INSTALL_DIR"
cargo build --quiet

echo "[*] Creating launcher script..."
sudo tee "$LAUNCHER" > /dev/null <<EOF
#!/bin/bash
cd "$INSTALL_DIR" || exit 1
./target/debug/subdomains "\$@"
EOF

sudo chmod +x "$LAUNCHER"

echo "[*] Setup complete! You can now run 'scoutkit' from anywhere."
