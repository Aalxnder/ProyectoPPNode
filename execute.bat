@echo off
setlocal enabledelayedexpansion

echo [1/4] Iniciando servidor SIN locks...
for /f %%p in ('powershell -NoProfile -Command "Start-Process node -ArgumentList 'server.js','-locks','0' -PassThru | Select-Object -ExpandProperty Id"') do set SERVER_PID=%%p
timeout /t 2 /nobreak >nul

echo [2/4] Ejecutando ataque (SIN locks)...
python raceConditionNode.py

echo Deteniendo servidor SIN locks...
if defined SERVER_PID (
    taskkill /PID %SERVER_PID% /F /T >nul 2>nul
)
timeout /t 1 /nobreak >nul

echo [3/4] Iniciando servidor CON locks...
for /f %%p in ('powershell -NoProfile -Command "Start-Process node -ArgumentList 'server.js','-locks','1' -PassThru | Select-Object -ExpandProperty Id"') do set SERVER_PID=%%p
timeout /t 2 /nobreak >nul

echo [4/4] Ejecutando ataque (CON locks)...
python raceConditionNode.py

echo Deteniendo servidor CON locks...
if defined SERVER_PID (
    taskkill /PID %SERVER_PID% /F /T >nul 2>nul
)

echo Listo.
endlocal
