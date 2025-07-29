#!/usr/bin/env python3
"""
Simple test runner for E-Commerce MVC Controller Tests
"""

import subprocess
import sys
import os
import time
import requests

def check_server(url, name):
    """Check if a server is running"""
    try:
        response = requests.get(url, timeout=5)
        print(f"✓ {name} is running on {url}")
        return True
    except requests.exceptions.RequestException:
        print(f"✗ {name} is not running on {url}")
        return False

def start_server(command, name):
    """Start a server in the background"""
    try:
        print(f"Starting {name}...")
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(3)  # Give server time to start
        return process
    except Exception as e:
        print(f"Failed to start {name}: {e}")
        return None

def main():
    """Main function to run the tests"""
    print("=" * 60)
    print("E-COMMERCE MVC CONTROLLER TEST RUNNER")
    print("=" * 60)
    
    # Check if servers are running
    frontend_running = check_server("http://localhost:3000", "React Frontend")
    backend_running = check_server("http://localhost:5000/cart/test", "Backend API")
    
    # Start servers if not running
    frontend_process = None
    backend_process = None
    
    if not backend_running:
        print("\nStarting Backend Server...")
        backend_process = start_server(
            "cd ecommerce-backend && node server.js",
            "Backend API"
        )
        if backend_process:
            time.sleep(5)  # Wait for server to fully start
    
    if not frontend_running:
        print("\nStarting Frontend Server...")
        frontend_process = start_server(
            "cd ecommerce-app && npm start",
            "React Frontend"
        )
        if frontend_process:
            time.sleep(10)  # Wait for React to compile and start
    
    # Final check
    print("\nFinal server status check...")
    frontend_ok = check_server("http://localhost:3000", "React Frontend")
    backend_ok = check_server("http://localhost:5000/cart/test", "Backend API")
    
    if not (frontend_ok and backend_ok):
        print("\n❌ Cannot proceed with tests. Please ensure both servers are running.")
        print("\nManual startup commands:")
        print("1. Backend: cd ecommerce-backend && node server.js")
        print("2. Frontend: cd ecommerce-app && npm start")
        return 1
    
    # Run the tests
    print("\n" + "=" * 60)
    print("RUNNING MVC CONTROLLER TESTS")
    print("=" * 60)
    
    try:
        # Run the main test file
        result = subprocess.run([sys.executable, "mvc_controller_tests.py"], 
                              capture_output=False, text=True)
        
        if result.returncode == 0:
            print("\n🎉 All tests completed successfully!")
            return 0
        else:
            print("\n❌ Tests failed. Check the output above for details.")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        return 1
    finally:
        # Cleanup background processes
        if frontend_process:
            print("\nStopping Frontend Server...")
            frontend_process.terminate()
        
        if backend_process:
            print("Stopping Backend Server...")
            backend_process.terminate()

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 