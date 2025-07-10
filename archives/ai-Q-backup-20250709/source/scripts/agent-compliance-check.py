#!/usr/bin/env python3
"""
Agent Compliance Check Script
=============================

This script MUST be run by every agent before marking any task as complete.
It enforces the project's file size limits and coding standards.

Author: kOS Kitchen System
Version: 1.0.0
Created: 2025-07-08T02:00:00Z
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Import the file size enforcement script
sys.path.insert(0, str(Path(__file__).parent))
from enforce_file_size_limits import scan_directory, generate_report, TARGET_LINES_MIN, TARGET_LINES_MAX, HARD_LINE_LIMIT, MAX_TOKENS

def run_compliance_check(project_root: str = ".") -> Dict[str, Any]:
    """
    Run a comprehensive compliance check for agents.
    
    Args:
        project_root: Root directory to check
        
    Returns:
        Dictionary with compliance results
    """
    print("🔍 AGENT COMPLIANCE CHECK")
    print("=" * 50)
    print(f"Timestamp: {datetime.utcnow().isoformat()}Z")
    print(f"Project: {project_root}")
    print(f"Target: {TARGET_LINES_MIN}-{TARGET_LINES_MAX} lines, Hard limit: {HARD_LINE_LIMIT} lines, {MAX_TOKENS} tokens")
    print()
    
    # Scan for code files
    results = scan_directory(Path(project_root))
    
    # Separate compliant and non-compliant files
    compliant_files = [r for r in results if r.get('compliant', False)]
    non_compliant_files = [r for r in results if not r.get('compliant', False)]
    
    # Generate detailed report
    report = generate_report(results, 'text')
    print(report)
    
    # Compliance summary
    compliance_summary = {
        'timestamp': datetime.utcnow().isoformat() + "Z",
        'project_root': project_root,
        'total_files': len(results),
        'compliant_files': len(compliant_files),
        'non_compliant_files': len(non_compliant_files),
        'compliance_rate': len(compliant_files) / len(results) if results else 1.0,
        'is_compliant': len(non_compliant_files) == 0,
        'violations': []
    }
    
    # Collect violation details
    for file_result in non_compliant_files:
        if 'error' not in file_result:
            violations = []
            if file_result.get('line_limit_exceeded'):
                violations.append(f"lines ({file_result['line_count']} > {HARD_LINE_LIMIT})")
            if file_result.get('token_limit_exceeded'):
                violations.append(f"tokens ({file_result['token_count']} > {MAX_TOKENS})")
            
            compliance_summary['violations'].append({
                'file': file_result['file_path'],
                'violations': violations,
                'line_count': file_result.get('line_count', 0),
                'token_count': file_result.get('token_count', 0)
            })
    
    # Print compliance status
    print("\n" + "=" * 50)
    if compliance_summary['is_compliant']:
        print("✅ COMPLIANCE CHECK PASSED")
        print(f"All {len(results)} files are within size limits")
    else:
        print("❌ COMPLIANCE CHECK FAILED")
        print(f"Found {len(non_compliant_files)} files that exceed limits")
        print("\nVIOLATIONS:")
        for violation in compliance_summary['violations']:
            print(f"  {violation['file']}: {', '.join(violation['violations'])}")
    
    print("=" * 50)
    
    return compliance_summary

def agent_compliance_reminder():
    """Print a reminder for agents about compliance requirements."""
    print("\n" + "⚠️  AGENT COMPLIANCE REMINDER ⚠️")
    print("=" * 50)
    print("BEFORE MARKING ANY TASK AS COMPLETE:")
    print("1. Run this compliance check")
    print("2. Fix any violations")
    print("3. Re-run the check")
    print("4. Only proceed if ALL files are compliant")
    print("5. Include compliance report in your final message")
    print("=" * 50)

def main():
    """Main function for command-line usage."""
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = "."
    
    # Run compliance check
    compliance_summary = run_compliance_check(project_root)
    
    # Print agent reminder
    agent_compliance_reminder()
    
    # Exit with appropriate code
    if compliance_summary['is_compliant']:
        print("\n✅ Agent can proceed - all files are compliant")
        sys.exit(0)
    else:
        print("\n❌ Agent must fix violations before proceeding")
        sys.exit(1)

if __name__ == "__main__":
    main() 