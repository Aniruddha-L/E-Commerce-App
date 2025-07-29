# E-Commerce MVC Controller Automation Tests

This project contains comprehensive Selenium automation tests for the E-Commerce application's MVC (Model-View-Controller) architecture.

## MVC Architecture Analysis

### Model Layer
- **Data Models**: 
  - `ecommerce-app/src/data/products.json` - Product catalog data
  - `ecommerce-backend/users.json` - User authentication data
  - `ecommerce-backend/carts.json` - Shopping cart data

### View Layer
- **React Components**:
  - `ecommerce-app/src/pages/` - Page components (Login, Register, Dashboard, Cart)
  - `ecommerce-app/src/components/` - Reusable UI components (Navbar, Toast)
  - `ecommerce-app/src/App.js` - Main application router

### Controller Layer
- **Express.js Routes** (`ecommerce-backend/server.js`):
  - **Authentication Controllers**:
    - `POST /register` - User registration
    - `POST /login` - User authentication
  - **Cart Controllers**:
    - `GET /cart/:username` - Retrieve user's cart
    - `POST /cart/:username/add` - Add item to cart
    - `PUT /cart/:username/update` - Update item quantity
    - `DELETE /cart/:username/remove/:productId` - Remove item from cart
    - `DELETE /cart/:username/clear` - Clear entire cart

## Test Coverage

The automation test suite covers all major controller functionalities:

### 1. Authentication Controller Tests
- ✅ User registration
- ✅ User login
- ✅ Error handling for invalid credentials
- ✅ Duplicate user registration handling

### 2. Cart Controller Tests
- ✅ Add items to cart
- ✅ View cart contents
- ✅ Update item quantities
- ✅ Remove items from cart
- ✅ Clear entire cart
- ✅ Cart persistence across sessions

### 3. API Endpoint Tests
- ✅ Direct API testing for all endpoints
- ✅ HTTP status code validation
- ✅ Request/response validation

### 4. UI Integration Tests
- ✅ Navigation between pages
- ✅ Form submissions
- ✅ Error message display
- ✅ User interface responsiveness

## Prerequisites

Before running the tests, ensure you have:

1. **Python 3.7+** installed
2. **Node.js** and **npm** installed
3. **Chrome browser** installed (for Selenium WebDriver)

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the backend server**:
   ```bash
   cd ecommerce-backend
   npm install
   node server.js
   ```

3. **Start the React frontend** (in a new terminal):
   ```bash
   cd ecommerce-app
   npm install
   npm start
   ```

## Running the Tests

### Run All Tests
```bash
python mvc_controller_tests.py
```

### Run Specific Test Categories
```bash
# Run only authentication tests
python -m pytest mvc_controller_tests.py::ECommerceControllerTests::test_01_register_controller -v
python -m pytest mvc_controller_tests.py::ECommerceControllerTests::test_02_login_controller -v

# Run only cart tests
python -m pytest mvc_controller_tests.py::ECommerceControllerTests::test_03_cart_add_controller -v
python -m pytest mvc_controller_tests.py::ECommerceControllerTests::test_04_cart_view_controller -v
python -m pytest mvc_controller_tests.py::ECommerceControllerTests::test_05_cart_update_controller -v
python -m pytest mvc_controller_tests.py::ECommerceControllerTests::test_06_cart_remove_controller -v
python -m pytest mvc_controller_tests.py::ECommerceControllerTests::test_07_cart_clear_controller -v

# Run API endpoint tests
python -m pytest mvc_controller_tests.py::ECommerceControllerTests::test_08_api_endpoints_controller -v
```

## Test Structure

### Test Classes
- `ECommerceControllerTests` - Main test class containing all controller tests

### Test Methods
1. `test_01_register_controller` - Tests user registration functionality
2. `test_02_login_controller` - Tests user login functionality
3. `test_03_cart_add_controller` - Tests adding items to cart
4. `test_04_cart_view_controller` - Tests viewing cart contents
5. `test_05_cart_update_controller` - Tests updating item quantities
6. `test_06_cart_remove_controller` - Tests removing items from cart
7. `test_07_cart_clear_controller` - Tests clearing entire cart
8. `test_08_api_endpoints_controller` - Tests API endpoints directly
9. `test_09_error_handling_controller` - Tests error handling
10. `test_10_navigation_controller` - Tests page navigation

### Helper Methods
- `_login_user()` - Helper to login test user
- `_add_item_to_cart()` - Helper to add items to cart
- `_cleanup_test_data()` - Cleanup test data after tests

## Test Configuration

### URLs
- **Frontend**: `http://localhost:3000` (React app)
- **Backend**: `http://localhost:5000` (Express API)

### Test Data
- **Test User**: `testuser_selenium` / `testpass123`
- **Test Product**: Apple iPhone 16 Pro Max (ID: 1)

### Browser Configuration
- **Browser**: Chrome (headless mode)
- **Window Size**: 1920x1080
- **Timeout**: 10 seconds for element waits

## Expected Test Results

When all tests pass, you should see output similar to:

```
============================================================
E-COMMERCE MVC CONTROLLER AUTOMATION TESTS
============================================================
Setting up test environment...
Backend server is running
Test environment setup complete!

Testing Registration Controller...
✓ Registration controller test passed

Testing Login Controller...
✓ Login controller test passed

Testing Cart Add Controller...
✓ Cart add controller test passed

...

============================================================
TEST SUMMARY
============================================================
Tests run: 10
Failures: 0
Errors: 0
Success rate: 100.0%

🎉 All tests completed successfully!
```

## Troubleshooting

### Common Issues

1. **Chrome WebDriver Issues**:
   - Ensure Chrome browser is installed
   - The test automatically downloads the correct ChromeDriver version

2. **Server Connection Issues**:
   - Ensure both frontend and backend servers are running
   - Check ports 3000 and 5000 are not blocked

3. **Test Failures**:
   - Check server logs for errors
   - Ensure test data is not corrupted
   - Verify network connectivity

### Debug Mode

To run tests in debug mode (non-headless), modify the Chrome options in the test file:

```python
# Remove or comment out this line:
# chrome_options.add_argument("--headless")
```

## Continuous Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
name: MVC Controller Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: python mvc_controller_tests.py
```

## Contributing

When adding new tests:

1. Follow the existing naming convention: `test_XX_description_controller`
2. Add appropriate error handling and cleanup
3. Update this README with new test descriptions
4. Ensure tests are independent and can run in any order

## License

This test suite is part of the E-Commerce application project. 