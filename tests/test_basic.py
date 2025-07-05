# AI-Q Knowledge Library System - Basic Tests
# TOKEN COUNT: ~500 tokens
"""
Basic tests for AI-Q Knowledge Library System.
Tests core functionality without requiring all services.
"""

import pytest
import asyncio
from src.config.settings import get_settings

class TestBasicFunctionality:
    """Test basic system functionality."""
    
    def test_settings_loading(self):
        """Test that settings can be loaded correctly."""
        settings = get_settings()
        assert settings is not None
        assert hasattr(settings, 'database')
        assert hasattr(settings, 'api_server')
        assert hasattr(settings, 'logging')
    
    def test_database_settings(self):
        """Test database settings configuration."""
        settings = get_settings()
        assert settings.database.postgresql.port == 5432
        assert settings.database.postgresql.database == "aiq_knowledge"
        assert settings.database.redis.port == 6379
    
    def test_api_server_settings(self):
        """Test API server settings configuration."""
        settings = get_settings()
        assert settings.api_server.host == "0.0.0.0"
        assert settings.api_server.port == 8000
        assert settings.api_server.environment == "development"
    
    def test_feature_flags(self):
        """Test feature flags configuration."""
        settings = get_settings()
        assert settings.feature_flags.enable_rag is True
        assert settings.feature_flags.enable_knowledge_graph is True
        assert settings.feature_flags.enable_vector_search is True
        assert settings.feature_flags.enable_object_storage is True

class TestAsyncFunctionality:
    """Test async functionality."""
    
    @pytest.mark.asyncio
    async def test_async_basic(self):
        """Test basic async functionality."""
        await asyncio.sleep(0.1)  # Simple async operation
        assert True
    
    @pytest.mark.asyncio
    async def test_settings_async(self):
        """Test settings in async context."""
        settings = get_settings()
        assert settings is not None
        # Simulate async operation
        await asyncio.sleep(0.1)
        assert settings.api_server.port == 8000 