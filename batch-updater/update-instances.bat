@echo off
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "CONF=%SCRIPT_DIR%\instances.conf"
set "HELPER=%SCRIPT_DIR%\update-helper.cjs"
set "DEFAULT_TEMPLATE=%SCRIPT_DIR%\..\scribboleth.html"
if not exist "%DEFAULT_TEMPLATE%" set "DEFAULT_TEMPLATE=%SCRIPT_DIR%\scribboleth.html"
set "TEMPLATE=%~1"
if "%TEMPLATE%"=="" set "TEMPLATE=%DEFAULT_TEMPLATE%"

if not exist "%CONF%" (
    echo instances.conf not found at %CONF%
    echo.
    echo Create it with one full path per line to each scribboleth .html file to upgrade:
    echo   C:\path\to\scrib1\notes.html
    echo   C:\path\to\scrib2\journal.html
    exit /b 1
)

if not exist "%HELPER%" (
    echo update-helper.cjs not found at %HELPER%
    exit /b 1
)

if not exist "%TEMPLATE%" (
    echo Template not found at %TEMPLATE%
    exit /b 1
)

where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Node.js is required but not found in PATH
    exit /b 1
)

set count=0
for /f "usebackq delims=" %%i in ("%CONF%") do (
    set "line=%%i"
    if not "!line!"=="" (
        if not exist "%%i" (
            echo [SKIP] File not found: %%i
        ) else (
            echo [INSTANCE] %%i
            node "%HELPER%" "%%i" "%TEMPLATE%"
            set /a count+=1
        )
    )
)

echo.
echo Done. %count% instance^(s^) processed.
