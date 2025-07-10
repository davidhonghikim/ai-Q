#!/bin/bash

# AI-Q Gitea Setup Script
# Version: 1.0.0
# Created: 2025-01-28
# Purpose: Setup and configure Gitea Git server

set -euo pipefail

# Configuration
SELF_HOSTED_ROOT="/opt/ai-q/self-hosted"
GITEA_DIR="$SELF_HOSTED_ROOT/gitea"
CONFIGS_DIR="$SELF_HOSTED_ROOT/configs"
LOG_FILE="$SELF_HOSTED_ROOT/logs/gitea-setup-$(date +%Y%m%d-%H%M%S).log"

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

# Create Gitea directories
create_gitea_directories() {
    log "Creating Gitea directories..."
    
    mkdir -p "$GITEA_DIR"
    mkdir -p "$CONFIGS_DIR"
    mkdir -p "$SELF_HOSTED_ROOT/logs"
    
    log "Gitea directories created"
}

# Create Gitea configuration
create_gitea_config() {
    log "Creating Gitea configuration..."
    
    local config_file="$CONFIGS_DIR/gitea-app.ini"
    
    cat > "$config_file" << 'EOF'
[server]
DOMAIN = localhost
ROOT_URL = http://localhost:3002/
HTTP_ADDR = 0.0.0.0
HTTP_PORT = 3000

[database]
DB_TYPE = sqlite3
PATH = /data/gitea/gitea.db

[repository]
ROOT = /data/git/repositories

[server]
START_SSH_SERVER = true
SSH_PORT = 22

[security]
INSTALL_LOCK = true
SECRET_KEY = your-super-secret-gitea-key-change-in-production

[service]
DISABLE_REGISTRATION = false
REQUIRE_SIGNIN_VIEW = false

[admin]
USERNAME = admin
EMAIL = admin@ai-q.local
PASSWORD = admin123

[log]
MODE = file
LEVEL = Info
FILE_PATH = /data/gitea/log/gitea.log
EOF
    
    log "Gitea configuration created: $config_file"
}

# Start Gitea container
start_gitea_container() {
    log "Starting Gitea container..."
    
    # Stop existing container if running
    docker stop ai-q-gitea 2>/dev/null || true
    docker rm ai-q-gitea 2>/dev/null || true
    
    # Start Gitea container
    docker run -d \
        --name ai-q-gitea \
        --restart unless-stopped \
        -p 3002:3000 \
        -p 222:22 \
        -e USER_UID=1000 \
        -e USER_GID=1000 \
        -v "$GITEA_DIR:/data" \
        -v "$CONFIGS_DIR/gitea-app.ini:/data/gitea/conf/app.ini" \
        gitea/gitea:1.21.0 2>> "$LOG_FILE" || {
        error_exit "Failed to start Gitea container"
    }
    
    log "Gitea container started successfully"
}

# Wait for Gitea to be ready
wait_for_gitea() {
    log "Waiting for Gitea to be ready..."
    
    local max_attempts=30
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        if curl -s http://localhost:3002 > /dev/null 2>&1; then
            log "Gitea is ready"
            return 0
        fi
        
        log "Attempt $attempt/$max_attempts: Gitea not ready yet, waiting..."
        sleep 10
        ((attempt++))
    done
    
    error_exit "Gitea failed to start within expected time"
}

# Create initial repositories
create_initial_repositories() {
    log "Creating initial repositories..."
    
    # Wait a bit more for Gitea to fully initialize
    sleep 30
    
    # Create AI-Q repository
    curl -X POST "http://localhost:3002/api/v1/user/repos" \
        -H "Content-Type: application/json" \
        -d '{
            "name": "ai-q",
            "description": "AI-Q Knowledge Library System",
            "private": false,
            "auto_init": true
        }' \
        -u "admin:admin123" 2>> "$LOG_FILE" || {
        log "Warning: Failed to create ai-q repository"
    }
    
    # Create documentation repository
    curl -X POST "http://localhost:3002/api/v1/user/repos" \
        -H "Content-Type: application/json" \
        -d '{
            "name": "ai-q-docs",
            "description": "AI-Q Documentation",
            "private": false,
            "auto_init": true
        }' \
        -u "admin:admin123" 2>> "$LOG_FILE" || {
        log "Warning: Failed to create ai-q-docs repository"
    }
    
    log "Initial repositories created"
}

# Verify Gitea installation
verify_gitea_installation() {
    log "Verifying Gitea installation..."
    
    # Check if container is running
    if ! docker ps | grep -q ai-q-gitea; then
        error_exit "Gitea container is not running"
    fi
    
    # Check if web interface is accessible
    if ! curl -s http://localhost:3002 > /dev/null; then
        error_exit "Gitea web interface is not accessible"
    fi
    
    # Check if API is working
    if ! curl -s http://localhost:3002/api/v1/version > /dev/null; then
        error_exit "Gitea API is not working"
    fi
    
    log "Gitea installation verified successfully"
}

# Main execution
main() {
    log "Starting Gitea setup process..."
    
    check_prerequisites
    create_gitea_directories
    create_gitea_config
    start_gitea_container
    wait_for_gitea
    create_initial_repositories
    verify_gitea_installation
    
    log "Gitea setup process completed successfully"
    log "Gitea is accessible at: http://localhost:3002"
    log "Admin credentials: admin / admin123"
}

# Execute main function
main "$@" 