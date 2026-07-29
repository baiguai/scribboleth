# Scribboleth Windows Installer

A Python GUI for installing and uninstalling Scribboleth instances on Windows.

## Files

- `installer_gui.py` - The main Python GUI application
- `build.bat` - Build script for Windows (run on Windows)
- `build_linux_to_windows.sh` - Build script for Linux (cross-compile using Wine)
- `README.md` - This file

## Building on Windows

1. Install Python 3.9+ on Windows
2. Install PyInstaller: `pip install pyinstaller`
3. Run: `build.bat`
4. Find the executable in `dist/ScribbolethInstaller.exe`

## Building on Linux (Cross-Compile)

**Option 1: Using Wine (automated)**
```bash
chmod +x build_linux_to_windows.sh
./build_linux_to_windows.sh
```

**Option 2: Manual (using Windows VM)**
1. Copy the `windows-installer` folder to a Windows machine
2. Run `build.bat` on Windows

**Option 3: Using a Windows CI/CD service**
- Use GitHub Actions with Windows runner to build the .exe

## Distribution

The resulting `ScribbolethInstaller.exe` is standalone and includes:
- Python runtime
- tkinter GUI
- All required scripts

Users can simply double-click the .exe - no Python or Node.js installation required.

## Usage

1. Place `ScribbolethInstaller.exe` in the same directory as `scribboleth.html` and `saver.js`
2. Run `ScribbolethInstaller.exe`
3. Use "Install" tab to create new Scribboleth instances
4. Use "Uninstall" tab to remove existing instances
5. The installer handles port assignment, file creation, and npm setup automatically

**Note:** The .exe automatically finds `scribboleth.html` and `saver.js` in its own directory - no installation needed!
