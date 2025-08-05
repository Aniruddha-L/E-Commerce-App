#!/usr/bin/env python3
"""
Main test runner for E-Commerce App Selenium Tests using EdgeDriver
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime
import platform

def run_tests(test_type="all", parallel=False, html_report=True, verbose=False):
    """
    Run the Selenium tests with specified options
    
    Args:
        test_type (str): Type of tests to run ('all', 'login', 'register', 'dashboard', 'cart', 'navigation', 'integration')
        parallel (bool): Run tests in parallel
        html_report (bool): Generate HTML report
        verbose (bool): Verbose output
    """
    
    # Create screenshots directory if it doesn't exist
    os.makedirs("screenshots", exist_ok=True)
    
    # Base pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add test files based on type
    if test_type == "all":
        test_files = [
            "test_login_page.py",
            "test_register_page.py", 
            "test_dashboard_page.py",
            "test_cart_page.py",
            "test_navigation.py",
            "test_integration.py"
        ]
    elif test_type == "login":
        test_files = ["test_login_page.py"]
    elif test_type == "register":
        test_files = ["test_register_page.py"]
    elif test_type == "dashboard":
        test_files = ["test_dashboard_page.py"]
    elif test_type == "cart":
        test_files = ["test_cart_page.py"]
    elif test_type == "navigation":
        test_files = ["test_navigation.py"]
    elif test_type == "integration":
        test_files = ["test_integration.py"]
    else:
        print(f"Unknown test type: {test_type}")
        return False
    
    cmd.extend(test_files)
    
    # Add options
    if parallel:
        cmd.extend(["-n", "auto"])  # Use all available CPU cores
    
    if html_report:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"test_report_{timestamp}.html"
        cmd.extend(["--html", report_file, "--self-contained-html"])
    
    if verbose:
        cmd.append("-v")
    
    # Add additional pytest options
    cmd.extend([
        "--tb=short",  # Short traceback format
        "--strict-markers",  # Strict marker checking
        "--disable-warnings",  # Disable warnings
        "-x",  # Stop on first failure
        "--maxfail=5"  # Stop after 5 failures
    ])
    
    print(f"Running tests: {test_type}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print("\n" + "=" * 50)
        print("✅ All tests completed successfully!")
        
        if html_report:
            print(f"📊 HTML report generated: {report_file}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 50)
        print("❌ Tests failed!")
        print(f"Exit code: {e.returncode}")
        return False

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("Checking prerequisites...")
    
    # Check if required packages are installed
    required_packages = [
        "selenium",
        "pytest", 
        "webdriver-manager",
        "pytest-html"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install them using: pip install -r test_requirements.txt")
        return False
    
    # Check if Edge WebDriver is available and works
    try:
        from selenium import webdriver
        from selenium.webdriver.edge.service import Service
        from selenium.webdriver.edge.options import Options
        
        local_driver_path = os.path.join(os.getcwd(), "msedgedriver.exe")  # Change if different OS or path
        
        edge_options = Options()
        edge_options.add_argument("--headless")
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")

        # Windows-specific options
        if platform.system() == "Windows":
            edge_options.add_argument("--disable-extensions")
            edge_options.add_argument("--disable-plugins")
            edge_options.add_argument("--disable-web-security")
            edge_options.add_argument("--allow-running-insecure-content")
        
        if os.path.exists(local_driver_path):
            print(f"Using local Edge driver at: {local_driver_path}")
            service = Service(local_driver_path)
        else:
            print("Local Edge driver not found. Attempting to download via webdriver_manager...")
            from webdriver_manager.microsoft import EdgeChromiumDriverManager
            service = Service(EdgeChromiumDriverManager().install())

        driver = webdriver.Edge(service=service, options=edge_options)
        driver.quit()
        print("✅ Edge WebDriver")
    except Exception as e:
        print(f"❌ Edge WebDriver: {e}")
        print("\nTroubleshooting steps:")
        print("1. Ensure Microsoft Edge is installed")
        print("2. Try updating Edge to the latest version")
        print("3. Close all Edge browser instances")
        print("4. If you have a local 'msedgedriver.exe', place it in this script's folder")
        print("5. Run: pip install --upgrade webdriver-manager")
        print("6. If behind proxy/firewall, ensure internet access for webdriver_manager")
        print("7. Run script as Administrator if on Windows")
        return False
    
    print("✅ All prerequisites met!")
    return True

def install_edge_driver():
    """Install Edge driver manually"""
    try:
        print("Installing Edge driver...")
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        driver_path = EdgeChromiumDriverManager().install()
        print(f"✅ Edge driver installed at: {driver_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to install Edge driver: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Run E-Commerce App Selenium Tests")
    parser.add_argument(
        "--type", 
        choices=["all", "login", "register", "dashboard", "cart", "navigation", "integration"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--parallel", 
        action="store_true",
        help="Run tests in parallel"
    )
    parser.add_argument(
        "--no-html", 
        action="store_true",
        help="Don't generate HTML report"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--check-prerequisites", 
        action="store_true",
        help="Check prerequisites only"
    )
    parser.add_argument(
        "--install-driver", 
        action="store_true",
        help="Install Edge driver manually"
    )
    
    args = parser.parse_args()
    
    if args.check_prerequisites:
        return check_prerequisites()
    
    if args.install_driver:
        return install_edge_driver()
    
    # Check prerequisites before running tests
    if not check_prerequisites():
        print("\n❌ Prerequisites not met.")
        print("\nTo fix Edge WebDriver issues on Windows:")
        print("1. Close all Edge browser windows")
        print("2. Run: pip install --upgrade webdriver-manager")
        print("3. Try running as administrator")
        print("4. Or run: python run_tests.py --install-driver")
        print("5. Or download 'msedgedriver.exe' manually and place it in this folder")
        return False
    
    # Run tests
    success = run_tests(
        test_type=args.type,
        parallel=args.parallel,
        html_report=not args.no_html,
        verbose=args.verbose
    )
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
