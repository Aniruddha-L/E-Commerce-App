#!/usr/bin/env python3
"""
Simple test script to verify basic Selenium functionality
"""

import os
import sys
import subprocess
import platform

def test_basic_selenium():
    """Test basic Selenium functionality without webdriver-manager"""
    print("🧪 Testing basic Selenium functionality...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        
        # Basic Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        
        # Try to find chromedriver in PATH or current directory
        chromedriver_paths = [
            "chromedriver.exe",
            "chromedriver",
            os.path.join(os.getcwd(), "chromedriver", "chromedriver.exe"),
            os.path.join(os.getcwd(), "chromedriver.exe")
        ]
        
        driver_path = None
        for path in chromedriver_paths:
            if os.path.exists(path):
                driver_path = path
                print(f"✅ Found Chrome driver at: {driver_path}")
                break
        
        if driver_path:
            service = Service(driver_path)
        else:
            print("⚠️  Chrome driver not found, trying system default...")
            service = Service()
        
        # Create driver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Test basic functionality
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        print(f"✅ Basic Selenium test successful! Page title: {title}")
        return True
        
    except Exception as e:
        print(f"❌ Basic Selenium test failed: {e}")
        return False

def download_chrome_driver_simple():
    """Download Chrome driver using a simple approach"""
    print("\n📥 Downloading Chrome driver (simple method)...")
    
    try:
        import requests
        import zipfile
        
        # Use a stable Chrome driver version
        driver_version = "114.0.5735.90"
        download_url = f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_win32.zip"
        
        print(f"Downloading Chrome driver version: {driver_version}")
        
        # Download
        response = requests.get(download_url)
        if response.status_code != 200:
            print(f"❌ Download failed: HTTP {response.status_code}")
            return False
        
        # Save and extract
        with open("chromedriver.zip", "wb") as f:
            f.write(response.content)
        
        with zipfile.ZipFile("chromedriver.zip", "r") as zip_ref:
            zip_ref.extractall(".")
        
        # Clean up
        os.remove("chromedriver.zip")
        
        if os.path.exists("chromedriver.exe"):
            print("✅ Chrome driver downloaded successfully")
            return True
        else:
            print("❌ Chrome driver not found after extraction")
            return False
            
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Simple Selenium Test")
    print("=" * 30)
    
    # Test basic Selenium first
    if test_basic_selenium():
        print("\n🎉 Selenium is working! You can run your tests.")
        return True
    
    # If basic test fails, try downloading Chrome driver
    print("\n⚠️  Basic test failed, trying to download Chrome driver...")
    
    if download_chrome_driver_simple():
        if test_basic_selenium():
            print("\n🎉 Chrome driver downloaded and working!")
            return True
    
    print("\n❌ Could not get Selenium working")
    print("\nManual steps:")
    print("1. Download Chrome driver from: https://chromedriver.chromium.org/")
    print("2. Extract chromedriver.exe to this directory")
    print("3. Run this script again")
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 