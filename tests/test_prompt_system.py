# AI-Q Prompt System Tests
# Generated: 2025-01-27T03:10:00Z
# Created by: AI-Q Agent - Claude Sonnet 4
# Purpose: Test prompt loading and validation system

"""
Comprehensive test suite for AI-Q prompt loading and validation system.
Tests all components including loader, validator, and API endpoints.
"""

import pytest
import tempfile
import os
import yaml
import json
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch

from src.prompt_loader import PromptLoader, PromptMetadata, PromptRegistry
from src.prompt_validator import PromptValidator, ValidationResult, ValidationRule

class TestPromptLoader:
    """Test cases for PromptLoader class."""
    
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.loader = PromptLoader(self.temp_dir)
        
        # Create test prompt files
        self.create_test_prompts()
    
    def teardown_method(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_test_prompts(self):
        """Create test prompt files."""
        # Valid prompt
        valid_prompt = {
            "version": "1.0.0",
            "last_updated": "2025-01-27T03:10:00Z",
            "created_by": "Test Agent",
            "purpose": "Test prompt for validation",
            "agent_workflow": {
                "introduction_template": "I am [AGENT_NAME], [MODEL_VERSION]"
            }
        }
        
        with open(os.path.join(self.temp_dir, "valid_prompt.yml"), "w") as f:
            yaml.dump(valid_prompt, f)
        
        # Invalid prompt (missing required fields)
        invalid_prompt = {
            "version": "1.0.0",
            "purpose": "Invalid prompt"
        }
        
        with open(os.path.join(self.temp_dir, "invalid_prompt.yml"), "w") as f:
            yaml.dump(invalid_prompt, f)
        
        # JSON prompt
        json_prompt = {
            "version": "1.0.0",
            "last_updated": "2025-01-27T03:10:00Z",
            "created_by": "Test Agent",
            "purpose": "JSON test prompt",
            "execution_sequence": {
                "phase_1": "validation"
            }
        }
        
        with open(os.path.join(self.temp_dir, "json_prompt.json"), "w") as f:
            json.dump(json_prompt, f)
    
    def test_load_valid_prompt(self):
        """Test loading a valid prompt file."""
        content = self.loader.load_prompt("valid_prompt.yml")
        
        assert content is not None
        assert content["version"] == "1.0.0"
        assert content["created_by"] == "Test Agent"
        assert "agent_workflow" in content
    
    def test_load_invalid_prompt(self):
        """Test loading an invalid prompt file."""
        content = self.loader.load_prompt("invalid_prompt.yml")
        
        assert content is not None
        assert content["version"] == "1.0.0"
        assert "last_updated" not in content
    
    def test_load_json_prompt(self):
        """Test loading a JSON prompt file."""
        content = self.loader.load_prompt("json_prompt.json")
        
        assert content is not None
        assert content["version"] == "1.0.0"
        assert "execution_sequence" in content
    
    def test_load_nonexistent_prompt(self):
        """Test loading a non-existent prompt file."""
        with pytest.raises(FileNotFoundError):
            self.loader.load_prompt("nonexistent.yml")
    
    def test_load_all_prompts(self):
        """Test loading all prompts in directory."""
        prompts = self.loader.load_all_prompts()
        
        assert len(prompts) == 3
        assert "valid_prompt.yml" in prompts
        assert "invalid_prompt.yml" in prompts
        assert "json_prompt.json" in prompts
    
    def test_get_prompt(self):
        """Test getting a prompt by ID."""
        # Load prompts first
        self.loader.load_all_prompts()
        
        content = self.loader.get_prompt("valid_prompt")
        assert content is not None
        assert content["version"] == "1.0.0"
    
    def test_get_metadata(self):
        """Test getting metadata for a prompt."""
        # Load prompts first
        self.loader.load_all_prompts()
        
        metadata = self.loader.get_metadata("valid_prompt")
        assert metadata is not None
        assert metadata.version == "1.0.0"
        assert metadata.created_by == "Test Agent"
    
    def test_list_prompts(self):
        """Test listing all prompt IDs."""
        # Load prompts first
        self.loader.load_all_prompts()
        
        prompt_ids = self.loader.list_prompts()
        assert len(prompt_ids) == 3
        assert "valid_prompt" in prompt_ids
        assert "invalid_prompt" in prompt_ids
        assert "json_prompt" in prompt_ids
    
    def test_cache_prompt(self):
        """Test caching data for a prompt."""
        self.loader.cache_prompt("test_prompt", "test_key", "test_value")
        
        cached_data = self.loader.get_cached_data("test_prompt", "test_key")
        assert cached_data == "test_value"
    
    def test_add_dependency(self):
        """Test adding dependencies for a prompt."""
        self.loader.add_dependency("test_prompt", "dependency1")
        self.loader.add_dependency("test_prompt", "dependency2")
        
        dependencies = self.loader.get_dependencies("test_prompt")
        assert len(dependencies) == 2
        assert "dependency1" in dependencies
        assert "dependency2" in dependencies

class TestPromptValidator:
    """Test cases for PromptValidator class."""
    
    def setup_method(self):
        """Set up test environment."""
        self.validator = PromptValidator()
    
    def test_validate_required_metadata(self):
        """Test validation of required metadata."""
        # Valid prompt
        valid_prompt = {
            "version": "1.0.0",
            "last_updated": "2025-01-27T03:10:00Z",
            "created_by": "Test Agent",
            "purpose": "Test prompt"
        }
        
        result = self.validator._validate_required_metadata("test", valid_prompt)
        assert result is True
        
        # Invalid prompt (missing fields)
        invalid_prompt = {
            "version": "1.0.0",
            "purpose": "Test prompt"
        }
        
        result = self.validator._validate_required_metadata("test", invalid_prompt)
        assert result is False
    
    def test_validate_version_format(self):
        """Test validation of version format."""
        # Valid versions
        valid_versions = ["1.0.0", "2.1.3", "10.5.2"]
        for version in valid_versions:
            prompt = {"version": version}
            result = self.validator._validate_version_format("test", prompt)
            assert result is True
        
        # Invalid versions
        invalid_versions = ["1.0", "v1.0.0", "1.0.0.0", "1.0.0-beta"]
        for version in invalid_versions:
            prompt = {"version": version}
            result = self.validator._validate_version_format("test", prompt)
            assert result is False
    
    def test_validate_timestamp_format(self):
        """Test validation of timestamp format."""
        # Valid timestamps
        valid_timestamps = [
            "2025-01-27T03:10:00Z",
            "2025-01-27T03:10:00+00:00",
            "2025-01-27T03:10:00.123Z"
        ]
        for timestamp in valid_timestamps:
            prompt = {"last_updated": timestamp}
            result = self.validator._validate_timestamp_format("test", prompt)
            assert result is True
        
        # Invalid timestamps
        invalid_timestamps = [
            "2025-01-27",
            "invalid-timestamp",
            "2025-13-45T25:70:00Z"
        ]
        for timestamp in invalid_timestamps:
            prompt = {"last_updated": timestamp}
            result = self.validator._validate_timestamp_format("test", prompt)
            assert result is False
    
    def test_validate_content_structure(self):
        """Test validation of content structure."""
        # Valid structure
        valid_prompt = {
            "version": "1.0.0",
            "agent_workflow": {
                "introduction_template": "I am [AGENT_NAME]"
            },
            "execution_sequence": {
                "phase_1": "validation"
            }
        }
        
        result = self.validator._validate_content_structure("test", valid_prompt)
        assert result is True
        
        # Invalid structure (no common sections)
        invalid_prompt = {
            "version": "1.0.0",
            "custom_field": "value"
        }
        
        result = self.validator._validate_content_structure("test", invalid_prompt)
        assert result is False
    
    def test_validate_template_syntax(self):
        """Test validation of template syntax."""
        # Valid template
        valid_prompt = {
            "version": "1.0.0",
            "agent_workflow": {
                "introduction_template": "I am [AGENT_NAME], [MODEL_VERSION]"
            }
        }
        
        result = self.validator._validate_template_syntax("test", valid_prompt)
        assert result is True
        
        # Invalid template
        invalid_prompt = {
            "version": "1.0.0",
            "agent_workflow": {
                "introduction_template": "I am [agent-name], [model.version]"
            }
        }
        
        result = self.validator._validate_template_syntax("test", invalid_prompt)
        assert result is False
    
    def test_validate_security(self):
        """Test validation of security content."""
        # Clean prompt
        clean_prompt = {
            "version": "1.0.0",
            "agent_workflow": {
                "introduction_template": "I am [AGENT_NAME]"
            }
        }
        
        result = self.validator._validate_security("test", clean_prompt)
        assert result is True
        
        # Prompt with sensitive content
        sensitive_prompt = {
            "version": "1.0.0",
            "config": {
                "password": "secret123",
                "api_key": "sk-1234567890abcdef"
            }
        }
        
        result = self.validator._validate_security("test", sensitive_prompt)
        assert result is False
    
    def test_validate_prompt(self):
        """Test complete prompt validation."""
        # Valid prompt
        valid_prompt = {
            "version": "1.0.0",
            "last_updated": "2025-01-27T03:10:00Z",
            "created_by": "Test Agent",
            "purpose": "Test prompt",
            "agent_workflow": {
                "introduction_template": "I am [AGENT_NAME]"
            }
        }
        
        result = self.validator.validate_prompt("test", valid_prompt)
        assert result.is_valid is True
        assert len(result.errors) == 0
        
        # Invalid prompt
        invalid_prompt = {
            "version": "invalid",
            "purpose": "Test prompt"
        }
        
        result = self.validator.validate_prompt("test", invalid_prompt)
        assert result.is_valid is False
        assert len(result.errors) > 0
    
    def test_add_custom_rule(self):
        """Test adding custom validation rules."""
        def custom_rule(prompt_id: str, content: dict) -> bool:
            return "custom_field" in content
        
        rule = ValidationRule(
            name="custom_rule",
            description="Check for custom field",
            severity="warning",
            rule_function=custom_rule
        )
        
        self.validator.add_validation_rule(rule)
        
        # Test with valid content
        valid_prompt = {
            "version": "1.0.0",
            "custom_field": "value"
        }
        
        result = self.validator.validate_prompt("test", valid_prompt)
        assert len(result.warnings) == 0
        
        # Test with invalid content
        invalid_prompt = {
            "version": "1.0.0"
        }
        
        result = self.validator.validate_prompt("test", invalid_prompt)
        assert len(result.warnings) > 0

class TestPromptRegistry:
    """Test cases for PromptRegistry class."""
    
    def setup_method(self):
        """Set up test environment."""
        self.registry = PromptRegistry()
    
    def test_registry_initialization(self):
        """Test registry initialization."""
        assert self.registry.prompts == {}
        assert self.registry.metadata == {}
        assert self.registry.cache == {}
        assert self.registry.dependencies == {}
    
    def test_add_prompt(self):
        """Test adding a prompt to registry."""
        prompt_content = {"version": "1.0.0", "purpose": "test"}
        metadata = PromptMetadata(
            version="1.0.0",
            last_updated="2025-01-27T03:10:00Z",
            created_by="Test Agent",
            purpose="test",
            file_path="test.yml",
            file_size=100
        )
        
        self.registry.prompts["test"] = prompt_content
        self.registry.metadata["test"] = metadata
        
        assert "test" in self.registry.prompts
        assert "test" in self.registry.metadata
        assert self.registry.prompts["test"] == prompt_content
        assert self.registry.metadata["test"] == metadata

class TestIntegration:
    """Integration tests for prompt system."""
    
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.loader = PromptLoader(self.temp_dir)
        self.validator = PromptValidator()
        
        # Create test prompt
        self.test_prompt = {
            "version": "1.0.0",
            "last_updated": "2025-01-27T03:10:00Z",
            "created_by": "Test Agent",
            "purpose": "Integration test prompt",
            "agent_workflow": {
                "introduction_template": "I am [AGENT_NAME], [MODEL_VERSION]"
            },
            "execution_sequence": {
                "phase_1": "validation",
                "phase_2": "implementation"
            }
        }
        
        with open(os.path.join(self.temp_dir, "integration_test.yml"), "w") as f:
            yaml.dump(self.test_prompt, f)
    
    def teardown_method(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_load_and_validate(self):
        """Test loading and validating a prompt."""
        # Load prompt
        content = self.loader.load_prompt("integration_test.yml")
        assert content is not None
        
        # Validate prompt
        result = self.validator.validate_prompt("integration_test", content)
        assert result.is_valid is True
        assert len(result.errors) == 0
    
    def test_cache_and_dependencies(self):
        """Test caching and dependency management."""
        # Load prompt
        self.loader.load_prompt("integration_test.yml")
        
        # Add cache
        self.loader.cache_prompt("integration_test", "processed", True)
        
        # Add dependencies
        self.loader.add_dependency("integration_test", "core_rules")
        self.loader.add_dependency("integration_test", "agent_workflow")
        
        # Verify
        cached_data = self.loader.get_cached_data("integration_test", "processed")
        assert cached_data is True
        
        dependencies = self.loader.get_dependencies("integration_test")
        assert len(dependencies) == 2
        assert "core_rules" in dependencies
        assert "agent_workflow" in dependencies

# Performance tests
class TestPerformance:
    """Performance tests for prompt system."""
    
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.loader = PromptLoader(self.temp_dir)
        self.validator = PromptValidator()
        
        # Create multiple test prompts
        for i in range(10):
            prompt = {
                "version": "1.0.0",
                "last_updated": "2025-01-27T03:10:00Z",
                "created_by": f"Test Agent {i}",
                "purpose": f"Performance test prompt {i}",
                "agent_workflow": {
                    "introduction_template": f"I am [AGENT_NAME_{i}], [MODEL_VERSION]"
                }
            }
            
            with open(os.path.join(self.temp_dir, f"perf_test_{i}.yml"), "w") as f:
                yaml.dump(prompt, f)
    
    def teardown_method(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_load_performance(self):
        """Test loading performance with multiple prompts."""
        import time
        
        start_time = time.time()
        prompts = self.loader.load_all_prompts()
        end_time = time.time()
        
        assert len(prompts) == 10
        assert (end_time - start_time) < 1.0  # Should load in under 1 second
    
    def test_validation_performance(self):
        """Test validation performance with multiple prompts."""
        import time
        
        # Load prompts first
        self.loader.load_all_prompts()
        
        start_time = time.time()
        for prompt_id in self.loader.list_prompts():
            content = self.loader.get_prompt(prompt_id)
            self.validator.validate_prompt(prompt_id, content)
        end_time = time.time()
        
        assert (end_time - start_time) < 2.0  # Should validate in under 2 seconds

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 