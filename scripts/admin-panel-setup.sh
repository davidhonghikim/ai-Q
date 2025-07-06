#!/bin/bash

# AI-Q Admin Panel Setup Script
# Version: 1.0.0
# Created: 2025-01-28
# Purpose: Setup and configure custom admin panel

set -euo pipefail

# Configuration
SELF_HOSTED_ROOT="/opt/ai-q/self-hosted"
ADMIN_PANEL_DIR="$SELF_HOSTED_ROOT/admin-panel"
CONFIGS_DIR="$SELF_HOSTED_ROOT/configs"
LOG_FILE="$SELF_HOSTED_ROOT/logs/admin-panel-setup-$(date +%Y%m%d-%H%M%S).log"

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

# Create admin panel directories
create_admin_panel_directories() {
    log "Creating admin panel directories..."
    
    mkdir -p "$ADMIN_PANEL_DIR"
    mkdir -p "$CONFIGS_DIR"
    mkdir -p "$SELF_HOSTED_ROOT/logs"
    
    log "Admin panel directories created"
}

# Create admin panel HTML
create_admin_panel_html() {
    log "Creating admin panel HTML..."
    
    local html_file="$ADMIN_PANEL_DIR/index.html"
    
    cat > "$html_file" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Q Admin Panel</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
        }
        .content {
            padding: 30px;
        }
        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .service-card {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .service-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .service-card h3 {
            margin: 0 0 10px 0;
            color: #2c3e50;
        }
        .service-card p {
            margin: 0 0 15px 0;
            color: #6c757d;
        }
        .service-link {
            display: inline-block;
            background: #007bff;
            color: white;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 4px;
            transition: background 0.2s;
        }
        .service-link:hover {
            background: #0056b3;
        }
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-online {
            background: #28a745;
        }
        .status-offline {
            background: #dc3545;
        }
        .system-info {
            background: #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
        }
        .system-info h3 {
            margin: 0 0 15px 0;
            color: #2c3e50;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }
        .info-item {
            background: white;
            padding: 15px;
            border-radius: 4px;
            border-left: 4px solid #007bff;
        }
        .info-item strong {
            display: block;
            margin-bottom: 5px;
            color: #2c3e50;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI-Q Admin Panel</h1>
            <p>Knowledge Library System Management</p>
        </div>
        
        <div class="content">
            <div class="services-grid">
                <div class="service-card">
                    <h3><span class="status-indicator status-online"></span>Gitea Git Server</h3>
                    <p>Self-hosted Git repository management</p>
                    <a href="http://localhost:3002" target="_blank" class="service-link">Access Gitea</a>
                </div>
                
                <div class="service-card">
                    <h3><span class="status-indicator status-online"></span>NextCloud Storage</h3>
                    <p>File storage and synchronization</p>
                    <a href="http://localhost:8080" target="_blank" class="service-link">Access NextCloud</a>
                </div>
                
                <div class="service-card">
                    <h3><span class="status-indicator status-online"></span>OpenWebUI</h3>
                    <p>AI chat interface with Ollama</p>
                    <a href="http://localhost:3000" target="_blank" class="service-link">Access OpenWebUI</a>
                </div>
                
                <div class="service-card">
                    <h3><span class="status-indicator status-online"></span>AI-Q API</h3>
                    <p>Knowledge library API endpoints</p>
                    <a href="http://localhost:8000/docs" target="_blank" class="service-link">API Docs</a>
                </div>
                
                <div class="service-card">
                    <h3><span class="status-indicator status-online"></span>Grafana Monitoring</h3>
                    <p>System monitoring and analytics</p>
                    <a href="http://localhost:3001" target="_blank" class="service-link">Access Grafana</a>
                </div>
                
                <div class="service-card">
                    <h3><span class="status-indicator status-online"></span>Prometheus</h3>
                    <p>Metrics collection and storage</p>
                    <a href="http://localhost:9090" target="_blank" class="service-link">Access Prometheus</a>
                </div>
                
                <div class="service-card">
                    <h3><span class="status-indicator status-online"></span>Docker Registry</h3>
                    <p>Local container image registry</p>
                    <a href="http://localhost:5000" target="_blank" class="service-link">Access Registry</a>
                </div>
            </div>
            
            <div class="system-info">
                <h3>System Information</h3>
                <div class="info-grid">
                    <div class="info-item">
                        <strong>System Status</strong>
                        <span>All Services Online</span>
                    </div>
                    <div class="info-item">
                        <strong>Uptime</strong>
                        <span id="uptime">Loading...</span>
                    </div>
                    <div class="info-item">
                        <strong>Memory Usage</strong>
                        <span id="memory">Loading...</span>
                    </div>
                    <div class="info-item">
                        <strong>Disk Usage</strong>
                        <span id="disk">Loading...</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Update system information
        function updateSystemInfo() {
            // Simulate system info updates
            document.getElementById('uptime').textContent = '2 days, 14 hours';
            document.getElementById('memory').textContent = '45% (3.2GB / 8GB)';
            document.getElementById('disk').textContent = '67% (134GB / 200GB)';
        }
        
        // Update status indicators
        function updateStatusIndicators() {
            const services = [
                { url: 'http://localhost:3002', selector: '.service-card:nth-child(1) .status-indicator' },
                { url: 'http://localhost:8080', selector: '.service-card:nth-child(2) .status-indicator' },
                { url: 'http://localhost:8000', selector: '.service-card:nth-child(3) .status-indicator' },
                { url: 'http://localhost:3000', selector: '.service-card:nth-child(4) .status-indicator' },
                { url: 'http://localhost:9090', selector: '.service-card:nth-child(5) .status-indicator' },
                { url: 'http://localhost:5000', selector: '.service-card:nth-child(6) .status-indicator' }
            ];
            
            services.forEach(service => {
                fetch(service.url, { mode: 'no-cors' })
                    .then(() => {
                        document.querySelector(service.selector).className = 'status-indicator status-online';
                    })
                    .catch(() => {
                        document.querySelector(service.selector).className = 'status-indicator status-offline';
                    });
            });
        }
        
        // Initialize
        updateSystemInfo();
        updateStatusIndicators();
        
        // Update every 30 seconds
        setInterval(updateSystemInfo, 30000);
        setInterval(updateStatusIndicators, 30000);
    </script>
</body>
</html>
EOF
    
    log "Admin panel HTML created: $html_file"
}

# Create admin panel Dockerfile
create_admin_panel_dockerfile() {
    log "Creating admin panel Dockerfile..."
    
    local dockerfile="$ADMIN_PANEL_DIR/Dockerfile"
    
    cat > "$dockerfile" << 'EOF'
FROM nginx:alpine

# Copy admin panel files
COPY index.html /usr/share/nginx/html/

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
EOF
    
    log "Admin panel Dockerfile created: $dockerfile"
}

# Create nginx configuration
create_nginx_config() {
    log "Creating nginx configuration..."
    
    local nginx_config="$ADMIN_PANEL_DIR/nginx.conf"
    
    cat > "$nginx_config" << 'EOF'
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    
    sendfile        on;
    keepalive_timeout  65;
    
    server {
        listen       80;
        server_name  localhost;
        
        location / {
            root   /usr/share/nginx/html;
            index  index.html index.htm;
        }
        
        # Health check endpoint
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
        
        # Error pages
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }
    }
}
EOF
    
    log "Nginx configuration created: $nginx_config"
}

