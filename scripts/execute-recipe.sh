#!/bin/bash

echo "Starting AI-Q Universal Digital Twin Core Infrastructure Setup..."

# Create project directory
mkdir -p ai-Q-universal-digital-twin
cd ai-Q-universal-digital-twin

# Create directory structure
mkdir -p src/{api,services,models,utils,config}
mkdir -p frontend/{src,public}
mkdir -p docker config data logs tests docs scripts recipes

# Initialize Git
git init
echo "__pycache__/
node_modules/
.env*
logs/*.log" > .gitignore

# Create Docker Compose
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

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

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

volumes:
  postgres_data:
  minio_data:
EOF

# Start infrastructure
docker-compose up -d

echo "Core infrastructure setup completed!"
echo "Services available at:"
echo "- PostgreSQL: localhost:5432"
echo "- Redis: localhost:6379" 
echo "- Minio: localhost:9000 (console: localhost:9001)" 