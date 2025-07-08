#!/usr/bin/env python3
"""
Test Kitchen System Structure
=============================

Comprehensive test script for the new kOS kitchen system structure.
Tests the kitchen engine, pantry system, and recipe system integration.

Author: kOS Kitchen System
Version: 1.0.0
Created: 2025-07-08T02:00:00Z
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add kitchen to path
sys.path.insert(0, str(Path(__file__).parent / "kitchen"))

def setup_logging() -> logging.Logger:
    """Setup logging for tests."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('logs/kitchen_test.log')
        ]
    )
    return logging.getLogger('kitchen_test')

def test_directory_structure() -> Dict[str, Any]:
    """Test that the kitchen directory structure is correct."""
    logger = logging.getLogger('kitchen_test')
    logger.info("Testing kitchen directory structure")
    
    results = {
        "test": "directory_structure",
        "status": "running",
        "errors": [],
        "warnings": [],
        "details": {}
    }
    
    kitchen_path = Path("kitchen")
    required_dirs = ["core", "pantry", "recipes", "schemas", "config"]
    required_files = [
        "README.json",
        "core/__init__.py",
        "core/kitchen_engine.py",
        "config/kitchen_config.json"
    ]
    
    # Check kitchen directory exists
    if not kitchen_path.exists():
        results["errors"].append("kitchen directory does not exist")
        results["status"] = "failed"
        return results
    
    # Check required directories
    for dir_name in required_dirs:
        dir_path = kitchen_path / dir_name
        if dir_path.exists():
            results["details"][f"dir_{dir_name}"] = "exists"
        else:
            results["errors"].append(f"Required directory missing: {dir_name}")
    
    # Check required files
    for file_path in required_files:
        full_path = kitchen_path / file_path
        if full_path.exists():
            results["details"][f"file_{file_path}"] = "exists"
        else:
            results["errors"].append(f"Required file missing: {file_path}")
    
    # Check pantry structure
    pantry_path = kitchen_path / "pantry"
    if pantry_path.exists():
        pantry_dirs = ["ingredients", "operations", "core"]
        for dir_name in pantry_dirs:
            dir_path = pantry_path / dir_name
            if dir_path.exists():
                results["details"][f"pantry_{dir_name}"] = "exists"
            else:
                results["warnings"].append(f"Pantry directory missing: {dir_name}")
    
    # Check recipes structure
    recipes_path = kitchen_path / "recipes"
    if recipes_path.exists():
        recipe_dirs = ["01-infrastructure", "02-ai-services", "03-intelligence", "examples"]
        for dir_name in recipe_dirs:
            dir_path = recipes_path / dir_name
            if dir_path.exists():
                results["details"][f"recipes_{dir_name}"] = "exists"
            else:
                results["warnings"].append(f"Recipe directory missing: {dir_name}")
    
    # Determine final status
    if results["errors"]:
        results["status"] = "failed"
    elif results["warnings"]:
        results["status"] = "warning"
    else:
        results["status"] = "passed"
    
    logger.info(f"Directory structure test: {results['status']}")
    return results

def test_kitchen_engine_import() -> Dict[str, Any]:
    """Test that the kitchen engine can be imported."""
    logger = logging.getLogger('kitchen_test')
    logger.info("Testing kitchen engine import")
    
    results = {
        "test": "kitchen_engine_import",
        "status": "running",
        "errors": [],
        "warnings": [],
        "details": {}
    }
    
    try:
        from kitchen.core import KitchenEngine
        results["details"]["import"] = "successful"
        results["status"] = "passed"
        logger.info("Kitchen engine import successful")
    except ImportError as e:
        results["errors"].append(f"Import failed: {e}")
        results["status"] = "failed"
        logger.error(f"Kitchen engine import failed: {e}")
    except Exception as e:
        results["errors"].append(f"Unexpected error: {e}")
        results["status"] = "failed"
        logger.error(f"Unexpected error during import: {e}")
    
    return results

def test_kitchen_engine_initialization() -> Dict[str, Any]:
    """Test that the kitchen engine can be initialized."""
    logger = logging.getLogger('kitchen_test')
    logger.info("Testing kitchen engine initialization")
    
    results = {
        "test": "kitchen_engine_initialization",
        "status": "running",
        "errors": [],
        "warnings": [],
        "details": {}
    }
    
    try:
        from kitchen.core import KitchenEngine
        
        # Test initialization
        engine = KitchenEngine()
        results["details"]["initialization"] = "successful"
        
        # Test configuration loading
        if hasattr(engine, 'config'):
            results["details"]["config_loaded"] = "successful"
        else:
            results["warnings"].append("Configuration not loaded")
        
        # Test registry initialization
        if hasattr(engine, 'registry'):
            results["details"]["registry_initialized"] = "successful"
        else:
            results["warnings"].append("Registry not initialized")
        
        # Test context manager initialization
        if hasattr(engine, 'context_manager'):
            results["details"]["context_manager_initialized"] = "successful"
        else:
            results["warnings"].append("Context manager not initialized")
        
        results["status"] = "passed"
        logger.info("Kitchen engine initialization successful")
        
    except Exception as e:
        results["errors"].append(f"Initialization failed: {e}")
        results["status"] = "failed"
        logger.error(f"Kitchen engine initialization failed: {e}")
    
    return results

