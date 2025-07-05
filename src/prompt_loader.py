# AI-Q Prompt Loader System
# Generated: 2025-01-27T02:55:00Z
# Created by: AI-Q Agent - Claude Sonnet 4
# Purpose: Load and manage prompts for AI-Q system

"""
Prompt loading system for AI-Q Knowledge Library System.
Handles loading, validation, and management of all prompts.
"""

import os
import yaml
import json
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PromptMetadata:
    """Metadata for a prompt file."""
    version: str
    last_updated: str
    created_by: str
    purpose: str
    file_path: str
    file_size: int
    load_time: datetime = field(default_factory=datetime.now)

@dataclass
class PromptRegistry:
    """Registry for managing loaded prompts."""
    prompts: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, PromptMetadata] = field(default_factory=dict)
    cache: Dict[str, Any] = field(default_factory=dict)
    dependencies: Dict[str, List[str]] = field(default_factory=dict)

class PromptLoader:
    """Load and manage prompts from YAML and JSON files."""
    
    def __init__(self, base_path: str = "prompts"):
        """Initialize the prompt loader."""
        self.base_path = Path(base_path)
        self.registry = PromptRegistry()
        self.supported_extensions = {'.yml', '.yaml', '.json'}
        
        # Ensure base directory exists
        self.base_path.mkdir(exist_ok=True)
        
        logger.info(f"PromptLoader initialized with base path: {self.base_path}")
    
    def load_prompt(self, file_path: str) -> Dict[str, Any]:
        """Load a single prompt file."""
        full_path = self.base_path / file_path
        
        if not full_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {full_path}")
        
        if full_path.suffix not in self.supported_extensions:
            raise ValueError(f"Unsupported file extension: {full_path.suffix}")
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                if full_path.suffix == '.json':
                    content = json.load(f)
                else:
                    content = yaml.safe_load(f)
            
            # Extract metadata
            metadata = self._extract_metadata(content, str(full_path))
            
            # Store in registry
            prompt_id = self._generate_prompt_id(file_path)
            self.registry.prompts[prompt_id] = content
            self.registry.metadata[prompt_id] = metadata
            
            logger.info(f"Loaded prompt: {prompt_id}")
            return content
            
        except Exception as e:
            logger.error(f"Error loading prompt {full_path}: {e}")
            raise
    
    def load_all_prompts(self) -> Dict[str, Any]:
        """Load all prompts from the base directory."""
        all_prompts = {}
        
        for file_path in self._find_prompt_files():
            try:
                relative_path = str(file_path.relative_to(self.base_path))
                content = self.load_prompt(relative_path)
                all_prompts[relative_path] = content
            except Exception as e:
                logger.warning(f"Failed to load {file_path}: {e}")
                continue
        
        logger.info(f"Loaded {len(all_prompts)} prompt files")
        return all_prompts
    
    def get_prompt(self, prompt_id: str) -> Optional[Dict[str, Any]]:
        """Get a prompt by ID."""
        return self.registry.prompts.get(prompt_id)
    
    def get_metadata(self, prompt_id: str) -> Optional[PromptMetadata]:
        """Get metadata for a prompt."""
        return self.registry.metadata.get(prompt_id)
    
    def list_prompts(self) -> List[str]:
        """List all loaded prompt IDs."""
        return list(self.registry.prompts.keys())
    
    def validate_prompt(self, content: Dict[str, Any]) -> bool:
        """Validate prompt content structure."""
        required_fields = ['version', 'last_updated', 'created_by', 'purpose']
        
        for field in required_fields:
            if field not in content:
                logger.error(f"Missing required field: {field}")
                return False
        
        # Validate version format
        if not isinstance(content['version'], str):
            logger.error("Version must be a string")
            return False
        
        # Validate timestamp format
        try:
            datetime.fromisoformat(content['last_updated'].replace('Z', '+00:00'))
        except ValueError:
            logger.error("Invalid timestamp format")
            return False
        
        return True
    
    def cache_prompt(self, prompt_id: str, cache_key: str, data: Any) -> None:
        """Cache data for a prompt."""
        if prompt_id not in self.registry.cache:
            self.registry.cache[prompt_id] = {}
        
        self.registry.cache[prompt_id][cache_key] = data
        logger.debug(f"Cached data for {prompt_id}:{cache_key}")
    
    def get_cached_data(self, prompt_id: str, cache_key: str) -> Optional[Any]:
        """Get cached data for a prompt."""
        return self.registry.cache.get(prompt_id, {}).get(cache_key)
    
    def add_dependency(self, prompt_id: str, dependency: str) -> None:
        """Add a dependency for a prompt."""
        if prompt_id not in self.registry.dependencies:
            self.registry.dependencies[prompt_id] = []
        
        if dependency not in self.registry.dependencies[prompt_id]:
            self.registry.dependencies[prompt_id].append(dependency)
            logger.debug(f"Added dependency {dependency} for {prompt_id}")
    
    def get_dependencies(self, prompt_id: str) -> List[str]:
        """Get dependencies for a prompt."""
        return self.registry.dependencies.get(prompt_id, [])
    
    def _find_prompt_files(self) -> List[Path]:
        """Find all prompt files in the base directory."""
        prompt_files = []
        
        for ext in self.supported_extensions:
            prompt_files.extend(self.base_path.rglob(f"*{ext}"))
        
        return sorted(prompt_files)
    
    def _extract_metadata(self, content: Dict[str, Any], file_path: str) -> PromptMetadata:
        """Extract metadata from prompt content."""
        file_stat = Path(file_path).stat()
        
        return PromptMetadata(
            version=content.get('version', '1.0'),
            last_updated=content.get('last_updated', datetime.now().isoformat()),
            created_by=content.get('created_by', 'Unknown'),
            purpose=content.get('purpose', ''),
            file_path=file_path,
            file_size=file_stat.st_size
        )
    
    def _generate_prompt_id(self, file_path: str) -> str:
        """Generate a unique prompt ID from file path."""
        # Remove extension and replace separators
        return file_path.replace('/', '_').replace('\\', '_').replace('.yml', '').replace('.yaml', '').replace('.json', '')

