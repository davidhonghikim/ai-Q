"""
Binary File Operations - Focused Component

Handles binary file operations for media files, documents, and binary data.
Supports various binary formats: images, videos, audio, documents, archives
"""

import os
import shutil
import mimetypes
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BinaryFileOperations:
    """Binary file operations for media and binary files"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.supported_formats = {
            # Images
            '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png',
            '.gif': 'image/gif', '.bmp': 'image/bmp', '.tiff': 'image/tiff',
            '.webp': 'image/webp', '.svg': 'image/svg+xml',
            
            # Videos
            '.mp4': 'video/mp4', '.avi': 'video/x-msvideo', '.mov': 'video/quicktime',
            '.mkv': 'video/x-matroska', '.wmv': 'video/x-ms-wmv', '.flv': 'video/x-flv',
            '.webm': 'video/webm', '.m4v': 'video/x-m4v',
            
            # Audio
            '.mp3': 'audio/mpeg', '.wav': 'audio/wav', '.flac': 'audio/flac',
            '.aac': 'audio/aac', '.ogg': 'audio/ogg', '.wma': 'audio/x-ms-wma',
            
            # Documents
            '.pdf': 'application/pdf', '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.ppt': 'application/vnd.ms-powerpoint',
            '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            
            # Archives
            '.zip': 'application/zip', '.rar': 'application/x-rar-compressed',
            '.7z': 'application/x-7z-compressed', '.tar': 'application/x-tar',
            '.gz': 'application/gzip', '.bz2': 'application/x-bzip2'
        }
    
    def read_binary_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Read binary file and return metadata"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {
                    'success': False,
                    'error': f'File does not exist: {file_path}',
                    'operation': 'read_binary_file'
                }
            
            file_size = file_path.stat().st_size
            mime_type = self.supported_formats.get(file_path.suffix.lower(), 'application/octet-stream')
            
            return {
                'success': True,
                'file_path': str(file_path),
                'file_size': file_size,
                'mime_type': mime_type,
                'file_extension': file_path.suffix.lower(),
                'modified_time': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                'operation': 'read_binary_file',
                'timestamp': datetime.now().isoformat()
            }
                
        except Exception as e:
            logger.error(f"Error reading binary file {file_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'read_binary_file'
            }
    
    def copy_binary_file(self, source_path: Union[str, Path], destination_path: Union[str, Path]) -> Dict[str, Any]:
        """Copy binary file with metadata preservation"""
        try:
            source_path = Path(source_path)
            destination_path = Path(destination_path)
            
            if not source_path.exists():
                return {
                    'success': False,
                    'error': f'Source file does not exist: {source_path}',
                    'operation': 'copy_binary_file'
                }
            
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file with metadata
            shutil.copy2(source_path, destination_path)
            
            file_size = destination_path.stat().st_size
            mime_type = self.supported_formats.get(destination_path.suffix.lower(), 'application/octet-stream')
            
            return {
                'success': True,
                'source_path': str(source_path),
                'destination_path': str(destination_path),
                'file_size': file_size,
                'mime_type': mime_type,
                'operation': 'copy_binary_file',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error copying binary file from {source_path} to {destination_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'copy_binary_file'
            }
    
    def get_file_info(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Get detailed file information"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {
                    'success': False,
                    'error': f'File does not exist: {file_path}',
                    'operation': 'get_file_info'
                }
            
            stat = file_path.stat()
            mime_type = self.supported_formats.get(file_path.suffix.lower(), 'application/octet-stream')
            
            return {
                'success': True,
                'file_path': str(file_path),
                'file_name': file_path.name,
                'file_extension': file_path.suffix.lower(),
                'file_size': stat.st_size,
                'mime_type': mime_type,
                'created_time': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'accessed_time': datetime.fromtimestamp(stat.st_atime).isoformat(),
                'is_file': file_path.is_file(),
                'is_directory': file_path.is_dir(),
                'operation': 'get_file_info',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting file info for {file_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'get_file_info'
            }
    
    def validate_file_format(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Validate if file format is supported"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {
                    'success': False,
                    'error': f'File does not exist: {file_path}',
                    'operation': 'validate_file_format'
                }
            
            extension = file_path.suffix.lower()
            is_supported = extension in self.supported_formats
            mime_type = self.supported_formats.get(extension, 'unknown')
            
            return {
                'success': True,
                'file_path': str(file_path),
                'file_extension': extension,
                'is_supported': is_supported,
                'mime_type': mime_type,
                'supported_formats': list(self.supported_formats.keys()),
                'operation': 'validate_file_format',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error validating file format for {file_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'validate_file_format'
            }

# Export the operations
binary_file_operations = BinaryFileOperations() 