"""Simplified camping reservation bot"""
import time
import logging
import colorama
from colorama import Fore, Style
from browser_utils import setup_chrome_driver
from login_handler import LoginHandler
from booking_handler import BookingHandler
from config import Config

colorama.init()

class CampingBot:
    def __init__(self):
        self.setup_logging()
        self.driver, self.wait = setup_chrome_driver(
            headless=Config.HEADLESS, 
            timeout=Config.BROWSER_TIMEOUT
        )
        self.login_handler = LoginHandler(self.driver, self.wait, Config)
        self.booking_handler = BookingHandler(self.driver, self.wait, Config)
        
    def setup_logging(self):
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def check_availability(self):
        """Check for campsite availability"""
        try:
            # Step 1: Skip date selection and search - look for available spots directly
            self.logger.info("Looking for available spots on the page...")
            
            # Step 2: Find available dates and display them
            available_spots = self.booking_handler.find_available_dates()
            
            if available_spots:
                self.logger.info(f"{Fore.GREEN}Found {len(available_spots)} available spots!{Style.RESET_ALL}")
                
                # Step 3: Click on the first available spot
                if self.booking_handler.book_available_spot(available_spots):
                    self.logger.info(f"{Fore.GREEN}Selected campsite, now adding to cart...{Style.RESET_ALL}")
                    
                    # Step 4: Click Add to Cart button
                    if self.booking_handler.click_add_to_cart_button():
                        self.logger.info(f"{Fore.GREEN}Successfully added campsite to cart! Stopping execution but keeping browser open...{Style.RESET_ALL}")
                        return True  # Signal success to stop execution
                    else:
                        self.logger.info(f"{Fore.YELLOW}Failed to add to cart{Style.RESET_ALL}")
                else:
                    self.logger.info(f"{Fore.YELLOW}Failed to select the campsite{Style.RESET_ALL}")
            else:
                self.logger.info(f"{Fore.YELLOW}No available spots found on the page{Style.RESET_ALL}")
                
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking availability: {str(e)}")
            return False
    
    def run(self):
        """Main bot loop"""
        self.logger.info(f"Starting bot for {Config.CAMPGROUND_NAME}")
        
        # Login once
        if not self.login_handler.login():
            self.logger.error("Failed to login. Exiting.")
            self.cleanup()
            return
            
        self.logger.info(f"{Fore.GREEN}Login successful! Starting checks...{Style.RESET_ALL}")

        #Navigate to campground
        if not self.booking_handler.navigate_to_campground():
            return False
        
        if not self.booking_handler.select_dates():
            return False
        
        while True:
            try:
                if self.check_availability():  # Check if successful
                    self.logger.info(f"{Fore.GREEN}Task completed successfully! Browser will remain open.{Style.RESET_ALL}")
                    self.logger.info("You can now manually complete the checkout process.")
                    # Don't call cleanup() to keep browser open
                    break
                else:
                    self.logger.info(f"Waiting {Config.REFRESH_INTERVAL} seconds...")
                    time.sleep(Config.REFRESH_INTERVAL)
                    
            except KeyboardInterrupt:
                self.logger.info("Stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error: {str(e)}")
                time.sleep(Config.RETRY_DELAY)     
        self.cleanup()
    
    def cleanup(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    errors = Config.validate_config()
    if errors:
        print(f"{Fore.RED}Config errors:{Style.RESET_ALL}")
        for error in errors:
            print(f"  - {error}")
        exit(1)
        
    bot = CampingBot()
    bot.run()