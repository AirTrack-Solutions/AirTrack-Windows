@echo off
title AirTrack - Stopping...
echo.
echo  ================================================
echo   AirTrack Solutions - Stopping AirTrack
echo  ================================================
echo.
docker compose -f docker-compose.windows.yml down
echo.
echo  AirTrack has been stopped.
echo.
pause
