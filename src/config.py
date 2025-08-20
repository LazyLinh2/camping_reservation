import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Recreation.gov credentials
    USERNAME = os.getenv('RECREATION_USERNAME', '')
    PASSWORD = os.getenv('RECREATION_PASSWORD', '')
    
    # Campground settings
    CAMPGROUND_URL = "https://www.recreation.gov/camping/campgrounds/259084"
    CAMPGROUND_NAME = "Fairholme"
    
    START_DATE = 'August 23, 2025'  #Date range for within which we'll look for availabilities
    END_DATE = 'August 30, 2025'
    
    # Site preferences
    PREFERRED_LOOPS = ['A', 'B', 'C']  # Priority order: Preference order
    PREFERRED_DATES = ['Aug 26, 2025']
    # Specific site preferences (if any)
    PREFERRED_SITE_NUMBERS = []  # Leave empty for any site, or add specific site numbers
    
    
    # Bot behavior
    REFRESH_INTERVAL = 30  # seconds between checks
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds between retries
    
    # Notification settings
    ENABLE_NOTIFICATIONS = True
    ENABLE_SOUND = True
    
    # Browser settings
    HEADLESS = False  # Set to True for background operation
    BROWSER_TIMEOUT = 30
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'camping_bot.log'
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        errors = []
        
        if not cls.USERNAME:
            errors.append("RECREATION_USERNAME not set in environment variables")
        if not cls.PASSWORD:
            errors.append("RECREATION_PASSWORD not set in environment variables")
        if not cls.START_DATE:
            errors.append("START_DATE not set in environment variables")
        if not cls.END_DATE:
            errors.append("END_DATE not set in environment variables")
            
        return errors 