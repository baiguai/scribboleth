@echo off
REM Build script for Scribboleth Installer GUI
REM Requires: pip install pyinstaller

echo Installing PyInstaller...
pip install pyinstaller

echo Building executable...
pyinstaller --onefile --windowed --name "ScribbolethInstaller" --icon=NONE installer_gui.py

echo.
echo Build complete! Executable is in dist\ScribbolethInstaller.exe
echo.

if exist "dist\ScribbolethInstaller.exe" (
    echo You can now distribute ScribbolethInstaller.exe
    echo It includes everything needed - no Python or Node.js required for installation
) else (
    echo Build failed. Check the output above.
)

pause
