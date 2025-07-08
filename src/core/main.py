# AI-Q Knowledge Library System - Main Application
# created_by: configurable via config
# last_updated: configurable via config
# purpose: Main FastAPI application entry point for the AI-Q Knowledge Library System.
# Provides unified API access to both structured (YAML) and unstructured (RAG) knowledge.

import asyncio
import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram
import structlog

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import get_settings
from api.routes import knowledge, rag, system
from api.middleware import (
    RequestLoggingMiddleware,
    SecurityMiddleware,
    PerformanceMiddleware
)
from services.database import init_database
from services.cache import init_cache
from services.search import init_search
from services.graph import init_graph
from services.vector import init_vector_db
from services.storage import init_storage
from utils.logging import setup_logging

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

# Structured logging
logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    settings = get_settings()
    # Startup
    logger.info("Starting AI-Q Knowledge Library System", 
                agent=settings.external_api.agent_name, 
                version=settings.external_api.agent_version)
    
    try:
        # Initialize all services
        await init_database()
        await init_cache()
        await init_search()
        await init_graph()
        await init_vector_db()
        await init_storage()
        
        logger.info("All services initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize services", error=str(e))
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI-Q Knowledge Library System")

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title="AI-Q Knowledge Library System",
        description="Dual-representation knowledge management framework with structured (YAML) and unstructured (RAG) storage",
        version=settings.external_api.agent_version,
        docs_url="/docs" if settings.feature_flags.enable_api_documentation else None,
        redoc_url="/redoc" if settings.feature_flags.enable_api_documentation else None,
        lifespan=lifespan
    )
    
    # Security middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.security.allowed_hosts
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.security.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    
    # Custom middleware
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(SecurityMiddleware)
    app.add_middleware(PerformanceMiddleware)
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error("Unhandled exception", 
                    path=request.url.path,
                    method=request.method,
                    error=str(exc))
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "agent": settings.external_api.agent_name,
            "version": settings.external_api.agent_version
        }
    
    # Include routers
    app.include_router(system.router, prefix="/api/v1/system", tags=["system"])
    app.include_router(knowledge.router, prefix="/api/v1/knowledge", tags=["knowledge"])
    
    if settings.feature_flags.enable_rag:
        app.include_router(rag.router, prefix="/api/v1/rag", tags=["rag"])
    
    return app

def main():
    """Main application entry point."""
    # Setup logging
    setup_logging()
    
    # Create application
    app = create_app()
    
    # Get settings
    settings = get_settings()
    
    # Start server
    uvicorn.run(
        "main:app",
        host=settings.api_server.host,
        port=settings.api_server.port,
        reload=settings.api_server.environment == "development",
        log_level=settings.logging.level.lower(),
        access_log=True
    )

if __name__ == "__main__":
    main() 