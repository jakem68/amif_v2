@echo off
echo -----------------------------------------------------------------
echo Giving Docker desktop time to startup before starting containers.
echo -----------------------------------------------------------------

timeout /t 90 /nobreak

rem "C:\Program Files\PHP\v7.3\php-win.exe" "C:\Users\demonstrator-share\4.0_made_real\php_scanner_event.php"
rem "C:\Program Files\PHP\v7.3\php-win.exe" "C:\Users\demonstrator-share\4.0_made_real\php_scanner_mqtt.php"
rem "C:\Program Files\PHP\v7.3\php-win.exe" "C:\Users\demonstrator-share\4.0_made_real\php_scanner_statemonitor.php"

start PowerShell -Command "Set-ExecutionPolicy Unrestricted" >> "%TEMP%\StartupLog.txt" 2>&1
start PowerShell "C:\Users\demonstratoradmin\Desktop\docker_containers_start.ps1" >> "%TEMP%\StartupLog.txt" 2>&1