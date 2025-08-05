#!/usr/bin/env python3
"""
Chrome WebDriver Troubleshooting Script for Windows
"""

import os
import sys
import subprocess
import platform
import shutil
import requests
import zipfile
import tempfile

def check_chrome_installation():
    """Check if Chrome is installed"""
    print("🔍 Checking Chrome installation...")
    
    # Common Chrome installation paths on Windows
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv('USERNAME')),
    ]
    
    chrome_found = False
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ Chrome found at: {path}")
            chrome_found = True
            break
    
    if not chrome_found:
        print("❌ Chrome not found in common locations")
        print("Please install Google Chrome from: https://www.google.com/chrome/")
        return False
    
    return True

def check_chrome_processes():
    """Check if Chrome processes are running"""
    print("\n🔍 Checking for running Chrome processes...")
    
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq chrome.exe'], 
                              capture_output=True, text=True)
        if 'chrome.exe' in result.stdout:
            print("⚠️  Chrome processes are running")
            print("Please close all Chrome windows and try again")
            return False
        else:
            print("✅ No Chrome processes running")
            return True
    except Exception as e:
        print(f"⚠️  Could not check Chrome processes: {e}")
        return True

def upgrade_webdriver_manager():
    """Upgrade webdriver-manager"""
    print("\n🔄 Upgrading webdriver-manager...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "webdriver-manager"], 
                      check=True)
        print("✅ webdriver-manager upgraded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to upgrade webdriver-manager: {e}")
        return False

def get_chrome_version():
    """Get Chrome version"""
    try:
        result = subprocess.run([
            r"C:\Program Files\Google\Chrome\Application\chrome.exe", 
            "--version"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            version = result.stdout.strip().split()[-1]
            print(f"✅ Chrome version: {version}")
            return version
        else:
            print("⚠️  Could not get Chrome version")
            return None
    except Exception as e:
        print(f"⚠️  Could not get Chrome version: {e}")
        return None

def download_chrome_driver_manual():
    """Download Chrome driver manually"""
    print("\n📥 Downloading Chrome driver manually...")
    
    try:
        # Get Chrome version
        chrome_version = get_chrome_version()
        if not chrome_version:
            print("⚠️  Using default Chrome driver version")
            driver_version = "114.0.5735.90"  # Stable version
        else:
            # Extract major version
            major_version = chrome_version.split('.')[0]
            driver_version = f"{major_version}.0.5735.90"
        
        # Download URL
        download_url = f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_win32.zip"
        
        print(f"Downloading Chrome driver version: {driver_version}")
        
        # Download the file
        response = requests.get(download_url)
        if response.status_code != 200:
            print(f"❌ Failed to download Chrome driver: HTTP {response.status_code}")
            return False
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
            tmp_file.write(response.content)
            zip_path = tmp_file.name
        
        # Extract to current directory
        extract_dir = os.path.join(os.getcwd(), "chromedriver")
        os.makedirs(extract_dir, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Clean up
        os.unlink(zip_path)
        
        # Set PATH to include chromedriver
        chromedriver_path = os.path.join(extract_dir, "chromedriver.exe")
        if os.path.exists(chromedriver_path):
            print(f"✅ Chrome driver downloaded to: {chromedriver_path}")
            return chromedriver_path
        else:
            print("❌ Chrome driver not found in extracted files")
            return False
            
    except Exception as e:
        print(f"❌ Failed to download Chrome driver manually: {e}")
        return False

def test_chrome_driver_with_path(driver_path=None):
    """Test Chrome driver functionality with specific path"""
    print("\n🧪 Testing Chrome driver...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        
        if driver_path:
            service = Service(driver_path)
        else:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Test basic functionality
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        print(f"✅ Chrome driver test successful! Page title: {title}")
        return True
        
    except Exception as e:
        print(f"❌ Chrome driver test failed: {e}")
        return False

def install_chrome_driver():
    """Install Chrome driver with fallback options"""
    print("\n📥 Installing Chrome driver...")
    
    # Try webdriver-manager first
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        driver_path = ChromeDriverManager().install()
        print(f"✅ Chrome driver installed at: {driver_path}")
        
        # Test the installation
        if test_chrome_driver_with_path():
            return True
        else:
            print("⚠️  webdriver-manager installation failed, trying manual download...")
    except Exception as e:
        print(f"⚠️  webdriver-manager failed: {e}")
    
    # Try manual download as fallback
    driver_path = download_chrome_driver_manual()
    if driver_path:
        return test_chrome_driver_with_path(driver_path)
    
    return False

def main():
    """Main troubleshooting function"""
    print("🔧 Chrome WebDriver Troubleshooting Tool")
    print("=" * 50)
    
    if platform.system() != "Windows":
        print("⚠️  This script is designed for Windows systems")
        return False
    
    # Step 1: Check Chrome installation
    if not check_chrome_installation():
        return False
    
    # Step 2: Check for running Chrome processes
    if not check_chrome_processes():
        print("\n💡 Please close all Chrome windows and run this script again")
        return False
    
    # Step 3: Upgrade webdriver-manager
    if not upgrade_webdriver_manager():
        return False
    
    # Step 4: Install Chrome driver with fallback
    if not install_chrome_driver():
        print("\n❌ All Chrome driver installation methods failed")
        print("\nManual steps to try:")
        print("1. Download Chrome driver manually from: https://chromedriver.chromium.org/")
        print("2. Extract to a folder and add to PATH")
        print("3. Or try running tests with: python run_tests.py --type login --verbose")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Chrome WebDriver setup completed successfully!")
    print("You can now run your tests with: python run_tests.py")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 