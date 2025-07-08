"""
Text File Operations - Focused Component

Handles text-based file operations for documents, code, and text files.
Supports various text formats: .txt, .json, .yaml, .yml, .md, .py, .js, .html, .css, .xml, .csv
"""

import json
import csv
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TextFileOperations:
    """Text file operations for documents and text-based files"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.supported_formats = {
            '.txt': 'plain_text',
            '.json': 'json',
            '.yaml': 'yaml', 
            '.yml': 'yaml',
            '.md': 'markdown',
            '.py': 'python',
            '.js': 'javascript',
            '.html': 'html',
            '.css': 'css',
            '.xml': 'xml',
            '.csv': 'csv',
            '.tsv': 'tsv',
            '.log': 'log',
            '.ini': 'ini',
            '.cfg': 'config'
        }
    
    def read_text_file(self, file_path: Union[str, Path], encoding: str = 'utf-8') -> Dict[str, Any]:
        """Read text file contents with format detection"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {
                    'success': False,
                    'error': f'File does not exist: {file_path}',
                    'operation': 'read_text_file'
                }
            
            file_format = self.supported_formats.get(file_path.suffix.lower(), 'plain_text')
            
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            return {
                'success': True,
                'content': content,
                'file_path': str(file_path),
                'file_size': len(content),
                'file_format': file_format,
                'encoding': encoding,
                'line_count': len(content.splitlines()),
                'operation': 'read_text_file',
                'timestamp': datetime.now().isoformat()
            }
                
        except Exception as e:
            logger.error(f"Error reading text file {file_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'read_text_file'
            }
    
    def write_text_file(self, file_path: Union[str, Path], content: str, encoding: str = 'utf-8') -> Dict[str, Any]:
        """Write text content to file"""
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            
            file_size = file_path.stat().st_size
            return {
                'success': True,
                'file_path': str(file_path),
                'file_size': file_size,
                'content_length': len(content),
                'line_count': len(content.splitlines()),
                'encoding': encoding,
                'operation': 'write_text_file',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error writing text file {file_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'write_text_file'
            }
    
    def read_json_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Read and parse JSON file"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {
                    'success': False,
                    'error': f'File does not exist: {file_path}',
                    'operation': 'read_json_file'
                }
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return {
                'success': True,
                'data': data,
                'file_path': str(file_path),
                'file_size': file_path.stat().st_size,
                'data_type': type(data).__name__,
                'operation': 'read_json_file',
                'timestamp': datetime.now().isoformat()
            }
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in {file_path}: {e}")
            return {
                'success': False,
                'error': f'Invalid JSON: {e}',
                'operation': 'read_json_file'
            }
        except Exception as e:
            logger.error(f"Error reading JSON file {file_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'read_json_file'
            }
    
    def write_json_file(self, file_path: Union[str, Path], data: Any, indent: int = 2) -> Dict[str, Any]:
        """Write data to JSON file"""
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            
            file_size = file_path.stat().st_size
            return {
                'success': True,
                'file_path': str(file_path),
                'file_size': file_size,
                'data_type': type(data).__name__,
                'indent': indent,
                'operation': 'write_json_file',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error writing JSON file {file_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'write_json_file'
            }
    
    def read_csv_file(self, file_path: Union[str, Path], delimiter: str = ',') -> Dict[str, Any]:
        """Read and parse CSV file"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {
                    'success': False,
                    'error': f'File does not exist: {file_path}',
                    'operation': 'read_csv_file'
                }
            
            rows = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=delimiter)
                for row in reader:
                    rows.append(row)
            
            headers = rows[0] if rows else []
            data_rows = rows[1:] if len(rows) > 1 else []
            
            return {
                'success': True,
                'headers': headers,
                'data': data_rows,
                'file_path': str(file_path),
                'file_size': file_path.stat().st_size,
                'row_count': len(data_rows),
                'column_count': len(headers),
                'delimiter': delimiter,
                'operation': 'read_csv_file',
                'timestamp': datetime.now().isoformat()
            }
                
        except Exception as e:
            logger.error(f"Error reading CSV file {file_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'operation': 'read_csv_file'
            }

# Export the operations
text_file_operations = TextFileOperations() 