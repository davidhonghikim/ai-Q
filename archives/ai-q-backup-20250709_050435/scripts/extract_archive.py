#!/usr/bin/env python3
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
