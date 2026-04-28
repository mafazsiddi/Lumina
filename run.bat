@echo off
echo =========================================
echo       Plant Scanner Application Setup
echo =========================================
echo.

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting Backend API Server (FastAPI)...
start "Plant Scanner API" cmd /k "cd backend && uvicorn app:app --host 127.0.0.1 --port 8000"

echo.
echo Starting Frontend UI Server...
start "Plant Scanner UI" cmd /k "cd frontend && python -m http.server 8080"

echo.
echo =========================================
echo All services started!
echo.
echo The backend API is running at: http://127.0.0.1:8000
echo The frontend UI is running at: http://127.0.0.1:8080
echo.
echo Please open http://127.0.0.1:8080 in your web browser.
echo You may need to grant camera permissions in the browser to scan plants.
echo =========================================
pause
