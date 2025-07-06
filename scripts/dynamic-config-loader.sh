#!/bin/bash

# AI-Q Dynamic Configuration Loader
# Version: 1.0.0
# Created: 2025-01-28
# Purpose: Load dynamic port and IP configuration from JSON files

set -euo pipefail

# Configuration paths
CONFIG_ROOT="/opt/ai-q/config"
DYNAMIC_CONFIG="$CONFIG_ROOT/dynamic/dynamic-config.json"
NETWORK_CONFIG="$CONFIG_ROOT/network/ip-config.json"
ENV_FILE="/opt/ai-q/.env.dynamic"

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Error handling
error_exit() {
    log "ERROR: $1"
    exit 1
}

# Check if jq is available
check_dependencies() {
    if ! command -v jq &> /dev/null; then
        error_exit "jq is required but not installed"
    fi
}

# Load network profile
load_network_profile() {
    local profile="${AIQ_NETWORK_PROFILE:-local_network}"
    
    log "Loading network profile: $profile"
    
    # Extract network configuration
    local bind_address=$(jq -r ".network_profiles.$profile.bind_address" "$DYNAMIC_CONFIG")
    local external_address=$(jq -r ".network_profiles.$profile.external_address" "$DYNAMIC_CONFIG")
    local base_url=$(jq -r ".network_profiles.$profile.base_url" "$DYNAMIC_CONFIG")
    local subnet=$(jq -r ".network_profiles.$profile.subnet" "$DYNAMIC_CONFIG")
    local gateway=$(jq -r ".network_profiles.$profile.gateway" "$DYNAMIC_CONFIG")
    
    # Export network variables
    export AIQ_NETWORK_PROFILE="$profile"
    export AIQ_BIND_ADDRESS="$bind_address"
    export AIQ_EXTERNAL_ADDRESS="$external_address"
    export AIQ_BASE_URL="$base_url"
    export AIQ_SUBNET="$subnet"
    export AIQ_GATEWAY="$gateway"
    
    log "Network profile loaded: $external_address ($bind_address)"
}

# Generate service URLs
generate_service_urls() {
    log "Generating service URLs..."
    
    # Clear existing environment file
    > "$ENV_FILE"
    
    # Add network configuration
    cat >> "$ENV_FILE" << EOF
# AI-Q Dynamic Configuration
# Generated: $(date)
AIQ_NETWORK_PROFILE=$AIQ_NETWORK_PROFILE
AIQ_BIND_ADDRESS=$AIQ_BIND_ADDRESS
AIQ_EXTERNAL_ADDRESS=$AIQ_EXTERNAL_ADDRESS
AIQ_BASE_URL=$AIQ_BASE_URL
AIQ_SUBNET=$AIQ_SUBNET
AIQ_GATEWAY=$AIQ_GATEWAY

EOF
    
    # Generate URLs for each service category
    local categories=("frontend_services" "backend_services" "ai_ml_services" "middleware_services" "monitoring_services" "storage_services")
    
    for category in "${categories[@]}"; do
        log "Processing $category..."
        
        # Get all services in this category
        local services=$(jq -r ".port_configuration.$category.services | keys[]" "$DYNAMIC_CONFIG" 2>/dev/null || true)
        
        for service in $services; do
            local port=$(jq -r ".port_configuration.$category.services.$service.port" "$DYNAMIC_CONFIG")
            local name=$(jq -r ".port_configuration.$category.services.$service.name" "$DYNAMIC_CONFIG")
            local description=$(jq -r ".port_configuration.$category.services.$service.description" "$DYNAMIC_CONFIG")
            local url_template=$(jq -r ".port_configuration.$category.services.$service.url_template" "$DYNAMIC_CONFIG")
            local health_check=$(jq -r ".port_configuration.$category.services.$service.health_check" "$DYNAMIC_CONFIG")
            
            # Generate URL
            local url=$(echo "$url_template" | sed "s/{base_url}/$AIQ_BASE_URL/g" | sed "s/{port}/$port/g")
            
            # Export variables
            local service_upper=$(echo "$service" | tr '[:lower:]' '[:upper:]')
            export "${service_upper}_PORT=$port"
            export "${service_upper}_URL=$url"
            export "${service_upper}_HEALTH_CHECK=$health_check"
            
            # Add to environment file
            cat >> "$ENV_FILE" << EOF
# $name - $description
${service_upper}_PORT=$port
${service_upper}_URL=$url
${service_upper}_HEALTH_CHECK=$health_check

EOF
            
            log "  $name: $url (port $port)"
        done
    done
    
    log "Service URLs generated and saved to $ENV_FILE"
}

