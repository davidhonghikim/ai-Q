"""
Prompt Validator Rules - Extended validation rules
=================================================

Additional validation rules for prompt content, structure, and security.

Author: kOS Kitchen System
Version: 1.0.0
Created: 2025-07-08T02:15:00Z
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ValidationRule:
    """A validation rule for prompts."""
    name: str
    description: str
    severity: str  # 'error' or 'warning'
    rule_function: callable

def create_content_structure_rule() -> ValidationRule:
    """Create a rule for validating content structure."""
    def validate_content_structure(prompt_id: str, content: Dict[str, Any]) -> bool:
        """Validate that prompt has logical content structure."""
        # Check for required sections
        required_sections = ['metadata', 'content']
        
        for section in required_sections:
            if section not in content:
                logger.warning(f"Missing section '{section}' in prompt {prompt_id}")
                return False
        
        # Validate content section
        content_section = content.get('content', {})
        if not isinstance(content_section, dict):
            logger.error(f"Content section must be a dictionary in prompt {prompt_id}")
            return False
        
        return True
    
    return ValidationRule(
        name="content_structure",
        description="Prompt must have logical content structure",
        severity="warning",
        rule_function=validate_content_structure
    )

def create_template_syntax_rule() -> ValidationRule:
    """Create a rule for validating template syntax."""
    def validate_template_syntax(prompt_id: str, content: Dict[str, Any]) -> bool:
        """Validate template syntax in prompt content."""
        def check_template_syntax(obj, path=""):
            if isinstance(obj, str):
                # Check for valid template variables {{variable}}
                template_vars = re.findall(r'\{\{([^}]+)\}\}', obj)
                for var in template_vars:
                    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', var.strip()):
                        logger.error(f"Invalid template variable '{var}' in {path}")
                        return False
            elif isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    if not check_template_syntax(value, new_path):
                        return False
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    new_path = f"{path}[{i}]"
                    if not check_template_syntax(item, new_path):
                        return False
            return True
        
        return check_template_syntax(content)
    
    return ValidationRule(
        name="template_syntax",
        description="Template syntax must be valid",
        severity="error",
        rule_function=validate_template_syntax
    )

def create_cross_references_rule() -> ValidationRule:
    """Create a rule for validating cross-references."""
    def validate_cross_references(prompt_id: str, content: Dict[str, Any]) -> bool:
        """Validate cross-references in prompt content."""
        def find_file_references(obj, path=""):
            references = []
            
            if isinstance(obj, str):
                # Look for file references
                file_refs = re.findall(r'@([a-zA-Z0-9_/.-]+)', obj)
                references.extend([(ref, path) for ref in file_refs])
            elif isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    references.extend(find_file_references(value, new_path))
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    new_path = f"{path}[{i}]"
                    references.extend(find_file_references(item, new_path))
            
            return references
        
        references = find_file_references(content)
        
        # For now, just log the references (could validate file existence later)
        for ref, path in references:
            logger.debug(f"Found reference '{ref}' at {path} in prompt {prompt_id}")
        
        return True
    
    return ValidationRule(
        name="cross_references",
        description="Cross-references must be valid",
        severity="warning",
        rule_function=validate_cross_references
    )

def create_security_rule() -> ValidationRule:
    """Create a rule for security validation."""
    def validate_security(prompt_id: str, content: Dict[str, Any]) -> bool:
        """Validate that prompt doesn't contain sensitive information."""
        sensitive_patterns = [
            r'password\s*[:=]\s*\S+',
            r'api_key\s*[:=]\s*\S+',
            r'secret\s*[:=]\s*\S+',
            r'token\s*[:=]\s*\S+',
            r'private_key\s*[:=]\s*\S+'
        ]
        
        def check_sensitive_content(obj, path=""):
            if isinstance(obj, str):
                for pattern in sensitive_patterns:
                    if re.search(pattern, obj, re.IGNORECASE):
                        logger.error(f"Potential sensitive content found at {path}")
                        return False
            elif isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    if not check_sensitive_content(value, new_path):
                        return False
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    new_path = f"{path}[{i}]"
                    if not check_sensitive_content(item, new_path):
                        return False
            return True
        
        return check_sensitive_content(content)
    
    return ValidationRule(
        name="security_validation",
        description="Prompt must not contain sensitive information",
        severity="error",
        rule_function=validate_security
    )

def get_all_validation_rules() -> List[ValidationRule]:
    """Get all available validation rules."""
    return [
        create_content_structure_rule(),
        create_template_syntax_rule(),
        create_cross_references_rule(),
        create_security_rule()
    ] 