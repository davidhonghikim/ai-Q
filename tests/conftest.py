# AI-Q Knowledge Library System - Test Configuration
# TOKEN COUNT: ~400 tokens
"""
Test configuration and fixtures for AI-Q Knowledge Library System.
Provides common test fixtures and configuration.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from typing import Dict, Any

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    settings = Mock()
    
    # Database settings
    settings.database = Mock()
    settings.database.postgresql = Mock(
        user="test_user",
        password="test_password",
        host="localhost",
        port=5432,
        database="test_db"
    )
    settings.database.redis = Mock(
        host="localhost",
        port=6379,
        password="",
        database=0
    )
    
    # Search engine settings
    settings.search_engine = Mock()
    settings.search_engine.elasticsearch = Mock(
        host="localhost",
        port=9200,
        password="elastic"
    )
    
    # Graph database settings
    settings.graph_database = Mock()
    settings.graph_database.neo4j = Mock(
        host="localhost",
        bolt_port=7687,
        user="neo4j",
        password="password"
    )
    
    # Vector database settings
    settings.vector_database = Mock()
    settings.vector_database.weaviate = Mock(
        host="localhost",
        port=8080
    )
    
    # Object storage settings
    settings.object_storage = Mock()
    settings.object_storage.minio = Mock(
        host="localhost",
        api_port=9000,
        root_user="minioadmin",
        root_password="minioadmin"
    )
    
    # API server settings
    settings.api_server = Mock(
        environment="test"
    )
    
    return settings

@pytest.fixture
def sample_knowledge_data():
    """Sample knowledge data for testing."""
    return {
        "id": "test-knowledge-001",
        "title": "Test Knowledge Entry",
        "content": "This is a test knowledge entry for testing purposes.",
        "category": "test",
        "author": "test_user",
        "tags": ["test", "sample"],
        "created_at": "2025-01-27T22:00:00Z",
        "updated_at": "2025-01-27T22:00:00Z"
    }

@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "id": "test-user-001",
        "email": "test@example.com",
        "name": "Test User",
        "role": "user",
        "created_at": "2025-01-27T22:00:00Z",
        "updated_at": "2025-01-27T22:00:00Z"
    }

@pytest.fixture
def sample_document_data():
    """Sample document data for testing."""
    return {
        "id": "test-doc-001",
        "title": "Test Document",
        "content": "This is a test document for testing purposes.",
        "source": "test_source",
        "chunk_index": 0,
        "created_at": "2025-01-27T22:00:00Z"
    }

@pytest.fixture
def mock_logger():
    """Mock logger for testing."""
    with patch('src.utils.logging.structlog.get_logger') as mock_logger:
        yield mock_logger

@pytest.fixture
def mock_async_context():
    """Mock async context manager."""
    class MockAsyncContext:
        async def __aenter__(self):
            return self
        
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass
    
    return MockAsyncContext() 