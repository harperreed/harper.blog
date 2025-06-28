"""
API Security utilities for handling sensitive credentials safely.

This module provides functions for validating API keys and masking sensitive
information in logs to prevent accidental exposure of credentials.
"""

import os
import logging
from typing import Optional, Dict, Any


def validate_api_key(key_name: str, key_value: Optional[str] = None) -> str:
    """
    Validate that an API key is present and has a reasonable format.
    
    Args:
        key_name: The name of the environment variable (e.g., 'OPENAI_API_KEY')
        key_value: Optional pre-fetched key value. If None, will fetch from environment.
        
    Returns:
        str: The validated API key
        
    Raises:
        ValueError: If the key is missing or has invalid format
    """
    if key_value is None:
        key_value = os.getenv(key_name)
    
    if not key_value:
        raise ValueError(f"Missing required environment variable: {key_name}")
    
    if not isinstance(key_value, str):
        raise ValueError(f"Invalid {key_name} type: expected string, got {type(key_value)}")
    
    # Basic validation - API keys should be reasonably long
    if len(key_value.strip()) < 10:
        raise ValueError(f"Invalid {key_name} format: key appears too short")
    
    return key_value.strip()


def mask_key_in_logs(key: str, show_chars: int = 4) -> str:
    """
    Mask an API key for safe logging by showing only first and last characters.
    
    Args:
        key: The API key to mask
        show_chars: Number of characters to show at start and end (default: 4)
        
    Returns:
        str: Masked version of the key safe for logging
    """
    if not key or not isinstance(key, str):
        return "***"
    
    key = key.strip()
    if len(key) <= (show_chars * 2):
        return "***"
    
    return f"{key[:show_chars]}***{key[-show_chars:]}"


def safe_log_api_error(logger: logging.Logger, error_msg: str, 
                      sensitive_data: Optional[Dict[str, Any]] = None) -> None:
    """
    Log an API error message while ensuring no sensitive data is exposed.
    
    Args:
        logger: Logger instance to use
        error_msg: The error message to log
        sensitive_data: Optional dict of sensitive data to mask in logs
    """
    if sensitive_data:
        # Create a safe version of any data that might contain keys
        safe_data = {}
        for key, value in sensitive_data.items():
            if isinstance(value, str) and (
                'key' in key.lower() or 
                'token' in key.lower() or 
                'secret' in key.lower() or
                'password' in key.lower()
            ):
                safe_data[key] = mask_key_in_logs(value)
            else:
                safe_data[key] = value
        logger.error(f"{error_msg}. Data: {safe_data}")
    else:
        logger.error(error_msg)


def validate_multiple_keys(key_mapping: Dict[str, Optional[str]]) -> Dict[str, str]:
    """
    Validate multiple API keys at once.
    
    Args:
        key_mapping: Dict mapping env var names to optional pre-fetched values
                    e.g., {'OPENAI_API_KEY': None, 'GOODREADS_KEY': 'abc123'}
    
    Returns:
        Dict[str, str]: Dict mapping env var names to validated key values
        
    Raises:
        ValueError: If any key is missing or invalid, with details about which keys failed
    """
    validated_keys = {}
    failed_keys = []
    
    for key_name, key_value in key_mapping.items():
        try:
            validated_keys[key_name] = validate_api_key(key_name, key_value)
        except ValueError as e:
            failed_keys.append(f"{key_name}: {str(e)}")
    
    if failed_keys:
        raise ValueError(f"API key validation failed for: {'; '.join(failed_keys)}")
    
    return validated_keys


def setup_secure_logging(logger_name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with security-conscious formatting that avoids accidentally
    logging sensitive information.
    
    Args:
        logger_name: Name for the logger
        level: Logging level (default: INFO)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(logger_name)
    
    # Only add handler if none exists to avoid duplicate logs
    if not logger.handlers:
        handler = logging.StreamHandler()
        
        # Format that doesn't include potentially sensitive message content in timestamps
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    logger.setLevel(level)
    return logger