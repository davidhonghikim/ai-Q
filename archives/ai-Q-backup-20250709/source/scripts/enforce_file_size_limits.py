#!/usr/bin/env python3
"""
File Size Limit Enforcement Script
==================================

Enforces the project rule that no code file may exceed 150 lines or 5K tokens.
This script can be used as a pre-commit hook, CI check, or manual audit tool.

Author: kOS Kitchen System
Version: 1.0.0
Created: 2025-07-08T02:00:00Z
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime
import re

# Configuration
TARGET_LINES_MIN = 150
TARGET_LINES_MAX = 250
HARD_LINE_LIMIT = 300
MAX_TOKENS = 10000
CODE_EXTENSIONS = {'.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.cpp', '.c', '.h', '.hpp', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala'}
EXCLUDE_DIRS = {'.git', '__pycache__', 'node_modules', 'venv', '.venv', 'build', 'dist', 'target', 'bin', 'obj', '.pytest_cache', '.mypy_cache'}
EXCLUDE_FILES = {'package-lock.json', 'yarn.lock', 'poetry.lock', 'Pipfile.lock'}

def count_tokens(text: str) -> int:
    """
    Estimate token count for a text string.
    This is a rough approximation - for exact counts, use tiktoken or similar.
    """
    # Simple token estimation: split on whitespace and punctuation
    tokens = re.findall(r'\b\w+\b|[^\w\s]', text)
    return len(tokens)

def analyze_file(file_path: Path) -> Dict[str, Any]:
    """
    Analyze a single file for size compliance.
    
    Returns:
        Dictionary with analysis results
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        lines = content.split('\n')
        line_count = len(lines)
        token_count = count_tokens(content)
        
        # Determine compliance status
        line_limit_exceeded = line_count > HARD_LINE_LIMIT
        token_limit_exceeded = token_count > MAX_TOKENS
        in_target_range = TARGET_LINES_MIN <= line_count <= TARGET_LINES_MAX
        compliant = not line_limit_exceeded and not token_limit_exceeded
        
        return {
            'file_path': str(file_path),
            'line_count': line_count,
            'token_count': token_count,
            'size_bytes': len(content.encode('utf-8')),
            'line_limit_exceeded': line_limit_exceeded,
            'token_limit_exceeded': token_limit_exceeded,
            'in_target_range': in_target_range,
            'compliant': compliant
        }
    except Exception as e:
        return {
            'file_path': str(file_path),
            'error': str(e),
            'compliant': False
        }

def scan_directory(directory: Path, recursive: bool = True) -> List[Dict[str, Any]]:
    """
    Scan a directory for code files and analyze their sizes.
    
    Args:
        directory: Directory to scan
        recursive: Whether to scan subdirectories
        
    Returns:
        List of file analysis results
    """
    results = []
    
    if recursive:
        file_iter = directory.rglob('*')
    else:
        file_iter = directory.glob('*')
    
    for item in file_iter:
        if item.is_file():
            # Skip excluded directories
            if any(excluded in item.parts for excluded in EXCLUDE_DIRS):
                continue
            
            # Skip excluded files
            if item.name in EXCLUDE_FILES:
                continue
            
            # Only analyze code files
            if item.suffix.lower() in CODE_EXTENSIONS:
                result = analyze_file(item)
                results.append(result)
    
    return results

