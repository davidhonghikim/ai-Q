"""
Prompt Validator Schema - Schema validation functionality
=======================================================

Schema validation for prompts in the AI-Q system.

Author: kOS Kitchen System
Version: 1.0.0
Created: 2025-07-08T02:15:00Z
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Result of a validation operation."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    prompt_id: str = ""
    validation_type: str = ""

class SchemaValidator:
    """Validate content against JSON schemas."""
    
    def __init__(self):
        """Initialize the schema validator."""
        self.schemas = {}
        self._load_default_schemas()
    
    def add_schema(self, name: str, schema: Dict[str, Any]) -> None:
        """Add a schema for validation."""
        self.schemas[name] = schema
        logger.info(f"Added schema: {name}")
    
    def validate_against_schema(self, content: Dict[str, Any], schema_name: str) -> ValidationResult:
        """Validate content against a specific schema."""
        if schema_name not in self.schemas:
            return ValidationResult(
                is_valid=False,
                errors=[f"Schema '{schema_name}' not found"],
                validation_type="schema"
            )
        
        schema = self.schemas[schema_name]
        is_valid, errors = self._validate_schema(content, schema)
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            validation_type="schema"
        )
    
    def _validate_schema(self, content: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate content against a schema."""
        errors = []
        
        # Check required fields
        required_fields = schema.get('required', [])
        for field in required_fields:
            if field not in content:
                errors.append(f"Missing required field: {field}")
        
        # Check field types
        properties = schema.get('properties', {})
        for field_name, field_schema in properties.items():
            if field_name in content:
                field_value = content[field_name]
                field_type = field_schema.get('type')
                
                if field_type == 'string':
                    if not isinstance(field_value, str):
                        errors.append(f"Field '{field_name}' must be a string")
                elif field_type == 'number':
                    if not isinstance(field_value, (int, float)):
                        errors.append(f"Field '{field_name}' must be a number")
                elif field_type == 'boolean':
                    if not isinstance(field_value, bool):
                        errors.append(f"Field '{field_name}' must be a boolean")
                elif field_type == 'array':
                    if not isinstance(field_value, list):
                        errors.append(f"Field '{field_name}' must be an array")
                elif field_type == 'object':
                    if not isinstance(field_value, dict):
                        errors.append(f"Field '{field_name}' must be an object")
        
        # Check string patterns
        for field_name, field_schema in properties.items():
            if field_name in content and field_schema.get('type') == 'string':
                pattern = field_schema.get('pattern')
                if pattern:
                    import re
                    if not re.match(pattern, content[field_name]):
                        errors.append(f"Field '{field_name}' doesn't match pattern: {pattern}")
        
        return len(errors) == 0, errors
    
    def _load_default_schemas(self) -> None:
        """Load default schemas for common prompt types."""
        # Basic prompt schema
        basic_prompt_schema = {
            "type": "object",
            "required": ["version", "created_by", "purpose"],
            "properties": {
                "version": {
                    "type": "string",
                    "pattern": r"^\d+\.\d+\.\d+"
                },
                "created_by": {
                    "type": "string"
                },
                "purpose": {
                    "type": "string"
                },
                "last_updated": {
                    "type": "string"
                },
                "content": {
                    "type": "object"
                }
            }
        }
        
        # Agent workflow schema
        agent_workflow_schema = {
            "type": "object",
            "required": ["metadata", "workflow"],
            "properties": {
                "metadata": {
                    "type": "object",
                    "required": ["version", "created_by", "purpose"]
                },
                "workflow": {
                    "type": "object",
                    "required": ["steps", "dependencies"]
                }
            }
        }
        
        # Recipe schema
        recipe_schema = {
            "type": "object",
            "required": ["id", "name", "description", "steps"],
            "properties": {
                "id": {
                    "type": "string",
                    "pattern": r"^[a-zA-Z0-9._-]+$"
                },
                "name": {
                    "type": "string"
                },
                "description": {
                    "type": "string"
                },
                "steps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["operation"],
                        "properties": {
                            "operation": {
                                "type": "string"
                            },
                            "parameters": {
                                "type": "object"
                            }
                        }
                    }
                }
            }
        }
        
        self.add_schema("basic_prompt", basic_prompt_schema)
        self.add_schema("agent_workflow", agent_workflow_schema)
        self.add_schema("recipe", recipe_schema)

def create_schema_validator() -> SchemaValidator:
    """Create a new schema validator instance."""
    return SchemaValidator() 