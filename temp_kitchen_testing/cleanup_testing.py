#!/usr/bin/env python3
"""
Kitchen Testing Environment Cleanup Script
Removes temporary testing environment
"""

import shutil
import os

def cleanup_testing_environment():
    """Remove temporary testing environment"""
    temp_dir = "temp_kitchen_testing"
    
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        print(f"✅ Cleaned up temporary testing environment: {temp_dir}")
    else:
        print(f"⚠️  Temporary directory not found: {temp_dir}")

if __name__ == "__main__":
    cleanup_testing_environment()
