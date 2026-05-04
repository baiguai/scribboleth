@echo off
setlocal enabledelayedexpansion

REM Check for the correct number of arguments
if "%~1"=="" goto usage

REM Check for Node.js
where node >nul 2>&1
IF %ERRORLEVEL% NEQ 0 goto nonode

REM Check for npm
where npm >nul 2>&1
IF %ERRORLEVEL% NEQ 0 goto nonode

set "FULL_PATH=%~1"
for %%F in ("%FULL_PATH%") do (
    set "TARGET_DIR=%%~dpF"
    set "FILENAME=%%~nF"
)

if "%FILENAME%"=="" (
    echo Error: Could not extract filename from path.
    exit /b 1
)

set "SCRNODES_BAT=%USERPROFILE%\scrnodes.bat"
set "HTML_FILE=%TARGET_DIR%\%FILENAME%.html"
set "SAVER_JS_FILE=%TARGET_DIR%\svr_%FILENAME%.js"

REM Ensure target directory exists
if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"

if exist "%HTML_FILE%" (
  if exist "%SAVER_JS_FILE%" (
    echo "Installation for %FILENAME% in %TARGET_DIR% already exists. Aborting."
    exit /b 0
  )
)

REM Determine the next available port
set "PORT=3000"
set "LAST_PORT="
if exist "%SCRNODES_BAT%" (
    for /f "tokens=2" %%i in ('findstr /r "^REM [0-9][0-9]*" "%SCRNODES_BAT%"') do set "LAST_PORT=%%i"
    if not defined LAST_PORT (
        for /f "tokens=2 delims=:" %%i in ('findstr /r "echo.*:[0-9]*" "%SCRNODES_BAT%"') do (
            set "LAST_PORT=%%i"
            set "LAST_PORT=!LAST_PORT: =!"
        )
    )
    if defined LAST_PORT (
        set /a "PORT=LAST_PORT + 1" 2>nul
        if errorlevel 1 set "PORT=3000"
    )
)


REM Create or update the scrnodes.bat script
if not exist "%SCRNODES_BAT%" goto create_new_scrnodes
goto update_existing_scrnodes

:create_new_scrnodes
(
    echo @echo off
    echo.
    echo REM %PORT%
    echo.
    echo cd /d "%TARGET_DIR%"
    echo start "" /b node "%SAVER_JS_FILE%"
    echo.
    echo timeout /t 3 /nobreak ^>nul
    echo.
    echo echo.
    echo echo.
    echo echo.
    echo echo %FILENAME%: %PORT%
    echo echo.
    echo echo.
    echo echo.
    echo.
    echo :wait_loop
    echo timeout /t 1 /nobreak ^>nul
    echo goto wait_loop
) > "%SCRNODES_BAT%"
goto after_scrnodes_update

:update_existing_scrnodes
set "TEMP_PS=%TEMP%\update_scrnodes.ps1"
echo $file = '%SCRNODES_BAT%' > "%TEMP_PS%"
echo $targetDir = '%TARGET_DIR%' >> "%TEMP_PS%"
echo $saverFile = '%SAVER_JS_FILE%' >> "%TEMP_PS%"
echo $filename = '%FILENAME%' >> "%TEMP_PS%"
echo $port = '%PORT%' >> "%TEMP_PS%"
echo. >> "%TEMP_PS%"
echo $content = @(Get-Content -path $file -ErrorAction SilentlyContinue) >> "%TEMP_PS%"
echo if (-not $content) { Write-Host 'Error reading file'; exit 1 } >> "%TEMP_PS%"
echo. >> "%TEMP_PS%"
echo $exists = $false >> "%TEMP_PS%"
echo foreach ($line in $content) { >> "%TEMP_PS%"
echo     if ($line -match [regex]::Escape($saverFile)) { >> "%TEMP_PS%"
echo         $exists = $true >> "%TEMP_PS%"
echo         break >> "%TEMP_PS%"
echo     } >> "%TEMP_PS%"
echo } >> "%TEMP_PS%"
echo. >> "%TEMP_PS%"
echo if ($exists) { >> "%TEMP_PS%"
echo     Write-Host 'Instance already exists in scrnodes.bat' >> "%TEMP_PS%"
echo     exit 0 >> "%TEMP_PS%"
echo } >> "%TEMP_PS%"
echo. >> "%TEMP_PS%"
echo $lastRemIndex = -1 >> "%TEMP_PS%"
echo for ($i = 0; $i -lt $content.Count; $i++) { >> "%TEMP_PS%"
echo     if ($content[$i] -match '^REM [0-9]') { >> "%TEMP_PS%"
echo         $lastRemIndex = $i >> "%TEMP_PS%"
echo     } >> "%TEMP_PS%"
echo } >> "%TEMP_PS%"
echo. >> "%TEMP_PS%"
echo if ($lastRemIndex -ge 0) { >> "%TEMP_PS%"
echo     $content = $content[0..$lastRemIndex] + "REM $port" + $content[($lastRemIndex+1)..($content.Count-1)] >> "%TEMP_PS%"
echo } >> "%TEMP_PS%"
echo. >> "%TEMP_PS%"
echo $waitLoopIndex = -1 >> "%TEMP_PS%"
echo for ($i = 0; $i -lt $content.Count; $i++) { >> "%TEMP_PS%"
echo     if ($content[$i] -match ':wait_loop') { >> "%TEMP_PS%"
echo         $waitLoopIndex = $i >> "%TEMP_PS%"
echo         break >> "%TEMP_PS%"
echo     } >> "%TEMP_PS%"
echo } >> "%TEMP_PS%"
echo. >> "%TEMP_PS%"
echo if ($waitLoopIndex -lt 0) { >> "%TEMP_PS%"
echo     Write-Host ':wait_loop not found' >> "%TEMP_PS%"
echo     exit 1 >> "%TEMP_PS%"
echo } >> "%TEMP_PS%"
echo. >> "%TEMP_PS%"
echo $cdLine = "cd /d \"" + $targetDir + "\""" >> "%TEMP_PS%"
echo $startLine = "start \""\"" /b node \"" + $saverFile + "\""" >> "%TEMP_PS%"
echo $content = $content[0..($waitLoopIndex-1)] + $cdLine + $startLine + $content[$waitLoopIndex..($content.Count-1)] >> "%TEMP_PS%"
echo. >> "%TEMP_PS%"
echo $waitLoopIndex = $waitLoopIndex + 2 >> "%TEMP_PS%"
echo. >> "%TEMP_PS%"
echo $lastEchoIndex = -1 >> "%TEMP_PS%"
echo for ($i = 0; $i -lt $waitLoopIndex; $i++) { >> "%TEMP_PS%"
echo     if ($content[$i] -match 'echo .*:[0-9]') { >> "%TEMP_PS%"
echo         $lastEchoIndex = $i >> "%TEMP_PS%"
echo     } >> "%TEMP_PS%"
echo } >> "%TEMP_PS%"
echo. >> "%TEMP_PS%"
echo if ($lastEchoIndex -ge 0) { >> "%TEMP_PS%"
echo     $echoLine = "echo " + $filename + ": " + $port >> "%TEMP_PS%"
echo     $content = $content[0..$lastEchoIndex] + $echoLine + $content[($lastEchoIndex+1)..($content.Count-1)] >> "%TEMP_PS%"
echo } >> "%TEMP_PS%"
echo. >> "%TEMP_PS%"
echo $content | Out-File -filepath $file -encoding ASCII >> "%TEMP_PS%"
powershell -ExecutionPolicy Bypass -File "%TEMP_PS%"
del "%TEMP_PS%" >nul 2>&1

