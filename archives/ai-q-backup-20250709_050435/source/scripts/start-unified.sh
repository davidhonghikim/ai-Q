#!/bin/bash

echo "Starting AI-Q Unified Application..."

# Wait for all infrastructure services to be ready
echo "Waiting for infrastructure services..."
./scripts/wait-for-services.sh

# Start the API server in the background
echo "Starting API server..."
python3 src/main.py &
API_PID=$!

# Wait a moment for the API server to start
sleep 5

# Start the web dashboard in the background
echo "Starting web dashboard..."
cd src/web
npm start &
WEB_PID=$!

# Start Cadvisor for monitoring
echo "Starting container monitoring..."
cadvisor &
CADVISOR_PID=$!

# Function to handle shutdown
cleanup() {
    echo "Shutting down services..."
    kill $API_PID $WEB_PID $CADVISOR_PID 2>/dev/null
    wait
    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT

echo "All services started successfully!"
echo "API Server: http://localhost:8000"
echo "Web Dashboard: http://localhost:3000"
echo "Monitoring: http://localhost:8081"

# Wait for all background processes
wait 