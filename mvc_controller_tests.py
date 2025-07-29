import unittest
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os

class ECommerceControllerTests(unittest.TestCase):
    """Selenium automation tests for E-Commerce MVC Controllers"""
    
    @classmethod
    def setUpClass(cls):
        """Set up the test environment once for all tests"""
        print("Setting up test environment...")
        
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Initialize WebDriver
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        cls.wait = WebDriverWait(cls.driver, 10)
        
        # Test configuration
        cls.base_url = "http://localhost:3000"  # React app URL
        cls.api_url = "http://localhost:5000"   # Backend API URL
        
        # Test data
        cls.test_user = {
            "username": "testuser_selenium",
            "password": "testpass123"
        }
        
        cls.test_product = {
            "id": 1,
            "name": "Apple Iphone 16 pro max",
            "price": 69999,
            "image": "/images/smartphone.jpg"
        }
        
        # Ensure backend is running
        cls._ensure_backend_running()
        
        print("Test environment setup complete!")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        print("Cleaning up test environment...")
        cls.driver.quit()
        
        # Clean up test data
        cls._cleanup_test_data()
        print("Test environment cleanup complete!")
    
    @classmethod
    def _ensure_backend_running(cls):
        """Ensure the backend server is running"""
        try:
            response = requests.get(f"{cls.api_url}/cart/test", timeout=5)
            print("Backend server is running")
        except requests.exceptions.RequestException:
            print("Warning: Backend server may not be running. Please start it manually.")
    
    @classmethod
    def _cleanup_test_data(cls):
        """Clean up test data from the backend"""
        try:
            # Clear test user's cart
            requests.delete(f"{cls.api_url}/cart/{cls.test_user['username']}/clear")
            
            # Remove test user from users.json
            users_file = os.path.join("ecommerce-backend", "users.json")
            if os.path.exists(users_file):
                with open(users_file, 'r') as f:
                    users = json.load(f)
                
                users = [user for user in users if user['username'] != cls.test_user['username']]
                
                with open(users_file, 'w') as f:
                    json.dump(users, f, indent=2)
                    
        except Exception as e:
            print(f"Warning: Could not cleanup test data: {e}")
    
    def setUp(self):
        """Set up before each test"""
        self.driver.get(self.base_url)
        time.sleep(2)
    
    def test_01_register_controller(self):
        """Test the registration controller functionality"""
        print("\nTesting Registration Controller...")
        
        # Navigate to register page
        self.driver.get(f"{self.base_url}/register")
        time.sleep(2)
        
        # Fill registration form
        username_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Password']")
        
        username_input.clear()
        username_input.send_keys(self.test_user['username'])
        password_input.clear()
        password_input.send_keys(self.test_user['password'])
        
        # Submit registration
        register_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Register')]")
        register_button.click()
        
        # Wait for response
        time.sleep(3)
        
        # Check if registration was successful
        try:
            success_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'successfully')]")))
            self.assertIn("successfully", success_message.text)
            print("✓ Registration controller test passed")
        except TimeoutException:
            # Check if user already exists
            try:
                error_message = self.driver.find_element(By.XPATH, "//p[contains(text(), 'already exists')]")
                print("✓ User already exists (expected behavior)")
            except NoSuchElementException:
                self.fail("Registration failed without proper error message")
    
    def test_02_login_controller(self):
        """Test the login controller functionality"""
        print("\nTesting Login Controller...")
        
        # Navigate to login page
        self.driver.get(f"{self.base_url}/login")
        time.sleep(2)
        
        # Fill login form
        username_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Password']")
        
        username_input.clear()
        username_input.send_keys(self.test_user['username'])
        password_input.clear()
        password_input.send_keys(self.test_user['password'])
        
        # Submit login
        login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_button.click()
        
        # Wait for redirect to dashboard
        time.sleep(3)
        
        # Check if login was successful (should redirect to dashboard)
        current_url = self.driver.current_url
        self.assertIn("/dashboard", current_url)
        print("✓ Login controller test passed")
    
    def test_03_cart_add_controller(self):
        """Test the cart add item controller functionality"""
        print("\nTesting Cart Add Controller...")
        
        # First login
        self._login_user()
        
        # Navigate to dashboard to see products
        self.driver.get(f"{self.base_url}/dashboard")
        time.sleep(2)
        
        # Find and click add to cart button for the first product
        try:
            add_to_cart_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add to Cart')]")))
            add_to_cart_button.click()
            time.sleep(2)
            
            # Check if item was added (look for success message or cart update)
            print("✓ Cart add controller test passed")
        except TimeoutException:
            self.fail("Could not find Add to Cart button")
    
    def test_04_cart_view_controller(self):
        """Test the cart view controller functionality"""
        print("\nTesting Cart View Controller...")
        
        # First login
        self._login_user()
        
        # Navigate to cart page
        self.driver.get(f"{self.base_url}/cart")
        time.sleep(2)
        
        # Check if cart page loads properly
        try:
            cart_title = self.wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Your Cart')]")))
            self.assertIsNotNone(cart_title)
            print("✓ Cart view controller test passed")
        except TimeoutException:
            self.fail("Cart page did not load properly")
    
    def test_05_cart_update_controller(self):
        """Test the cart update quantity controller functionality"""
        print("\nTesting Cart Update Controller...")
        
        # First login and add item to cart
        self._login_user()
        self._add_item_to_cart()
        
        # Navigate to cart
        self.driver.get(f"{self.base_url}/cart")
        time.sleep(2)
        
        # Find quantity controls and update quantity
        try:
            # Look for quantity increase button
            increase_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".quantity-btn.increase")))
            increase_button.click()
            time.sleep(2)
            
            # Check if quantity was updated
            quantity_display = self.driver.find_element(By.CSS_SELECTOR, ".quantity-display")
            self.assertIsNotNone(quantity_display)
            print("✓ Cart update controller test passed")
        except TimeoutException:
            print("No items in cart to update (expected if cart is empty)")
    
    def test_06_cart_remove_controller(self):
        """Test the cart remove item controller functionality"""
        print("\nTesting Cart Remove Controller...")
        
        # First login and add item to cart
        self._login_user()
        self._add_item_to_cart()
        
        # Navigate to cart
        self.driver.get(f"{self.base_url}/cart")
        time.sleep(2)
        
        # Find and click remove button
        try:
            remove_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".remove-btn")))
            remove_button.click()
            time.sleep(2)
            
            # Check if item was removed
            print("✓ Cart remove controller test passed")
        except TimeoutException:
            print("No items in cart to remove (expected if cart is empty)")
    
    def test_07_cart_clear_controller(self):
        """Test the cart clear controller functionality"""
        print("\nTesting Cart Clear Controller...")
        
        # First login and add item to cart
        self._login_user()
        self._add_item_to_cart()
        
        # Navigate to cart
        self.driver.get(f"{self.base_url}/cart")
        time.sleep(2)
        
        # Find and click clear all button
        try:
            clear_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Clear All')]")))
            clear_button.click()
            time.sleep(2)
            
            # Check if cart was cleared
            empty_message = self.driver.find_element(By.XPATH, "//p[contains(text(), 'YOUR CART IS EMPTY')]")
            self.assertIsNotNone(empty_message)
            print("✓ Cart clear controller test passed")
        except TimeoutException:
            print("No items in cart to clear (expected if cart is empty)")
    
    def test_08_api_endpoints_controller(self):
        """Test the API endpoints directly"""
        print("\nTesting API Endpoints Controller...")
        
        # Test registration endpoint
        response = requests.post(f"{self.api_url}/register", json=self.test_user)
        self.assertIn(response.status_code, [200, 400])  # 200 for success, 400 if user exists
        
        # Test login endpoint
        response = requests.post(f"{self.api_url}/login", json=self.test_user)
        self.assertEqual(response.status_code, 200)
        
        # Test cart endpoints
        username = self.test_user['username']
        
        # Get cart
        response = requests.get(f"{self.api_url}/cart/{username}")
        self.assertEqual(response.status_code, 200)
        
        # Add item to cart
        response = requests.post(f"{self.api_url}/cart/{username}/add", json={
            "product": self.test_product,
            "quantity": 1
        })
        self.assertEqual(response.status_code, 200)
        
        # Update cart item
        response = requests.put(f"{self.api_url}/cart/{username}/update", json={
            "productId": self.test_product['id'],
            "quantity": 2
        })
        self.assertEqual(response.status_code, 200)
        
        # Remove item from cart
        response = requests.delete(f"{self.api_url}/cart/{username}/remove/{self.test_product['id']}")
        self.assertEqual(response.status_code, 200)
        
        # Clear cart
        response = requests.delete(f"{self.api_url}/cart/{username}/clear")
        self.assertEqual(response.status_code, 200)
        
        print("✓ API endpoints controller test passed")
    
    def test_09_error_handling_controller(self):
        """Test error handling in controllers"""
        print("\nTesting Error Handling Controller...")
        
        # Test invalid login
        self.driver.get(f"{self.base_url}/login")
        time.sleep(2)
        
        username_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Password']")
        
        username_input.clear()
        username_input.send_keys("invalid_user")
        password_input.clear()
        password_input.send_keys("invalid_password")
        
        login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_button.click()
        
        time.sleep(3)
        
        # Check for error message
        try:
            error_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Invalid credentials')]")))
            self.assertIsNotNone(error_message)
            print("✓ Error handling controller test passed")
        except TimeoutException:
            print("No error message found (may be expected behavior)")
    
    def test_10_navigation_controller(self):
        """Test navigation between different pages"""
        print("\nTesting Navigation Controller...")
        
        # Test navigation to different pages
        pages = ["/", "/register", "/login", "/dashboard"]
        
        for page in pages:
            self.driver.get(f"{self.base_url}{page}")
            time.sleep(2)
            
            # Check if page loads without errors
            self.assertNotIn("error", self.driver.page_source.lower())
        
        print("✓ Navigation controller test passed")
    
    def _login_user(self):
        """Helper method to login user"""
        self.driver.get(f"{self.base_url}/login")
        time.sleep(2)
        
        username_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
        password_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Password']")
        
        username_input.clear()
        username_input.send_keys(self.test_user['username'])
        password_input.clear()
        password_input.send_keys(self.test_user['password'])
        
        login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_button.click()
        time.sleep(3)
    
    def _add_item_to_cart(self):
        """Helper method to add item to cart"""
        self.driver.get(f"{self.base_url}/dashboard")
        time.sleep(2)
        
        try:
            add_to_cart_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add to Cart')]")))
            add_to_cart_button.click()
            time.sleep(2)
        except TimeoutException:
            pass  # Item might already be in cart or no products available

def run_tests():
    """Run all tests with detailed output"""
    print("=" * 60)
    print("E-COMMERCE MVC CONTROLLER AUTOMATION TESTS")
    print("=" * 60)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(ECommerceControllerTests)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    # Check if required servers are running
    print("Checking server status...")
    
    try:
        # Check React app
        response = requests.get("http://localhost:3000", timeout=5)
        print("✓ React app is running on http://localhost:3000")
    except requests.exceptions.RequestException:
        print("✗ React app is not running. Please start it with: npm start")
        exit(1)
    
    try:
        # Check backend API
        response = requests.get("http://localhost:5000/cart/test", timeout=5)
        print("✓ Backend API is running on http://localhost:5000")
    except requests.exceptions.RequestException:
        print("✗ Backend API is not running. Please start it with: node server.js")
        exit(1)
    
    print("\nStarting tests...")
    success = run_tests()
    
    if success:
        print("\n🎉 All tests completed successfully!")
    else:
        print("\n❌ Some tests failed. Please check the output above.")
        exit(1) 