:after_scrnodes_update

if not exist "%HTML_FILE%" (
    REM Copy scribboleth.html to the target directory
    copy "%~dp0scribboleth.html" "%HTML_FILE%" >nul

    REM Update the node port in the new html file
    powershell -Command "(Get-Content -path '%HTML_FILE%') -replace 'let nodePort = 0;', 'let nodePort = %PORT%;' | Set-Content -path '%HTML_FILE%'"
    powershell -Command "(Get-Content -path '%HTML_FILE%') -replace 'let fileName = \"help\";', 'let fileName = \"%FILENAME%\";' | Set-Content -path '%HTML_FILE%'"
) else (
    REM Update the node port and file name in the existing html file
    powershell -Command "(Get-Content -path '%HTML_FILE%') -replace 'let nodePort = [0-9]*;', 'let nodePort = %PORT%;' | Set-Content -path '%HTML_FILE%'"
    powershell -Command "(Get-Content -path '%HTML_FILE%') -replace 'let fileName = \".*\";', 'let fileName = \"%FILENAME%\";' | Set-Content -path '%HTML_FILE%'"
)

if not exist "%SAVER_JS_FILE%" (
    REM Copy saver.js to the target directory
    copy "%~dp0saver.js" "%SAVER_JS_FILE%" >nul

    REM Update the file name and port in the new saver.js file
    powershell -Command "(Get-Content -path '%SAVER_JS_FILE%') -replace 'const FILE_PATH = \"./scribboleth.html\";', 'const FILE_PATH = \"./%FILENAME%.html\";' | Set-Content -path '%SAVER_JS_FILE%'"
    powershell -Command "(Get-Content -path '%SAVER_JS_FILE%') -replace 'const PORT = 3000;', 'const PORT = %PORT%;' | Set-Content -path '%SAVER_JS_FILE%'"
) else (
    REM Update the file name and port in the existing saver.js file
    powershell -Command "(Get-Content -path '%SAVER_JS_FILE%') -replace 'const FILE_PATH = \".*\";', 'const FILE_PATH = \"./%FILENAME%.html\";' | Set-Content -path '%SAVER_JS_FILE%'"
    powershell -Command "(Get-Content -path '%SAVER_JS_FILE%') -replace 'const PORT = [0-9]*;', 'const PORT = %PORT%;' | Set-Content -path '%SAVER_JS_FILE%'"
)


echo New scribboleth instance '%FILENAME%' created in '%TARGET_DIR%' on port %PORT%.
echo To start the node services, run: %SCRNODES_BAT%

cd "%TARGET_DIR%"
powershell -Command "Set-Content -Path 'package.json' -Value '{ \"dependencies\": { \"express\": \"^5.1.0\", \"body-parser\": \"^1.20.0\" } }' -Encoding ASCII"
call npm install
goto:eof

:usage
echo Usage: %0 ^<path\to\filename_without_extension^>
exit /b 1

:nonode
echo Node.js or Npm is not installed.
echo Please install Node.js from https://nodejs.org/
exit /b 1