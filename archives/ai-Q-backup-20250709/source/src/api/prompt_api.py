# AI-Q Prompt API
# Generated: 2025-01-27T03:05:00Z
# Created by: AI-Q Agent - Claude Sonnet 4
# Purpose: API endpoints for prompt management

"""
FastAPI endpoints for prompt management in AI-Q Knowledge Library System.
Provides CRUD operations for prompts and validation.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import logging

from ..prompt_loader import PromptLoader, PromptMetadata
from ..prompt_validator import PromptValidator, ValidationResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/prompts", tags=["prompts"])

# Pydantic models for API
class PromptCreate(BaseModel):
    """Model for creating a new prompt."""
    content: Dict[str, Any] = Field(..., description="Prompt content")
    prompt_id: Optional[str] = Field(None, description="Optional prompt ID")

class PromptUpdate(BaseModel):
    """Model for updating a prompt."""
    content: Dict[str, Any] = Field(..., description="Updated prompt content")

class PromptResponse(BaseModel):
    """Model for prompt response."""
    prompt_id: str
    content: Dict[str, Any]
    metadata: Dict[str, Any]
    validation_result: Optional[Dict[str, Any]] = None

class ValidationResponse(BaseModel):
    """Model for validation response."""
    is_valid: bool
    errors: List[str] = []
    warnings: List[str] = []
    timestamp: datetime
    prompt_id: str

class PromptListResponse(BaseModel):
    """Model for prompt list response."""
    prompts: List[Dict[str, Any]]
    total_count: int
    validation_summary: Dict[str, int]

# Dependency injection
def get_prompt_loader() -> PromptLoader:
    """Get prompt loader instance."""
    return PromptLoader()

def get_prompt_validator() -> PromptValidator:
    """Get prompt validator instance."""
    return PromptValidator()

# API Endpoints
@router.get("/", response_model=PromptListResponse)
async def list_prompts(
    loader: PromptLoader = Depends(get_prompt_loader),
    validator: PromptValidator = Depends(get_prompt_validator),
    include_content: bool = Query(False, description="Include prompt content in response"),
    validate: bool = Query(True, description="Validate prompts before returning")
) -> PromptListResponse:
    """List all available prompts."""
    try:
        # Load all prompts
        prompts = loader.load_all_prompts()
        prompt_list = []
        validation_summary = {"valid": 0, "invalid": 0, "warnings": 0}
        
        for prompt_id, content in prompts.items():
            prompt_info = {
                "prompt_id": prompt_id,
                "metadata": {
                    "version": content.get("version", "unknown"),
                    "created_by": content.get("created_by", "unknown"),
                    "last_updated": content.get("last_updated", "unknown"),
                    "purpose": content.get("purpose", "")
                }
            }
            
            if include_content:
                prompt_info["content"] = content
            
            # Validate if requested
            if validate:
                validation_result = validator.validate_prompt(prompt_id, content)
                prompt_info["validation"] = {
                    "is_valid": validation_result.is_valid,
                    "error_count": len(validation_result.errors),
                    "warning_count": len(validation_result.warnings)
                }
                
                if validation_result.is_valid:
                    validation_summary["valid"] += 1
                else:
                    validation_summary["invalid"] += 1
                
                if validation_result.warnings:
                    validation_summary["warnings"] += 1
            
            prompt_list.append(prompt_info)
        
        return PromptListResponse(
            prompts=prompt_list,
            total_count=len(prompt_list),
            validation_summary=validation_summary
        )
        
    except Exception as e:
        logger.error(f"Error listing prompts: {e}")
        raise HTTPException(status_code=500, detail=f"Error listing prompts: {str(e)}")

@router.get("/{prompt_id}", response_model=PromptResponse)
async def get_prompt(
    prompt_id: str,
    loader: PromptLoader = Depends(get_prompt_loader),
    validator: PromptValidator = Depends(get_prompt_validator),
    validate: bool = Query(True, description="Validate prompt before returning")
) -> PromptResponse:
    """Get a specific prompt by ID."""
    try:
        # Get prompt content
        content = loader.get_prompt(prompt_id)
        if not content:
            raise HTTPException(status_code=404, detail=f"Prompt '{prompt_id}' not found")
        
        # Get metadata
        metadata = loader.get_metadata(prompt_id)
        metadata_dict = {
            "version": metadata.version if metadata else "unknown",
            "created_by": metadata.created_by if metadata else "unknown",
            "last_updated": metadata.last_updated if metadata else "unknown",
            "purpose": metadata.purpose if metadata else "",
            "file_path": metadata.file_path if metadata else "",
            "file_size": metadata.file_size if metadata else 0,
            "load_time": metadata.load_time.isoformat() if metadata else datetime.now().isoformat()
        }
        
        # Validate if requested
        validation_result = None
        if validate:
            result = validator.validate_prompt(prompt_id, content)
            validation_result = {
                "is_valid": result.is_valid,
                "errors": result.errors,
                "warnings": result.warnings,
                "timestamp": result.timestamp.isoformat()
            }
        
        return PromptResponse(
            prompt_id=prompt_id,
            content=content,
            metadata=metadata_dict,
            validation_result=validation_result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting prompt {prompt_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting prompt: {str(e)}")

@router.post("/", response_model=PromptResponse)
async def create_prompt(
    prompt_data: PromptCreate,
    loader: PromptLoader = Depends(get_prompt_loader),
    validator: PromptValidator = Depends(get_prompt_validator)
) -> PromptResponse:
    """Create a new prompt."""
    try:
        # Validate prompt content
        validation_result = validator.validate_prompt(
            prompt_data.prompt_id or "new_prompt", 
            prompt_data.content
        )
        
        if not validation_result.is_valid:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid prompt content: {validation_result.errors}"
            )
        
        # Generate prompt ID if not provided
        prompt_id = prompt_data.prompt_id or f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Check if prompt already exists
        if loader.get_prompt(prompt_id):
            raise HTTPException(
                status_code=409, 
                detail=f"Prompt '{prompt_id}' already exists"
            )
        
        # Store prompt in registry
        loader.registry.prompts[prompt_id] = prompt_data.content
        
        # Create metadata
        metadata = PromptMetadata(
            version=prompt_data.content.get("version", "1.0"),
            last_updated=datetime.now().isoformat(),
            created_by=prompt_data.content.get("created_by", "API"),
            purpose=prompt_data.content.get("purpose", ""),
            file_path=f"api_created_{prompt_id}",
            file_size=len(str(prompt_data.content))
        )
        
        loader.registry.metadata[prompt_id] = metadata
        
        logger.info(f"Created new prompt: {prompt_id}")
        
        return PromptResponse(
            prompt_id=prompt_id,
            content=prompt_data.content,
            metadata={
                "version": metadata.version,
                "created_by": metadata.created_by,
                "last_updated": metadata.last_updated,
                "purpose": metadata.purpose,
                "file_path": metadata.file_path,
                "file_size": metadata.file_size,
                "load_time": metadata.load_time.isoformat()
            },
            validation_result={
                "is_valid": validation_result.is_valid,
                "errors": validation_result.errors,
                "warnings": validation_result.warnings,
                "timestamp": validation_result.timestamp.isoformat()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating prompt: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating prompt: {str(e)}")

@router.put("/{prompt_id}", response_model=PromptResponse)
async def update_prompt(
    prompt_id: str,
    prompt_data: PromptUpdate,
    loader: PromptLoader = Depends(get_prompt_loader),
    validator: PromptValidator = Depends(get_prompt_validator)
) -> PromptResponse:
    """Update an existing prompt."""
    try:
        # Check if prompt exists
        existing_content = loader.get_prompt(prompt_id)
        if not existing_content:
            raise HTTPException(status_code=404, detail=f"Prompt '{prompt_id}' not found")
        
        # Validate updated content
        validation_result = validator.validate_prompt(prompt_id, prompt_data.content)
        
        if not validation_result.is_valid:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid prompt content: {validation_result.errors}"
            )
        
        # Update prompt content
        loader.registry.prompts[prompt_id] = prompt_data.content
        
        # Update metadata
        metadata = loader.get_metadata(prompt_id)
        if metadata:
            metadata.last_updated = datetime.now().isoformat()
            metadata.file_size = len(str(prompt_data.content))
        
        logger.info(f"Updated prompt: {prompt_id}")
        
        return PromptResponse(
            prompt_id=prompt_id,
            content=prompt_data.content,
            metadata={
                "version": metadata.version if metadata else "unknown",
                "created_by": metadata.created_by if metadata else "unknown",
                "last_updated": metadata.last_updated if metadata else datetime.now().isoformat(),
                "purpose": metadata.purpose if metadata else "",
                "file_path": metadata.file_path if metadata else "",
                "file_size": metadata.file_size if metadata else 0,
                "load_time": metadata.load_time.isoformat() if metadata else datetime.now().isoformat()
            },
            validation_result={
                "is_valid": validation_result.is_valid,
                "errors": validation_result.errors,
                "warnings": validation_result.warnings,
                "timestamp": validation_result.timestamp.isoformat()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating prompt {prompt_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating prompt: {str(e)}")

@router.delete("/{prompt_id}")
async def delete_prompt(
    prompt_id: str,
    loader: PromptLoader = Depends(get_prompt_loader)
) -> JSONResponse:
    """Delete a prompt."""
    try:
        # Check if prompt exists
        if not loader.get_prompt(prompt_id):
            raise HTTPException(status_code=404, detail=f"Prompt '{prompt_id}' not found")
        
        # Remove from registry
        if prompt_id in loader.registry.prompts:
            del loader.registry.prompts[prompt_id]
        
        if prompt_id in loader.registry.metadata:
            del loader.registry.metadata[prompt_id]
        
        if prompt_id in loader.registry.cache:
            del loader.registry.cache[prompt_id]
        
        if prompt_id in loader.registry.dependencies:
            del loader.registry.dependencies[prompt_id]
        
        logger.info(f"Deleted prompt: {prompt_id}")
        
        return JSONResponse(
            status_code=200,
            content={
                "message": f"Prompt '{prompt_id}' deleted successfully",
                "prompt_id": prompt_id,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting prompt {prompt_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting prompt: {str(e)}")

@router.post("/{prompt_id}/validate", response_model=ValidationResponse)
async def validate_prompt(
    prompt_id: str,
    loader: PromptLoader = Depends(get_prompt_loader),
    validator: PromptValidator = Depends(get_prompt_validator)
) -> ValidationResponse:
    """Validate a specific prompt."""
    try:
        # Get prompt content
        content = loader.get_prompt(prompt_id)
        if not content:
            raise HTTPException(status_code=404, detail=f"Prompt '{prompt_id}' not found")
        
        # Validate prompt
        result = validator.validate_prompt(prompt_id, content)
        
        return ValidationResponse(
            is_valid=result.is_valid,
            errors=result.errors,
            warnings=result.warnings,
            timestamp=result.timestamp,
            prompt_id=prompt_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating prompt {prompt_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error validating prompt: {str(e)}")

@router.post("/validate-all")
async def validate_all_prompts(
    loader: PromptLoader = Depends(get_prompt_loader),
    validator: PromptValidator = Depends(get_prompt_validator)
) -> JSONResponse:
    """Validate all loaded prompts."""
    try:
        results = {}
        summary = {"total": 0, "valid": 0, "invalid": 0, "warnings": 0}
        
        for prompt_id in loader.list_prompts():
            content = loader.get_prompt(prompt_id)
            if content:
                result = validator.validate_prompt(prompt_id, content)
                results[prompt_id] = {
                    "is_valid": result.is_valid,
                    "errors": result.errors,
                    "warnings": result.warnings,
                    "timestamp": result.timestamp.isoformat()
                }
                
                summary["total"] += 1
                if result.is_valid:
                    summary["valid"] += 1
                else:
                    summary["invalid"] += 1
                
                if result.warnings:
                    summary["warnings"] += 1
        
        return JSONResponse(
            status_code=200,
            content={
                "validation_results": results,
                "summary": summary,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Error validating all prompts: {e}")
        raise HTTPException(status_code=500, detail=f"Error validating prompts: {str(e)}")

@router.get("/{prompt_id}/dependencies")
async def get_prompt_dependencies(
    prompt_id: str,
    loader: PromptLoader = Depends(get_prompt_loader)
) -> JSONResponse:
    """Get dependencies for a specific prompt."""
    try:
        dependencies = loader.get_dependencies(prompt_id)
        
        return JSONResponse(
            status_code=200,
            content={
                "prompt_id": prompt_id,
                "dependencies": dependencies,
                "dependency_count": len(dependencies),
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Error getting dependencies for {prompt_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting dependencies: {str(e)}")

@router.get("/{prompt_id}/cache")
async def get_prompt_cache(
    prompt_id: str,
    loader: PromptLoader = Depends(get_prompt_loader)
) -> JSONResponse:
    """Get cached data for a specific prompt."""
    try:
        cache_data = loader.registry.cache.get(prompt_id, {})
        
        return JSONResponse(
            status_code=200,
            content={
                "prompt_id": prompt_id,
                "cache_keys": list(cache_data.keys()),
                "cache_data": cache_data,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Error getting cache for {prompt_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting cache: {str(e)}")

# Health check endpoint
@router.get("/health")
async def health_check() -> JSONResponse:
    """Health check for prompt API."""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "prompt-api",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    ) 