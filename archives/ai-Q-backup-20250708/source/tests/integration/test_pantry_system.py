#!/usr/bin/env python3
"""
Comprehensive Test Script for Pantry System

Tests all components of the pantry system to ensure they work correctly together.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all components
from operations.tools.text_file_operations import TextFileOperations
from operations.tools.binary_file_operations import BinaryFileOperations
from operations.tools.file_system_operations import FileSystemOperations
from operations.registry import OperationRegistry
from operations.context_manager import ContextManager

def test_imports():
    """Test that all components can be imported successfully"""
    print("Testing imports...")
    
    try:
        # Test that classes can be instantiated
        text_ops = TextFileOperations()
        print("✓ TextFileOperations instantiated successfully")
    except Exception as e:
        print(f"✗ TextFileOperations instantiation failed: {e}")
        return False
    
    try:
        binary_ops = BinaryFileOperations()
        print("✓ BinaryFileOperations instantiated successfully")
    except Exception as e:
        print(f"✗ BinaryFileOperations instantiation failed: {e}")
        return False
    
    try:
        fs_ops = FileSystemOperations()
        print("✓ FileSystemOperations instantiated successfully")
    except Exception as e:
        print(f"✗ FileSystemOperations instantiation failed: {e}")
        return False
    
    try:
        registry = OperationRegistry()
        print("✓ OperationRegistry instantiated successfully")
    except Exception as e:
        print(f"✗ OperationRegistry instantiation failed: {e}")
        return False
    
    try:
        context_manager = ContextManager()
        print("✓ ContextManager instantiated successfully")
    except Exception as e:
        print(f"✗ ContextManager instantiation failed: {e}")
        return False
    
    return True

def test_text_file_operations():
    """Test text file operations"""
    print("\nTesting TextFileOperations...")
    
    text_ops = TextFileOperations()
    test_content = "Hello, World!\nThis is a test file.\n"
    
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = Path(temp_dir) / "test.txt"
        
        # Test write
        result = text_ops.write_text_file(str(test_file), test_content)
        if result['success']:
            print("✓ Text file write successful")
        else:
            print(f"✗ Text file write failed: {result['error']}")
            return False
        
        # Test read
        result = text_ops.read_text_file(str(test_file))
        if result['success'] and result['content'] == test_content:
            print("✓ Text file read successful")
        else:
            print(f"✗ Text file read failed: {result.get('error', 'Content mismatch')}")
            return False
        
        # Test JSON operations
        json_data = {"test": "data", "number": 42}
        json_file = Path(temp_dir) / "test.json"
        
        result = text_ops.write_json_file(str(json_file), json_data)
        if result['success']:
            print("✓ JSON file write successful")
        else:
            print(f"✗ JSON file write failed: {result['error']}")
            return False
        
        result = text_ops.read_json_file(str(json_file))
        if result['success'] and result['data'] == json_data:
            print("✓ JSON file read successful")
        else:
            print(f"✗ JSON file read failed: {result.get('error', 'Data mismatch')}")
            return False
    
    return True

def test_binary_file_operations():
    """Test binary file operations"""
    print("\nTesting BinaryFileOperations...")
    
    binary_ops = BinaryFileOperations()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test binary file
        test_file = Path(temp_dir) / "test.bin"
        test_data = b"Hello, Binary World!"
        
        with open(test_file, 'wb') as f:
            f.write(test_data)
        
        # Test file info
        result = binary_ops.get_file_info(str(test_file))
        if result['success']:
            print("✓ Binary file info successful")
        else:
            print(f"✗ Binary file info failed: {result['error']}")
            return False
        
        # Test file validation
        result = binary_ops.validate_file_format(str(test_file))
        if result['success']:
            print("✓ Binary file validation successful")
        else:
            print(f"✗ Binary file validation failed: {result['error']}")
            return False
        
        # Test file copy
        copy_file = Path(temp_dir) / "test_copy.bin"
        result = binary_ops.copy_binary_file(str(test_file), str(copy_file))
        if result['success'] and copy_file.exists():
            print("✓ Binary file copy successful")
        else:
            print(f"✗ Binary file copy failed: {result.get('error', 'File not created')}")
            return False
    
    return True

def test_file_system_operations():
    """Test file system operations"""
    print("\nTesting FileSystemOperations...")
    
    fs_ops = FileSystemOperations()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Test directory creation
        test_dir = temp_path / "test_dir"
        result = fs_ops.create_directory(str(test_dir))
        if result['success']:
            print("✓ Directory creation successful")
        else:
            print(f"✗ Directory creation failed: {result['error']}")
            return False
        
        # Test directory listing
        result = fs_ops.list_directory(str(temp_path))
        if result['success'] and len(result['directories']) > 0:
            print("✓ Directory listing successful")
        else:
            print(f"✗ Directory listing failed: {result.get('error', 'No directories found')}")
            return False
        
        # Test directory size
        result = fs_ops.get_directory_size(str(temp_path))
        if result['success']:
            print("✓ Directory size calculation successful")
        else:
            print(f"✗ Directory size calculation failed: {result['error']}")
            return False
        
        # Test file move
        source_file = temp_path / "source.txt"
        dest_file = test_dir / "dest.txt"
        
        with open(source_file, 'w') as f:
            f.write("Test content")
        
        result = fs_ops.move_file(str(source_file), str(dest_file))
        if result['success'] and dest_file.exists() and not source_file.exists():
            print("✓ File move successful")
        else:
            print(f"✗ File move failed: {result.get('error', 'File not moved correctly')}")
            return False
    
    return True

def test_registry():
    """Test operation registry"""
    print("\nTesting OperationRegistry...")
    
    try:
        registry = OperationRegistry()
        print("✓ OperationRegistry instantiated successfully")
        
        # Test discovery
        operations = registry.discover_operations()
        if operations:
            print(f"✓ Discovered {len(operations)} operations")
        else:
            print("⚠ No operations discovered (this may be normal)")
        
        return True
    except Exception as e:
        print(f"✗ OperationRegistry test failed: {e}")
        return False

def test_context_manager():
    """Test context manager"""
    print("\nTesting ContextManager...")
    
    try:
        context_manager = ContextManager()
        print("✓ ContextManager instantiated successfully")
        
        # Test context creation
        context = context_manager.create_context({
            'required_tools': ['text_file_operations'],
            'required_skills': [],
            'required_modules': []
        })
        
        if context:
            print("✓ Context creation successful")
        else:
            print("✗ Context creation failed")
            return False
        
        return True
    except Exception as e:
        print(f"✗ ContextManager test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("PANTRY SYSTEM COMPREHENSIVE TEST")
    print("=" * 60)
    
    tests = [
        ("Import Tests", test_imports),
        ("Text File Operations", test_text_file_operations),
        ("Binary File Operations", test_binary_file_operations),
        ("File System Operations", test_file_system_operations),
        ("Operation Registry", test_registry),
        ("Context Manager", test_context_manager)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Pantry system is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 