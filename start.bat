@echo off
title PocketLaw Launcher
echo ===================================================
echo      Starting PocketLaw Legal Intelligence System
echo ===================================================

echo [1/2] Starting Backend Server (Flask on port 5001)...
start "PocketLaw Backend (Port 5001)" cmd /k "cd /d %~dp0backend && python app.py"

echo Waiting 3 seconds for backend to initialize...
ping -n 4 127.0.0.1 >nul

echo [2/2] Starting Frontend Development Server (React on port 3000)...
start "PocketLaw Frontend (Port 3000)" cmd /k "cd /d %~dp0frontend && npm start"

echo.
echo ===================================================
echo PocketLaw is running!
echo - Frontend Web App: http://localhost:3000
echo - Backend REST API: http://127.0.0.1:5001
echo ===================================================
