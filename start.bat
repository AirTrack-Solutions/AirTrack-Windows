@echo off
title AirTrack - Starting...
echo.
echo  ================================================
echo   AirTrack Solutions - Starting AirTrack
echo  ================================================
echo.
echo  Please wait while AirTrack starts up...
echo  This may take a minute on first run.
echo.
docker compose -f docker-compose.windows.yml up -d
if %errorlevel% neq 0 (
    echo.
    echo  ERROR: AirTrack failed to start.
    echo  Make sure Docker Desktop is running and try again.
    pause
    exit /b 1
)
echo.
echo  ================================================
echo   AirTrack is running!
echo   Open your browser and go to:
echo   http://localhost:5000
echo  ================================================
echo.
start http://localhost:5000
pause
