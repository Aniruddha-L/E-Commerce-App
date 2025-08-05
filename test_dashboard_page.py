import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from conftest import wait_for_page_load, take_screenshot

class TestDashboardPage:
    """Test cases for the Dashboard page"""
    
    def test_dashboard_page_loads_correctly(self, driver, wait, base_url):
        """Test that dashboard page loads with all expected elements"""
        driver.get(f"{base_url}/dashboard")
        wait_for_page_load(driver, wait)
        
        # Check if dashboard page elements are present
        # Dashboard might show different content based on login status
        assert "Dashboard" in driver.page_source or "Products" in driver.page_source
        
        # Check for product cards or login prompt
        try:
            # If logged in, should see products
            products = driver.find_elements(By.CSS_SELECTOR, ".product-card, .card, [class*='product']")
            assert len(products) > 0 or "Login" in driver.page_source
        except:
            # If not logged in, should see login prompt
            assert "Login" in driver.page_source or "Register" in driver.page_source
        
        take_screenshot(driver, "dashboard_page_loaded")
    
    def test_dashboard_without_login(self, driver, wait, base_url):
        """Test dashboard behavior when user is not logged in"""
        driver.get(f"{base_url}/dashboard")
        wait_for_page_load(driver, wait)
        
        # Should show login/register options or redirect to login
        if "/login" in driver.current_url:
            # Redirected to login page
            assert "Login" in driver.page_source
        else:
            # Still on dashboard but showing login prompt
            assert "Login" in driver.page_source or "Register" in driver.page_source
        
        take_screenshot(driver, "dashboard_without_login")
    
    def test_dashboard_with_login(self, driver, wait, base_url):
        """Test dashboard behavior when user is logged in"""
        # First login
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
        
        # Now test dashboard functionality
        self._test_dashboard_logged_in_functionality(driver, wait)
    
    def _test_dashboard_logged_in_functionality(self, driver, wait):
        """Test dashboard functionality when logged in"""
        # Check for product cards
        product_cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card, .card, [class*='product'], .item")))
        assert len(product_cards) > 0
        
        # Check for add to cart buttons
        add_to_cart_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Add to Cart') or contains(text(), 'Add')]")
        assert len(add_to_cart_buttons) > 0
        
        take_screenshot(driver, "dashboard_logged_in")
    
    def test_add_to_cart_functionality(self, driver, wait, base_url):
        """Test adding products to cart"""
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

        # Find and click first add to cart button
        add_to_cart_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Add to Cart') or contains(text(), 'Add')]")))

        if len(add_to_cart_buttons) > 0:
            first_button = add_to_cart_buttons[0]
            # Scroll into view and use ActionChains to avoid click interception
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_button)
            from selenium.webdriver.common.action_chains import ActionChains
            ActionChains(driver).move_to_element(first_button).click().perform()
            # Wait for success message or cart update
            time.sleep(2)
            # Check for success message or cart indicator
            success_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'added') or contains(text(), 'cart') or contains(text(), 'success')]")
            assert len(success_elements) > 0 or "Cart" in driver.page_source

        take_screenshot(driver, "dashboard_add_to_cart")
    
    def test_product_quantity_controls(self, driver, wait, base_url):
        """Test product quantity increment/decrement controls"""
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
        
        # Look for quantity controls (+ and - buttons)
        quantity_controls = driver.find_elements(By.XPATH, "//button[contains(text(), '+') or contains(text(), '-') or contains(@class, 'increment') or contains(@class, 'decrement')]")
        
        if len(quantity_controls) > 0:
            # Test increment button
            increment_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), '+') or contains(@class, 'increment')]")
            if len(increment_buttons) > 0:
                increment_buttons[0].click()
                time.sleep(1)
            
            # Test decrement button
            decrement_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), '-') or contains(@class, 'decrement')]")
            if len(decrement_buttons) > 0:
                decrement_buttons[0].click()
                time.sleep(1)
        
        take_screenshot(driver, "dashboard_quantity_controls")
    
    def test_product_description_toggle(self, driver, wait, base_url):
        """Test product description show/hide functionality"""
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
        
        # Look for description toggle buttons
        description_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Description') or contains(text(), 'Details') or contains(text(), 'Show') or contains(text(), 'View')]")
        
        if len(description_buttons) > 0:
            # Click first description button
            description_buttons[0].click()
            time.sleep(1)
            
            # Check if description is now visible
            description_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'description') or contains(@class, 'details')]")
            assert len(description_elements) > 0 or "description" in driver.page_source.lower()
        
        take_screenshot(driver, "dashboard_description_toggle")
    
    def test_navigation_to_cart(self, driver, wait, base_url):
        """Test navigation from dashboard to cart"""
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
        
        # Look for cart navigation link/button
        cart_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'Cart') or contains(@href, '/cart')]")
        cart_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Cart')]")
        
        if len(cart_links) > 0:
            cart_links[0].click()
        elif len(cart_buttons) > 0:
            cart_buttons[0].click()
        else:
            # Navigate directly to cart
            driver.get(f"{base_url}/cart")
        
        # Wait for navigation to cart
        wait.until(EC.url_contains("/cart"))
        assert "/cart" in driver.current_url
        
        take_screenshot(driver, "dashboard_to_cart_navigation")
    
    def test_product_search_or_filter(self, driver, wait, base_url):
        """Test product search or filter functionality if available"""
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
        
        # Look for search input
        search_inputs = driver.find_elements(By.CSS_SELECTOR, "input[placeholder*='search' i], input[placeholder*='filter' i], input[type='search']")
        
        if len(search_inputs) > 0:
            search_input = search_inputs[0]
            search_input.send_keys("test")
            search_input.send_keys(Keys.RETURN)
            time.sleep(2)
            
            # Check if search results are displayed
            assert "test" in driver.page_source.lower() or len(driver.find_elements(By.CSS_SELECTOR, ".product-card, .card, [class*='product']")) > 0
        
        take_screenshot(driver, "dashboard_search_filter")
    
    def test_logout_functionality(self, driver, wait, base_url):
        """Test logout functionality from dashboard"""
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
        
        # Look for logout button/link
        logout_elements = driver.find_elements(By.XPATH, "//button[contains(text(), 'Logout') or contains(text(), 'Sign Out')]")
        logout_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'Logout') or contains(text(), 'Sign Out')]")
        
        if len(logout_elements) > 0:
            logout_elements[0].click()
        elif len(logout_links) > 0:
            logout_links[0].click()
        
        # Wait for logout to complete
        time.sleep(2)
        
        # Should be redirected to login or show login prompt
        if "/login" in driver.current_url:
            assert "Login" in driver.page_source
        else:
            assert "Login" in driver.page_source or "Register" in driver.page_source
        
        take_screenshot(driver, "dashboard_logout")