class PromptValidator:
    """Validate prompts for consistency and completeness."""
    
    def __init__(self, loader: PromptLoader):
        """Initialize the validator."""
        self.loader = loader
        self.validation_errors = []
        self.validation_warnings = []
    
    def validate_all_prompts(self) -> bool:
        """Validate all loaded prompts."""
        self.validation_errors = []
        self.validation_warnings = []
        
        for prompt_id in self.loader.list_prompts():
            self._validate_single_prompt(prompt_id)
        
        if self.validation_errors:
            logger.error(f"Validation failed with {len(self.validation_errors)} errors")
            for error in self.validation_errors:
                logger.error(f"  - {error}")
            return False
        
        if self.validation_warnings:
            logger.warning(f"Validation completed with {len(self.validation_warnings)} warnings")
            for warning in self.validation_warnings:
                logger.warning(f"  - {warning}")
        
        logger.info("All prompts validated successfully")
        return True
    
    def _validate_single_prompt(self, prompt_id: str) -> None:
        """Validate a single prompt."""
        content = self.loader.get_prompt(prompt_id)
        if not content:
            self.validation_errors.append(f"Prompt {prompt_id} not found")
            return
        
        # Basic structure validation
        if not self.loader.validate_prompt(content):
            self.validation_errors.append(f"Prompt {prompt_id} failed basic validation")
            return
        
        # Content-specific validation
        self._validate_prompt_content(prompt_id, content)
    
    def _validate_prompt_content(self, prompt_id: str, content: Dict[str, Any]) -> None:
        """Validate prompt content based on type."""
        # Check for common sections
        common_sections = ['agent_workflow', 'execution_sequence', 'error_handling', 'documentation']
        
        for section in common_sections:
            if section in content:
                self._validate_section(prompt_id, section, content[section])
    
    def _validate_section(self, prompt_id: str, section: str, section_content: Any) -> None:
        """Validate a specific section of a prompt."""
        if not isinstance(section_content, dict):
            self.validation_warnings.append(f"Section {section} in {prompt_id} is not a dictionary")
            return
        
        # Section-specific validation
        if section == 'agent_workflow':
            self._validate_agent_workflow(prompt_id, section_content)
        elif section == 'execution_sequence':
            self._validate_execution_sequence(prompt_id, section_content)
        elif section == 'error_handling':
            self._validate_error_handling(prompt_id, section_content)
        elif section == 'documentation':
            self._validate_documentation(prompt_id, section_content)
    
    def _validate_agent_workflow(self, prompt_id: str, workflow: Dict[str, Any]) -> None:
        """Validate agent workflow section."""
        required_fields = ['introduction_requirements', 'critical_assumptions']
        
        for field in required_fields:
            if field not in workflow:
                self.validation_warnings.append(f"Missing {field} in agent_workflow for {prompt_id}")
    
    def _validate_execution_sequence(self, prompt_id: str, sequence: Dict[str, Any]) -> None:
        """Validate execution sequence section."""
        if not sequence:
            self.validation_warnings.append(f"Empty execution_sequence in {prompt_id}")
            return
        
        # Check for at least one phase
        phases = [key for key in sequence.keys() if key.startswith('phase_')]
        if not phases:
            self.validation_warnings.append(f"No execution phases found in {prompt_id}")
    
    def _validate_error_handling(self, prompt_id: str, error_handling: Dict[str, Any]) -> None:
        """Validate error handling section."""
        required_fields = ['detection', 'recovery']
        
        for field in required_fields:
            if field not in error_handling:
                self.validation_warnings.append(f"Missing {field} in error_handling for {prompt_id}")
    
    def _validate_documentation(self, prompt_id: str, documentation: Dict[str, Any]) -> None:
        """Validate documentation section."""
        if not documentation:
            self.validation_warnings.append(f"Empty documentation section in {prompt_id}")

def create_prompt_loader(base_path: str = "prompts") -> PromptLoader:
    """Create and configure a prompt loader."""
    loader = PromptLoader(base_path)
    return loader

def create_prompt_validator(loader: PromptLoader) -> PromptValidator:
    """Create and configure a prompt validator."""
    validator = PromptValidator(loader)
    return validator

# Example usage
if __name__ == "__main__":
    # Create loader and validator
    loader = create_prompt_loader()
    validator = create_prompt_validator(loader)
    
    # Load all prompts
    prompts = loader.load_all_prompts()
    
    # Validate all prompts
    is_valid = validator.validate_all_prompts()
    
    print(f"Loaded {len(prompts)} prompts")
    print(f"Validation result: {'PASSED' if is_valid else 'FAILED'}")
    
    # List all prompts
    for prompt_id in loader.list_prompts():
        metadata = loader.get_metadata(prompt_id)
        print(f"  - {prompt_id} (v{metadata.version}, {metadata.created_by})") 