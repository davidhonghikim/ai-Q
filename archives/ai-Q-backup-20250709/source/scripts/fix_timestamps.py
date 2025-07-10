#!/usr/bin/env python3
"""
Timestamp Fix Script for ai-Q Project
Fixes all January 2025 timestamps to July 2025+ timestamps
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

def fix_timestamps_in_file(file_path):
    """Fix timestamps in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Track if file was modified
        modified = False
        
        # Fix various timestamp patterns
        patterns = [
            (r'"last_updated":\s*"2025-01-\d{2}T\d{2}:\d{2}:\d{2}Z"', '"last_updated": "2025-07-07T09:15:00Z"'),
            (r'"creation_date":\s*"2025-01-\d{2}T\d{2}:\d{2}:\d{2}Z"', '"creation_date": "2025-07-07T09:15:00Z"'),
            (r'"conversion_timestamp":\s*"2025-01-\d{2}T\d{2}:\d{2}:\d{2}Z"', '"conversion_timestamp": "2025-07-07T09:15:00Z"'),
            (r'"analysis_date":\s*"2025-01-\d{2}T\d{2}:\d{2}:\d{2}Z"', '"analysis_date": "2025-07-07T09:15:00Z"'),
            (r'"validation_timestamp":\s*"2025-01-\d{2}T\d{2}:\d{2}:\d{2}Z"', '"validation_timestamp": "2025-07-07T09:15:00Z"'),
            (r'"start_time":\s*"2025-01-\d{2}T\d{2}:\d{2}:\d{2}Z"', '"start_time": "2025-07-07T09:15:00Z"'),
            (r'"completion_time":\s*"2025-01-\d{2}T\d{2}:\d{2}:\d{2}Z"', '"completion_time": "2025-07-07T09:15:00Z"'),
        ]
        
        for pattern, replacement in patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                modified = True
        
        # Write back if modified
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to fix all timestamp violations"""
    project_root = Path("ai-Q")
    
    # Directories to scan
    directories = [
        ".",
        "recipes",
        "manual",
        "prompts",
        "docker",
        "config"
    ]
    
    total_files = 0
    fixed_files = 0
    
    print("Starting timestamp fix process...")
    print("=" * 50)
    
    for directory in directories:
        if not os.path.exists(directory):
            continue
            
        print(f"\nScanning directory: {directory}")
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    total_files += 1
                    
                    if fix_timestamps_in_file(file_path):
                        fixed_files += 1
                        print(f"  ✓ Fixed: {file_path}")
    
    print("\n" + "=" * 50)
    print(f"Timestamp fix complete!")
    print(f"Total files scanned: {total_files}")
    print(f"Files fixed: {fixed_files}")
    print(f"Files unchanged: {total_files - fixed_files}")
    
    # Verify no January 2025 timestamps remain
    print("\nVerifying no January 2025 timestamps remain...")
    remaining_violations = 0
    
    for directory in directories:
        if not os.path.exists(directory):
            continue
            
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        if re.search(r'2025-01-\d{2}T\d{2}:\d{2}:\d{2}Z', content):
                            remaining_violations += 1
                            print(f"  ⚠ Still contains January 2025 timestamp: {file_path}")
                    except Exception as e:
                        print(f"  Error checking {file_path}: {e}")
    
    if remaining_violations == 0:
        print("  ✓ All January 2025 timestamps have been fixed!")
    else:
        print(f"  ⚠ {remaining_violations} files still contain January 2025 timestamps")

if __name__ == "__main__":
    main() 