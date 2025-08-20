"""Login functionality for Recreation.gov"""
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from browser_utils import find_element_with_fallback

class LoginHandler:
    def __init__(self, driver, wait, config):
        self.driver = driver
        self.wait = wait
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def login(self):
        """Login to Recreation.gov"""
        try:
            self.logger.info("Attempting to login to Recreation.gov...")
            
            # Go to recreation.gov and click login link
            self.driver.get("https://www.recreation.gov")
            time.sleep(3)
            
            # Click the login link
            login_link = self.wait.until(
                EC.element_to_be_clickable((By.ID, "ga-global-nav-log-in-link"))
            )
            login_link.click()
            time.sleep(5)
            
            # Find and fill username
            username_selectors = [
                (By.ID, "email"),
                (By.NAME, "email"), 
                (By.CSS_SELECTOR, "input[type='email']"),
                (By.XPATH, "//input[contains(@placeholder, 'email')]")
            ]
            username_field = find_element_with_fallback(
                self.driver, self.wait, username_selectors, "username field", 
                quick_timeout=10, clickable=True
            )
            if not username_field:
                return False
                
            # Use JavaScript to fill username
            try:
                username_field.clear()
                username_field.send_keys(self.config.USERNAME)
            except:
                # Fallback to JavaScript
                self.driver.execute_script(f"arguments[0].value = '{self.config.USERNAME}';", username_field)
            time.sleep(1)
            
            # Find and fill password
            password_selectors = [
                (By.CSS_SELECTOR, "input[type='password']"),
                (By.ID, "rec-acct-sign-in-password"),
                (By.XPATH, "//input[@type='password']")
            ]
            password_field = find_element_with_fallback(
                self.driver, self.wait, password_selectors, "password field", 
                quick_timeout=10, clickable=True
            )
            if not password_field:
                return False
                
            # Use JavaScript to fill password
            try:
                password_field.clear()
                password_field.send_keys(self.config.PASSWORD)
            except:
                # Fallback to JavaScript
                self.driver.execute_script(f"arguments[0].value = '{self.config.PASSWORD}';", password_field)
            time.sleep(1)
            
            # Click login button
            login_selectors = [
                (By.CSS_SELECTOR, "button.rec-acct-sign-in-btn"),
                (By.CSS_SELECTOR, "button[data-component='Button'][type='submit']"),
                (By.XPATH, "//button[contains(@class, 'rec-acct-sign-in-btn')]"),
                (By.XPATH, "//button[contains(text(), 'Log In')]"),
                (By.XPATH, "//button[@type='submit']")
            ]
            
            login_button = find_element_with_fallback(
                self.driver, self.wait, login_selectors, "login button", 
                quick_timeout=5, clickable=True
            )
            if not login_button:
                return False
                
            # Try multiple click methods
            try:
                login_button.click()
            except:
                try:
                    # Fallback to JavaScript click
                    self.driver.execute_script("arguments[0].click();", login_button)
                except Exception as e:
                    self.logger.error(f"Failed to click login button: {str(e)}")
                    return False
            time.sleep(5)
            
            # Check if login was successful
            if "signin" not in self.driver.current_url:
                self.logger.info("Login successful!")
                return True
            else:
                self.logger.error("Login failed!")
                return False
                
        except Exception as e:
            self.logger.error(f"Login error: {str(e)}")
            return False