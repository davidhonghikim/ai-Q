"""
Modular Pantry System Test

Comprehensive test suite for the modular pantry system components.
"""

import os
import tempfile
import shutil
import logging
from pathlib import Path
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_file_utils_operations():
    """Test file utility operations."""
    print("\n=== Testing File Utils Operations ===")
    
    # Import file utils operations
    try:
        from operations.tools.file_utils import read_file, write_file, file_exists, delete_file
        print("✓ File utils imports successful")
    except ImportError as e:
        print(f"✗ File utils import failed: {e}")
        return False
    
    # Create temporary test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        test_content = "This is a test file for pantry system validation."
        f.write(test_content)
        test_file_path = f.name
    
    try:
        # Test file_exists
        result = file_exists(test_file_path)
        if result['success'] and result['exists']:
            print("✓ file_exists operation working")
        else:
            print(f"✗ file_exists failed: {result}")
            return False
        
        # Test read_file
        result = read_file(test_file_path)
        if result['success'] and result['content'] == test_content:
            print("✓ read_file operation working")
        else:
            print(f"✗ read_file failed: {result}")
            return False
        
        # Test write_file
        new_content = "Updated test content for pantry system."
        result = write_file(test_file_path, new_content)
        if result['success']:
            print("✓ write_file operation working")
        else:
            print(f"✗ write_file failed: {result}")
            return False
        
        # Verify write worked
        result = read_file(test_file_path)
        if result['success'] and result['content'] == new_content:
            print("✓ write_file content verification successful")
        else:
            print(f"✗ write_file content verification failed: {result}")
            return False
        
        # Test delete_file
        result = delete_file(test_file_path)
        if result['success'] and result['deleted']:
            print("✓ delete_file operation working")
        else:
            print(f"✗ delete_file failed: {result}")
            return False
        
        # Verify deletion
        result = file_exists(test_file_path)
        if result['success'] and not result['exists']:
            print("✓ delete_file verification successful")
        else:
            print(f"✗ delete_file verification failed: {result}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ File utils test error: {e}")
        return False

def test_content_creator_skills():
    """Test content creator skills."""
    print("\n=== Testing Content Creator Skills ===")
    
    # Import content creator skills
    try:
        from operations.skills.content_creator import generate_content_strategy
        print("✓ Content creator imports successful")
    except ImportError as e:
        print(f"✗ Content creator import failed: {e}")
        return False
    
    try:
        # Test generate_content_strategy
        result = generate_content_strategy(
            topic="AI and Machine Learning",
            platform="twitter",
            target_audience="Tech professionals and developers",
            content_goals=["educate", "engage"],
            timeline_days=7
        )
        
        if result['success'] and 'strategy' in result:
            strategy = result['strategy']
            if (strategy['topic'] == "AI and Machine Learning" and 
                strategy['platform'] == "twitter"):
                print("✓ generate_content_strategy operation working")
            else:
                print(f"✗ generate_content_strategy returned unexpected data: {strategy}")
                return False
        else:
            print(f"✗ generate_content_strategy failed: {result}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Content creator test error: {e}")
        return False

def test_statistics_modules():
    """Test statistics modules."""
    print("\n=== Testing Statistics Modules ===")
    
    # Import statistics modules
    try:
        from operations.modules.statistics import calculate_mean
        print("✓ Statistics imports successful")
    except ImportError as e:
        print(f"✗ Statistics import failed: {e}")
        return False
    
    try:
        # Test calculate_mean with arithmetic mean
        test_data = [1, 2, 3, 4, 5]
        result = calculate_mean(test_data, 'arithmetic')
        
        if result['success'] and result['mean'] == 3.0:
            print("✓ calculate_mean (arithmetic) operation working")
        else:
            print(f"✗ calculate_mean (arithmetic) failed: {result}")
            return False
        
        # Test calculate_mean with geometric mean
        test_data = [1, 2, 4, 8]
        result = calculate_mean(test_data, 'geometric')
        
        if result['success'] and abs(result['mean'] - 2.83) < 0.1:
            print("✓ calculate_mean (geometric) operation working")
        else:
            print(f"✗ calculate_mean (geometric) failed: {result}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Statistics test error: {e}")
        return False

def test_file_processing_tasks():
    """Test file processing tasks."""
    print("\n=== Testing File Processing Tasks ===")
    
    # Import file processing tasks
    try:
        from operations.tasks.file_processing import validate_file
        print("✓ File processing imports successful")
    except ImportError as e:
        print(f"✗ File processing import failed: {e}")
        return False
    
    # Create temporary test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        test_content = '{"test": "data", "number": 42}'
        f.write(test_content)
        test_file_path = f.name
    
    try:
        # Test validate_file with basic validations
        result = validate_file(
            test_file_path,
            validations=['existence', 'readability', 'size'],
            max_size_mb=1.0
        )
        
        if result['success'] and result['overall_valid']:
            print("✓ validate_file operation working")
        else:
            print(f"✗ validate_file failed: {result}")
            return False
        
        # Test validate_file with format validation
        result = validate_file(
            test_file_path,
            validations=['format'],
            allowed_formats=['txt', 'json']
        )
        
        if result['success'] and result['overall_valid']:
            print("✓ validate_file format validation working")
        else:
            print(f"✗ validate_file format validation failed: {result}")
            return False
        
        # Clean up test file
        os.remove(test_file_path)
        return True
        
    except Exception as e:
        print(f"✗ File processing test error: {e}")
        return False

def main():
    """Run all modular pantry system tests."""
    print("============================================================")
    print("MODULAR PANTRY SYSTEM COMPREHENSIVE TEST")
    print("============================================================")
    
    test_results = []
    
    # Run all tests
    test_results.append(("File Utils Operations", test_file_utils_operations()))
    test_results.append(("Content Creator Skills", test_content_creator_skills()))
    test_results.append(("Statistics Modules", test_statistics_modules()))
    test_results.append(("File Processing Tasks", test_file_processing_tasks()))
    
    # Print summary
    print("\n============================================================")
    print("TEST SUMMARY")
    print("============================================================")
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "PASSED" if result else "FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Modular pantry system is working correctly!")
        return True
    else:
        print("❌ Some tests failed - Modular pantry system needs attention.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 