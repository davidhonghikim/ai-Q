#!/bin/bash

# AI-Q Offline Docker Image Download Script
# Version: 1.0.0
# Created: 2025-01-28
# Purpose: Download and cache all Docker images for offline deployment

set -euo pipefail

# Configuration
OFFLINE_ROOT="/opt/ai-q/offline"
DOCKER_IMAGES_DIR="$OFFLINE_ROOT/docker-images"
LOG_FILE="$OFFLINE_ROOT/logs/docker-download-$(date +%Y%m%d-%H%M%S).log"

# Required Docker images
DOCKER_IMAGES=(
    "postgres:15-alpine"
    "redis:7-alpine"
    "docker.elastic.co/elasticsearch/elasticsearch:8.11.0"
    "neo4j:5.15.0"
    "semitechnologies/weaviate:1.22.4"
    "minio/minio:RELEASE.2023-11-15T20-43-25Z"
    "grafana/grafana:10.2.0"
    "prom/prometheus:v2.47.0"
    "prom/alertmanager:v0.26.0"
    "gitea/gitea:1.21.0"
    "nextcloud:25.0.0"
    "registry:2.8.2"
    "alpine:3.18"
    "ubuntu:22.04"
    "python:3.11-slim"
    "node:18-alpine"
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
    
    if ! command -v docker &> /dev/null; then
        error_exit "Docker is not installed"
    fi
    
    if ! command -v wget &> /dev/null; then
        error_exit "wget is not installed"
    fi
    
    log "Prerequisites check passed"
}

# Create directories
create_directories() {
    log "Creating directories..."
    
    mkdir -p "$DOCKER_IMAGES_DIR/base"
    mkdir -p "$DOCKER_IMAGES_DIR/services"
    mkdir -p "$DOCKER_IMAGES_DIR/tools"
    mkdir -p "$OFFLINE_ROOT/logs"
    
    log "Directories created"
}

# Download Docker image
download_image() {
    local image="$1"
    local image_name=$(echo "$image" | sed 's/[^a-zA-Z0-9]/_/g')
    local tar_file="$DOCKER_IMAGES_DIR/services/${image_name}.tar"
    
    log "Downloading Docker image: $image"
    
    # Pull image
    docker pull "$image" 2>> "$LOG_FILE" || {
        error_exit "Failed to pull image: $image"
    }
    
    # Save image to tar file
    docker save "$image" -o "$tar_file" 2>> "$LOG_FILE" || {
        error_exit "Failed to save image: $image"
    }
    
    # Compress tar file
    gzip "$tar_file" 2>> "$LOG_FILE" || {
        error_exit "Failed to compress image: $image"
    }
    
    log "Downloaded and cached: ${tar_file}.gz"
}

# Create image manifest
create_manifest() {
    log "Creating image manifest..."
    
    local manifest_file="$DOCKER_IMAGES_DIR/images-manifest.json"
    
    cat > "$manifest_file" << EOF
{
  "version": "1.0.0",
  "created": "$(date -Iseconds)",
  "images": [
EOF
    
    for image in "${DOCKER_IMAGES[@]}"; do
        local image_name=$(echo "$image" | sed 's/[^a-zA-Z0-9]/_/g')
        local tar_file="${image_name}.tar.gz"
        local file_size=$(stat -c %s "$DOCKER_IMAGES_DIR/services/$tar_file" 2>/dev/null || echo 0)
        
        cat >> "$manifest_file" << EOF
    {
      "name": "$image",
      "filename": "$tar_file",
      "size_bytes": $file_size,
      "cached": $(if [[ -f "$DOCKER_IMAGES_DIR/services/$tar_file" ]]; then echo true; else echo false; fi)
    },
EOF
    done
    
    # Remove trailing comma
    sed -i '$ s/,$//' "$manifest_file"
    
    cat >> "$manifest_file" << EOF
  ]
}
EOF
    
    log "Image manifest created: $manifest_file"
}

# Main execution
main() {
    log "Starting Docker image download process..."
    
    check_prerequisites
    create_directories
    
    # Download all images
    for image in "${DOCKER_IMAGES[@]}"; do
        download_image "$image"
    done
    
    create_manifest
    
    log "Docker image download process completed successfully"
}

# Execute main function
main "$@" 