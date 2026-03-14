@echo off
cd /d "%~dp0"
start http://localhost:5000
docker compose -f docker-compose.windows.yml up -d