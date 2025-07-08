"""
Prompt Loader Batch - Batch loading functionality
===============================================

Batch loading and validation functionality for prompts.

Author: kOS Kitchen System
Version: 1.0.0
Created: 2025-07-08T02:15:00Z
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
import logging
from .prompt_loader_core import PromptLoader

logger = logging.getLogger(__name__)

class BatchPromptLoader:
    """Handle batch loading of prompts."""
    
    def __init__(self, loader: PromptLoader):
        """Initialize the batch loader."""
        self.loader = loader
    
    def load_all_prompts(self) -> Dict[str, Any]:
        """Load all prompts from the base directory."""
        all_prompts = {}
        
        for file_path in self._find_prompt_files():
            try:
                relative_path = str(file_path.relative_to(self.loader.base_path))
                content = self.loader.load_prompt(relative_path)
                all_prompts[relative_path] = content
            except Exception as e:
                logger.warning(f"Failed to load {file_path}: {e}")
                continue
        
        logger.info(f"Loaded {len(all_prompts)} prompt files")
        return all_prompts
    
    def load_prompts_by_pattern(self, pattern: str) -> Dict[str, Any]:
        """Load prompts matching a specific pattern."""
        matching_prompts = {}
        
        for file_path in self._find_prompt_files():
            if pattern in file_path.name:
                try:
                    relative_path = str(file_path.relative_to(self.loader.base_path))
                    content = self.loader.load_prompt(relative_path)
                    matching_prompts[relative_path] = content
                except Exception as e:
                    logger.warning(f"Failed to load {file_path}: {e}")
                    continue
        
        logger.info(f"Loaded {len(matching_prompts)} prompts matching pattern '{pattern}'")
        return matching_prompts
    
    def validate_all_prompts(self) -> Dict[str, bool]:
        """Validate all loaded prompts."""
        validation_results = {}
        
        for prompt_id in self.loader.list_prompts():
            content = self.loader.get_prompt(prompt_id)
            if content:
                is_valid = self.loader.validate_prompt(content)
                validation_results[prompt_id] = is_valid
                
                if not is_valid:
                    logger.warning(f"Prompt {prompt_id} failed validation")
        
        valid_count = sum(validation_results.values())
        total_count = len(validation_results)
        
        logger.info(f"Validation complete: {valid_count}/{total_count} prompts valid")
        return validation_results
    
    def _find_prompt_files(self) -> List[Path]:
        """Find all prompt files in the base directory."""
        prompt_files = []
        
        for ext in self.loader.supported_extensions:
            prompt_files.extend(self.loader.base_path.rglob(f"*{ext}"))
        
        return sorted(prompt_files)

def create_batch_loader(loader: PromptLoader) -> BatchPromptLoader:
    """Create a new batch loader instance."""
    return BatchPromptLoader(loader) 