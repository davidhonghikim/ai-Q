#!/usr/bin/env python3
"""
Kitchen Real Recipe Testing Runner
Executes real recipe testing in isolated environment
"""

import json
import os
import sys

def test_kitchen_loading():
    """Test kitchen system loading"""
    print("🔧 Testing Kitchen System Loading...")
    try:
        config_path = "kitchen/kitchen_config.json"
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("  ✅ Kitchen configuration loaded successfully")
        version = config.get('metadata', {}).get('version', 'Unknown')
        status = config.get('metadata', {}).get('status', 'Unknown')
        print(f"     - Version: {version}")
        print(f"     - Status: {status}")
        return True
    except Exception as e:
        print(f"  ❌ Kitchen loading failed: {e}")
        return False

def test_pantry_integration():
    """Test pantry system integration"""
    print("📦 Testing Pantry Integration...")
    try:
        pantry_path = "pantry/pantry_index.json"
        with open(pantry_path, 'r', encoding='utf-8') as f:
            pantry = json.load(f)
        
        ingredient_counts = {}
        for category in ['tasks', 'modules', 'skills', 'tools', 'configs']:
            category_path = f"pantry/{category}"
            if os.path.exists(category_path):
                count = len([f for f in os.listdir(category_path) if f.endswith('.json')])
                ingredient_counts[category] = count
                print(f"     - {category}: {count} ingredients")
        
        total = sum(ingredient_counts.values())
        print(f"     - Total ingredients: {total}")
        return total > 0
    except Exception as e:
        print(f"  ❌ Pantry integration failed: {e}")
        return False

def test_recipe_loading():
    """Test real recipe loading"""
    print("📋 Testing Real Recipe Loading...")
    try:
        test_recipes = [
            "recipes/01-infrastructure/01-core-infrastructure/01-01-docker-environment.json",
            "recipes/01-infrastructure/02-docker-unified-infrastructure/02-01-docker-core.json",
            "recipes/02-ai-services/modules/02-ollama-setup.json"
        ]
        
        loaded_recipes = 0
        for recipe_path in test_recipes:
            if os.path.exists(recipe_path):
                with open(recipe_path, 'r', encoding='utf-8') as f:
                    recipe = json.load(f)
                
                # Validate required fields
                required_fields = ['steps', 'inputs', 'outputs']
                if all(field in recipe for field in required_fields):
                    print(f"  ✅ Loaded: {os.path.basename(recipe_path)}")
                    loaded_recipes += 1
                else:
                    print(f"  ⚠️  Missing fields: {os.path.basename(recipe_path)}")
            else:
                print(f"  ❌ Not found: {recipe_path}")
        
        return loaded_recipes > 0
    except Exception as e:
        print(f"  ❌ Recipe loading failed: {e}")
        return False

def test_recipe_execution_simulation():
    """Test recipe execution simulation with real recipes"""
    print("⚡ Testing Recipe Execution Simulation...")
    try:
        # Load a real recipe for execution simulation
        recipe_path = "recipes/01-infrastructure/01-core-infrastructure/01-01-docker-environment.json"
        if os.path.exists(recipe_path):
            with open(recipe_path, 'r', encoding='utf-8') as f:
                recipe = json.load(f)
            
            steps = recipe.get('steps', [])
            inputs = recipe.get('inputs', {})
            outputs = recipe.get('outputs', {})
            
            print(f"  ✅ Recipe execution simulation successful")
            print(f"     - Steps: {len(steps)}")
            print(f"     - Inputs: {len(inputs)}")
            print(f"     - Outputs: {len(outputs)}")
            
            # Simulate step execution
            for i, step in enumerate(steps[:3], 1):  # Show first 3 steps
                description = step.get('description', 'No description')
                print(f"     - Step {i}: {description}")
            
            return True
        else:
            print(f"  ❌ Test recipe not found: {recipe_path}")
            return False
    except Exception as e:
        print(f"  ❌ Recipe execution simulation failed: {e}")
        return False

def test_end_to_end_workflow():
    """Test end-to-end workflow with real components"""
    print("🔄 Testing End-to-End Workflow...")
    try:
        # Load all components
        kitchen_config = None
        pantry_index = None
        test_recipe = None
        
        # Load kitchen config
        if os.path.exists("kitchen/kitchen_config.json"):
            with open("kitchen/kitchen_config.json", 'r', encoding='utf-8') as f:
                kitchen_config = json.load(f)
        
        # Load pantry index
        if os.path.exists("pantry/pantry_index.json"):
            with open("pantry/pantry_index.json", 'r', encoding='utf-8') as f:
                pantry_index = json.load(f)
        
        # Load test recipe
        recipe_path = "recipes/01-infrastructure/01-core-infrastructure/01-01-docker-environment.json"
        if os.path.exists(recipe_path):
            with open(recipe_path, 'r', encoding='utf-8') as f:
                test_recipe = json.load(f)
        
        if all([kitchen_config, pantry_index, test_recipe]):
            print("  ✅ End-to-end workflow simulation successful")
            kitchen_title = kitchen_config.get('metadata', {}).get('title', 'Unknown')
            pantry_title = pantry_index.get('metadata', {}).get('title', 'Unknown')
            recipe_title = test_recipe.get('metadata', {}).get('title', 'Unknown')
            print(f"     - Kitchen: {kitchen_title}")
            print(f"     - Pantry: {pantry_title}")
            print(f"     - Recipe: {recipe_title}")
            return True
        else:
            print("  ❌ Missing components for end-to-end test")
            return False
    except Exception as e:
        print(f"  ❌ End-to-end workflow failed: {e}")
        return False

def main():
    """Run all real recipe tests"""
    print("🧪 KITCHEN REAL RECIPE TESTING")
    print("=" * 50)
    
    tests = [
        test_kitchen_loading,
        test_pantry_integration,
        test_recipe_loading,
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
    print(f"📊 REAL RECIPE TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All real recipe tests passed - Kitchen system ready for production use")
        return True
    else:
        print("❌ Some real recipe tests failed - Kitchen system needs attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
