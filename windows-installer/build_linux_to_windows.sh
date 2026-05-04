#!/bin/bash
# Build script to create Windows .exe from Linux using Wine
# This script installs Python for Windows under Wine and runs PyInstaller

set -e

# Suppress Wine ld.so errors from Citrix AppProtection
export LD_PRELOAD=""

echo "=== Scribboleth Installer - Cross-Compile for Windows ==="
echo

# Get absolute path to script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

# Check if Wine is installed
if ! command -v wine &> /dev/null; then
    echo "Wine is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y wine wine64
fi

# Set up Wine Python directory
WINE_PYTHON_DIR="$HOME/.wine/drive_c/Python39"
PYTHON_EXE="$WINE_PYTHON_DIR/python.exe"
PIP_EXE="$WINE_PYTHON_DIR/Scripts/pip.exe"

# Check if Python is already installed in Wine
if [ ! -f "$PYTHON_EXE" ]; then
    echo "Downloading Python for Windows..."
    cd /tmp
    wget -q https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe

    echo "Installing Python for Windows (via Wine)..."
    wine python-3.9.13-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 TargetDir=C:\\Python39
    rm python-3.9.13-amd64.exe
fi

# Verify Python is working in Wine
echo "Verifying Python installation..."
wine "$PYTHON_EXE" --version

# Install PyInstaller in Wine Python
echo "Installing PyInstaller..."
wine "$PIP_EXE" install pyinstaller

# Go to the windows-installer directory
cd "$SCRIPT_DIR"

# Copy required files
echo "Copying files..."
cp "$BASE_DIR/scribboleth.html" .
cp "$BASE_DIR/saver.js" .
cp "$BASE_DIR/installer.bat" .
cp "$BASE_DIR/uninstaller.bat" .

# Run PyInstaller through Wine
echo "Building Windows executable..."
wine "$PYTHON_EXE" -m PyInstaller --onefile --windowed --name "ScribbolethInstaller" installer_gui.py

# Check if build succeeded
if [ -f "dist/ScribbolethInstaller.exe" ]; then
    echo
    echo "=== Build Complete! ==="
    echo "Executable: $(pwd)/dist/ScribbolethInstaller.exe"
    echo
    echo "You can distribute ScribbolethInstaller.exe - it includes everything needed."
else
    echo "Build failed. Check the output above."
    exit 1
fi
