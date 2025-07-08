"""
Test File Operations - Verify All Components Work

Simple test to verify that all file operation components work correctly.
"""

import sys
import os
from pathlib import Path

# Add the tools directory to the path
sys.path.append(os.path.dirname(__file__))

def test_file_operations():
    """Test all file operation components"""
    print("Testing File Operations Components...")
    
    # Test text file operations
    try:
        from text_file_operations import text_file_operations
        print("✓ Text file operations imported successfully")
        
        # Test writing a text file
        test_content = "This is a test file for pantry operations."
        result = text_file_operations.write_text_file("test_output.txt", test_content)
        if result['success']:
            print("✓ Text file write operation successful")
        else:
            print("✗ Text file write operation failed:", result['error'])
            
    except Exception as e:
        print("✗ Text file operations import failed:", e)
    
    # Test binary file operations
    try:
        from binary_file_operations import binary_file_operations
        print("✓ Binary file operations imported successfully")
        
        # Test getting file info
        result = binary_file_operations.get_file_info("test_output.txt")
        if result['success']:
            print("✓ Binary file info operation successful")
        else:
            print("✗ Binary file info operation failed:", result['error'])
            
    except Exception as e:
        print("✗ Binary file operations import failed:", e)
    
    # Test file system operations
    try:
        from file_system_operations import file_system_operations
        print("✓ File system operations imported successfully")
        
        # Test listing directory
        result = file_system_operations.list_directory(".", "*.py")
        if result['success']:
            print(f"✓ File system list operation successful - found {result['total_files']} Python files")
        else:
            print("✗ File system list operation failed:", result['error'])
            
    except Exception as e:
        print("✗ File system operations import failed:", e)
    
    # Clean up test file
    try:
        if Path("test_output.txt").exists():
            Path("test_output.txt").unlink()
            print("✓ Test file cleaned up")
    except Exception as e:
        print("✗ Test file cleanup failed:", e)
    
    print("\nFile Operations Test Complete!")

if __name__ == "__main__":
    test_file_operations() 