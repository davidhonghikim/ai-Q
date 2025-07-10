"""
Unit tests for modular file operations

Tests each file operation module independently.
"""

import pytest
import tempfile
import os
from pathlib import Path
from kitchen.pantry.operations.tools.file_reader import FileReader
from kitchen.pantry.operations.tools.file_writer import FileWriter
from kitchen.pantry.operations.tools.file_checker import FileChecker
from kitchen.pantry.operations.tools.file_deleter import FileDeleter
from kitchen.pantry.operations.tools.file_copier import FileCopier
from kitchen.pantry.operations.tools.directory_lister import DirectoryLister

class TestFileReader:
    """Test file reading operations"""
    
    def test_read_text_file(self):
        """Test reading a text file"""
        reader = FileReader()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Hello, World!")
            temp_file = f.name
        
        try:
            result = reader.read_file(temp_file)
            assert result['success'] is True
            assert result['content'] == "Hello, World!"
            assert result['content_type'] == 'text'
        finally:
            os.unlink(temp_file)
    
    def test_read_nonexistent_file(self):
        """Test reading a file that doesn't exist"""
        reader = FileReader()
        result = reader.read_file("/nonexistent/file.txt")
        assert result['success'] is False
        assert "File not found" in result['error']

class TestFileWriter:
    """Test file writing operations"""
    
    def test_write_text_file(self):
        """Test writing a text file"""
        writer = FileWriter()
        
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            temp_file = f.name
        
        try:
            result = writer.write_file(temp_file, "Test content")
            assert result['success'] is True
            assert result['content_type'] == 'text'
            assert result['file_size'] > 0
            
            # Verify content was written
            with open(temp_file, 'r') as f:
                content = f.read()
            assert content == "Test content"
        finally:
            os.unlink(temp_file)
    
    def test_write_binary_file(self):
        """Test writing a binary file"""
        writer = FileWriter()
        
        with tempfile.NamedTemporaryFile(suffix='.bin', delete=False) as f:
            temp_file = f.name
        
        try:
            binary_content = b"Binary test content"
            result = writer.write_file(temp_file, binary_content)
            assert result['success'] is True
            assert result['content_type'] == 'binary'
            assert result['file_size'] == len(binary_content)
        finally:
            os.unlink(temp_file)

class TestFileChecker:
    """Test file checking operations"""
    
    def test_file_exists(self):
        """Test checking if file exists"""
        checker = FileChecker()
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_file = f.name
        
        try:
            result = checker.file_exists(temp_file)
            assert result['success'] is True
            assert result['exists'] is True
            assert result['file_size'] >= 0  # Empty files have size 0
        finally:
            os.unlink(temp_file)
    
    def test_file_not_exists(self):
        """Test checking if file doesn't exist"""
        checker = FileChecker()
        result = checker.file_exists("/nonexistent/file.txt")
        assert result['success'] is True
        assert result['exists'] is False
    
    def test_get_file_info(self):
        """Test getting file information"""
        checker = FileChecker()
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_file = f.name
        
        try:
            result = checker.get_file_info(temp_file)
            assert result['success'] is True
            assert result['file_name'] == Path(temp_file).name
            assert result['file_size'] >= 0  # Empty files have size 0
            assert result['is_file'] is True
            assert result['is_dir'] is False
        finally:
            os.unlink(temp_file)

class TestFileDeleter:
    """Test file deletion operations"""
    
    def test_delete_file(self):
        """Test deleting a file"""
        deleter = FileDeleter()
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_file = f.name
        
        # Verify file exists
        assert os.path.exists(temp_file)
        
        # Delete the file
        result = deleter.delete_file(temp_file)
        assert result['success'] is True
        assert result['deleted_size'] >= 0  # Empty files have size 0
        
        # Verify file is gone
        assert not os.path.exists(temp_file)
    
    def test_delete_nonexistent_file(self):
        """Test deleting a file that doesn't exist"""
        deleter = FileDeleter()
        result = deleter.delete_file("/nonexistent/file.txt")
        assert result['success'] is False
        assert "File not found" in result['error']

class TestFileCopier:
    """Test file copying operations"""
    
    def test_copy_file(self):
        """Test copying a file"""
        copier = FileCopier()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("Test content")
            source_file = f.name
        
        dest_file = source_file + ".copy"
        
        try:
            # Copy the file
            result = copier.copy_file(source_file, dest_file)
            assert result['success'] is True
            assert result['copy_successful'] is True
            assert result['source_size'] == result['dest_size']
            
            # Verify content was copied
            with open(dest_file, 'r') as f:
                content = f.read()
            assert content == "Test content"
        finally:
            os.unlink(source_file)
            if os.path.exists(dest_file):
                os.unlink(dest_file)

class TestDirectoryLister:
    """Test directory listing operations"""
    
    def test_list_directory(self):
        """Test listing directory contents"""
        lister = DirectoryLister()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create some test files
            test_file1 = os.path.join(temp_dir, "test1.txt")
            test_file2 = os.path.join(temp_dir, "test2.txt")
            
            with open(test_file1, 'w') as f:
                f.write("Test 1")
            with open(test_file2, 'w') as f:
                f.write("Test 2")
            
            result = lister.list_directory(temp_dir)
            assert result['success'] is True
            assert result['total_files'] == 2
            assert result['total_directories'] == 0
            
            # Check file names
            file_names = [f['name'] for f in result['files']]
            assert "test1.txt" in file_names
            assert "test2.txt" in file_names 