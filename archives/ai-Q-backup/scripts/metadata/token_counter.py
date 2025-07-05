#!/usr/bin/env python3
# TOKEN COUNT: ~1,247 tokens
"""
AI-Q Knowledge Library System - Token Counter Script
Updates all documents and files with token count metadata for context window tracking.
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Any, Optional

class TokenCounter:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.token_counts = {}
        
    def estimate_tokens(self, content: str) -> int:
        """Estimate token count using simple word-based approximation"""
        # Rough approximation: 1 token ≈ 4 characters or 0.75 words
        words = len(content.split())
        chars = len(content)
        return max(words, chars // 4)
    
    def find_files(self, extensions: Optional[List[str]] = None) -> List[Path]:
        """Find all files with specified extensions"""
        if extensions is None:
            extensions = ['.yml', '.yaml', '.json', '.md', '.ts', '.js', '.py', '.txt']
        
        files = []
        for ext in extensions:
            files.extend(self.base_path.rglob(f"*{ext}"))
        return files
    
    def has_token_metadata(self, content: str, file_extension: str) -> bool:
        """Check if file already has token count metadata"""
        if file_extension.lower() == '.json':
            # For JSON files, check if _metadata field exists
            try:
                data = json.loads(content)
                return '_metadata' in data and 'token_count' in data['_metadata']
            except json.JSONDecodeError:
                return False
        else:
            # For other files, check for comment-style metadata
            return re.search(r'# TOKEN COUNT:', content, re.IGNORECASE) is not None
    
    def update_token_metadata(self, content: str, token_count: int, file_extension: str) -> str:
        """Add or update token count metadata in file content"""
        if file_extension.lower() == '.json':
            return self._update_json_token_metadata(content, token_count)
        else:
            return self._update_comment_token_metadata(content, token_count)
    
    def _update_json_token_metadata(self, content: str, token_count: int) -> str:
        """Add or update token count metadata in JSON files"""
        try:
            data = json.loads(content)
            
            # Create or update _metadata field
            if '_metadata' not in data:
                data['_metadata'] = {}
            
            data['_metadata']['token_count'] = token_count
            data['_metadata']['token_count_estimated'] = True
            data['_metadata']['last_updated'] = '2025-01-27T12:00:00Z'
            
            return json.dumps(data, indent=2)
        except json.JSONDecodeError as e:
            print(f"Warning: Could not parse JSON file: {e}")
            return content
    
    def _update_comment_token_metadata(self, content: str, token_count: int) -> str:
        """Add or update token count metadata in comment-style files"""
        lines = content.split('\n')
        
        # Find the title line (first non-empty line that starts with #)
        title_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('#') and line.strip() != '#':
                title_index = i
                break
        
        if title_index == -1:
            # No title found, add at beginning
            token_line = f"# TOKEN COUNT: ~{token_count:,} tokens"
            return f"{token_line}\n{content}"
        
        # Check if token metadata already exists
        for i, line in enumerate(lines):
            if re.search(r'# TOKEN COUNT:', line, re.IGNORECASE):
                # Update existing token count
                lines[i] = f"# TOKEN COUNT: ~{token_count:,} tokens"
                return '\n'.join(lines)
        
        # Add token metadata after title
        token_line = f"# TOKEN COUNT: ~{token_count:,} tokens"
        lines.insert(title_index + 1, token_line)
        return '\n'.join(lines)
    
    def process_file(self, file_path: Path) -> Tuple[bool, int]:
        """Process a single file and return (updated, token_count)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            token_count = self.estimate_tokens(content)
            file_extension = file_path.suffix
            
            if not self.has_token_metadata(content, file_extension):
                updated_content = self.update_token_metadata(content, token_count, file_extension)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                return True, token_count
            else:
                return False, token_count
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return False, 0
    
    def process_all_files(self, extensions: Optional[List[str]] = None, dry_run: bool = False) -> Dict[str, Any]:
        """Process all files and return summary"""
        files = self.find_files(extensions)
        updated_files = []
        total_tokens = 0
        
        print(f"Found {len(files)} files to process...")
        
        for file_path in files:
            if dry_run:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                token_count = self.estimate_tokens(content)
                file_extension = file_path.suffix
                has_metadata = self.has_token_metadata(content, file_extension)
                status = "HAS METADATA" if has_metadata else "NEEDS UPDATE"
                print(f"{status}: {file_path} (~{token_count:,} tokens)")
                total_tokens += token_count
            else:
                updated, token_count = self.process_file(file_path)
                if updated:
                    updated_files.append(str(file_path))
                    print(f"UPDATED: {file_path} (~{token_count:,} tokens)")
                else:
                    print(f"SKIPPED: {file_path} (~{token_count:,} tokens)")
                total_tokens += token_count
        
        return {
            'updated_files': updated_files,
            'total_files': len(files),
            'total_tokens': total_tokens
        }
    
    def generate_summary_report(self, results: Dict[str, Any]) -> str:
        """Generate a summary report"""
        report = f"""
# TOKEN COUNT SUMMARY REPORT
# TOKEN COUNT: ~{self.estimate_tokens(str(results))} tokens
---
total_files_processed: {results['total_files']}
files_updated: {len(results['updated_files'])}
total_tokens: {results['total_tokens']:,}
average_tokens_per_file: {results['total_tokens'] // results['total_files'] if results['total_files'] > 0 else 0:,}

updated_files:
"""
        for file_path in results['updated_files']:
            report += f"  - {file_path}\n"
        
        return report

def main():
    parser = argparse.ArgumentParser(description='Update files with token count metadata')
    parser.add_argument('--path', default='.', help='Base path to search for files')
    parser.add_argument('--extensions', nargs='+', 
                       default=['.yml', '.yaml', '.json', '.md', '.ts', '.js', '.py', '.txt'],
                       help='File extensions to process')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be updated without making changes')
    parser.add_argument('--summary', action='store_true',
                       help='Generate summary report')
    
    args = parser.parse_args()
    
    counter = TokenCounter(args.path)
    results = counter.process_all_files(args.extensions, args.dry_run)
    
    if args.summary:
        summary = counter.generate_summary_report(results)
        summary_file = Path(args.path) / 'TOKEN_COUNT_SUMMARY.yml'
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"\nSummary report saved to: {summary_file}")
    
    print(f"\nProcessing complete:")
    print(f"  Total files: {results['total_files']}")
    print(f"  Files updated: {len(results['updated_files'])}")
    print(f"  Total tokens: {results['total_tokens']:,}")

if __name__ == '__main__':
    main() 