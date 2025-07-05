# AI-Q Prompt Validator System
# Generated: 2025-01-27T03:00:00Z
# Created by: AI-Q Agent - Claude Sonnet 4
# Purpose: Validate prompts for AI-Q system

"""
Prompt validation system for AI-Q Knowledge Library System.
Handles validation of prompt structure, content, and cross-references.
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
    
    def validate_prompt_directory(self, directory_path: str) -> Dict[str, ValidationResult]:
        """Validate all prompts in a directory."""
        results = {}
        directory = Path(directory_path)
        
        if not directory.exists():
            logger.error(f"Directory not found: {directory_path}")
            return results
        
        # Find all prompt files
        prompt_files = []
        for ext in ['.yml', '.yaml', '.json']:
            prompt_files.extend(directory.rglob(f"*{ext}"))
        
        for file_path in prompt_files:
            relative_path = str(file_path.relative_to(directory))
            result = self.validate_prompt_file(str(file_path))
            results[relative_path] = result
        
        return results
    
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
        
        # Content structure rules
        self.add_validation_rule(ValidationRule(
            name="content_structure",
            description="Prompt must have logical content structure",
            severity="warning",
            rule_function=self._validate_content_structure
        ))
        
        self.add_validation_rule(ValidationRule(
            name="template_syntax",
            description="Template syntax must be valid",
            severity="error",
            rule_function=self._validate_template_syntax
        ))
        
        # Cross-reference rules
        self.add_validation_rule(ValidationRule(
            name="cross_references",
            description="Cross-references must be valid",
            severity="warning",
            rule_function=self._validate_cross_references
        ))
        
        # Security rules
        self.add_validation_rule(ValidationRule(
            name="security_validation",
            description="Prompt must not contain sensitive information",
            severity="error",
            rule_function=self._validate_security
        ))
    
    def _validate_required_metadata(self, prompt_id: str, content: Dict[str, Any]) -> bool:
        """Validate that required metadata fields are present."""
        required_fields = ['version', 'last_updated', 'created_by', 'purpose']
        
        for field in required_fields:
            if field not in content:
                logger.error(f"Missing required field '{field}' in {prompt_id}")
                return False
        
        return True
    
    def _validate_version_format(self, prompt_id: str, content: Dict[str, Any]) -> bool:
        """Validate version format."""
        version = content.get('version', '')
        if not version:
            return False
        
        # Check for semantic versioning format (x.y.z)
        version_pattern = r'^\d+\.\d+\.\d+$'
        if not re.match(version_pattern, version):
            logger.error(f"Invalid version format '{version}' in {prompt_id}")
            return False
        
        return True
    
    def _validate_timestamp_format(self, prompt_id: str, content: Dict[str, Any]) -> bool:
        """Validate timestamp format."""
        timestamp = content.get('last_updated', '')
        if not timestamp:
            return False
        
        try:
            # Handle both ISO format and ISO format with Z
            if timestamp.endswith('Z'):
                timestamp = timestamp[:-1] + '+00:00'
            datetime.fromisoformat(timestamp)
        except ValueError:
            logger.error(f"Invalid timestamp format '{timestamp}' in {prompt_id}")
            return False
        
        return True
    
    def _validate_content_structure(self, prompt_id: str, content: Dict[str, Any]) -> bool:
        """Validate content structure."""
        # Check for common sections
        common_sections = [
            'agent_workflow', 'execution_sequence', 'error_handling',
            'documentation', 'quality_assurance', 'success_criteria'
        ]
        
        found_sections = [key for key in content.keys() if key in common_sections]
        
        if not found_sections:
            logger.warning(f"No common sections found in {prompt_id}")
            return False
        
        # Validate each section
        for section in found_sections:
            if not isinstance(content[section], dict):
                logger.warning(f"Section '{section}' in {prompt_id} is not a dictionary")
                return False
        
        return True
    
    def _validate_template_syntax(self, prompt_id: str, content: Dict[str, Any]) -> bool:
        """Validate template syntax in prompts."""
        # Look for template variables in string content
        template_pattern = r'\[([A-Z_]+)\]'
        
        def check_template_syntax(obj, path=""):
            if isinstance(obj, str):
                matches = re.findall(template_pattern, obj)
                for match in matches:
                    # Validate template variable format
                    if not re.match(r'^[A-Z_]+$', match):
                        logger.error(f"Invalid template variable '{match}' in {prompt_id}{path}")
                        return False
            elif isinstance(obj, dict):
                for key, value in obj.items():
                    if not check_template_syntax(value, f"{path}.{key}"):
                        return False
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    if not check_template_syntax(item, f"{path}[{i}]"):
                        return False
            return True
        
        return check_template_syntax(content)
    
    def _validate_cross_references(self, prompt_id: str, content: Dict[str, Any]) -> bool:
        """Validate cross-references in prompts."""
        # Look for file references
        file_pattern = r'([a-zA-Z0-9_/-]+\.(yml|yaml|json|md))'
        
        def find_file_references(obj, path=""):
            references = []
            if isinstance(obj, str):
                matches = re.findall(file_pattern, obj)
                for match in matches:
                    references.append((match[0], f"{path}"))
            elif isinstance(obj, dict):
                for key, value in obj.items():
                    references.extend(find_file_references(value, f"{path}.{key}"))
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    references.extend(find_file_references(item, f"{path}[{i}]"))
            return references
        
        references = find_file_references(content)
        
        # Store cross-references for later validation
        if prompt_id not in self.cross_references:
            self.cross_references[prompt_id] = []
        
        self.cross_references[prompt_id].extend(references)
        
        return True
    
    def _validate_security(self, prompt_id: str, content: Dict[str, Any]) -> bool:
        """Validate that prompt doesn't contain sensitive information."""
        sensitive_patterns = [
            r'password\s*[:=]\s*["\'][^"\']+["\']',
            r'secret\s*[:=]\s*["\'][^"\']+["\']',
            r'key\s*[:=]\s*["\'][^"\']+["\']',
            r'token\s*[:=]\s*["\'][^"\']+["\']',
            r'api_key\s*[:=]\s*["\'][^"\']+["\']',
        ]
        
        def check_sensitive_content(obj, path=""):
            if isinstance(obj, str):
                for pattern in sensitive_patterns:
                    if re.search(pattern, obj, re.IGNORECASE):
                        logger.error(f"Potential sensitive content found in {prompt_id}{path}")
                        return False
            elif isinstance(obj, dict):
                for key, value in obj.items():
                    if not check_sensitive_content(value, f"{path}.{key}"):
                        return False
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    if not check_sensitive_content(item, f"{path}[{i}]"):
                        return False
            return True
        
        return check_sensitive_content(content)

