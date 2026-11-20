@echo off
title PocketLaw Offline Launcher
echo ========================================================
echo           Starting PocketLaw 100%% Offline Mode
echo ========================================================
echo.
echo [1/2] Starting Python Flask & RAG Backend (Port 5001)...
start "PocketLaw Backend" cmd /k "cd /d "%~dp0backend" && python app.py"

echo [2/2] Starting React Frontend UI (Port 3000)...
start "PocketLaw Frontend" cmd /k "cd /d "%~dp0frontend" && npm start"

echo.
echo Both servers are launching!
echo Backend:  http://127.0.0.1:5001
echo Frontend: http://localhost:3000
echo.
echo (Keep both command windows open while using PocketLaw)
echo ========================================================
