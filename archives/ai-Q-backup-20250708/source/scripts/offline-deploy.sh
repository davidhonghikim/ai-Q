#!/bin/bash

# AI-Q Offline Deployment Script
# Version: 1.0.0
# Created: 2025-01-28
# Purpose: Deploy AI-Q system without internet connectivity

set -euo pipefail

# Configuration
OFFLINE_ROOT="/opt/ai-q/offline"
DOCKER_IMAGES_DIR="$OFFLINE_ROOT/docker-images"
PACKAGES_DIR="$OFFLINE_ROOT/packages"
LOG_FILE="$OFFLINE_ROOT/logs/offline-deploy-$(date +%Y%m%d-%H%M%S).log"

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
    log "ERROR: $1"
    exit 1
}

# Check offline prerequisites
check_offline_prerequisites() {
    log "Checking offline prerequisites..."
    
    if [[ ! -d "$OFFLINE_ROOT" ]]; then
        error_exit "Offline root directory does not exist"
    fi
    
    if [[ ! -d "$DOCKER_IMAGES_DIR" ]]; then
        error_exit "Docker images directory does not exist"
    fi
    
    if [[ ! -d "$PACKAGES_DIR" ]]; then
        error_exit "Packages directory does not exist"
    fi
    
    log "Offline prerequisites check passed"
}

# Load Docker images
load_docker_images() {
    log "Loading Docker images..."
    
    local images_loaded=0
    
    for tar_file in "$DOCKER_IMAGES_DIR/services/"*.tar.gz; do
        if [[ -f "$tar_file" ]]; then
            log "Loading Docker image: $(basename "$tar_file")"
            
            gunzip -c "$tar_file" | docker load 2>> "$LOG_FILE" || {
                error_exit "Failed to load Docker image: $tar_file"
            }
            
            ((images_loaded++))
        fi
    done
    
    log "Loaded $images_loaded Docker images"
}

# Install Python packages
install_python_packages() {
    log "Installing Python packages..."
    
    if [[ -d "$PACKAGES_DIR/python" ]]; then
        cd "$PACKAGES_DIR/python"
        
        for wheel_file in *.whl; do
            if [[ -f "$wheel_file" ]]; then
                log "Installing Python package: $wheel_file"
                
                pip install "$wheel_file" 2>> "$LOG_FILE" || {
                    error_exit "Failed to install Python package: $wheel_file"
                }
            fi
        done
        
        log "Python packages installed successfully"
    fi
}

# Install Node.js packages
install_node_packages() {
    log "Installing Node.js packages..."
    
    if [[ -d "$PACKAGES_DIR/node" ]]; then
        cd "$PACKAGES_DIR/node"
        
        for tgz_file in *.tgz; do
            if [[ -f "$tgz_file" ]]; then
                log "Installing Node.js package: $tgz_file"
                
                npm install "$tgz_file" 2>> "$LOG_FILE" || {
                    error_exit "Failed to install Node.js package: $tgz_file"
                }
            fi
        done
        
        log "Node.js packages installed successfully"
    fi
}

# Setup local Docker registry
setup_local_registry() {
    log "Setting up local Docker registry..."
    
    # Start local registry
    docker run -d --name ai-q-offline-registry \
        -p 5000:5000 \
        -v /opt/ai-q/data/registry:/var/lib/registry \
        registry:2.8.2 2>> "$LOG_FILE" || {
        error_exit "Failed to start local Docker registry"
    }
    
    log "Local Docker registry started on port 5000"
}

# Deploy services
deploy_services() {
    log "Deploying services..."
    
    # Change to project directory
    cd /opt/ai-q
    
    # Deploy using Docker Compose
    docker-compose -f docker/compose/docker-compose.yml up -d 2>> "$LOG_FILE" || {
        error_exit "Failed to deploy services"
    }
    
    log "Services deployed successfully"
}

# Verify deployment
verify_deployment() {
    log "Verifying deployment..."
    
    # Check if all containers are running
    local running_containers=$(docker ps --format "table {{.Names}}" | grep ai-q | wc -l)
    local expected_containers=12  # Adjust based on your services
    
    if [[ $running_containers -lt $expected_containers ]]; then
        error_exit "Not all containers are running (expected: $expected_containers, running: $running_containers)"
    fi
    
    log "Deployment verification passed ($running_containers containers running)"
}

# Main execution
main() {
    log "Starting offline deployment process..."
    
    check_offline_prerequisites
    load_docker_images
    install_python_packages
    install_node_packages
    setup_local_registry
    deploy_services
    verify_deployment
    
    log "Offline deployment process completed successfully"
}

# Execute main function
main "$@" 