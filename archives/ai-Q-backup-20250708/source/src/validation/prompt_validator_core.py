"""
Core Prompt Validator - Basic validation functionality
====================================================

Core validation logic for prompts in the AI-Q system.
Handles basic structure and metadata validation.

Author: kOS Kitchen System
Version: 1.0.0
Created: 2025-07-08T02:15:00Z
"""

import re
import json
import yaml
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
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

@dataclass
class ValidationRule:
    """A validation rule for prompts."""
    name: str
    description: str
    severity: str  # 'error' or 'warning'
    rule_function: callable

class PromptValidator:
    """Validate prompts for structure, content, and consistency."""
    
    def __init__(self):
        """Initialize the validator."""
        self.validation_rules = []
        self.schema_definitions = {}
        self.cross_references = {}
        self._register_default_rules()
    
    def validate_prompt(self, prompt_id: str, content: Dict[str, Any]) -> ValidationResult:
        """Validate a single prompt."""
        errors = []
        warnings = []
        
        # Run all validation rules
        for rule in self.validation_rules:
            try:
                rule_result = rule.rule_function(prompt_id, content)
                if not rule_result:
                    if rule.severity == 'error':
                        errors.append(f"Rule '{rule.name}' failed: {rule.description}")
                    else:
                        warnings.append(f"Rule '{rule.name}' failed: {rule.description}")
            except Exception as e:
                errors.append(f"Rule '{rule.name}' threw exception: {e}")
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            prompt_id=prompt_id,
            validation_type="prompt"
        )
    
    def validate_prompt_file(self, file_path: str) -> ValidationResult:
        """Validate a prompt file."""
        try:
            path = Path(file_path)
            if not path.exists():
                return ValidationResult(
                    is_valid=False,
                    errors=[f"File not found: {file_path}"],
                    prompt_id="",
                    validation_type="file"
                )
            
            # Load file content
            with open(path, 'r', encoding='utf-8') as f:
                if path.suffix in ['.yml', '.yaml']:
                    content = yaml.safe_load(f)
                elif path.suffix == '.json':
                    content = json.load(f)
                else:
                    return ValidationResult(
                        is_valid=False,
                        errors=[f"Unsupported file type: {path.suffix}"],
                        prompt_id="",
                        validation_type="file"
                    )
            
            # Validate content
            prompt_id = path.stem
            return self.validate_prompt(prompt_id, content)
            
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                errors=[f"Error loading file {file_path}: {e}"],
                prompt_id="",
                validation_type="file"
            )
    
    def add_validation_rule(self, rule: ValidationRule) -> None:
        """Add a custom validation rule."""
        self.validation_rules.append(rule)
        logger.info(f"Added validation rule: {rule.name}")
    
    def get_validation_rules(self) -> List[ValidationRule]:
        """Get all registered validation rules."""
        return self.validation_rules.copy()
    
    def _register_default_rules(self) -> None:
        """Register default validation rules."""
        # Basic structure rules
        self.add_validation_rule(ValidationRule(
            name="required_metadata",
            description="Prompt must have required metadata fields",
            severity="error",
            rule_function=self._validate_required_metadata
        ))
        
        self.add_validation_rule(ValidationRule(
            name="version_format",
            description="Version must be in semantic versioning format",
            severity="error",
            rule_function=self._validate_version_format
        ))
        
        self.add_validation_rule(ValidationRule(
            name="timestamp_format",
            description="Timestamp must be in ISO format",
            severity="error",
            rule_function=self._validate_timestamp_format
        ))
    
    def _validate_required_metadata(self, prompt_id: str, content: Dict[str, Any]) -> bool:
        """Validate that required metadata fields are present."""
        required_fields = ['version', 'created_by', 'purpose']
        
        for field in required_fields:
            if field not in content:
                logger.error(f"Missing required field '{field}' in prompt {prompt_id}")
                return False
        
        return True
    
    def _validate_version_format(self, prompt_id: str, content: Dict[str, Any]) -> bool:
        """Validate version format."""
        version = content.get('version', '')
        
        # Check for semantic versioning format (x.y.z)
        if not re.match(r'^\d+\.\d+\.\d+', version):
            logger.error(f"Invalid version format '{version}' in prompt {prompt_id}")
            return False
        
        return True
    
    def _validate_timestamp_format(self, prompt_id: str, content: Dict[str, Any]) -> bool:
        """Validate timestamp format."""
        timestamp = content.get('last_updated', '')
        
        try:
            # Handle both ISO format and Z suffix
            if timestamp.endswith('Z'):
                timestamp = timestamp[:-1] + '+00:00'
            datetime.fromisoformat(timestamp)
        except (ValueError, TypeError):
            logger.error(f"Invalid timestamp format '{timestamp}' in prompt {prompt_id}")
            return False
        
        return True

def create_prompt_validator() -> PromptValidator:
    """Create a new prompt validator instance."""
    return PromptValidator() 