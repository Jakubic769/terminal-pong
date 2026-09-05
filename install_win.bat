@echo off
REM Installs the "pong" command on Windows and adds it to PATH
REM automatically - no manual steps, no admin rights required.
setlocal

set "INSTALL_DIR=%USERPROFILE%\PyPong"
set "PS1=%TEMP%\pypong_addpath.ps1"

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

copy /Y "%~dp0pong.py" "%INSTALL_DIR%\pong.py" >nul

echo @echo off> "%INSTALL_DIR%\pong.bat"
echo python "%INSTALL_DIR%\pong.py" %%*>> "%INSTALL_DIR%\pong.bat"

echo Copied files to: %INSTALL_DIR%

REM --- build a small PowerShell helper that safely adds INSTALL_DIR to the
REM --- user PATH (no length limits, no duplicates), then run and delete it
echo $dir = '%INSTALL_DIR%' > "%PS1%"
echo $current = [Environment]::GetEnvironmentVariable('Path', 'User') >> "%PS1%"
echo if (-not $current) { $current = '' } >> "%PS1%"
echo $parts = $current -split ';' ^| Where-Object { $_ -ne '' } >> "%PS1%"
echo if ($parts -contains $dir) { >> "%PS1%"
echo     Write-Host 'Already in PATH.' >> "%PS1%"
echo } else { >> "%PS1%"
echo     if ($current -and $current.Substring($current.Length-1) -ne ';') { $newPath = $current + ';' + $dir } else { $newPath = $current + $dir } >> "%PS1%"
echo     [Environment]::SetEnvironmentVariable('Path', $newPath, 'User') >> "%PS1%"
echo     Write-Host ('Added ' + $dir + ' to your user PATH.') >> "%PS1%"
echo } >> "%PS1%"

powershell -NoProfile -ExecutionPolicy Bypass -File "%PS1%"
del "%PS1%"

echo.
echo Done! Close this window, open a NEW terminal (cmd or PowerShell),
echo and type: pong
echo (Windows only picks up PATH changes in newly opened terminals.)
pause