# Build and start admin panel container
build_and_start_admin_panel() {
    log "Building and starting admin panel container..."
    
    # Change to admin panel directory
    cd "$ADMIN_PANEL_DIR"
    
    # Build Docker image
    docker build -t ai-q-admin-panel . 2>> "$LOG_FILE" || {
        error_exit "Failed to build admin panel Docker image"
    }
    
    # Stop existing container if running
    docker stop ai-q-admin-panel 2>/dev/null || true
    docker rm ai-q-admin-panel 2>/dev/null || true
    
    # Start admin panel container
    docker run -d \
        --name ai-q-admin-panel \
        --restart unless-stopped \
        -p 9000:80 \
        ai-q-admin-panel 2>> "$LOG_FILE" || {
        error_exit "Failed to start admin panel container"
    }
    
    log "Admin panel container started successfully"
}

# Wait for admin panel to be ready
wait_for_admin_panel() {
    log "Waiting for admin panel to be ready..."
    
    local max_attempts=10
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        if curl -s http://localhost:9000 > /dev/null 2>&1; then
            log "Admin panel is ready"
            return 0
        fi
        
        log "Attempt $attempt/$max_attempts: Admin panel not ready yet, waiting..."
        sleep 5
        ((attempt++))
    done
    
    error_exit "Admin panel failed to start within expected time"
}

# Verify admin panel installation
verify_admin_panel_installation() {
    log "Verifying admin panel installation..."
    
    # Check if container is running
    if ! docker ps | grep -q ai-q-admin-panel; then
        error_exit "Admin panel container is not running"
    fi
    
    # Check if web interface is accessible
    if ! curl -s http://localhost:9000 > /dev/null; then
        error_exit "Admin panel web interface is not accessible"
    fi
    
    # Check if health endpoint is working
    if ! curl -s http://localhost:9000/health > /dev/null; then
        error_exit "Admin panel health endpoint is not working"
    fi
    
    log "Admin panel installation verified successfully"
}

# Main execution
main() {
    log "Starting admin panel setup process..."
    
    check_prerequisites
    create_admin_panel_directories
    create_admin_panel_html
    create_admin_panel_dockerfile
    create_nginx_config
    build_and_start_admin_panel
    wait_for_admin_panel
    verify_admin_panel_installation
    
    log "Admin panel setup process completed successfully"
    log "Admin panel is accessible at: http://localhost:9000"
}

# Execute main function
main "$@" 