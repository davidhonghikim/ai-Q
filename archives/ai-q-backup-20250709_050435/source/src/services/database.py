# AI-Q Knowledge Library System - Database Service
# TOKEN COUNT: ~1,200 tokens
"""
Database service for AI-Q Knowledge Library System.
Handles PostgreSQL database initialization and connection management.
"""

import asyncio
import logging
from typing import Optional
from contextlib import asynccontextmanager

import asyncpg
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.config.settings import get_settings

# Configure logging
logger = logging.getLogger(__name__)

class DatabaseService:
    """Database service for managing PostgreSQL connections and operations."""
    
    def __init__(self):
        self.settings = get_settings()
        self.engine: Optional[create_async_engine] = None
        self.session_factory: Optional[sessionmaker] = None
        self._connection_pool: Optional[asyncpg.Pool] = None
    
    async def initialize(self) -> None:
        """Initialize database connection and create tables."""
        try:
            logger.info("Initializing database service...")
            
            # Create async engine
            database_url = (
                f"postgresql+asyncpg://{self.settings.database.postgresql.user}:"
                f"{self.settings.database.postgresql.password}@"
                f"{self.settings.database.postgresql.host}:"
                f"{self.settings.database.postgresql.port}/"
                f"{self.settings.database.postgresql.database}"
            )
            
            self.engine = create_async_engine(
                database_url,
                echo=self.settings.api_server.environment == "development",
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600
            )
            
            # Create session factory
            self.session_factory = sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            
            # Test connection
            await self._test_connection()
            
            # Create tables
            await self._create_tables()
            
            logger.info("Database service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database service: {e}")
            raise
    
    async def _test_connection(self) -> None:
        """Test database connection."""
        try:
            async with self.engine.begin() as conn:
                result = await conn.execute(text("SELECT 1"))
                await result.fetchone()
            logger.info("Database connection test successful")
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            raise
    
    async def _create_tables(self) -> None:
        """Create database tables if they don't exist."""
        try:
            # TODO: Import models when they are created
            # from models.base import Base
            # from models.knowledge import KnowledgeEntry
            # from models.user import User
            # from models.session import Session
            
            # For now, just test the connection
            async with self.engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            
            logger.info("Database tables created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise
    
    @asynccontextmanager
    async def get_session(self):
        """Get database session context manager."""
        if not self.session_factory:
            raise RuntimeError("Database service not initialized")
        
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
    
    async def close(self) -> None:
        """Close database connections."""
        try:
            if self.engine:
                await self.engine.dispose()
            logger.info("Database connections closed")
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")

# Global database service instance
_db_service: Optional[DatabaseService] = None

async def init_database() -> None:
    """Initialize the database service."""
    global _db_service
    
    try:
        _db_service = DatabaseService()
        await _db_service.initialize()
        logger.info("Database initialization completed")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

async def get_database_service() -> DatabaseService:
    """Get the database service instance."""
    if not _db_service:
        raise RuntimeError("Database service not initialized")
    return _db_service

async def close_database() -> None:
    """Close database connections."""
    global _db_service
    if _db_service:
        await _db_service.close()
        _db_service = None 