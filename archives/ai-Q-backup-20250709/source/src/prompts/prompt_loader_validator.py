"""
Prompt Loader Validator - Validation functionality
================================================

Validation functionality for prompt loading operations.

Author: kOS Kitchen System
Version: 1.0.0
Created: 2025-07-08T02:15:00Z
"""

from typing import Dict, List, Any, Optional
import logging
from .prompt_loader_core import PromptLoader

logger = logging.getLogger(__name__)

class PromptValidator:
    """Validate prompts for consistency and completeness."""
    
    def __init__(self, loader: PromptLoader):
        """Initialize the validator."""
        self.loader = loader
        self.validation_errors = []
        self.validation_warnings = []
    
    def validate_all_prompts(self) -> Dict[str, Dict[str, List[str]]]:
        """Validate all loaded prompts."""
        results = {}
        
        for prompt_id in self.loader.list_prompts():
            self._validate_single_prompt(prompt_id)
            results[prompt_id] = {
                'errors': self.validation_errors.copy(),
                'warnings': self.validation_warnings.copy()
            }
            self.validation_errors.clear()
            self.validation_warnings.clear()
        
        return results
    
    def validate_prompt(self, prompt_id: str) -> Dict[str, List[str]]:
        """Validate a specific prompt."""
        self._validate_single_prompt(prompt_id)
        
        result = {
            'errors': self.validation_errors.copy(),
            'warnings': self.validation_warnings.copy()
        }
        
        self.validation_errors.clear()
        self.validation_warnings.clear()
        
        return result
    
    def _validate_single_prompt(self, prompt_id: str) -> None:
        """Validate a single prompt."""
        content = self.loader.get_prompt(prompt_id)
        if not content:
            self.validation_errors.append(f"Prompt {prompt_id} not found")
            return
        
        self._validate_prompt_content(prompt_id, content)
    
    def _validate_prompt_content(self, prompt_id: str, content: Dict[str, Any]) -> None:
        """Validate prompt content structure."""
        # Validate metadata
        if 'metadata' in content:
            self._validate_section(prompt_id, 'metadata', content['metadata'])
        
        # Validate content sections
        if 'content' in content:
            self._validate_section(prompt_id, 'content', content['content'])
        
        # Validate workflow if present
        if 'workflow' in content:
            self._validate_agent_workflow(prompt_id, content['workflow'])
    
    def _validate_section(self, prompt_id: str, section: str, section_content: Any) -> None:
        """Validate a content section."""
        if not isinstance(section_content, dict):
            self.validation_errors.append(f"Section '{section}' in {prompt_id} must be a dictionary")
            return
        
        # Check for required fields based on section type
        if section == 'metadata':
            required_fields = ['version', 'created_by', 'purpose']
            for field in required_fields:
                if field not in section_content:
                    self.validation_errors.append(f"Missing required field '{field}' in metadata for {prompt_id}")
    
    def _validate_agent_workflow(self, prompt_id: str, workflow: Dict[str, Any]) -> None:
        """Validate agent workflow structure."""
        if not isinstance(workflow, dict):
            self.validation_errors.append(f"Workflow in {prompt_id} must be a dictionary")
            return
        
        # Validate workflow components
        if 'steps' in workflow:
            self._validate_execution_sequence(prompt_id, workflow['steps'])
        
        if 'error_handling' in workflow:
            self._validate_error_handling(prompt_id, workflow['error_handling'])
        
        if 'documentation' in workflow:
            self._validate_documentation(prompt_id, workflow['documentation'])
    
    def _validate_execution_sequence(self, prompt_id: str, sequence: Dict[str, Any]) -> None:
        """Validate execution sequence."""
        if not isinstance(sequence, dict):
            self.validation_errors.append(f"Execution sequence in {prompt_id} must be a dictionary")
            return
        
        # Check for required sequence fields
        required_fields = ['order', 'dependencies']
        for field in required_fields:
            if field not in sequence:
                self.validation_warnings.append(f"Missing field '{field}' in execution sequence for {prompt_id}")
    
    def _validate_error_handling(self, prompt_id: str, error_handling: Dict[str, Any]) -> None:
        """Validate error handling configuration."""
        if not isinstance(error_handling, dict):
            self.validation_errors.append(f"Error handling in {prompt_id} must be a dictionary")
            return
        
        # Check for error handling strategies
        if 'strategies' not in error_handling:
            self.validation_warnings.append(f"No error handling strategies defined for {prompt_id}")
    
    def _validate_documentation(self, prompt_id: str, documentation: Dict[str, Any]) -> None:
        """Validate documentation section."""
        if not isinstance(documentation, dict):
            self.validation_errors.append(f"Documentation in {prompt_id} must be a dictionary")
            return
        
        # Check for required documentation fields
        required_fields = ['description', 'usage']
        for field in required_fields:
            if field not in documentation:
                self.validation_warnings.append(f"Missing documentation field '{field}' for {prompt_id}")

def create_prompt_validator(loader: PromptLoader) -> PromptValidator:
    """Create a new prompt validator instance."""
    return PromptValidator(loader) 