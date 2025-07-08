#!/usr/bin/env python3
"""
AI-Q Project Archive Script
Creates organized archives of the AI-Q project with intelligent exclusions.

Usage:
    python archive_project.py [source_path] [destination_path] [options]

Examples:
    python archive_project.py . ./archives/ai-q-backup-$(date +%Y%m%d)
    python archive_project.py /path/to/project ./backups --exclude-temp --verbose
"""

import os
import sys
import shutil
import argparse
import logging
from datetime import datetime
from pathlib import Path
import json
import hashlib
import zipfile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('archive.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ProjectArchiver:
    """Handles project archiving with intelligent exclusions and organization."""
    
    def __init__(self, source_path, destination_path, **options):
        self.source_path = Path(source_path).resolve()
        self.destination_path = Path(destination_path).resolve()
        self.options = options
        
        # Common directories to exclude
        self.common_exclusions = {
            'venv', 'node_modules', '.git', '.gitignore',
            '__pycache__', '.pytest_cache', '.coverage',
            '.DS_Store', 'Thumbs.db', '.vscode', '.idea',
            '*.pyc', '*.pyo', '*.pyd', '*.so', '*.dll',
            '*.log', '*.tmp', '*.temp', '*.swp', '*.swo',
            'dist', 'build', '*.egg-info', '.tox',
            'archives', 'backups', 'temp', 'tmp'
        }
        
        # Specific path exclusions
        self.specific_exclusions = {
            Path('E:/kos/ai-Q/archives'),
            Path('E:\\kos\\ai-Q\\archives'),
            Path('/e/kos/ai-Q/archives')
        }
        
        # File types to handle specially
        self.special_file_types = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.json': 'json',
            '.yml': 'yaml',
            '.yaml': 'yaml',
            '.md': 'markdown',
            '.txt': 'text',
            '.html': 'html',
            '.css': 'css',
            '.sql': 'sql',
            '.sh': 'shell',
            '.bat': 'batch',
            '.ps1': 'powershell'
        }
        
        # Archive metadata
        self.metadata = {
            'archive_date': datetime.now().isoformat(),
            'source_path': str(self.source_path),
            'destination_path': str(self.destination_path),
            'options': options,
            'file_count': 0,
            'directory_count': 0,
            'total_size': 0,
            'excluded_items': [],
            'errors': []
        }

    def should_exclude(self, path):
        """Determine if a path should be excluded from archiving."""
        path_str = str(path)
        path_name = path.name
        
        # Check common exclusions
        if path_name in self.common_exclusions:
            return True, f"Common exclusion: {path_name}"
        
        # Check specific path exclusions
        for exclusion in self.specific_exclusions:
            if str(path).startswith(str(exclusion)):
                return True, f"Specific exclusion: {exclusion}"
        
        # Check for patterns
        for pattern in self.common_exclusions:
            if pattern.startswith('*') and path_name.endswith(pattern[1:]):
                return True, f"Pattern exclusion: {pattern}"
        
        # Check for temporary files
        if self.options.get('exclude_temp', False):
            if any(temp_indicator in path_str.lower() for temp_indicator in ['temp', 'tmp', 'cache']):
                return True, f"Temporary file: {path_name}"
        
        return False, None

    def calculate_file_hash(self, file_path):
        """Calculate SHA-256 hash of a file."""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            logger.warning(f"Could not calculate hash for {file_path}: {e}")
            return None

    def get_file_info(self, file_path):
        """Get detailed information about a file."""
        try:
            stat = file_path.stat()
            return {
                'name': file_path.name,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'hash': self.calculate_file_hash(file_path),
                'type': self.special_file_types.get(file_path.suffix, 'unknown')
            }
        except Exception as e:
            logger.warning(f"Could not get file info for {file_path}: {e}")
            return None

    def create_archive_structure(self):
        """Create the archive directory structure."""
        try:
            # Create main archive directory
            self.destination_path.mkdir(parents=True, exist_ok=True)
            
            # Create subdirectories
            subdirs = ['source', 'metadata', 'documentation', 'scripts']
            for subdir in subdirs:
                (self.destination_path / subdir).mkdir(exist_ok=True)
            
            logger.info(f"Created archive structure at {self.destination_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to create archive structure: {e}")
            return False

    def copy_file(self, source_file, dest_file):
        """Copy a file with error handling."""
        try:
            # Create destination directory if it doesn't exist
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            shutil.copy2(source_file, dest_file)
            
            # Update metadata
            self.metadata['file_count'] += 1
            self.metadata['total_size'] += source_file.stat().st_size
            
            return True
        except Exception as e:
            error_msg = f"Failed to copy {source_file}: {e}"
            logger.error(error_msg)
            self.metadata['errors'].append(error_msg)
            return False

    def archive_directory(self, source_dir, dest_dir):
        """Recursively archive a directory."""
        try:
            source_dir = Path(source_dir)
            dest_dir = Path(dest_dir)
            
            if not source_dir.exists():
                logger.warning(f"Source directory does not exist: {source_dir}")
                return
            
            # Create destination directory
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            # Process all items in the directory
            for item in source_dir.iterdir():
                # Check if item should be excluded
                should_exclude, reason = self.should_exclude(item)
                if should_exclude:
                    self.metadata['excluded_items'].append({
                        'path': str(item),
                        'reason': reason
                    })
                    if self.options.get('verbose', False):
                        logger.info(f"Excluded: {item} - {reason}")
                    continue
                
                # Process item
                if item.is_file():
                    dest_file = dest_dir / item.name
                    if self.copy_file(item, dest_file):
                        if self.options.get('verbose', False):
                            logger.info(f"Archived: {item}")
                elif item.is_dir():
                    dest_subdir = dest_dir / item.name
                    self.archive_directory(item, dest_subdir)
                    self.metadata['directory_count'] += 1
            
        except Exception as e:
            error_msg = f"Failed to archive directory {source_dir}: {e}"
            logger.error(error_msg)
            self.metadata['errors'].append(error_msg)

    def create_metadata_file(self):
        """Create metadata file with archive information."""
        try:
            metadata_file = self.destination_path / 'metadata' / 'archive_info.json'
            
            # Add additional metadata
            self.metadata['archive_complete'] = True
            self.metadata['archive_duration'] = str(datetime.now() - datetime.fromisoformat(self.metadata['archive_date']))
            
            with open(metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
            
            logger.info(f"Created metadata file: {metadata_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to create metadata file: {e}")
            return False

    def create_archive_script(self):
        """Create a script to extract the archive."""
        try:
            extract_script = self.destination_path / 'scripts' / 'extract_archive.py'
            script_content = '''#!/usr/bin/env python3
"""
Archive Extraction Script
Extracts the AI-Q project archive.

Usage:
    python extract_archive.py [destination_path]
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

def extract_archive(archive_path, destination_path):
    """Extract the archive to the specified destination."""
    try:
        archive_source = Path(archive_path) / 'source'
        dest = Path(destination_path)
        if not archive_source.exists():
            print(f"Error: Archive source not found at {archive_source}")
            return False
        # Copy source files
        shutil.copytree(archive_source, dest, dirs_exist_ok=True)
        print(f"Archive extracted to: {dest}")
        return True
    except Exception as e:
        print(f"Error extracting archive: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract AI-Q project archive")
    parser.add_argument("destination", help="Destination path for extraction")
    args = parser.parse_args()
    archive_path = Path(__file__).parent.parent
    extract_archive(archive_path, args.destination)
'''
            with open(extract_script, 'w') as f:
                f.write(script_content)
            extract_script.chmod(0o755)
            logger.info(f"Created extraction script: {extract_script}")
            return True
        except Exception as e:
            logger.error(f"Failed to create extraction script: {e}")
            return False

    def create_readme(self):
        """Create a README file for the archive."""
        try:
            readme_file = self.destination_path / 'README.md'
            
            readme_content = f'''# AI-Q Project Archive

This archive was created on {self.metadata['archive_date']}.

## Archive Contents

- **source/**: Project source code and files
- **metadata/**: Archive metadata and information
- **documentation/**: Project documentation
- **scripts/**: Utility scripts including extraction script

## Archive Information

- **Source Path**: {self.metadata['source_path']}
- **Archive Date**: {self.metadata['archive_date']}
- **File Count**: {self.metadata['file_count']}
- **Directory Count**: {self.metadata['directory_count']}
- **Total Size**: {self.metadata['total_size']} bytes

## Excluded Items

The following items were excluded from this archive:

{chr(10).join([f"- {{item['path']}} ({{item['reason']}})" for item in self.metadata['excluded_items']])}

## Extraction

To extract this archive:

```bash
python scripts/extract_archive.py [destination_path]
```

## Archive Options

{json.dumps(self.metadata['options'], indent=2)}

## Errors

{chr(10).join([f"- {{error}}" for error in self.metadata['errors']]) if self.metadata['errors'] else "No errors encountered."}
'''
            
            with open(readme_file, 'w') as f:
                f.write(readme_content)
            
            logger.info(f"Created README file: {readme_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to create README file: {e}")
            return False

    def archive(self):
        """Main archiving process."""
        logger.info(f"Starting archive process...")
        logger.info(f"Source: {self.source_path}")
        logger.info(f"Destination: {self.destination_path}")
        
        # Create archive structure
        if not self.create_archive_structure():
            return False
        
        # Archive source files
        source_dest = self.destination_path / 'source'
        self.archive_directory(self.source_path, source_dest)
        
        # Create metadata and documentation
        self.create_metadata_file()
        self.create_archive_script()
        self.create_readme()
        
        # Compress the archive directory unless --no-zip is set
        if not self.options.get('no_zip', False):
            # Create the zip file first
            temp_zip_path = str(self.destination_path) + '.zip'
            logger.info(f"Compressing archive to: {temp_zip_path}")
            try:
                shutil.make_archive(str(self.destination_path), 'zip', root_dir=str(self.destination_path))
                
                # Get the actual creation time of the zip file and rename it
                zip_file = Path(temp_zip_path)
                if zip_file.exists():
                    # Get creation time and format it properly
                    creation_time = datetime.fromtimestamp(zip_file.stat().st_ctime)
                    timestamp_str = creation_time.strftime('%Y-%m-%d_%H-%M-%S')
                    final_zip_name = f"ai-Q-backup_{timestamp_str}.zip"
                    final_zip_path = self.destination_path.parent / final_zip_name
                    
                    # Rename the zip file to use the standardized timestamp format
                    zip_file.rename(final_zip_path)
                    logger.info(f"Archive compressed and renamed to: {final_zip_path}")
                else:
                    logger.error("Zip file was not created successfully")
            except Exception as e:
                logger.error(f"Failed to compress archive: {e}")
        else:
            logger.info("Skipping compression due to --no-zip option.")
        
        # Log summary
        logger.info(f"Archive completed successfully!")
        logger.info(f"Files archived: {self.metadata['file_count']}")
        logger.info(f"Directories archived: {self.metadata['directory_count']}")
        logger.info(f"Total size: {self.metadata['total_size']} bytes")
        logger.info(f"Items excluded: {len(self.metadata['excluded_items'])}")
        logger.info(f"Errors: {len(self.metadata['errors'])}")
        
        return True

def main():
    """Main function to handle command line arguments and execute archiving."""
    parser = argparse.ArgumentParser(
        description="Archive AI-Q project with intelligent exclusions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python archive_project.py . ./archives/ai-q-backup-$(date +%Y%m%d)
  python archive_project.py /path/to/project ./backups --exclude-temp --verbose
  python archive_project.py . ./archive --dry-run
        """
    )
    
    parser.add_argument(
        'source',
        help='Source directory to archive'
    )
    
    parser.add_argument(
        'destination',
        help='Destination directory for archive'
    )
    
    parser.add_argument(
        '--exclude-temp',
        action='store_true',
        help='Exclude temporary files and directories'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be archived without actually doing it'
    )
    
    parser.add_argument(
        '--no-zip',
        action='store_true',
        help='Do not compress the archive directory into a zip file.'
    )
    
    args = parser.parse_args()
    
    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create archiver
    archiver = ProjectArchiver(
        args.source,
        args.destination,
        exclude_temp=args.exclude_temp,
        verbose=args.verbose,
        dry_run=args.dry_run,
        no_zip=args.no_zip
    )
    
    # Execute archiving
    if args.dry_run:
        logger.info("DRY RUN MODE - No files will be copied")
        # In dry run mode, just show what would be excluded
        for item in Path(args.source).rglob('*'):
            should_exclude, reason = archiver.should_exclude(item)
            if should_exclude:
                logger.info(f"Would exclude: {item} - {reason}")
        logger.info("Dry run completed")
    else:
        success = archiver.archive()
        if success:
            logger.info("Archive process completed successfully!")
            sys.exit(0)
        else:
            logger.error("Archive process failed!")
            sys.exit(1)

if __name__ == "__main__":
    main() 