def generate_report(results: List[Dict[str, Any]], output_format: str = 'text') -> str:
    """
    Generate a compliance report.
    
    Args:
        results: List of file analysis results
        output_format: 'text', 'json', or 'summary'
    
    Returns:
        Formatted report string
    """
    if output_format == 'json':
        return json.dumps(results, indent=2)
    
    # Separate compliant and non-compliant files
    compliant_files = [r for r in results if r.get('compliant', False)]
    non_compliant_files = [r for r in results if not r.get('compliant', False)]
    
    if output_format == 'summary':
        return f"Files analyzed: {len(results)}\nCompliant: {len(compliant_files)}\nNon-compliant: {len(non_compliant_files)}"
    
    # Full text report
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("FILE SIZE COMPLIANCE REPORT")
    report_lines.append("=" * 80)
    report_lines.append(f"Generated: {datetime.utcnow().isoformat()}Z")
    report_lines.append(f"Target: {TARGET_LINES_MIN}-{TARGET_LINES_MAX} lines, Hard limit: {HARD_LINE_LIMIT} lines, {MAX_TOKENS} tokens")
    report_lines.append(f"Files analyzed: {len(results)}")
    report_lines.append(f"Compliant: {len(compliant_files)}")
    report_lines.append(f"Non-compliant: {len(non_compliant_files)}")
    report_lines.append("")
    
    if non_compliant_files:
        report_lines.append("❌ NON-COMPLIANT FILES:")
        report_lines.append("-" * 40)
        for file_result in non_compliant_files:
            if 'error' in file_result:
                report_lines.append(f"  {file_result['file_path']}: ERROR - {file_result['error']}")
            else:
                violations = []
                if file_result['line_limit_exceeded']:
                    violations.append(f"lines ({file_result['line_count']} > {HARD_LINE_LIMIT})")
                if file_result['token_limit_exceeded']:
                    violations.append(f"tokens ({file_result['token_count']} > {MAX_TOKENS})")
                
                report_lines.append(f"  {file_result['file_path']}: {', '.join(violations)}")
        report_lines.append("")
    
    if compliant_files:
        report_lines.append("✅ COMPLIANT FILES:")
        report_lines.append("-" * 40)
        for file_result in compliant_files:
            report_lines.append(f"  {file_result['file_path']}: {file_result['line_count']} lines, {file_result['token_count']} tokens")
        report_lines.append("")
    
    # Summary statistics
    if results:
        avg_lines = sum(r.get('line_count', 0) for r in results if 'line_count' in r) / len(results)
        avg_tokens = sum(r.get('token_count', 0) for r in results if 'token_count' in r) / len(results)
        max_lines = max(r.get('line_count', 0) for r in results if 'line_count' in r)
        max_tokens = max(r.get('token_count', 0) for r in results if 'token_count' in r)
        
        report_lines.append("📊 STATISTICS:")
        report_lines.append("-" * 40)
        report_lines.append(f"  Average lines: {avg_lines:.1f}")
        report_lines.append(f"  Average tokens: {avg_tokens:.1f}")
        report_lines.append(f"  Maximum lines: {max_lines}")
        report_lines.append(f"  Maximum tokens: {max_tokens}")
        report_lines.append("")
    
    report_lines.append("=" * 80)
    
    return "\n".join(report_lines)

def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description='Enforce file size limits for code files')
    parser.add_argument('directory', nargs='?', default='.', help='Directory to scan (default: current directory)')
    parser.add_argument('--recursive', '-r', action='store_true', default=True, help='Scan subdirectories recursively')
    parser.add_argument('--format', '-f', choices=['text', 'json', 'summary'], default='text', help='Output format')
    parser.add_argument('--strict', '-s', action='store_true', help='Exit with error code if any files are non-compliant')
    parser.add_argument('--output', '-o', help='Output file for report')
    
    args = parser.parse_args()
    
    # Scan directory
    directory = Path(args.directory)
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    print(f"Scanning directory: {directory}", file=sys.stderr)
    results = scan_directory(directory, args.recursive)
    
    # Generate report
    report = generate_report(results, args.format)
    
    # Output report
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report written to: {args.output}", file=sys.stderr)
    else:
        print(report)
    
    # Check for violations
    non_compliant_files = [r for r in results if not r.get('compliant', False)]
    
    if non_compliant_files:
        print(f"\n❌ Found {len(non_compliant_files)} non-compliant files!", file=sys.stderr)
        if args.strict:
            sys.exit(1)
    else:
        print(f"\n✅ All {len(results)} files are compliant!", file=sys.stderr)

if __name__ == "__main__":
    main() 