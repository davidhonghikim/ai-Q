#!/bin/bash

# AI-Q Offline Package Download Script
# Version: 1.0.0
# Created: 2025-01-28
# Purpose: Download and cache all packages for offline deployment

set -euo pipefail

# Configuration
OFFLINE_ROOT="/opt/ai-q/offline"
PACKAGES_DIR="$OFFLINE_ROOT/packages"
LOG_FILE="$OFFLINE_ROOT/logs/package-download-$(date +%Y%m%d-%H%M%S).log"

# Required Python packages
PYTHON_PACKAGES=(
    "fastapi==0.104.1"
    "uvicorn==0.24.0"
    "sqlalchemy==2.0.23"
    "psycopg2-binary==2.9.9"
    "redis==5.0.1"
    "elasticsearch==8.11.0"
    "weaviate-client==3.25.3"
    "minio==7.2.0"
    "pydantic==2.5.0"
    "python-jose==3.3.0"
    "passlib==1.7.4"
    "python-multipart==0.0.6"
    "aiofiles==23.2.1"
    "httpx==0.25.2"
    "pytest==7.4.3"
    "pytest-asyncio==0.21.1"
)

# Required Node.js packages
NODE_PACKAGES=(
    "next@14.0.4"
    "react@18.2.0"
    "react-dom@18.2.0"
    "@types/node@20.10.4"
    "@types/react@18.2.45"
    "@types/react-dom@18.2.18"
    "typescript@5.3.3"
    "tailwindcss@3.3.6"
    "autoprefixer@10.4.16"
    "postcss@8.4.32"
)

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
    log "ERROR: $1"
    exit 1
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    if [[ ! -d "$OFFLINE_ROOT" ]]; then
        error_exit "Offline root directory does not exist"
    fi
    
    if ! command -v pip &> /dev/null; then
        error_exit "pip is not installed"
    fi
    
    if ! command -v npm &> /dev/null; then
        error_exit "npm is not installed"
    fi
    
    log "Prerequisites check passed"
}

# Create directories
create_directories() {
    log "Creating directories..."
    
    mkdir -p "$PACKAGES_DIR/python"
    mkdir -p "$PACKAGES_DIR/node"
    mkdir -p "$PACKAGES_DIR/system"
    mkdir -p "$OFFLINE_ROOT/logs"
    
    log "Directories created"
}

# Download Python packages
download_python_packages() {
    log "Downloading Python packages..."
    
    cd "$PACKAGES_DIR/python"
    
    for package in "${PYTHON_PACKAGES[@]}"; do
        log "Downloading Python package: $package"
        
        pip download "$package" 2>> "$LOG_FILE" || {
            error_exit "Failed to download Python package: $package"
        }
    done
    
    log "Python packages downloaded successfully"
}

# Download Node.js packages
download_node_packages() {
    log "Downloading Node.js packages..."
    
    cd "$PACKAGES_DIR/node"
    
    for package in "${NODE_PACKAGES[@]}"; do
        log "Downloading Node.js package: $package"
        
        npm pack "$package" 2>> "$LOG_FILE" || {
            error_exit "Failed to download Node.js package: $package"
        }
    done
    
    log "Node.js packages downloaded successfully"
}

# Create package manifest
create_manifest() {
    log "Creating package manifest..."
    
    local manifest_file="$PACKAGES_DIR/packages-manifest.json"
    
    cat > "$manifest_file" << EOF
{
  "version": "1.0.0",
  "created": "$(date -Iseconds)",
  "python_packages": [
EOF
    
    for package in "${PYTHON_PACKAGES[@]}"; do
        cat >> "$manifest_file" << EOF
    "$package",
EOF
    done
    
    # Remove trailing comma
    sed -i '$ s/,$//' "$manifest_file"
    
    cat >> "$manifest_file" << EOF
  ],
  "node_packages": [
EOF
    
    for package in "${NODE_PACKAGES[@]}"; do
        cat >> "$manifest_file" << EOF
    "$package",
EOF
    done
    
    # Remove trailing comma
    sed -i '$ s/,$//' "$manifest_file"
    
    cat >> "$manifest_file" << EOF
  ]
}
EOF
    
    log "Package manifest created: $manifest_file"
}

# Main execution
main() {
    log "Starting package download process..."
    
    check_prerequisites
    create_directories
    download_python_packages
    download_node_packages
    create_manifest
    
    log "Package download process completed successfully"
}

# Execute main function
main "$@" 