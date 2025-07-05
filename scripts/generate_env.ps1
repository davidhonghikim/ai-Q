# AI-Q Knowledge Library System - Environment File Generator
# Created by: Claude Sonnet 4 - Claude Sonnet 4
# Timestamp: 2025-01-27T22:00:00Z

$envContent = @"
# AI-Q Knowledge Library System - Environment Configuration
# Created by: Claude Sonnet 4 - Claude Sonnet 4
# Timestamp: 2025-01-27T22:00:00Z
# Purpose: Environment variables for AI-Q Knowledge Library System

# Project Configuration
PROJECT_NAME=AI-Q Knowledge Library System
PROJECT_VERSION=1.0.0
ENVIRONMENT=development
NODE_ENV=development

# Network Configuration
NETWORK_SUBNET=172.20.0.0/16
NETWORK_GATEWAY=172.20.0.1
CONTAINER_PREFIX=aiq
SERVICE_NAMESPACE=aiq

# Database Configuration - PostgreSQL
POSTGRES_PORT=5432
POSTGRES_DB=aiq_knowledge
POSTGRES_USER=aiq_user
POSTGRES_PASSWORD=aiq_password
POSTGRES_HOST=postgres
POSTGRES_INITDB_ARGS=--auth-host=scram-sha-256

# Database Configuration - Redis
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_HOST=redis
REDIS_DB=0

# Search Engine Configuration - Elasticsearch
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_CLUSTER_PORT=9300
ELASTICSEARCH_PASSWORD=elastic
ELASTICSEARCH_HOST=elasticsearch
ELASTICSEARCH_DISCOVERY_TYPE=single-node
ELASTICSEARCH_XPACK_SECURITY_ENABLED=true
ELASTICSEARCH_JAVA_OPTS=-Xms512m -Xmx512m

# Graph Database Configuration - Neo4j
NEO4J_BROWSER_PORT=7474
NEO4J_BOLT_PORT=7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
NEO4J_HOST=neo4j
NEO4J_PLUGINS=["apoc", "graph-data-science"]
NEO4J_PROCEDURES_UNRESTRICTED=gds.*,apoc.*
NEO4J_HEAP_INITIAL_SIZE=512m
NEO4J_HEAP_MAX_SIZE=1G
NEO4J_PAGECACHE_SIZE=512m

# Vector Database Configuration - Weaviate
WEAVIATE_PORT=8080
WEAVIATE_HOST=weaviate
WEAVIATE_QUERY_DEFAULTS_LIMIT=25
WEAVIATE_AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true
WEAVIATE_PERSISTENCE_DATA_PATH=/var/lib/weaviate
WEAVIATE_DEFAULT_VECTORIZER_MODULE=text2vec-transformers
WEAVIATE_ENABLE_MODULES=text2vec-transformers,ref2vec-centroid,generative-openai,qna-openai
WEAVIATE_TRANSFORMERS_INFERENCE_API=http://t2v-transformers:8080
WEAVIATE_CLUSTER_HOSTNAME=node1

# Object Storage Configuration - MinIO
MINIO_API_PORT=9000
MINIO_CONSOLE_PORT=9001
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_HOST=minio
MINIO_CONSOLE_ADDRESS=minio:9001

# API Server Configuration
API_SERVER_PORT=8000
API_SERVER_HOST=0.0.0.0
JWT_SECRET=your-super-secret-jwt-key-change-in-production
API_ENVIRONMENT=development

# Web Dashboard Configuration
WEB_DASHBOARD_PORT=3000
WEB_DASHBOARD_HOST=0.0.0.0
WEB_ENVIRONMENT=development

# Security Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
RATE_LIMIT_REQUESTS_PER_MINUTE=100
JWT_EXPIRATION_HOURS=24
BCRYPT_ROUNDS=12

# Logging Configuration
LOG_LEVEL=info
LOG_FORMAT=JSON
LOG_DESTINATION=console

# Feature Flags
ENABLE_RAG=true
ENABLE_KNOWLEDGE_GRAPH=true
ENABLE_VECTOR_SEARCH=true
ENABLE_OBJECT_STORAGE=true
ENABLE_API_DOCUMENTATION=true
"@

# Write the content to .env file
$envContent | Out-File -FilePath ".env" -Encoding UTF8

Write-Host "Environment file (.env) created successfully!"
Write-Host "Location: $(Get-Location)\.env" 