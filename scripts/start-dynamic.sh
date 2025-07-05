#!/bin/bash

echo "Starting AI-Q Dynamic Application with Feature Flags..."

# Parse feature flags and generate configurations
echo "Parsing feature flags..."
python3 scripts/feature-flag-parser.py generate-compose
python3 scripts/feature-flag-parser.py generate-env

# Load environment variables
if [ -f ".env.feature-flags" ]; then
    echo "Loading feature flag environment variables..."
    export $(cat .env.feature-flags | xargs)
fi

# Check which services are enabled
echo "Checking enabled services..."
ENABLED_SERVICES=$(python3 -c "
import sys
sys.path.append('src')
from core.feature_manager import feature_manager
print(' '.join(feature_manager.get_enabled_components()))
")

echo "Enabled services: $ENABLED_SERVICES"

# Start infrastructure services based on feature flags
if [ "$ENABLE_POSTGRESQL" = "true" ]; then
    echo "Starting PostgreSQL..."
    docker-compose -f docker-compose.feature-flags.yml up -d postgres
fi

if [ "$ENABLE_REDIS" = "true" ]; then
    echo "Starting Redis..."
    docker-compose -f docker-compose.feature-flags.yml up -d redis
fi

if [ "$ENABLE_ELASTICSEARCH" = "true" ]; then
    echo "Starting Elasticsearch..."
    docker-compose -f docker-compose.feature-flags.yml up -d elasticsearch
fi

if [ "$ENABLE_NEO4J" = "true" ]; then
    echo "Starting Neo4j..."
    docker-compose -f docker-compose.feature-flags.yml up -d neo4j
fi

if [ "$ENABLE_WEAVIATE" = "true" ]; then
    echo "Starting Weaviate..."
    docker-compose -f docker-compose.feature-flags.yml up -d weaviate
fi

if [ "$ENABLE_MINIO" = "true" ]; then
    echo "Starting MinIO..."
    docker-compose -f docker-compose.feature-flags.yml up -d minio
fi

if [ "$ENABLE_PROMETHEUS" = "true" ]; then
    echo "Starting Prometheus..."
    docker-compose -f docker-compose.feature-flags.yml up -d prometheus
fi

if [ "$ENABLE_GRAFANA" = "true" ]; then
    echo "Starting Grafana..."
    docker-compose -f docker-compose.feature-flags.yml up -d grafana
fi

# Wait for infrastructure services
echo "Waiting for infrastructure services..."
sleep 10

# Start the main application with dynamic loading
echo "Starting AI-Q Dynamic Application..."
python3 src/main_dynamic.py 