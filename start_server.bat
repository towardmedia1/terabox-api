@echo off
echo ========================================
echo Starting TeraBox API Server
echo ========================================
echo.

echo Checking Python...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
pip install -q fastapi uvicorn httpx pydantic

echo.
echo ========================================
echo Starting server on http://localhost:8000
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn api_server:app --reload --port 8000 --host 0.0.0.0

pause