def test_pantry_system() -> Dict[str, Any]:
    """Test the pantry system structure and components."""
    logger = logging.getLogger('kitchen_test')
    logger.info("Testing pantry system")
    
    results = {
        "test": "pantry_system",
        "status": "running",
        "errors": [],
        "warnings": [],
        "details": {}
    }
    
    pantry_path = Path("kitchen/pantry")
    
    if not pantry_path.exists():
        results["errors"].append("Pantry directory does not exist")
        results["status"] = "failed"
        return results
    
    # Check pantry core components
    core_path = pantry_path / "core"
    if core_path.exists():
        core_files = [
            "pantry_manager.py",
            "ingredient_registry.py", 
            "resource_storage.py",
            "dependency_tracker.py",
            "access_control.py",
            "discovery_engine.py",
            "validation_system.py"
        ]
        
        for file_name in core_files:
            file_path = core_path / file_name
            if file_path.exists():
                results["details"][f"core_{file_name}"] = "exists"
            else:
                results["warnings"].append(f"Core file missing: {file_name}")
    
    # Check pantry operations
    operations_path = pantry_path / "operations"
    if operations_path.exists():
        operation_dirs = ["tools", "skills", "modules", "tasks"]
        for dir_name in operation_dirs:
            dir_path = operations_path / dir_name
            if dir_path.exists():
                results["details"][f"operations_{dir_name}"] = "exists"
                
                # Check for __init__.py files
                init_file = dir_path / "__init__.py"
                if init_file.exists():
                    results["details"][f"operations_{dir_name}_init"] = "exists"
                else:
                    results["warnings"].append(f"Missing __init__.py in operations/{dir_name}")
            else:
                results["warnings"].append(f"Operations directory missing: {dir_name}")
    
    # Check pantry ingredients
    ingredients_path = pantry_path / "ingredients"
    if ingredients_path.exists():
        ingredient_dirs = ["tools", "skills", "modules", "tasks", "configs", "schemas"]
        for dir_name in ingredient_dirs:
            dir_path = ingredients_path / dir_name
            if dir_path.exists():
                results["details"][f"ingredients_{dir_name}"] = "exists"
                
                # Count ingredient files
                ingredient_files = list(dir_path.glob("*.json"))
                results["details"][f"ingredients_{dir_name}_count"] = len(ingredient_files)
            else:
                results["warnings"].append(f"Ingredients directory missing: {dir_name}")
    
    # Determine final status
    if results["errors"]:
        results["status"] = "failed"
    elif results["warnings"]:
        results["status"] = "warning"
    else:
        results["status"] = "passed"
    
    logger.info(f"Pantry system test: {results['status']}")
    return results

def test_recipe_system() -> Dict[str, Any]:
    """Test the recipe system structure."""
    logger = logging.getLogger('kitchen_test')
    logger.info("Testing recipe system")
    
    results = {
        "test": "recipe_system",
        "status": "running",
        "errors": [],
        "warnings": [],
        "details": {}
    }
    
    recipes_path = Path("kitchen/recipes")
    
    if not recipes_path.exists():
        results["errors"].append("Recipes directory does not exist")
        results["status"] = "failed"
        return results
    
    # Check recipe categories
    recipe_categories = [
        "01-infrastructure",
        "02-ai-services", 
        "03-intelligence",
        "04-ai-agent-integration",
        "04-interface",
        "05-development-automation",
        "06-content-processing",
        "07-content-creation-workflows",
        "08-research-automation",
        "09-knowledge-synthesis",
        "10-collaboration-platform",
        "10-interface",
        "11-quality-assurance",
        "12-advanced-interfaces",
        "13-deployment",
        "14-monitoring-alerting",
        "15-backup-recovery",
        "16-scaling-optimization",
        "17-deployment-automation",
        "examples"
    ]
    
    for category in recipe_categories:
        category_path = recipes_path / category
        if category_path.exists():
            results["details"][f"recipe_category_{category}"] = "exists"
            
            # Count recipe files
            recipe_files = list(category_path.glob("*.json"))
            results["details"][f"recipe_category_{category}_count"] = len(recipe_files)
        else:
            results["warnings"].append(f"Recipe category missing: {category}")
    
    # Check for main recipe index
    index_file = recipes_path / "00-RECIPE_INDEX.json"
    if index_file.exists():
        results["details"]["recipe_index"] = "exists"
    else:
        results["warnings"].append("Recipe index file missing")
    
    # Determine final status
    if results["errors"]:
        results["status"] = "failed"
    elif results["warnings"]:
        results["status"] = "warning"
    else:
        results["status"] = "passed"
    
    logger.info(f"Recipe system test: {results['status']}")
    return results

