"""
AI-Q Dynamic Main Application
Main entry point with dynamic feature loading based on feature flags
"""

import asyncio
import logging
import sys
from pathlib import Path
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent))

from core.feature_manager import feature_manager
from core.component_loader import component_loader
from utils.logging import setup_logging

# Structured logging
logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager with dynamic component loading"""
    logger.info("Starting AI-Q Dynamic Application")
    
    try:
        # Load all enabled components
        logger.info("Loading enabled components...")
        loaded_components = await feature_manager.load_all_components()
        logger.info(f"Loaded {len(loaded_components)} components: {list(loaded_components.keys())}")
        
        # Store components in app state for access by routes
        app.state.components = loaded_components
        app.state.feature_manager = feature_manager
        
    except Exception as e:
        logger.error("Failed to initialize components", error=str(e))
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI-Q Dynamic Application")
    
    # Cleanup components
    for component_name in list(feature_manager.loaded_components.keys()):
        feature_manager.unload_component(component_name)

def create_dynamic_app() -> FastAPI:
    """Create FastAPI application with dynamic feature loading"""
    
    app = FastAPI(
        title="AI-Q Dynamic Knowledge Library System",
        description="Dynamic knowledge management framework with feature-flag-based component loading",
        version="2.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    
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
        component_status = feature_manager.get_component_status()
        enabled_components = feature_manager.get_enabled_components()
        
        return {
            "status": "healthy",
            "version": "2.0.0",
            "enabled_components": enabled_components,
            "loaded_components": list(feature_manager.loaded_components.keys()),
            "component_status": component_status
        }
    
    # Feature flags endpoint
    @app.get("/api/v1/features")
    async def get_features():
        return {
            "features": feature_manager.features,
            "enabled_components": feature_manager.get_enabled_components(),
            "component_status": feature_manager.get_component_status()
        }
    
    # Component management endpoints
    @app.get("/api/v1/components")
    async def get_components():
        return {
            "loaded_components": list(feature_manager.loaded_components.keys()),
            "available_components": list(feature_manager.component_registry.keys()),
            "component_status": feature_manager.get_component_status()
        }
    
    @app.post("/api/v1/components/{component_name}/reload")
    async def reload_component(component_name: str):
        try:
            await feature_manager.reload_component(component_name)
            return {"message": f"Component {component_name} reloaded successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    # Dynamic route loading based on enabled components
    async def load_dynamic_routes():
        """Load API routes based on enabled components"""
        
        # Load API routes if API server is enabled
        if feature_manager.is_component_enabled('api_server'):
            try:
                from api.routes import knowledge, rag, system
                app.include_router(system.router, prefix="/api/v1/system", tags=["system"])
                app.include_router(knowledge.router, prefix="/api/v1/knowledge", tags=["knowledge"])
                
                if feature_manager.is_component_enabled('rag'):
                    app.include_router(rag.router, prefix="/api/v1/rag", tags=["rag"])
                
                logger.info("Loaded API routes")
            except ImportError as e:
                logger.warning(f"Could not load API routes: {e}")
        
        # Load monitoring routes if monitoring is enabled
        if feature_manager.is_component_enabled('health_monitoring'):
            try:
                from monitoring.routes import health
                app.include_router(health.router, prefix="/api/v1/monitoring", tags=["monitoring"])
                logger.info("Loaded monitoring routes")
            except ImportError as e:
                logger.warning(f"Could not load monitoring routes: {e}")
    
    # Load routes after app creation
    asyncio.create_task(load_dynamic_routes())
    
    return app

def main():
    """Main application entry point"""
    # Setup logging
    setup_logging()
    
    # Create application
    app = create_dynamic_app()
    
    # Start server
    uvicorn.run(
        "main_dynamic:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disable reload for dynamic loading
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main() 