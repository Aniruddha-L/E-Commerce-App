import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from conftest import wait_for_page_load, take_screenshot

class TestLoginPage:
    """Test cases for the Login page"""
    
    def test_login_page_loads_correctly(self, driver, wait, base_url):
        """Test that login page loads with all expected elements"""
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        # Check if login page elements are present
        assert "Login" in driver.page_source
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Register')]")))
        
        assert username_input.is_displayed()
        assert password_input.is_displayed()
        assert login_button.is_displayed()
        assert register_button.is_displayed()
        
        take_screenshot(driver, "login_page_loaded")
    
    def test_login_form_validation_empty_password(self, driver, wait, base_url):
        """Test login form validation for empty password"""
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        # Fill username but leave password empty
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        username_input.send_keys("testuser")
        
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        login_button.click()
        
        # Wait for error message
        error_message = wait.until(EC.presence_of_element_located((By.TAG_NAME, "p")))
        assert "Password is empty" in error_message.text
        
        take_screenshot(driver, "login_empty_password_validation")
    
    def test_login_form_validation_short_password(self, driver, wait, base_url):
        """Test login form validation for short password"""
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        # Fill username and short password
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        username_input.send_keys("testuser")
        password_input.send_keys("123")
        
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        login_button.click()
        
        # Wait for error message
        error_message = wait.until(EC.presence_of_element_located((By.TAG_NAME, "p")))
        assert "Minimum password length should be 6" in error_message.text
        
        take_screenshot(driver, "login_short_password_validation")
    
    def test_show_password_toggle(self, driver, wait, base_url):
        """Test the show/hide password functionality"""
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        show_password_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Show Password')]")))
        
        # Initially password should be hidden
        assert password_input.get_attribute("type") == "password"
        
        # Click show password button
        show_password_button.click()
        time.sleep(0.5)
        
        # Password should now be visible
        assert password_input.get_attribute("type") == "text"
        
        # Click again to hide password
        show_password_button.click()
        time.sleep(0.5)
        
        # Password should be hidden again
        assert password_input.get_attribute("type") == "password"
        
        take_screenshot(driver, "login_show_password_toggle")
    
    def test_navigate_to_register_page(self, driver, wait, base_url):
        """Test navigation from login to register page"""
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Register')]")))
        register_button.click()
        
        # Wait for navigation to register page
        wait.until(EC.url_contains("/register"))
        assert "/register" in driver.current_url
        
        # Verify register page elements are present
        assert "Register" in driver.page_source
        
        take_screenshot(driver, "login_to_register_navigation")
    
    def test_successful_login_flow(self, driver, wait, base_url):
        """Test successful login with valid credentials"""
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        # Fill login form with valid credentials
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        username_input.send_keys("Aniruddha")
        password_input.send_keys("123456")
        
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        login_button.click()
        
        # Wait for navigation to dashboard
        wait.until(EC.url_contains("/dashboard"))
        assert "/dashboard" in driver.current_url
        
        # Verify dashboard elements are present
        assert "Dashboard" in driver.page_source or "Products" in driver.page_source
        
        take_screenshot(driver, "login_successful")
    
    def test_failed_login_invalid_credentials(self, driver, wait, base_url):
        """Test login with invalid credentials"""
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        # Fill login form with invalid credentials
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        username_input.send_keys("invaliduser")
        password_input.send_keys("invalidpass123")
        
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        login_button.click()
        
        # Wait for error message
        error_message = wait.until(EC.presence_of_element_located((By.TAG_NAME, "p")))
        assert "Login failed" in error_message.text or "Invalid credentials" in error_message.text
        
        # Should still be on login page
        assert "/login" in driver.current_url
        
        take_screenshot(driver, "login_failed_invalid_credentials")
    
    def test_input_field_functionality(self, driver, wait, base_url):
        """Test input field functionality and clearing"""
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        # Test typing in username field
        username_input.send_keys("testuser")
        assert username_input.get_attribute("value") == "testuser"
        
        # Test typing in password field
        password_input.send_keys("password123")
        assert password_input.get_attribute("value") == "password123"
        
        # Test clearing fields
        username_input.clear()
        password_input.clear()
        assert username_input.get_attribute("value") == ""
        assert password_input.get_attribute("value") == ""
        
        take_screenshot(driver, "login_input_field_functionality") 