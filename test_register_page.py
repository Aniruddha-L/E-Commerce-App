import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from conftest import wait_for_page_load, take_screenshot

class TestRegisterPage:
    """Test cases for the Register page"""
    
    def test_register_page_loads_correctly(self, driver, wait, base_url):
        """Test that register page loads with all expected elements"""
        driver.get(f"{base_url}/register")
        wait_for_page_load(driver, wait)
        
        assert "Register" in driver.page_source
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Register')]")))
        
        assert username_input.is_displayed()
        assert password_input.is_displayed()
        assert register_button.is_displayed()
        
        take_screenshot(driver, "register_page_loaded")
    
    def test_register_form_validation_empty_password(self, driver, wait, base_url):
        """Test register form validation for empty password"""
        driver.get(f"{base_url}/register")
        wait_for_page_load(driver, wait)
        
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        username_input.send_keys("newuser")
        
        register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Register')]")))
        register_button.click()
        
        error_message = wait.until(EC.presence_of_element_located((By.TAG_NAME, "p")))
        assert "Password is empty" in error_message.text
        
        take_screenshot(driver, "register_empty_password_validation")
    
    def test_register_form_validation_short_password(self, driver, wait, base_url):
        """Test register form validation for short password"""
        driver.get(f"{base_url}/register")
        wait_for_page_load(driver, wait)
        
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        username_input.send_keys("newuser")
        password_input.send_keys("123")
        
        register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Register')]")))
        register_button.click()
        
        error_message = wait.until(EC.presence_of_element_located((By.TAG_NAME, "p")))
        assert "Minimum length of the password should be 6" in error_message.text
        
        take_screenshot(driver, "register_short_password_validation")
    
    def test_successful_registration_flow(self, driver, wait, base_url):
        """Test successful registration with valid credentials"""
        driver.get(f"{base_url}/register")
        wait_for_page_load(driver, wait)
        
        import random
        unique_username = f"testuser{random.randint(1000, 9999)}"
        
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        username_input.send_keys(unique_username)
        password_input.send_keys("password123")
        
        register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Register')]")))
        register_button.click()
        
        success_message = wait.until(EC.presence_of_element_located((By.TAG_NAME, "p")))
        assert "success" in success_message.text.lower() or "registered" in success_message.text.lower()
        
        take_screenshot(driver, "register_successful")
    
    def test_failed_registration_existing_username(self, driver, wait, base_url):
        """Test registration with existing username"""
        driver.get(f"{base_url}/register")
        wait_for_page_load(driver, wait)
        
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        username_input.send_keys("testuser")  # Existing username
        password_input.send_keys("password123")
        
        register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Register')]")))
        register_button.click()
        
        error_message = wait.until(EC.presence_of_element_located((By.TAG_NAME, "p")))
        assert "Registration failed" in error_message.text or "already exists" in error_message.text.lower()
        
        assert "/register" in driver.current_url
        
        take_screenshot(driver, "register_failed_existing_username")
    
    def test_input_field_functionality(self, driver, wait, base_url):
        """Test input field functionality and clearing"""
        driver.get(f"{base_url}/register")
        wait_for_page_load(driver, wait)
        
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        username_input.send_keys("newuser")
        assert username_input.get_attribute("value") == "newuser"
        
        password_input.send_keys("password123")
        assert password_input.get_attribute("value") == "password123"
        
        username_input.clear()
        password_input.clear()
        assert username_input.get_attribute("value") == ""
        assert password_input.get_attribute("value") == ""
        
        take_screenshot(driver, "register_input_field_functionality")
    
    def test_password_field_type(self, driver, wait, base_url):
        """Test that password field is properly configured as password type"""
        driver.get(f"{base_url}/register")
        wait_for_page_load(driver, wait)
        
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        assert password_input.get_attribute("type") == "password"
        
        password_input.send_keys("testpassword")
        assert password_input.get_attribute("value") == "testpassword"
        
        take_screenshot(driver, "register_password_field_type")
    
    def test_form_submission_with_enter_key(self, driver, wait, base_url):
        """Test form submission using Enter key"""
        driver.get(f"{base_url}/register")
        wait_for_page_load(driver, wait)
        
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        username_input.send_keys("testuser")
        password_input.send_keys("password123")
        
        # Send Enter key on username input (instead of password input)
        username_input.send_keys(Keys.RETURN)
        
        # Wait for the message <p> element with non-empty text
        message = wait.until(lambda d: d.find_element(By.TAG_NAME, "p"))
        wait.until(lambda d: message.text.strip() != "")
        
        print(f"Message text: '{message.text}'")
        assert message.text.strip() != ""
        
        take_screenshot(driver, "register_form_submission_enter_key")
    
    def test_navigation_from_register_to_login(self, driver, wait, base_url):
        """Test navigation from register page to login page"""
        driver.get(f"{base_url}/register")
        wait_for_page_load(driver, wait)
        
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        assert "Login" in driver.page_source
        assert "/login" in driver.current_url
        
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        assert username_input.is_displayed()
        assert password_input.is_displayed()
        
        take_screenshot(driver, "register_to_login_navigation")
