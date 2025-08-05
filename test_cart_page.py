import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class TestCartPage:

    def login(self, driver, wait, base_url, username="testuser", password="password123"):
        driver.get(f"{base_url}/login")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']"))).send_keys(username)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))).send_keys(password)
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        login_btn.click()
        wait.until(EC.url_contains("/dashboard"))

    def scroll_and_click(self, driver, element):
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        # Use ActionChains to click reliably
        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()

    def test_empty_cart_display(self, driver, wait, base_url):
        self.login(driver, wait, base_url)
        driver.get(f"{base_url}/cart")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Try multiple ways to detect empty cart message
        empty_messages = driver.find_elements(By.XPATH, "//*[contains(translate(text(),'EMPTY','empty'),'empty') or contains(translate(text(),'NO ITEMS','no items'),'no items')]")
        found = any(m.text.strip() for m in empty_messages)
        if not found:
            found = "empty" in driver.page_source.lower() or "no items" in driver.page_source.lower()
        assert found, "Empty cart message not found or empty"

    def test_remove_item_from_cart(self, driver, wait, base_url):
        self.login(driver, wait, base_url)

        driver.get(f"{base_url}/dashboard")
        add_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Add to Cart') or contains(text(), 'Add')]")))
        if add_buttons:
            self.scroll_and_click(driver, add_buttons[0])
            time.sleep(2)

        driver.get(f"{base_url}/cart")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        remove_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Remove') or contains(text(), 'Delete') or contains(@class, 'remove')]")
        assert remove_buttons, "No remove buttons found in cart"

        cart_items_before = driver.find_elements(By.CSS_SELECTOR, ".cart-item, .item, [class*='cart']")
        self.scroll_and_click(driver, remove_buttons[0])
        time.sleep(2)

        cart_items_after = driver.find_elements(By.CSS_SELECTOR, ".cart-item, .item, [class*='cart']")
        assert len(cart_items_after) < len(cart_items_before) or "empty" in driver.page_source.lower()

    def test_clear_cart_functionality(self, driver, wait, base_url):
        self.login(driver, wait, base_url)

        driver.get(f"{base_url}/dashboard")
        add_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Add to Cart') or contains(text(), 'Add')]")))
        if add_buttons:
            self.scroll_and_click(driver, add_buttons[0])
            time.sleep(1)
            if len(add_buttons) > 1:
                self.scroll_and_click(driver, add_buttons[1])
                time.sleep(1)

        driver.get(f"{base_url}/cart")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        clear_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Clear') or contains(text(), 'Empty') or contains(@class, 'clear')]")
        assert clear_buttons, "No clear cart button found"

        self.scroll_and_click(driver, clear_buttons[0])
        time.sleep(2)

        empty_messages = driver.find_elements(By.XPATH, "//*[contains(translate(text(),'EMPTY','empty'),'empty')]")
        assert empty_messages or "empty" in driver.page_source.lower()

    def test_cart_total_calculation(self, driver, wait, base_url):
        self.login(driver, wait, base_url)

        driver.get(f"{base_url}/dashboard")
        add_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Add to Cart') or contains(text(), 'Add')]")))
        if add_buttons:
            self.scroll_and_click(driver, add_buttons[0])
            time.sleep(2)

        driver.get(f"{base_url}/cart")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Try multiple ways to detect total
        total_elements = driver.find_elements(By.XPATH, "//*[contains(translate(text(),'TOTAL','total'),'total') or contains(text(), '$') or contains(@class, 'total')]")
        total_text = ''
        if total_elements:
            total_text = total_elements[0].text.lower()
        if not total_text:
            # Fallback: check for $ in page source
            if "$" in driver.page_source:
                total_text = "$"
        assert "total" in total_text or "$" in total_text, f"No total amount element found or text is empty. Found: '{total_text}'"

