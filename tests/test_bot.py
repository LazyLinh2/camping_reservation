#!/usr/bin/env python3
"""
Test script for the camping reservation bot.
This script tests the bot setup and configuration without making actual reservations.
"""

import os
import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Add the parent directory to the Python path to enable imports from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import Config
from src.browser_utils import setup_chrome_driver, find_element_with_fallback

def test_configuration():
    """Test that all required configuration is present"""
    print("🔧 Testing configuration...")
    
    errors = Config.validate_config()
    if errors:
        print("❌ Configuration errors found:")
        for error in errors:
            print(f"   - {error}")
        return False
    else:
        print("✅ Configuration is valid")
        return True

def test_browser_setup():
    """Test that Chrome browser can be launched"""
    print("\n🌐 Testing browser setup...")
    
    try:
        # Setup driver using shared utility
        driver, wait = setup_chrome_driver(headless=True, timeout=10)
        
        # Test navigation
        driver.get("https://www.recreation.gov")
        time.sleep(3)
        
        title = driver.title
        driver.quit()
        
        if "Recreation.gov" in title:
            print("✅ Browser setup successful")
            return True
        else:
            print("❌ Browser setup failed - unexpected page title")
            return False
            
    except Exception as e:
        print(f"❌ Browser setup failed: {str(e)}")
        return False

def test_recreation_gov_access():
    """Test access to Recreation.gov"""
    print("\n🏕️ Testing Recreation.gov access...")
    
    try:
        # Setup driver using shared utility
        driver, wait = setup_chrome_driver(headless=True, timeout=10)
        
        # Test campground page access
        driver.get(Config.CAMPGROUND_URL)
        time.sleep(3)
        
        # Check if page loaded
        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print("✅ Recreation.gov access successful")
            driver.quit()
            return True
        except:
            print("❌ Recreation.gov access failed - page didn't load")
            driver.quit()
            return False
            
    except Exception as e:
        print(f"❌ Recreation.gov access failed: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🧪 Running camping bot tests...\n")
    
    tests = [
        ("Configuration", test_configuration),
        ("Browser Setup", test_browser_setup),
        ("Recreation.gov Access", test_recreation_gov_access),
        ("Credentials", test_credentials)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your bot is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please fix the issues before running the bot.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 