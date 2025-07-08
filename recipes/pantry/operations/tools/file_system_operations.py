"""
File System Operations - Focused Component

Handles file system operations for directories, file management, and system operations.
Supports directory creation, listing, deletion, and file system utilities.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FileSystemOperations:
    """File system operations for directories and file management"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.max_directory_depth = self.config.get('max_directory_depth', 10)
        self.max_files_per_directory = self.config.get('max_files_per_directory', 1000)
    
    def create_directory(self, directory_path: Union[str, Path], parents: bool = True) -> Dict[str, Any]:
        """Create directory with optional parent creation"""
        try:
            directory_path = Path(directory_path)
            
            if directory_path.exists():
                return {
                    'success': False,
                    'error': f'Directory already exists: {directory_path}',
                    'operation': 'create_directory'
                }
            
            directory_path.mkdir(parents=parents, exist_ok=False)
            
            return {
                'success': True,
                'directory_path': str(directory_path),
                'created': True,
                'parents_created': parents,
                'operation': 'create_directory',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error creating directory {directory_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'create_directory'
            }
    
    def list_directory(self, directory_path: Union[str, Path], pattern: str = "*", recursive: bool = False) -> Dict[str, Any]:
        """List directory contents with optional recursion"""
        try:
            directory_path = Path(directory_path)
            
            if not directory_path.exists():
                return {
                    'success': False,
                    'error': f'Directory does not exist: {directory_path}',
                    'operation': 'list_directory'
                }
            
            if not directory_path.is_dir():
                return {
                    'success': False,
                    'error': f'Path is not a directory: {directory_path}',
                    'operation': 'list_directory'
                }
            
            files = []
            directories = []
            
            if recursive:
                search_pattern = f"**/{pattern}"
                items = list(directory_path.glob(search_pattern))
            else:
                items = list(directory_path.glob(pattern))
            
            for item in items:
                if item.is_file():
                    files.append({
                        'name': item.name,
                        'path': str(item),
                        'relative_path': str(item.relative_to(directory_path)),
                        'size': item.stat().st_size,
                        'modified': datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                    })
                elif item.is_dir():
                    directories.append({
                        'name': item.name,
                        'path': str(item),
                        'relative_path': str(item.relative_to(directory_path)),
                        'modified': datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                    })
            
            return {
                'success': True,
                'directory_path': str(directory_path),
                'pattern': pattern,
                'recursive': recursive,
                'files': files,
                'directories': directories,
                'total_files': len(files),
                'total_directories': len(directories),
                'operation': 'list_directory',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error listing directory {directory_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'list_directory'
            }
    
    def delete_directory(self, directory_path: Union[str, Path], recursive: bool = False) -> Dict[str, Any]:
        """Delete directory with optional recursive deletion"""
        try:
            directory_path = Path(directory_path)
            
            if not directory_path.exists():
                return {
                    'success': False,
                    'error': f'Directory does not exist: {directory_path}',
                    'operation': 'delete_directory'
                }
            
            if not directory_path.is_dir():
                return {
                    'success': False,
                    'error': f'Path is not a directory: {directory_path}',
                    'operation': 'delete_directory'
                }
            
            # Count items before deletion
            item_count = len(list(directory_path.rglob("*"))) if recursive else len(list(directory_path.iterdir()))
            
            if recursive:
                shutil.rmtree(directory_path)
            else:
                directory_path.rmdir()
            
            return {
                'success': True,
                'directory_path': str(directory_path),
                'deleted': True,
                'recursive': recursive,
                'items_deleted': item_count,
                'operation': 'delete_directory',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error deleting directory {directory_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'delete_directory'
            }
    
    def move_file(self, source_path: Union[str, Path], destination_path: Union[str, Path]) -> Dict[str, Any]:
        """Move file or directory to new location"""
        try:
            source_path = Path(source_path)
            destination_path = Path(destination_path)
            
            if not source_path.exists():
                return {
                    'success': False,
                    'error': f'Source does not exist: {source_path}',
                    'operation': 'move_file'
                }
            
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Move the item
            shutil.move(str(source_path), str(destination_path))
            
            return {
                'success': True,
                'source_path': str(source_path),
                'destination_path': str(destination_path),
                'moved': True,
                'operation': 'move_file',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error moving from {source_path} to {destination_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'move_file'
            }
    
    def get_directory_size(self, directory_path: Union[str, Path]) -> Dict[str, Any]:
        """Calculate total size of directory and its contents"""
        try:
            directory_path = Path(directory_path)
            
            if not directory_path.exists():
                return {
                    'success': False,
                    'error': f'Directory does not exist: {directory_path}',
                    'operation': 'get_directory_size'
                }
            
            if not directory_path.is_dir():
                return {
                    'success': False,
                    'error': f'Path is not a directory: {directory_path}',
                    'operation': 'get_directory_size'
                }
            
            total_size = 0
            file_count = 0
            directory_count = 0
            
            for item in directory_path.rglob("*"):
                if item.is_file():
                    total_size += item.stat().st_size
                    file_count += 1
                elif item.is_dir():
                    directory_count += 1
            
            return {
                'success': True,
                'directory_path': str(directory_path),
                'total_size_bytes': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'file_count': file_count,
                'directory_count': directory_count,
                'operation': 'get_directory_size',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error calculating directory size for {directory_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'get_directory_size'
            }

# Export the operations
file_system_operations = FileSystemOperations() 