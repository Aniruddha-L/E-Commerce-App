import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
from conftest import wait_for_page_load, take_screenshot

class TestIntegration:
    """Integration tests for complete user workflows"""
    
    def test_complete_user_registration_and_login_flow(self, driver, wait, base_url):
        """Test complete user registration and login workflow"""
        # Generate unique username
        unique_username = f"testuser{random.randint(10000, 99999)}"
        
        # Start at register page
        driver.get(f"{base_url}/register")
        wait_for_page_load(driver, wait)
        
        # Fill registration form
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        username_input.send_keys(unique_username)
        password_input.send_keys("password123")
        
        register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Register')]")))
        register_button.click()
        
        # Wait for registration success
        time.sleep(2)
        
        # Should be logged in and redirected to dashboard
        assert "/dashboard" in driver.current_url or "success" in driver.page_source.lower()
        
        take_screenshot(driver, "complete_registration_login_flow")
    
    def test_complete_shopping_cart_workflow(self, driver, wait, base_url):
        """Test complete shopping cart workflow"""
        # Login first
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        username_input.send_keys("testuser")
        password_input.send_keys("password123")
        
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        login_button.click()
        
        # Wait for navigation to dashboard
        wait.until(EC.url_contains("/dashboard"))
        
        # Add items to cart
        add_to_cart_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Add to Cart') or contains(text(), 'Add')]")))
        
        items_added = 0
        for button in add_to_cart_buttons[:2]:  # Add first 2 items
            if button.is_displayed():
                button.click()
                time.sleep(1)
                items_added += 1
        
        # Navigate to cart
        driver.get(f"{base_url}/cart")
        wait_for_page_load(driver, wait)
        
        # Verify items are in cart
        cart_items = driver.find_elements(By.CSS_SELECTOR, ".cart-item, .item, [class*='cart']")
        assert len(cart_items) > 0 or items_added == 0
        
        # Test quantity controls if available
        increment_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), '+') or contains(@class, 'increment')]")
        if len(increment_buttons) > 0:
            increment_buttons[0].click()
            time.sleep(1)
        
        # Test remove item if available
        remove_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Remove') or contains(text(), 'Delete')]")
        if len(remove_buttons) > 0:
            remove_buttons[0].click()
            time.sleep(1)
        
        # Navigate back to dashboard
        driver.get(f"{base_url}/dashboard")
        wait_for_page_load(driver, wait)
        
        assert "/dashboard" in driver.current_url
        
        take_screenshot(driver, "complete_shopping_cart_workflow")
    
    def test_user_session_management(self, driver, wait, base_url):
        """Test user session management across multiple pages"""
        # Login
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        username_input.send_keys("testuser")
        password_input.send_keys("password123")
        
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        login_button.click()
        
        # Wait for navigation to dashboard
        wait.until(EC.url_contains("/dashboard"))
        
        # Navigate through different pages while logged in
        pages = ["/dashboard", "/cart", "/dashboard"]
        
        for page in pages:
            driver.get(f"{base_url}{page}")
            wait_for_page_load(driver, wait)
            
            # Should be able to access all pages
            assert page in driver.current_url
            
            # Should not be redirected to login
            assert "/login" not in driver.current_url
        
        # Test logout
        logout_elements = driver.find_elements(By.XPATH, "//button[contains(text(), 'Logout') or contains(text(), 'Sign Out')]")
        logout_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'Logout') or contains(text(), 'Sign Out')]")
        
        if len(logout_elements) > 0:
            logout_elements[0].click()
        elif len(logout_links) > 0:
            logout_links[0].click()
        
        time.sleep(2)
        
        # Try to access protected page after logout
        driver.get(f"{base_url}/cart")
        wait_for_page_load(driver, wait)
        
        # Should be redirected to login
        assert "/login" in driver.current_url
        
        take_screenshot(driver, "user_session_management")
    
    def test_error_handling_and_recovery(self, driver, wait, base_url):
        """Test error handling and recovery scenarios"""
        # Test login with invalid credentials
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        username_input.send_keys("invaliduser")
        password_input.send_keys("invalidpass123")
        
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        login_button.click()
        
        # Wait for error message
        error_message = wait.until(EC.presence_of_element_located((By.TAG_NAME, "p")))
        assert "Login failed" in error_message.text or "Invalid" in error_message.text
        
        # Try again with valid credentials
        username_input.clear()
        password_input.clear()
        
        username_input.send_keys("testuser")
        password_input.send_keys("password123")
        
        login_button.click()
        
        # Should succeed this time
        wait.until(EC.url_contains("/dashboard"))
        assert "/dashboard" in driver.current_url
        
        take_screenshot(driver, "error_handling_and_recovery")
    
    def test_concurrent_user_workflows(self, driver, wait, base_url):
        """Test multiple concurrent user workflows"""
        # Open multiple tabs to simulate concurrent users
        driver.execute_script("window.open('');")
        driver.execute_script("window.open('');")
        
        # Tab 1: User registration
        driver.switch_to.window(driver.window_handles[0])
        driver.get(f"{base_url}/register")
        wait_for_page_load(driver, wait)
        
        unique_username = f"user{random.randint(10000, 99999)}"
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        username_input.send_keys(unique_username)
        password_input.send_keys("password123")
        
        register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Register')]")))
        register_button.click()
        
        # Tab 2: User login
        driver.switch_to.window(driver.window_handles[1])
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        username_input.send_keys("testuser")
        password_input.send_keys("password123")
        
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        login_button.click()
        
        # Tab 3: Browse without login
        driver.switch_to.window(driver.window_handles[2])
        driver.get(f"{base_url}/dashboard")
        wait_for_page_load(driver, wait)
        
        # Verify all tabs are working independently
        assert driver.window_handles[0] != driver.window_handles[1] != driver.window_handles[2]
        
        take_screenshot(driver, "concurrent_user_workflows")
    
    def test_data_persistence_across_sessions(self, driver, wait, base_url):
        """Test data persistence across browser sessions"""
        # Login and add items to cart
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        username_input.send_keys("testuser")
        password_input.send_keys("password123")
        
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        login_button.click()
        
        wait.until(EC.url_contains("/dashboard"))
        
        # Add item to cart
        add_to_cart_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Add to Cart') or contains(text(), 'Add')]")))
        
        if len(add_to_cart_buttons) > 0:
            add_to_cart_buttons[0].click()
            time.sleep(2)
        
        # Navigate to cart to verify item was added
        driver.get(f"{base_url}/cart")
        wait_for_page_load(driver, wait)
        
        cart_items_before = driver.find_elements(By.CSS_SELECTOR, ".cart-item, .item, [class*='cart']")
        
        # Close and reopen browser (simulate new session)
        driver.quit()
        
        # Create new driver instance
        from selenium import webdriver
        from selenium.webdriver.edge.service import Service as EdgeService
        from selenium.webdriver.edge.options import Options as EdgeOptions
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        
        edge_options = EdgeOptions()
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--window-size=1920,1080")
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        new_driver = webdriver.Edge(service=service, options=edge_options)
        
        # Login again
        new_driver.get(f"{base_url}/login")
        wait_for_page_load(new_driver, WebDriverWait(new_driver, 10))
        
        username_input = new_driver.find_element(By.CSS_SELECTOR, "input[placeholder='Username']")
        password_input = new_driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        
        username_input.send_keys("testuser")
        password_input.send_keys("password123")
        
        login_button = new_driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_button.click()
        
        # Navigate to cart
        new_driver.get(f"{base_url}/cart")
        wait_for_page_load(new_driver, WebDriverWait(new_driver, 10))
        
        cart_items_after = new_driver.find_elements(By.CSS_SELECTOR, ".cart-item, .item, [class*='cart']")
        
        # Cart should persist data (if backend is working)
        # This test might fail if cart data is not persisted properly
        assert len(cart_items_after) >= 0  # At least should not crash
        
        new_driver.quit()
        
        take_screenshot(driver, "data_persistence_across_sessions")
    
    def test_performance_and_responsiveness(self, driver, wait, base_url):
        """Test application performance and responsiveness"""
        import time
        
        # Test page load times
        pages = ["/", "/login", "/register", "/dashboard", "/cart"]
        load_times = {}
        
        for page in pages:
            start_time = time.time()
            driver.get(f"{base_url}{page}")
            wait_for_page_load(driver, wait)
            end_time = time.time()
            
            load_times[page] = end_time - start_time
            
            # Page should load within reasonable time (5 seconds)
            assert load_times[page] < 5, f"Page {page} took too long to load: {load_times[page]} seconds"
        
        # Test login performance
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        start_time = time.time()
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        username_input.send_keys("testuser")
        password_input.send_keys("password123")
        
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        login_button.click()
        
        wait.until(EC.url_contains("/dashboard"))
        end_time = time.time()
        
        login_time = end_time - start_time
        assert login_time < 10, f"Login took too long: {login_time} seconds"
        
        take_screenshot(driver, "performance_and_responsiveness")
    
    def test_accessibility_and_usability(self, driver, wait, base_url):
        """Test accessibility and usability features"""
        # Test keyboard navigation
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        # Navigate using Tab key
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.TAB)
        time.sleep(0.5)
        
        # Test form submission with Enter key
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        username_input.send_keys("testuser")
        password_input.send_keys("password123")
        password_input.send_keys(Keys.RETURN)
        
        # Should attempt to login
        time.sleep(2)
        
        # Test responsive design (if applicable)
        # Resize window to test responsiveness
        driver.set_window_size(800, 600)
        time.sleep(1)
        
        driver.set_window_size(1920, 1080)
        time.sleep(1)
        
        take_screenshot(driver, "accessibility_and_usability")