#!/usr/bin/env python3
"""
Test script for the API security module to verify functionality.
"""

import os
import logging
from api_security import (
    validate_api_key, 
    mask_key_in_logs, 
    validate_multiple_keys,
    safe_log_api_error,
    setup_secure_logging
)

def test_api_key_validation():
    """Test the API key validation function."""
    print("Testing API key validation...")
    
    # Test missing key
    try:
        validate_api_key('NONEXISTENT_KEY')
        print("❌ Should have failed for missing key")
    except ValueError as e:
        print(f"✅ Correctly caught missing key: {e}")
    
    # Test short key
    try:
        validate_api_key('SHORT_KEY', 'abc')
        print("❌ Should have failed for short key")
    except ValueError as e:
        print(f"✅ Correctly caught short key: {e}")
    
    # Test valid key
    try:
        result = validate_api_key('VALID_KEY', 'this_is_a_valid_key_12345')
        print(f"✅ Valid key accepted: {result}")
    except ValueError as e:
        print(f"❌ Valid key rejected: {e}")

def test_key_masking():
    """Test the key masking function."""
    print("\nTesting key masking...")
    
    test_cases = [
        ("", "***"),
        ("abc", "***"), 
        ("short", "***"),
        ("this_is_a_long_key", "this***key"),
        ("sk-1234567890abcdef", "sk-1***cdef"),
        ("very_long_api_key_123456789", "very***789")
    ]
    
    for input_key, expected in test_cases:
        result = mask_key_in_logs(input_key)
        if result == expected:
            print(f"✅ '{input_key}' -> '{result}'")
        else:
            print(f"❌ '{input_key}' -> '{result}' (expected '{expected}')")

def test_multiple_key_validation():
    """Test validating multiple keys at once."""
    print("\nTesting multiple key validation...")
    
    # Test with valid keys
    try:
        keys = {
            'KEY1': 'valid_key_1234567890',
            'KEY2': 'another_valid_key_abc',
            'KEY3': 'third_key_xyz123456'
        }
        result = validate_multiple_keys(keys)
        print(f"✅ All valid keys accepted: {list(result.keys())}")
    except ValueError as e:
        print(f"❌ Valid keys rejected: {e}")
    
    # Test with some invalid keys
    try:
        keys = {
            'VALID_KEY': 'valid_key_1234567890',
            'INVALID_KEY': 'short',
            'MISSING_KEY': None
        }
        result = validate_multiple_keys(keys)
        print("❌ Should have failed for invalid keys")
    except ValueError as e:
        print(f"✅ Correctly caught invalid keys: {e}")

def test_secure_logging():
    """Test the secure logging setup."""
    print("\nTesting secure logging...")
    
    logger = setup_secure_logging("test_logger")
    
    # Test basic logging
    logger.info("This is a test info message")
    logger.debug("This is a test debug message")
    
    # Test safe error logging
    safe_log_api_error(logger, "Test error message", {
        "api_key": "secret_key_123456789",
        "user_token": "user_token_abcdef",
        "normal_data": "this should not be masked"
    })
    
    print("✅ Secure logging test completed (check output above)")

def main():
    """Run all tests."""
    print("🔒 Testing API Security Module")
    print("=" * 40)
    
    test_api_key_validation()
    test_key_masking()
    test_multiple_key_validation()
    test_secure_logging()
    
    print("\n" + "=" * 40)
    print("🎉 API Security tests completed!")

if __name__ == "__main__":
    main()