def test_configuration_files() -> Dict[str, Any]:
    """Test configuration files."""
    logger = logging.getLogger('kitchen_test')
    logger.info("Testing configuration files")
    
    results = {
        "test": "configuration_files",
        "status": "running",
        "errors": [],
        "warnings": [],
        "details": {}
    }
    
    config_path = Path("kitchen/config")
    
    if not config_path.exists():
        results["errors"].append("Config directory does not exist")
        results["status"] = "failed"
        return results
    
    # Check main configuration file
    kitchen_config = config_path / "kitchen_config.json"
    if kitchen_config.exists():
        try:
            with open(kitchen_config, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Validate configuration structure
            required_sections = ["kitchen", "pantry", "recipes", "logging"]
            for section in required_sections:
                if section in config_data:
                    results["details"][f"config_section_{section}"] = "exists"
                else:
                    results["warnings"].append(f"Configuration section missing: {section}")
            
            results["details"]["kitchen_config_valid"] = "valid_json"
        except json.JSONDecodeError as e:
            results["errors"].append(f"Invalid JSON in kitchen_config.json: {e}")
        except Exception as e:
            results["errors"].append(f"Error reading kitchen_config.json: {e}")
    else:
        results["errors"].append("kitchen_config.json does not exist")
    
    # Determine final status
    if results["errors"]:
        results["status"] = "failed"
    elif results["warnings"]:
        results["status"] = "warning"
    else:
        results["status"] = "passed"
    
    logger.info(f"Configuration files test: {results['status']}")
    return results

def run_all_tests() -> Dict[str, Any]:
    """Run all kitchen system tests."""
    logger = setup_logging()
    logger.info("Starting kitchen system tests")
    
    # Create logs directory
    Path("logs").mkdir(exist_ok=True)
    
    tests = [
        test_directory_structure,
        test_kitchen_engine_import,
        test_kitchen_engine_initialization,
        test_pantry_system,
        test_recipe_system,
        test_configuration_files
    ]
    
    results = {
        "test_suite": "kitchen_system_structure",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "total_tests": len(tests),
        "passed": 0,
        "failed": 0,
        "warnings": 0,
        "test_results": []
    }
    
    for test_func in tests:
        try:
            test_result = test_func()
            results["test_results"].append(test_result)
            
            if test_result["status"] == "passed":
                results["passed"] += 1
            elif test_result["status"] == "failed":
                results["failed"] += 1
            elif test_result["status"] == "warning":
                results["warnings"] += 1
                
        except Exception as e:
            logger.error(f"Test {test_func.__name__} failed with exception: {e}")
            error_result = {
                "test": test_func.__name__,
                "status": "failed",
                "errors": [f"Test exception: {e}"],
                "warnings": [],
                "details": {}
            }
            results["test_results"].append(error_result)
            results["failed"] += 1
    
    # Overall status
    if results["failed"] > 0:
        results["overall_status"] = "failed"
    elif results["warnings"] > 0:
        results["overall_status"] = "warning"
    else:
        results["overall_status"] = "passed"
    
    # Log summary
    logger.info(f"Test suite completed: {results['overall_status']}")
    logger.info(f"Passed: {results['passed']}, Failed: {results['failed']}, Warnings: {results['warnings']}")
    
    # Save results
    with open("logs/kitchen_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    return results

def print_summary(results: Dict[str, Any]) -> None:
    """Print a summary of test results."""
    print("\n" + "="*60)
    print("KITCHEN SYSTEM TEST RESULTS")
    print("="*60)
    print(f"Overall Status: {results['overall_status'].upper()}")
    print(f"Total Tests: {results['total_tests']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Warnings: {results['warnings']}")
    print(f"Timestamp: {results['timestamp']}")
    print("="*60)
    
    for test_result in results["test_results"]:
        status_symbol = {
            "passed": "✓",
            "failed": "✗", 
            "warning": "⚠",
            "running": "⟳"
        }.get(test_result["status"], "?")
        
        print(f"{status_symbol} {test_result['test']}: {test_result['status']}")
        
        if test_result["errors"]:
            for error in test_result["errors"]:
                print(f"    ERROR: {error}")
        
        if test_result["warnings"]:
            for warning in test_result["warnings"]:
                print(f"    WARNING: {warning}")
    
    print("="*60)
    print(f"Detailed results saved to: logs/kitchen_test_results.json")

if __name__ == "__main__":
    results = run_all_tests()
    print_summary(results)
    
    # Exit with appropriate code
    if results["overall_status"] == "failed":
        sys.exit(1)
    elif results["overall_status"] == "warning":
        sys.exit(2)
    else:
        sys.exit(0) 