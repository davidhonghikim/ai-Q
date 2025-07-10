# AI-Q Knowledge Library System - Logging Utility
# TOKEN COUNT: ~800 tokens
"""
Logging utility for AI-Q Knowledge Library System.
Handles structured logging configuration and setup.
"""

import logging
import sys
from typing import Any, Dict, Optional
from datetime import datetime

import structlog
from structlog.stdlib import LoggerFactory
from config.settings import get_settings

def setup_logging() -> None:
    """Set up structured logging for the application."""
    try:
        settings = get_settings()
        
        # Configure structlog
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer() if settings.logging.format == "JSON" 
                else structlog.dev.ConsoleRenderer()
            ],
            context_class=dict,
            logger_factory=LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
        
        # Configure standard library logging
        logging.basicConfig(
            format="%(message)s",
            stream=sys.stdout,
            level=getattr(logging, settings.logging.level.upper())
        )
        
        # Create logger
        logger = structlog.get_logger()
        logger.info("Logging system initialized", 
                   level=settings.logging.level,
                   format=settings.logging.format,
                   destination=settings.logging.destination)
        
    except Exception as e:
        # Fallback to basic logging if structlog fails
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logging.error(f"Failed to setup structured logging: {e}")

def get_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)

def log_function_call(func_name: str, **kwargs) -> None:
    """Log a function call with parameters."""
    logger = get_logger("function_calls")
    logger.info("Function called", function=func_name, parameters=kwargs)

def log_error(error: Exception, context: Optional[Dict[str, Any]] = None) -> None:
    """Log an error with context."""
    logger = get_logger("errors")
    error_context = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "timestamp": datetime.utcnow().isoformat()
    }
    if context:
        error_context.update(context)
    
    logger.error("Error occurred", **error_context)

def log_performance(operation: str, duration: float, **kwargs) -> None:
    """Log performance metrics."""
    logger = get_logger("performance")
    logger.info("Performance metric", 
               operation=operation, 
               duration_ms=duration * 1000,
               **kwargs)

def log_security_event(event_type: str, user_id: Optional[str] = None, **kwargs) -> None:
    """Log security events."""
    logger = get_logger("security")
    security_context = {
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat()
    }
    if user_id:
        security_context["user_id"] = user_id
    security_context.update(kwargs)
    
    logger.warning("Security event", **security_context)

def log_api_request(method: str, path: str, status_code: int, duration: float, 
                   user_id: Optional[str] = None) -> None:
    """Log API request details."""
    logger = get_logger("api_requests")
    logger.info("API request", 
               method=method,
               path=path,
               status_code=status_code,
               duration_ms=duration * 1000,
               user_id=user_id)

def log_database_operation(operation: str, table: str, duration: float, 
                          success: bool, **kwargs) -> None:
    """Log database operations."""
    logger = get_logger("database")
    log_level = "info" if success else "error"
    logger.log(log_level, "Database operation",
               operation=operation,
               table=table,
               duration_ms=duration * 1000,
               success=success,
               **kwargs)

def log_cache_operation(operation: str, key: str, success: bool, 
                       duration: Optional[float] = None) -> None:
    """Log cache operations."""
    logger = get_logger("cache")
    log_level = "info" if success else "error"
    log_data = {
        "operation": operation,
        "key": key,
        "success": success
    }
    if duration:
        log_data["duration_ms"] = duration * 1000
    
    logger.log(log_level, "Cache operation", **log_data)

def log_search_operation(query: str, results_count: int, duration: float, 
                        search_type: str = "full_text") -> None:
    """Log search operations."""
    logger = get_logger("search")
    logger.info("Search operation",
               query=query,
               results_count=results_count,
               duration_ms=duration * 1000,
               search_type=search_type)

def log_file_operation(operation: str, file_path: str, success: bool, 
                      file_size: Optional[int] = None) -> None:
    """Log file operations."""
    logger = get_logger("file_operations")
    log_level = "info" if success else "error"
    log_data = {
        "operation": operation,
        "file_path": file_path,
        "success": success
    }
    if file_size:
        log_data["file_size_bytes"] = file_size
    
    logger.log(log_level, "File operation", **log_data)

def log_system_event(event_type: str, message: str, **kwargs) -> None:
    """Log system events."""
    logger = get_logger("system")
    logger.info("System event",
               event_type=event_type,
               message=message,
               **kwargs)

def log_user_activity(user_id: str, activity: str, **kwargs) -> None:
    """Log user activities."""
    logger = get_logger("user_activity")
    logger.info("User activity",
               user_id=user_id,
               activity=activity,
               timestamp=datetime.utcnow().isoformat(),
               **kwargs) 