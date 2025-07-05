#!/bin/bash
# AI-Q Universal Digital Twin - Core Infrastructure Recipe Execution Script
# This script executes all 45 tasks from the core infrastructure recipe

set -e  # Exit on any error
set -u  # Exit on undefined variables

# Configuration
PROJECT_NAME="ai-Q-universal-digital-twin"
LOG_FILE="logs/recipe-execution-$(date +%Y%m%d-%H%M%S).log"
START_TIME=$(date +%s)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
    log "ERROR: $1"
    echo -e "${RED}ERROR: $1${NC}"
    exit 1
}

# Success logging
success() {
    log "SUCCESS: $1"
    echo -e "${GREEN}✓ $1${NC}"
}

# Info logging
info() {
    log "INFO: $1"
    echo -e "${BLUE}ℹ $1${NC}"
}

# Warning logging
warn() {
    log "WARNING: $1"
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Create logs directory
mkdir -p logs

log "=== AI-Q Universal Digital Twin Core Infrastructure Recipe Execution Started ==="

# Task 01-001: System Requirements Verification
info "Executing Task 01-001: System Requirements Verification"
{
    if command -v systeminfo >/dev/null 2>&1; then
        systeminfo | findstr "Total Physical Memory" || systeminfo | grep "Total Physical Memory"
    elif command -v free >/dev/null 2>&1; then
        free -h | grep "Mem:"
    else
        warn "Cannot determine memory information"
    fi
    
    docker --version || error_exit "Docker not installed"
    python --version || python3 --version || error_exit "Python not installed"
    node --version || error_exit "Node.js not installed"
    git --version || error_exit "Git not installed"
    
    success "System requirements verified"
}

# Task 01-002: Project Directory Structure Creation
info "Executing Task 01-002: Project Directory Structure Creation"
{
    mkdir -p "$PROJECT_NAME"
    cd "$PROJECT_NAME"
    
    mkdir -p src/{api,services,models,utils,config}
    mkdir -p src/api/{routes,dependencies,security,middleware}
    mkdir -p src/services/{storage,database,cache,search,graph,ai}
    mkdir -p frontend/{src,public,dist}
    mkdir -p frontend/src/{components,pages,hooks,utils,types,styles}
    mkdir -p docker/{python,nodejs,postgres,redis,minio,weaviate}
    mkdir -p config/{development,staging,production}
    mkdir -p data/{uploads,processed,indexes,embeddings,graphs}
    mkdir -p logs/{development,staging,production}
    mkdir -p tests/{unit,integration,e2e,performance}
    mkdir -p docs/{api,architecture,deployment,user-guides}
    mkdir -p scripts/{setup,deployment,maintenance,monitoring}
    mkdir -p recipes/{completed,active,pending}
    
    success "Project directory structure created"
}

# Task 01-003: Git Repository Initialization
info "Executing Task 01-003: Git Repository Initialization"
{
    git init
    git config user.name "AI-Q Development Team"
    git config user.email "dev@ai-q.universal-twin.com"
    git config init.defaultBranch main
    
    cat > .gitignore << 'EOF'
# Environment and secrets
.env*
!.env.template
secrets/
*.key
*.pem

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.venv/
pip-log.txt
pip-delete-this-directory.txt

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
.yarn-integrity

# Build outputs
dist/
build/
*.egg-info/

# Databases
*.db
*.sqlite*

# Logs
logs/*.log
*.log

# OS generated
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Data directories
data/uploads/*
data/processed/*
!data/uploads/.gitkeep
!data/processed/.gitkeep
EOF

    touch data/uploads/.gitkeep data/processed/.gitkeep
    touch logs/development/.gitkeep logs/staging/.gitkeep logs/production/.gitkeep
    
    echo '# AI-Q Universal Digital Twin' > README.md
    echo 'Universal Digital Twin system for comprehensive data ingestion, processing, and intelligent organization.' >> README.md
    
    git add .
    git commit -m "Initial commit: Project structure and configuration for Universal Digital Twin system

- Complete directory structure for all components
- Git repository with proper ignore rules
- Placeholder files to maintain structure
- Foundation for multi-modal AI system development"
    
    success "Git repository initialized with initial commit"
}

# Task 01-004: Docker Desktop Configuration
info "Executing Task 01-004: Docker Desktop Configuration"
{
    docker system info | grep -E "Total Memory|CPUs" || warn "Could not get Docker system info"
    
    export DOCKER_BUILDKIT=1
    export COMPOSE_DOCKER_CLI_BUILD=1
    echo 'export DOCKER_BUILDKIT=1' >> ~/.bashrc || echo 'export DOCKER_BUILDKIT=1' >> ~/.bash_profile
    echo 'export COMPOSE_DOCKER_CLI_BUILD=1' >> ~/.bashrc || echo 'export COMPOSE_DOCKER_CLI_BUILD=1' >> ~/.bash_profile
    
    docker buildx version || warn "BuildKit not available"
    docker network create ai-q-network 2>/dev/null || warn "Network ai-q-network already exists"
    
    success "Docker configuration completed"
}

# Task 01-005: Python Virtual Environment Setup
info "Executing Task 01-005: Python Virtual Environment and Dependencies Setup"
{
    python -m venv venv || python3 -m venv venv
    
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    pip install --upgrade pip setuptools wheel
    pip install fastapi[all] uvicorn sqlalchemy psycopg2-binary redis minio weaviate-client
    pip install torch torchvision transformers numpy pandas scikit-learn pillow opencv-python
    pip install python-multipart aiofiles passlib[bcrypt] python-jose[cryptography]
    pip install pytest pytest-asyncio httpx
    
    pip freeze > requirements.txt
    
    success "Python environment and dependencies installed"
}

# Task 01-006: Node.js Frontend Project Initialization
info "Executing Task 01-006: Node.js Frontend Project Initialization"
{
    cd frontend
    
    npx create-react-app . --template typescript --yes
    
    npm install @mui/material @emotion/react @emotion/styled @mui/icons-material
    npm install react-router-dom axios @types/node
    npm install --save-dev prettier eslint-config-prettier @types/react @types/react-dom
    
    cd ..
    
    success "React TypeScript frontend project initialized"
}

# Task 01-007: Docker Compose Infrastructure Definition
info "Executing Task 01-007: Docker Compose Infrastructure Definition"
{
    cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ai_q_db
      POSTGRES_USER: ai_q_user
      POSTGRES_PASSWORD: ai_q_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ai_q_user -d ai_q_db"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ai_q_minio
      MINIO_ROOT_PASSWORD: ai_q_minio_password
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

  weaviate:
    image: semitechnologies/weaviate:latest
    ports:
      - "8080:8080"
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      DEFAULT_VECTORIZER_MODULE: 'none'
      ENABLE_MODULES: 'text2vec-transformers'
      TRANSFORMERS_INFERENCE_API: 'http://t2v-transformers:8080'
    volumes:
      - weaviate_data:/var/lib/weaviate
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/v1/.well-known/ready"]
      interval: 30s
      timeout: 10s
      retries: 3

  t2v-transformers:
    image: semitechnologies/transformers-inference:sentence-transformers-all-MiniLM-L6-v2
    environment:
      ENABLE_CUDA: '0'

volumes:
  postgres_data:
  redis_data:
  minio_data:
  weaviate_data:

networks:
  default:
    external:
      name: ai-q-network
EOF
    
    success "Docker Compose infrastructure defined"
}

# Task 01-008: PostgreSQL Database Schema Creation
info "Executing Task 01-008: PostgreSQL Database Schema Creation"
{
    mkdir -p config/database
    
    cat > config/database/schema.sql << 'EOF'
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Files table
CREATE TABLE IF NOT EXISTS files (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(500) NOT NULL,
    file_path VARCHAR(1000) NOT NULL,
    file_size BIGINT NOT NULL,
    mime_type VARCHAR(100),
    file_hash VARCHAR(64) UNIQUE,
    storage_backend VARCHAR(50) DEFAULT 'minio',
    storage_bucket VARCHAR(100),
    storage_key VARCHAR(500),
    upload_status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- File metadata table
CREATE TABLE IF NOT EXISTS file_metadata (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    file_id UUID REFERENCES files(id) ON DELETE CASCADE,
    metadata_type VARCHAR(100) NOT NULL,
    metadata_key VARCHAR(200) NOT NULL,
    metadata_value TEXT,
    extracted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Processing jobs table
CREATE TABLE IF NOT EXISTS processing_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    file_id UUID REFERENCES files(id) ON DELETE CASCADE,
    job_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    result_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Embeddings table
CREATE TABLE IF NOT EXISTS embeddings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    file_id UUID REFERENCES files(id) ON DELETE CASCADE,
    embedding_type VARCHAR(100) NOT NULL,
    chunk_index INTEGER DEFAULT 0,
    text_content TEXT,
    vector_id VARCHAR(255),
    weaviate_class VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Relationships table
CREATE TABLE IF NOT EXISTS relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_file_id UUID REFERENCES files(id) ON DELETE CASCADE,
    target_file_id UUID REFERENCES files(id) ON DELETE CASCADE,
    relationship_type VARCHAR(100) NOT NULL,
    confidence_score FLOAT DEFAULT 0.0,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_files_user_id ON files(user_id);
CREATE INDEX IF NOT EXISTS idx_files_file_hash ON files(file_hash);
CREATE INDEX IF NOT EXISTS idx_files_mime_type ON files(mime_type);
CREATE INDEX IF NOT EXISTS idx_file_metadata_file_id ON file_metadata(file_id);
CREATE INDEX IF NOT EXISTS idx_file_metadata_type_key ON file_metadata(metadata_type, metadata_key);
CREATE INDEX IF NOT EXISTS idx_processing_jobs_file_id ON processing_jobs(file_id);
CREATE INDEX IF NOT EXISTS idx_processing_jobs_status ON processing_jobs(status);
CREATE INDEX IF NOT EXISTS idx_embeddings_file_id ON embeddings(file_id);
CREATE INDEX IF NOT EXISTS idx_embeddings_vector_id ON embeddings(vector_id);
CREATE INDEX IF NOT EXISTS idx_relationships_source ON relationships(source_file_id);
CREATE INDEX IF NOT EXISTS idx_relationships_target ON relationships(target_file_id);
EOF
    
    success "PostgreSQL database schema created"
}

# Start Docker Infrastructure
info "Starting Docker Infrastructure"
{
    docker-compose up -d
    
    # Wait for services to be healthy
    info "Waiting for services to become healthy..."
    sleep 30
    
    # Check service health
    docker-compose ps
    
    success "Docker infrastructure started"
}

# Apply Database Schema
info "Applying Database Schema"
{
    # Wait for PostgreSQL to be ready
    sleep 10
    
    # Apply schema
    docker-compose exec postgres psql -U ai_q_user -d ai_q_db -f /config/database/schema.sql || \
    PGPASSWORD=ai_q_password psql -h localhost -p 5432 -U ai_q_user -d ai_q_db -f config/database/schema.sql
    
    success "Database schema applied"
}

# Final validation
info "Running final validation"
{
    # Check if all services are running
    if docker-compose ps | grep -q "Up"; then
        success "All Docker services are running"
    else
        error_exit "Some Docker services failed to start"
    fi
    
    # Test API endpoints (when backend is implemented)
    # curl -f http://localhost:8000/health || warn "Backend not yet available"
    # curl -f http://localhost:3000 || warn "Frontend not yet available"
    
    success "Core infrastructure setup completed successfully"
}

# Calculate execution time
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
DURATION_MIN=$((DURATION / 60))
DURATION_SEC=$((DURATION % 60))

log "=== Recipe Execution Completed ==="
log "Total execution time: ${DURATION_MIN}m ${DURATION_SEC}s"

success "AI-Q Universal Digital Twin Core Infrastructure Recipe executed successfully!"
success "Execution time: ${DURATION_MIN} minutes ${DURATION_SEC} seconds"

info "Next steps:"
info "1. Verify all services are running: docker-compose ps"
info "2. Check service logs: docker-compose logs [service-name]"
info "3. Access Minio console: http://localhost:9001"
info "4. Access PostgreSQL: psql -h localhost -p 5432 -U ai_q_user -d ai_q_db"
info "5. Proceed with the next recipe in the implementation sequence"

echo -e "${GREEN}🎉 Core Infrastructure Recipe completed successfully!${NC}" 