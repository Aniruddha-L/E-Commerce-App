import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import platform

@pytest.fixture(scope="function")
def driver():
    """Setup Edge WebDriver with optimized options for Windows compatibility"""
    edge_options = EdgeOptions()
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--window-size=1920,1080")
    edge_options.add_argument("--disable-blink-features=AutomationControlled")
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option('useAutomationExtension', False)
    
    # Windows-specific options
    if platform.system() == "Windows":
        edge_options.add_argument("--disable-extensions")
        edge_options.add_argument("--disable-plugins")
        edge_options.add_argument("--disable-images")  # Faster loading
        edge_options.add_argument("--disable-javascript")  # For basic tests
        edge_options.add_argument("--disable-web-security")
        edge_options.add_argument("--allow-running-insecure-content")
        edge_options.add_argument("--disable-features=VizDisplayCompositor")
    
    try:
        # Try to find edgedriver in common locations
        edgedriver_paths = [
            "msedgedriver.exe",
            "msedgedriver",
            os.path.join(os.getcwd(), "msedgedriver", "msedgedriver.exe"),
            os.path.join(os.getcwd(), "msedgedriver.exe")
        ]
        
        driver_path = None
        for path in edgedriver_paths:
            if os.path.exists(path):
                driver_path = path
                print(f"Using Edge driver at: {driver_path}")
                break
        
        if driver_path:
            service = EdgeService(driver_path)
            driver = webdriver.Edge(service=service, options=edge_options)
        else:
            # Try webdriver-manager as fallback
            try:
                service = EdgeService(EdgeChromiumDriverManager().install())
                driver = webdriver.Edge(service=service, options=edge_options)
            except Exception as e:
                print(f"Warning: EdgeChromiumDriverManager failed: {e}")
                # Final fallback to system Edge driver
                driver = webdriver.Edge(options=edge_options)
                
    except Exception as e:
        print(f"Error: Could not initialize Edge WebDriver: {e}")
        print("Please ensure Edge browser is installed and accessible")
        print("Try running: python simple_test.py")
        raise e
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    yield driver
    
    try:
        driver.quit()
    except:
        pass

@pytest.fixture(scope="function")
def wait(driver):
    """WebDriverWait fixture with 10 second timeout"""
    return WebDriverWait(driver, 10)

@pytest.fixture(scope="function")
def base_url():
    """Base URL for the e-commerce application"""
    return "http://localhost:3000"

def wait_for_page_load(driver, wait):
    """Wait for page to be fully loaded"""
    try:
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        time.sleep(4)  # Additional small delay for React to render
    except:
        # Fallback if readyState check fails
        time.sleep(2)

def take_screenshot(driver, name):
    """Take a screenshot and save it"""
    try:
        # Create screenshots directory if it doesn't exist
        os.makedirs("screenshots", exist_ok=True)
        
        # Clean filename for Windows compatibility
        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        
        screenshot_path = f"screenshots/{safe_name}.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")
    except Exception as e:
        print(f"Warning: Could not take screenshot: {e}")

def check_edge_availability():
    """Check if Edge is available and accessible"""
    try:
        edge_options = EdgeOptions()
        edge_options.add_argument("--headless")
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=edge_options)
        driver.quit()
        return True
    except Exception as e:
        print(f"Edge WebDriver check failed: {e}")
        return False