class SchemaValidator:
    """Validate prompts against JSON schemas."""
    
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
        errors = []
        
        if schema_name not in self.schemas:
            errors.append(f"Schema '{schema_name}' not found")
            return ValidationResult(
                is_valid=False,
                errors=errors,
                validation_type=f"schema_{schema_name}"
            )
        
        try:
            # Simple schema validation (for basic cases)
            schema = self.schemas[schema_name]
            validation_result = self._validate_schema(content, schema)
            
            if not validation_result[0]:
                errors.extend(validation_result[1])
                return ValidationResult(
                    is_valid=False,
                    errors=errors,
                    validation_type=f"schema_{schema_name}"
                )
            else:
                return ValidationResult(
                    is_valid=True,
                    errors=[],
                    validation_type=f"schema_{schema_name}"
                )
                
        except Exception as e:
            errors.append(f"Schema validation error: {e}")
            return ValidationResult(
                is_valid=False,
                errors=errors,
                validation_type=f"schema_{schema_name}"
            )
    
    def _validate_schema(self, content: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Simple schema validation implementation."""
        errors = []
        
        # Check required fields
        required = schema.get('required', [])
        for field in required:
            if field not in content:
                errors.append(f"Missing required field: {field}")
        
        # Check field types
        properties = schema.get('properties', {})
        for field_name, field_schema in properties.items():
            if field_name in content:
                field_value = content[field_name]
                field_type = field_schema.get('type')
                
                if field_type == 'string' and not isinstance(field_value, str):
                    errors.append(f"Field '{field_name}' must be a string")
                elif field_type == 'object' and not isinstance(field_value, dict):
                    errors.append(f"Field '{field_name}' must be an object")
                elif field_type == 'array' and not isinstance(field_value, list):
                    errors.append(f"Field '{field_name}' must be an array")
        
        return len(errors) == 0, errors
    
    def _load_default_schemas(self) -> None:
        """Load default schemas for common prompt types."""
        # Basic prompt schema
        basic_schema = {
            "type": "object",
            "required": ["version", "last_updated", "created_by", "purpose"],
            "properties": {
                "version": {"type": "string"},
                "last_updated": {"type": "string"},
                "created_by": {"type": "string"},
                "purpose": {"type": "string"}
            }
        }
        
        self.add_schema("basic_prompt", basic_schema)
        
        # Agent workflow schema
        workflow_schema = {
            "type": "object",
            "required": ["version", "last_updated", "created_by", "purpose"],
            "properties": {
                "version": {"type": "string"},
                "last_updated": {"type": "string"},
                "created_by": {"type": "string"},
                "purpose": {"type": "string"},
                "agent_workflow": {"type": "object"},
                "execution_sequence": {"type": "object"},
                "error_handling": {"type": "object"}
            }
        }
        
        self.add_schema("agent_workflow", workflow_schema)

def create_prompt_validator() -> PromptValidator:
    """Create and configure a prompt validator."""
    return PromptValidator()

def create_schema_validator() -> SchemaValidator:
    """Create and configure a schema validator."""
    return SchemaValidator()

# Example usage
if __name__ == "__main__":
    # Create validators
    prompt_validator = create_prompt_validator()
    schema_validator = create_schema_validator()
    
    # Example prompt content
    example_prompt = {
        "version": "1.0",
        "last_updated": "2025-01-27T03:00:00Z",
        "created_by": "AI-Q Agent - Claude Sonnet 4",
        "purpose": "Example prompt for validation testing",
        "agent_workflow": {
            "introduction_template": "I am [AGENT_NAME], [MODEL_VERSION]"
        }
    }
    
    # Validate prompt
    result = prompt_validator.validate_prompt("example", example_prompt)
    
    print(f"Validation result: {'PASSED' if result.is_valid else 'FAILED'}")
    if result.errors:
        print("Errors:")
        for error in result.errors:
            print(f"  - {error}")
    if result.warnings:
        print("Warnings:")
        for warning in result.warnings:
            print(f"  - {warning}") 