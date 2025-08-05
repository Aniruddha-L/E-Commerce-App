import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from conftest import wait_for_page_load, take_screenshot

class TestNavigation:
    """Test cases for navigation functionality across all pages"""
    
    def test_navbar_presence(self, driver, wait, base_url):
        """Test that navbar is present on all pages"""
        pages = ["/", "/login", "/register", "/dashboard", "/cart"]
        
        for page in pages:
            driver.get(f"{base_url}{page}")
            wait_for_page_load(driver, wait)
            
            # Check if navbar elements are present
            navbar_elements = driver.find_elements(By.CSS_SELECTOR, "nav, .navbar, [class*='nav']")
            assert len(navbar_elements) > 0 or "nav" in driver.page_source.lower()
            
            take_screenshot(driver, f"navbar_presence_{page.replace('/', '')}")
    
    def test_navigation_between_pages(self, driver, wait, base_url):
        """Test navigation between different pages"""
        # Test navigation from login to register
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        register_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Register')]")))
        register_button.click()
        
        wait.until(EC.url_contains("/register"))
        assert "/register" in driver.current_url
        
        # Test navigation from register to login
        driver.get(f"{base_url}/register")
        wait_for_page_load(driver, wait)
        
        # Navigate to login (might be through browser back or direct navigation)
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        assert "/login" in driver.current_url
        
        take_screenshot(driver, "navigation_between_pages")
    
    def test_dashboard_navigation_after_login(self, driver, wait, base_url):
        """Test navigation to dashboard after successful login"""
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        username_input.send_keys("testuser")
        password_input.send_keys("password123")
        
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        login_button.click()
        
        # Should be redirected to dashboard
        wait.until(EC.url_contains("/dashboard"))
        assert "/dashboard" in driver.current_url
        
        take_screenshot(driver, "dashboard_navigation_after_login")
    
    def test_cart_navigation_requires_login(self, driver, wait, base_url):
        """Test that cart navigation requires login"""
        # Try to access cart without login
        driver.get(f"{base_url}/cart")
        wait_for_page_load(driver, wait)
        
        # Should be redirected to login
        assert "/login" in driver.current_url
        
        # Login and then access cart
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        
        username_input.send_keys("testuser")
        password_input.send_keys("password123")
        
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        login_button.click()
        
        # Should be redirected to dashboard
        wait.until(EC.url_contains("/dashboard"))
        
        # Now try to access cart
        driver.get(f"{base_url}/cart")
        wait_for_page_load(driver, wait)
        
        # Should be able to access cart now
        assert "/cart" in driver.current_url
        
        take_screenshot(driver, "cart_navigation_requires_login")
    
    def test_navbar_links_functionality(self, driver, wait, base_url):
        """Test navbar links functionality"""
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
        
        # Test navbar links
        navbar_links = driver.find_elements(By.CSS_SELECTOR, "nav a, .navbar a, [class*='nav'] a")
        
        for link in navbar_links:
            if link.is_displayed():
                link_text = link.text.lower()
                link.click()
                time.sleep(1)
                
                # Check if navigation was successful
                if "dashboard" in link_text:
                    assert "/dashboard" in driver.current_url
                elif "cart" in link_text:
                    assert "/cart" in driver.current_url
                elif "login" in link_text:
                    assert "/login" in driver.current_url
                elif "register" in link_text:
                    assert "/register" in driver.current_url
        
        take_screenshot(driver, "navbar_links_functionality")
    
    def test_browser_back_forward_navigation(self, driver, wait, base_url):
        """Test browser back and forward navigation"""
        # Navigate to different pages
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        driver.get(f"{base_url}/register")
        wait_for_page_load(driver, wait)
        
        driver.get(f"{base_url}/dashboard")
        wait_for_page_load(driver, wait)
        
        # Test browser back
        driver.back()
        time.sleep(1)
        assert "/register" in driver.current_url
        
        # Test browser forward
        driver.forward()
        time.sleep(1)
        assert "/dashboard" in driver.current_url
        
        take_screenshot(driver, "browser_back_forward_navigation")
    
    def test_direct_url_access(self, driver, wait, base_url):
        """Test direct URL access to different pages"""
        pages = [
            ("/", "Dashboard"),
            ("/login", "Login"),
            ("/register", "Register"),
            ("/dashboard", "Dashboard"),
            ("/cart", "Cart")
        ]
        
        for url, expected_content in pages:
            driver.get(f"{base_url}{url}")
            wait_for_page_load(driver, wait)
            
            # Check if expected content is present
            assert expected_content in driver.page_source or expected_content.lower() in driver.page_source.lower()
            
            take_screenshot(driver, f"direct_url_access_{url.replace('/', '')}")
    
    def test_navigation_with_invalid_urls(self, driver, wait, base_url):
        """Test navigation with invalid URLs"""
        invalid_urls = ["/invalid", "/nonexistent", "/test123"]
        
        for url in invalid_urls:
            driver.get(f"{base_url}{url}")
            wait_for_page_load(driver, wait)
            
            # Should show 404 or redirect to a valid page
            # Check if we're on a valid page or show error
            valid_pages = ["/", "/login", "/register", "/dashboard", "/cart"]
            current_url = driver.current_url
            
            is_valid = any(page in current_url for page in valid_pages)
            assert is_valid or "404" in driver.page_source or "not found" in driver.page_source.lower()
            
            take_screenshot(driver, f"invalid_url_{url.replace('/', '')}")
    
    def test_navigation_after_logout(self, driver, wait, base_url):
        """Test navigation after logout"""
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
        
        # Find and click logout button
        logout_elements = driver.find_elements(By.XPATH, "//button[contains(text(), 'Logout') or contains(text(), 'Sign Out')]")
        logout_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'Logout') or contains(text(), 'Sign Out')]")
        
        if len(logout_elements) > 0:
            logout_elements[0].click()
        elif len(logout_links) > 0:
            logout_links[0].click()
        
        time.sleep(2)
        
        # Try to access protected pages after logout
        driver.get(f"{base_url}/cart")
        wait_for_page_load(driver, wait)
        
        # Should be redirected to login
        assert "/login" in driver.current_url
        
        take_screenshot(driver, "navigation_after_logout")
    
    def test_navigation_with_refresh(self, driver, wait, base_url):
        """Test navigation behavior with page refresh"""
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
        
        # Navigate to cart
        driver.get(f"{base_url}/cart")
        wait_for_page_load(driver, wait)
        
        # Refresh the page
        driver.refresh()
        wait_for_page_load(driver, wait)
        
        # Should still be on cart page
        assert "/cart" in driver.current_url
        
        take_screenshot(driver, "navigation_with_refresh")
    
    def test_navigation_with_new_tab(self, driver, wait, base_url):
        """Test navigation behavior with new tab"""
        # Open new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        
        # Navigate to login page in new tab
        driver.get(f"{base_url}/login")
        wait_for_page_load(driver, wait)
        
        # Should be on login page
        assert "/login" in driver.current_url
        
        # Switch back to original tab
        driver.switch_to.window(driver.window_handles[0])
        
        # Should still be on original page
        assert driver.current_url != f"{base_url}/login"
        
        take_screenshot(driver, "navigation_with_new_tab")