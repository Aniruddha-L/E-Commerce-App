# E-Commerce App Selenium Test Suite

This directory contains a comprehensive automated testing suite for the E-Commerce application using Python Selenium WebDriver.

## 📋 Overview

The test suite covers all major pages and functionalities of the e-commerce application:

- **Login Page Tests** - User authentication, form validation, error handling
- **Register Page Tests** - User registration, validation, success/failure scenarios
- **Dashboard Page Tests** - Product display, add to cart, quantity controls
- **Cart Page Tests** - Shopping cart functionality, item management
- **Navigation Tests** - Cross-page navigation, routing, session management
- **Integration Tests** - Complete user workflows, performance, accessibility

## 🚀 Quick Start

### Prerequisites

1. **Python 3.7+** installed
2. **Chrome Browser** installed
3. **E-Commerce App** running on `http://localhost:3000`
4. **Backend Server** running on `http://localhost:5000`

### Installation

1. Install required packages:
```bash
pip install -r test_requirements.txt
```

2. Check prerequisites:
```bash
python run_tests.py --check-prerequisites
```

### Running Tests

#### Run All Tests
```bash
python run_tests.py
```

#### Run Specific Test Types
```bash
# Login tests only
python run_tests.py --type login

# Register tests only
python run_tests.py --type register

# Dashboard tests only
python run_tests.py --type dashboard

# Cart tests only
python run_tests.py --type cart

# Navigation tests only
python run_tests.py --type navigation

# Integration tests only
python run_tests.py --type integration
```

#### Advanced Options
```bash
# Run tests in parallel (faster execution)
python run_tests.py --parallel

# Verbose output
python run_tests.py --verbose

# Skip HTML report generation
python run_tests.py --no-html

# Combine options
python run_tests.py --type login --verbose --parallel
```

## 📁 Test Structure

```
├── conftest.py              # Pytest configuration and fixtures
├── test_login_page.py       # Login page tests
├── test_register_page.py    # Register page tests
├── test_dashboard_page.py   # Dashboard page tests
├── test_cart_page.py        # Cart page tests
├── test_navigation.py       # Navigation tests
├── test_integration.py      # Integration tests
├── run_tests.py            # Main test runner
├── test_requirements.txt   # Python dependencies
└── screenshots/            # Test screenshots (auto-generated)
```

## 🧪 Test Categories

### 1. Login Page Tests (`test_login_page.py`)
- ✅ Page loads correctly
- ✅ Form validation (empty password, short password)
- ✅ Show/hide password toggle
- ✅ Navigation to register page
- ✅ Successful login flow
- ✅ Failed login with invalid credentials
- ✅ Input field functionality

### 2. Register Page Tests (`test_register_page.py`)
- ✅ Page loads correctly
- ✅ Form validation (empty password, short password)
- ✅ Successful registration flow
- ✅ Failed registration with existing username
- ✅ Input field functionality
- ✅ Password field type verification
- ✅ Form submission with Enter key
- ✅ Navigation to login page

### 3. Dashboard Page Tests (`test_dashboard_page.py`)
- ✅ Page loads correctly (with/without login)
- ✅ Product display and functionality
- ✅ Add to cart functionality
- ✅ Quantity increment/decrement controls
- ✅ Product description toggle
- ✅ Navigation to cart
- ✅ Product search/filter (if available)
- ✅ Logout functionality

### 4. Cart Page Tests (`test_cart_page.py`)
- ✅ Access control (redirects to login when not logged in)
- ✅ Page loads correctly when logged in
- ✅ Empty cart display
- ✅ Add items to cart and verify
- ✅ Quantity increment/decrement
- ✅ Remove items from cart
- ✅ Clear cart functionality
- ✅ Cart total calculation
- ✅ Checkout functionality
- ✅ Navigation back to dashboard

### 5. Navigation Tests (`test_navigation.py`)
- ✅ Navbar presence on all pages
- ✅ Navigation between pages
- ✅ Dashboard navigation after login
- ✅ Cart navigation requires login
- ✅ Navbar links functionality
- ✅ Browser back/forward navigation
- ✅ Direct URL access
- ✅ Invalid URL handling
- ✅ Navigation after logout
- ✅ Page refresh behavior
- ✅ New tab navigation

### 6. Integration Tests (`test_integration.py`)
- ✅ Complete user registration and login flow
- ✅ Complete shopping cart workflow
- ✅ User session management
- ✅ Error handling and recovery
- ✅ Concurrent user workflows
- ✅ Data persistence across sessions
- ✅ Performance and responsiveness
- ✅ Accessibility and usability

## 📊 Test Reports

The test suite generates comprehensive HTML reports with:
- Test results summary
- Pass/fail statistics
- Screenshots of test failures
- Detailed error messages
- Execution time information

Reports are saved as `test_report_YYYYMMDD_HHMMSS.html`

## 🖼️ Screenshots

Test screenshots are automatically captured and saved in the `screenshots/` directory:
- Page load verification
- Form interactions
- Error states
- Success confirmations
- Navigation steps

## ⚙️ Configuration

### Base URL
The default base URL is `http://localhost:3000`. To change this, modify the `base_url` fixture in `conftest.py`.

### WebDriver Options
Chrome WebDriver is configured with optimized options in `conftest.py`:
- Headless mode support
- Window size: 1920x1080
- Disabled automation detection
- Performance optimizations

### Test Credentials
Default test credentials:
- Username: `testuser`
- Password: `password123`

## 🔧 Troubleshooting

### Common Issues

1. **Chrome WebDriver not found (Windows)**
   ```bash
   # Run the troubleshooting script
   python fix_chrome_driver.py
   
   # Or manually install/upgrade
   pip install --upgrade webdriver-manager
   python run_tests.py --install-driver
   ```

2. **"WinError 193] %1 is not a valid Win32 application"**
   - Close all Chrome browser windows
   - Run as administrator
   - Update Chrome to latest version
   - Run: `python fix_chrome_driver.py`

3. **Tests fail with "element not found"**
   - Ensure the e-commerce app is running on `http://localhost:3000`
   - Check that the backend server is running on `http://localhost:5000`
   - Verify the test user exists in the backend

4. **Tests timeout**
   - Increase wait time in `conftest.py`
   - Check network connectivity
   - Verify app performance

5. **Screenshots not generated**
   - Ensure write permissions in the current directory
   - Check available disk space

### Debug Mode

Run tests with verbose output for debugging:
```bash
python run_tests.py --verbose
```

### Manual Testing

For manual verification, you can run individual test methods:
```bash
python -m pytest test_login_page.py::TestLoginPage::test_login_page_loads_correctly -v
```

## 📈 Performance

- **Sequential execution**: ~5-10 minutes for all tests
- **Parallel execution**: ~2-3 minutes for all tests
- **Individual test files**: 30 seconds to 2 minutes each

## 🔒 Security Notes

- Test credentials are hardcoded for automation
- Tests run against local development environment
- No sensitive data is exposed in test reports
- Screenshots may contain test data

## 🤝 Contributing

When adding new tests:

1. Follow the existing naming conventions
2. Add appropriate docstrings
3. Include screenshots for visual verification
4. Test both positive and negative scenarios
5. Update this README with new test descriptions

## 📝 License

This test suite is part of the E-Commerce App project and follows the same license terms.

---

**Happy Testing! 🚀** 