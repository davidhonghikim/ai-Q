"""
Core Prompt Loader - Basic prompt loading functionality
=====================================================

Core functionality for loading and managing prompts in the AI-Q system.

Author: kOS Kitchen System
Version: 1.0.0
Created: 2025-07-08T02:15:00Z
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

def create_prompt_loader(base_path: str = "prompts") -> PromptLoader:
    """Create a new prompt loader instance."""
    return PromptLoader(base_path) 