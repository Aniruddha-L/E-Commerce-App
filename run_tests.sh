#!/bin/bash

echo "============================================================"
echo "E-COMMERCE MVC CONTROLLER TEST RUNNER (Unix/Linux/Mac)"
echo "============================================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7+ and try again"
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not available"
    echo "Please ensure pip is installed with Python"
    exit 1
fi

echo "Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Python dependencies"
    exit 1
fi

echo
echo "Checking server status..."
echo

# Check if backend is running
if curl -s http://localhost:5000/cart/test > /dev/null 2>&1; then
    echo "✓ Backend server is running on http://localhost:5000"
else
    echo "✗ Backend server is not running on http://localhost:5000"
    echo "Please start it manually with: cd ecommerce-backend && node server.js"
    echo
fi

# Check if frontend is running
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✓ Frontend server is running on http://localhost:3000"
else
    echo "✗ Frontend server is not running on http://localhost:3000"
    echo "Please start it manually with: cd ecommerce-app && npm start"
    echo
fi

echo
echo "Starting MVC Controller Tests..."
echo "============================================================"
echo

python3 mvc_controller_tests.py

if [ $? -eq 0 ]; then
    echo
    echo "🎉 All tests completed successfully!"
    exit 0
else
    echo
    echo "❌ Tests failed. Check the output above for details."
    exit 1
fi 