# Generate Docker Compose environment variables
generate_docker_env() {
    log "Generating Docker Compose environment variables..."
    
    local docker_env_file="/opt/ai-q/docker/.env.dynamic"
    
    # Clear existing file
    > "$docker_env_file"
    
    # Add network configuration
    cat >> "$docker_env_file" << EOF
# AI-Q Docker Dynamic Configuration
# Generated: $(date)

# Network Configuration
AIQ_NETWORK_PROFILE=$AIQ_NETWORK_PROFILE
AIQ_BIND_ADDRESS=$AIQ_BIND_ADDRESS
AIQ_EXTERNAL_ADDRESS=$AIQ_EXTERNAL_ADDRESS
AIQ_BASE_URL=$AIQ_BASE_URL

# Service Ports
EOF
    
    # Add service ports
    local categories=("frontend_services" "backend_services" "ai_ml_services" "middleware_services" "monitoring_services" "storage_services")
    
    for category in "${categories[@]}"; do
        local services=$(jq -r ".port_configuration.$category.services | keys[]" "$DYNAMIC_CONFIG" 2>/dev/null || true)
        
        for service in $services; do
            local port=$(jq -r ".port_configuration.$category.services.$service.port" "$DYNAMIC_CONFIG")
            local name=$(jq -r ".port_configuration.$category.services.$service.name" "$DYNAMIC_CONFIG")
            local service_upper=$(echo "$service" | tr '[:lower:]' '[:upper:]')
            
            echo "${service_upper}_PORT=$port" >> "$docker_env_file"
        done
    done
    
    log "Docker environment file generated: $docker_env_file"
}

# Validate configuration
validate_configuration() {
    log "Validating configuration..."
    
    # Check if all required files exist
    if [[ ! -f "$DYNAMIC_CONFIG" ]]; then
        error_exit "Dynamic configuration file not found: $DYNAMIC_CONFIG"
    fi
    
    if [[ ! -f "$NETWORK_CONFIG" ]]; then
        error_exit "Network configuration file not found: $NETWORK_CONFIG"
    fi
    
    # Validate JSON format
    if ! jq empty "$DYNAMIC_CONFIG" 2>/dev/null; then
        error_exit "Invalid JSON in dynamic configuration file"
    fi
    
    if ! jq empty "$NETWORK_CONFIG" 2>/dev/null; then
        error_exit "Invalid JSON in network configuration file"
    fi
    
    log "Configuration validation passed"
}

# Display current configuration
display_configuration() {
    log "Current Configuration:"
    log "  Network Profile: $AIQ_NETWORK_PROFILE"
    log "  Bind Address: $AIQ_BIND_ADDRESS"
    log "  External Address: $AIQ_EXTERNAL_ADDRESS"
    log "  Base URL: $AIQ_BASE_URL"
    log "  Environment File: $ENV_FILE"
    
    echo ""
    log "Service URLs:"
    local categories=("frontend_services" "backend_services" "ai_ml_services")
    
    for category in "${categories[@]}"; do
        local services=$(jq -r ".port_configuration.$category.services | keys[]" "$DYNAMIC_CONFIG" 2>/dev/null || true)
        
        for service in $services; do
            local name=$(jq -r ".port_configuration.$category.services.$service.name" "$DYNAMIC_CONFIG")
            local service_upper=$(echo "$service" | tr '[:lower:]' '[:upper:]')
            local url="${service_upper}_URL"
            
            if [[ -n "${!url:-}" ]]; then
                log "  $name: ${!url}"
            fi
        done
    done
}

# Main execution
main() {
    log "Starting dynamic configuration loader..."
    
    check_dependencies
    validate_configuration
    load_network_profile
    generate_service_urls
    generate_docker_env
    display_configuration
    
    log "Dynamic configuration loading completed successfully"
    log "To use this configuration, source the environment file:"
    log "  source $ENV_FILE"
}

# Execute main function
main "$@" 