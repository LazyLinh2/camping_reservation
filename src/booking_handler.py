"""Booking functionality for campsite reservations"""
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from browser_utils import find_element_with_fallback

class BookingHandler:
    def __init__(self, driver, wait, config):
        self.driver = driver
        self.wait = wait
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def navigate_to_campground(self):
        """Navigate to the campground page"""
        try:
            self.logger.info(f"Navigating to {self.config.CAMPGROUND_NAME}...")
            self.driver.get(self.config.CAMPGROUND_URL)
            time.sleep(3)
            
            campgroundNameHeader = f"//h1[contains(text(), {self.config.CAMPGROUND_NAME})]"
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, campgroundNameHeader))
            )
            
            self.logger.info("Successfully navigated to campground page")
            return True
            
        except Exception as e:
            self.logger.error(f"Navigation error: {str(e)}")
            return False
    
    def click_add_to_cart_button(self):
        """Click the Add to Cart button after selecting a site"""
        try:
            reserve_selectors = [
                (By.XPATH, "//button[contains(text(), 'Add to Cart')]"),
                (By.CSS_SELECTOR, "button.availability-page-book-now-button-tracker"),
                (By.CSS_SELECTOR, "button.availability-grid-book-now-button-tracker"),
                (By.XPATH, "//button[contains(text(), 'Reserve')]")
            ]
            
            reserve_button = find_element_with_fallback(
                self.driver, self.wait, reserve_selectors, "Add to Cart button", 
                quick_timeout=10
            )
            if not reserve_button:
                return False
                
            # Try multiple click methods
            try:
                reserve_button.click()
            except:
                # Fallback to JavaScript click
                self.driver.execute_script("arguments[0].click();", reserve_button)
            
            time.sleep(3)
            
            self.logger.info("Clicked Add to Cart button")
            return True
            
        except Exception as e:
            self.logger.error(f"Error clicking Add to Cart button: {str(e)}")
            return False
    
    def select_dates(self):
        """Select camping dates"""
        try:
            time.sleep(3)
            
            # Select start date
            start_date_input = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='month, Start Date, ']"))
            )
            start_date_input.click()
            start_date_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//div[contains(@aria-label, '{self.config.START_DATE}')]")))
            start_date_button.click()
            
            # Select end date
            end_date_input = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//div[contains(@aria-label, '{self.config.END_DATE}')]")))
            end_date_input.click()

            self.logger.info(f"Selected dates: {self.config.START_DATE} to {self.config.END_DATE}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error selecting dates: {str(e)}")
            return False

    def find_available_dates(self):
        """Find available dates matching our criteria"""
        try:
            time.sleep(3)  # Wait for results to load
            
            # Find all available date buttons
            available_buttons = self.driver.find_elements(
                By.CSS_SELECTOR, "button.rec-availability-date"
            )
            
            if not available_buttons:
                self.logger.info("No available date buttons found")
                return []
            
            # Parse available dates and sites - accept any available spot
            available_spots = []
            
            for button in available_buttons:
                try:
                    aria_label = button.get_attribute("aria-label")
                    if aria_label and "Site" in aria_label and "is available" in aria_label:
                        # Extract site number from aria-label
                        site_part = aria_label.split("Site")[1].strip()
                        site_number = site_part.split()[0]
                        
                        # Extract date from aria-label (before the " - Site" part)
                        date_part = aria_label.split(" - Site")[0] if " - Site" in aria_label else "Unknown date"
                        
                        available_spots.append({
                            'button': button,
                            'site': site_number,
                            'date': date_part,
                            'aria_label': aria_label,
                            'loop': button.text,
                        })
                        self.logger.info(f"Found available spot: {aria_label}")
                except Exception as e:
                    continue
            
            # Display available spots in table format
            if available_spots:
                self.logger.info(f"\n{'='*60}")
                self.logger.info("AVAILABLE CAMPSITES FOUND:")
                self.logger.info(f"{'='*60}")
                self.logger.info(f"{'Site':<10} {'Date':<12} {'Details'}")
                self.logger.info(f"{'-'*60}")
                
                for spot in available_spots:
                    self.logger.info(f"{spot['site']:<10} {spot['date']:<12} {spot['aria_label']}")
                
                self.logger.info(f"{'='*60}")
                self.logger.info(f"Total available sites: {len(available_spots)}")
            else:
                self.logger.info("No available sites found for the target date")
            
            return available_spots
            
        except Exception as e:
            self.logger.error(f"Error finding available dates: {str(e)}")
            return []
    
    def book_available_spot(self, available_spots):
        """Click on the first available spot"""
        if not available_spots:
            return False
        
        preferred_spot = []
        for spot in available_spots:
            if spot['date'] in self.config.PREFERRED_DATES:
                preferred_spot.append(spot)
        preferred_spot.sort(key=lambda spot:self.config.PREFERRED_LOOPS.index(spot['loop']))
        # if (len(preferred_spot) > 0):
        #     self.logger("Found spot(s) on preferred dates")
        #     self.logger.info(f"\n{'='*60}")
        #     self.logger.info("AVAILABLE CAMPSITES FOUND:")
        #     self.logger.info(f"{'='*60}")
        #     self.logger.info(f"{'Site':<10} {'Date':<12} {'Details'}")
        #     self.logger.info(f"{'-'*60}")
        #     for spot in preferred_spot:
        #         self.logger.info(f"{spot['site']:<10} {spot['date']:<12} {spot['aria_label']}")

        availabilities = preferred_spot if len(preferred_spot) > 0 else available_spots
        
        try:
            first_spot = availabilities[0]
            self.logger.info(f"Attempting to book Site {first_spot['site']} for {first_spot['date']}")
            
            # Try multiple click methods
            try:
                first_spot['button'].click()
            except:
                # Fallback to JavaScript click
                self.driver.execute_script("arguments[0].click();", first_spot['button'])
            
            time.sleep(5)  # Wait longer for Add to Cart button to appear
            self.logger.info(f"Successfully clicked on Site {first_spot['site']}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error booking first available spot: {str(e)}")
            return False