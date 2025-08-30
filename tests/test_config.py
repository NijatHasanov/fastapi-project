import pytest
from app.config import Settings
import os

def test_settings_from_env(monkeypatch):
    """Test that settings are loaded correctly from environment variables"""
    # Test data
    test_cors = '["http://test1.com","http://test2.com"]'
    test_db_url = "postgresql+asyncpg://test:test@localhost:5432/test_db"
    test_jwt_secret = "test_secret"
    test_log_level = "DEBUG"
    
    # Set environment variables
    monkeypatch.setenv("CORS_ORIGINS", test_cors)
    monkeypatch.setenv("DB_URL", test_db_url)
    monkeypatch.setenv("JWT_SECRET", test_jwt_secret)
    monkeypatch.setenv("LOG_LEVEL", test_log_level)
    
    # Initialize settings
    settings = Settings()
    
    # Verify settings
    assert len(settings.CORS_ORIGINS) == 2
    assert "http://test1.com" in settings.CORS_ORIGINS
    assert settings.DB_URL == test_db_url
    assert settings.JWT_SECRET == test_jwt_secret
    assert settings.LOG_LEVEL == test_log_level

def test_settings_default_log_level():
    """Test that LOG_LEVEL defaults to INFO"""
    if "LOG_LEVEL" in os.environ:
        del os.environ["LOG_LEVEL"]
    settings = Settings()
    assert settings.LOG_LEVEL == "INFO"
