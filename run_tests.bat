@echo off
echo ============================================================
echo E-COMMERCE MVC CONTROLLER TEST RUNNER (Windows)
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)

echo.
echo Checking server status...
echo.

REM Check if backend is running
curl -s http://localhost:5000/cart/test >nul 2>&1
if errorlevel 1 (
    echo WARNING: Backend server is not running on http://localhost:5000
    echo Please start it manually with: cd ecommerce-backend ^&^& node server.js
    echo.
)

REM Check if frontend is running
curl -s http://localhost:3000 >nul 2>&1
if errorlevel 1 (
    echo WARNING: Frontend server is not running on http://localhost:3000
    echo Please start it manually with: cd ecommerce-app ^&^& npm start
    echo.
)

echo.
echo Starting MVC Controller Tests...
echo ============================================================
echo.

python mvc_controller_tests.py

if errorlevel 1 (
    echo.
    echo ❌ Tests failed. Check the output above for details.
    pause
    exit /b 1
) else (
    echo.
    echo 🎉 All tests completed successfully!
    pause
    exit /b 0
) 