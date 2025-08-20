"""
Shared browser utilities to avoid code duplication
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import logging

def setup_chrome_driver(headless=False, timeout=30):
    """Setup Chrome WebDriver with appropriate options"""
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless")
        
    # Use a modern user agent
    ua = UserAgent()
    modern_user_agent = ua.random
    chrome_options.add_argument(f'--user-agent={modern_user_agent}')
    
    # Additional options to avoid detection and ensure compatibility
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Setup driver with fallback
    logger = logging.getLogger(__name__)
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logger.error(f"Failed to setup ChromeDriver with webdriver-manager: {str(e)}")
        # Try to use system chromedriver if webdriver-manager fails
        try:
            driver = webdriver.Chrome(options=chrome_options)
        except Exception as e2:
            logger.error(f"Failed to use system ChromeDriver: {str(e2)}")
            raise e
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    wait = WebDriverWait(driver, timeout)
    return driver, wait

def find_element_with_fallback(driver, wait, selectors, element_name="element", quick_timeout=3, clickable=False):
    """
    Try multiple selectors to find an element, returning the first one found
    
    Args:
        driver: Selenium WebDriver instance
        wait: WebDriverWait instance  
        selectors: List of tuples (By.X, "selector")
        element_name: Name for logging purposes
        quick_timeout: Timeout for each selector attempt
        clickable: If True, wait for element to be clickable instead of just present
        
    Returns:
        WebElement if found, None if not found
    """
    
    logger = logging.getLogger(__name__)
    
    # Use a shorter timeout for each selector attempt
    quick_wait = WebDriverWait(driver, quick_timeout)
    
    condition = EC.element_to_be_clickable if clickable else EC.presence_of_element_located
    
    for selector in selectors:
        try:
            element = quick_wait.until(condition(selector))
            logger.info(f"Found {element_name} using selector: {selector}")
            return element
        except Exception:
            continue
            
    logger.error(f"{element_name} not found with any selector")
    return None