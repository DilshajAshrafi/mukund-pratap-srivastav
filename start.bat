@echo off
title Mukund Portfolio Server (Port 5001)
echo ========================================================
echo   Launching Mukund Full-Stack Portfolio Server
echo   Port: 5001
echo   URL:  http://localhost:5001
echo ========================================================
echo.
cd /d "%~dp0"
python app.py
pause
