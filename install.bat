@echo off
title AirTrack - First Time Setup
echo.
echo  ================================================
echo   AirTrack Solutions - First Time Setup
echo  ================================================
echo.
echo  This will build and start AirTrack for the first time.
echo  This may take several minutes. Please be patient.
echo.
pause
echo.
echo  Building AirTrack...
docker compose -f docker-compose.windows.yml up --build -d
if %errorlevel% neq 0 (
    echo.
    echo  ERROR: Setup failed.
    echo  Make sure Docker Desktop is running and try again.
    pause
    exit /b 1
)
echo.
echo  ================================================
echo   Setup complete! AirTrack is running.
echo   Open your browser and go to:
echo   http://localhost:5000
echo  ================================================
echo.
start http://localhost:5000
pause
