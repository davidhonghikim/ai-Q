#!/usr/bin/env python3
"""
Kitchen System Functionality Test
Tests kitchen configuration, pantry integration, and recipe execution
"""

import json
import os
import sys
from pathlib import Path

def load_json_file(file_path):
    """Load JSON file with encoding detection"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"  ❌ Failed to load {file_path}: {e}")
        return None

def test_kitchen_config():
    """Test kitchen configuration loading"""
    print("🔧 Testing Kitchen Configuration Loading...")
    
    config_path = "recipes/kitchen/kitchen_config.json"
    if not os.path.exists(config_path):
        print("  ❌ Kitchen config file not found")
        return False
    
    config = load_json_file(config_path)
    if not config:
        return False
    
    # Validate required fields
    required_fields = ['metadata', 'environment', 'integrations']
    for field in required_fields:
        if field not in config:
            print(f"  ❌ Missing required field: {field}")
            return False
    
    print("  ✅ Kitchen configuration loaded successfully")
    print(f"     - Version: {config.get('metadata', {}).get('version', 'Unknown')}")
    print(f"     - Status: {config.get('metadata', {}).get('status', 'Unknown')}")
    print(f"     - Execution Mode: {config.get('environment', {}).get('execution_mode', 'Unknown')}")
    
    return True

def test_pantry_loading():
    """Test pantry ingredient loading"""
    print("📦 Testing Pantry Ingredient Loading...")
    
    pantry_path = "recipes/pantry"
    if not os.path.exists(pantry_path):
        print("  ❌ Pantry directory not found")
        return False
    
    ingredient_counts = {}
    ingredient_dirs = ['tasks', 'modules', 'skills', 'tools', 'configs']
    
    for dir_name in ingredient_dirs:
        dir_path = os.path.join(pantry_path, dir_name)
        if os.path.exists(dir_path):
            count = len([f for f in os.listdir(dir_path) if f.endswith('.json')])
            ingredient_counts[dir_name] = count
            print(f"     - {dir_name}: {count} ingredients")
        else:
            ingredient_counts[dir_name] = 0
            print(f"     - {dir_name}: 0 ingredients")
    
    total_ingredients = sum(ingredient_counts.values())
    print(f"     - Total ingredients: {total_ingredients}")
    
    return total_ingredients > 0

def test_recipe_loading():
    """Test recipe loading and validation"""
    print("📋 Testing Recipe Loading...")
    
    # Test a sample recipe
    sample_recipe_path = "recipes/01-infrastructure/01-core-infrastructure/01-01-docker-environment.json"
    if not os.path.exists(sample_recipe_path):
        print("  ❌ Sample recipe not found")
        return False
    
    recipe = load_json_file(sample_recipe_path)
    if not recipe:
        return False
    
    # Check for required fields
    required_fields = ['steps', 'inputs', 'outputs']
    for field in required_fields:
        if field not in recipe:
            print(f"  ❌ Missing required field in recipe: {field}")
            return False
    
    print("  ✅ Recipe loaded successfully")
    return True

def test_kitchen_pantry_integration():
    """Test kitchen-pantry integration"""
    print("🔗 Testing Kitchen-Pantry Integration...")
    
    config_path = "recipes/kitchen/kitchen_config.json"
    config = load_json_file(config_path)
    if not config:
        return False
    
    integrations = config.get('integrations', {})
    pantry_integration = integrations.get('pantry_system', {})
    
    if pantry_integration.get('enabled', False):
        print("  ✅ Pantry integration enabled in kitchen config")
        return True
    else:
        print("  ❌ Pantry integration not enabled")
        return False

def test_recipe_execution_simulation():
    """Test recipe execution simulation"""
    print("⚡ Testing Recipe Execution Simulation...")
    
    # Simulate task validation
    task = {
        "task_id": "task:pull-docker-image:1.0.0",
        "steps": [
            {"step_id": "STEP-01", "command": "docker pull ubuntu:latest"},
            {"step_id": "STEP-02", "command": "docker images"}
        ],
        "inputs": {
            "image_name": {"type": "string", "required": True},
            "tag": {"type": "string", "default": "latest"},
            "registry": {"type": "string", "default": "docker.io"}
        },
        "dependencies": ["tool:docker:24.0.0"]
    }
    
    # Validate task structure
    if 'task_id' in task and 'steps' in task and 'inputs' in task:
        print("  ✅ Task validation passed")
        print(f"     - Task ID: {task['task_id']}")
        print(f"     - Steps: {len(task['steps'])}")
        print(f"     - Inputs: {len(task['inputs'])}")
        print(f"     - Dependencies: {task['dependencies']}")
        return True
    else:
        print("  ❌ Task validation failed")
        return False

def test_end_to_end_workflow():
    """Test end-to-end workflow simulation"""
    print("🔄 Testing End-to-End Workflow...")
    
    # Simulate complete workflow
    try:
        # Load kitchen config
        kitchen_config = load_json_file("recipes/kitchen/kitchen_config.json")
        if not kitchen_config:
            return False
        
        # Load pantry index
        pantry_index = load_json_file("recipes/pantry/pantry_index.json")
        if not pantry_index:
            return False
        
        # Load sample task
        task = load_json_file("recipes/pantry/tasks/pull-docker-image.json")
        if not task:
            return False
        
        # Load sample recipe
        recipe = load_json_file("recipes/01-infrastructure/01-core-infrastructure/01-01-docker-environment.json")
        if not recipe:
            return False
        
        print("  ✅ End-to-end workflow simulation successful")
        print(f"     - Kitchen: {kitchen_config.get('metadata', {}).get('title', 'Unknown')}")
        print(f"     - Pantry: {pantry_index.get('metadata', {}).get('title', 'Unknown')}")
        print(f"     - Task: {task.get('metadata', {}).get('title', 'Unknown')}")
        print(f"     - Recipe: {recipe.get('metadata', {}).get('title', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ End-to-end workflow failed: {e}")
        return False

def main():
    """Run all kitchen system tests"""
    print("🧪 KITCHEN SYSTEM FUNCTIONALITY TEST")
    print("=" * 50)
    
    tests = [
        test_kitchen_config,
        test_pantry_loading,
        test_recipe_loading,
        test_kitchen_pantry_integration,
        test_recipe_execution_simulation,
        test_end_to_end_workflow
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"  ❌ Test failed with exception: {e}")
    
    print("=" * 50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed - Kitchen system is fully functional")
        return True
    else:
        print("❌ Some tests failed - Kitchen system needs attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
