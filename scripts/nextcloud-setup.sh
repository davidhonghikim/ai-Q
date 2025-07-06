#!/bin/bash

# AI-Q NextCloud Setup Script
# Version: 1.0.0
# Created: 2025-01-28
# Purpose: Setup and configure NextCloud file storage

set -euo pipefail

# Configuration
SELF_HOSTED_ROOT="/opt/ai-q/self-hosted"
NEXTCLOUD_DIR="$SELF_HOSTED_ROOT/nextcloud"
CONFIGS_DIR="$SELF_HOSTED_ROOT/configs"
LOG_FILE="$SELF_HOSTED_ROOT/logs/nextcloud-setup-$(date +%Y%m%d-%H%M%S).log"

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
    
    if [[ ! -d "$SELF_HOSTED_ROOT" ]]; then
        error_exit "Self-hosted root directory does not exist"
    fi
    
    if ! command -v docker &> /dev/null; then
        error_exit "Docker is not installed"
    fi
    
    log "Prerequisites check passed"
}

# Create NextCloud directories
create_nextcloud_directories() {
    log "Creating NextCloud directories..."
    
    mkdir -p "$NEXTCLOUD_DIR"
    mkdir -p "$CONFIGS_DIR"
    mkdir -p "$SELF_HOSTED_ROOT/logs"
    
    log "NextCloud directories created"
}

# Create NextCloud configuration
create_nextcloud_config() {
    log "Creating NextCloud configuration..."
    
    local config_file="$CONFIGS_DIR/nextcloud-config.php"
    
    cat > "$config_file" << 'EOF'
<?php
$CONFIG = array (
  'instanceid' => 'ai-q-nextcloud',
  'passwordsalt' => 'your-super-secret-nextcloud-salt-change-in-production',
  'secret' => 'your-super-secret-nextcloud-key-change-in-production',
  'trusted_domains' => 
  array (
    0 => 'localhost',
    1 => '127.0.0.1',
  ),
  'datadirectory' => '/var/www/html/data',
  'dbtype' => 'sqlite3',
  'version' => '25.0.0.0',
  'overwrite.cli.url' => 'http://localhost:8080',
  'htaccess.RewriteBase' => '/',
  'installed' => true,
);
EOF
    
    log "NextCloud configuration created: $config_file"
}

# Start NextCloud container
start_nextcloud_container() {
    log "Starting NextCloud container..."
    
    # Stop existing container if running
    docker stop ai-q-nextcloud 2>/dev/null || true
    docker rm ai-q-nextcloud 2>/dev/null || true
    
    # Start NextCloud container
    docker run -d \
        --name ai-q-nextcloud \
        --restart unless-stopped \
        -p 8080:80 \
        -e NEXTCLOUD_ADMIN_USER=admin \
        -e NEXTCLOUD_ADMIN_PASSWORD=admin123 \
        -v "$NEXTCLOUD_DIR:/var/www/html" \
        -v "$CONFIGS_DIR/nextcloud-config.php:/var/www/html/config/config.php" \
        nextcloud:25.0.0 2>> "$LOG_FILE" || {
        error_exit "Failed to start NextCloud container"
    }
    
    log "NextCloud container started successfully"
}

# Wait for NextCloud to be ready
wait_for_nextcloud() {
    log "Waiting for NextCloud to be ready..."
    
    local max_attempts=30
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        if curl -s http://localhost:8080 > /dev/null 2>&1; then
            log "NextCloud is ready"
            return 0
        fi
        
        log "Attempt $attempt/$max_attempts: NextCloud not ready yet, waiting..."
        sleep 10
        ((attempt++))
    done
    
    error_exit "NextCloud failed to start within expected time"
}

# Create initial folders
create_initial_folders() {
    log "Creating initial folders..."
    
    # Wait a bit more for NextCloud to fully initialize
    sleep 30
    
    # Create AI-Q folders
    curl -X MKCOL "http://localhost:8080/remote.php/dav/files/admin/ai-q" \
        -u "admin:admin123" 2>> "$LOG_FILE" || {
        log "Warning: Failed to create ai-q folder"
    }
    
    curl -X MKCOL "http://localhost:8080/remote.php/dav/files/admin/ai-q/documents" \
        -u "admin:admin123" 2>> "$LOG_FILE" || {
        log "Warning: Failed to create documents folder"
    }
    
    curl -X MKCOL "http://localhost:8080/remote.php/dav/files/admin/ai-q/backups" \
        -u "admin:admin123" 2>> "$LOG_FILE" || {
        log "Warning: Failed to create backups folder"
    }
    
    curl -X MKCOL "http://localhost:8080/remote.php/dav/files/admin/ai-q/logs" \
        -u "admin:admin123" 2>> "$LOG_FILE" || {
        log "Warning: Failed to create logs folder"
    }
    
    log "Initial folders created"
}

# Verify NextCloud installation
verify_nextcloud_installation() {
    log "Verifying NextCloud installation..."
    
    # Check if container is running
    if ! docker ps | grep -q ai-q-nextcloud; then
        error_exit "NextCloud container is not running"
    fi
    
    # Check if web interface is accessible
    if ! curl -s http://localhost:8080 > /dev/null; then
        error_exit "NextCloud web interface is not accessible"
    fi
    
    # Check if status endpoint is working
    if ! curl -s http://localhost:8080/status.php > /dev/null; then
        error_exit "NextCloud status endpoint is not working"
    fi
    
    log "NextCloud installation verified successfully"
}

# Main execution
main() {
    log "Starting NextCloud setup process..."
    
    check_prerequisites
    create_nextcloud_directories
    create_nextcloud_config
    start_nextcloud_container
    wait_for_nextcloud
    create_initial_folders
    verify_nextcloud_installation
    
    log "NextCloud setup process completed successfully"
    log "NextCloud is accessible at: http://localhost:8080"
    log "Admin credentials: admin / admin123"
}

# Execute main function
main "$@" 