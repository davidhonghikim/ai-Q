#!/bin/bash

# AI-Q Ollama Model Puller
# This script pulls the default models for the AI-Q system

echo "🚀 AI-Q Ollama Model Puller"
echo "=========================="

# Default models to pull (smallest/fastest for quick startup)
MODELS=(
    "gemma3:2b"      # Fast, efficient model for general tasks (2B parameters)
    "llama3.2:3b"    # Excellent function calling capabilities (3B parameters)
)

# Optional larger models (uncomment to include)
# MODELS+=(
#     "codellama:7b"   # Good for code generation and function calling (7B parameters)
#     "qwen2.5:7b"     # Good balance of performance and function calling (7B parameters)
# )

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "❌ Error: Ollama is not running on localhost:11434"
    echo "Please start Ollama first: docker-compose up ollama"
    exit 1
fi

echo "✅ Ollama is running"
echo "📥 Pulling default models..."

# Pull each model
for model in "${MODELS[@]}"; do
    echo "📦 Pulling $model..."
    if ollama pull "$model"; then
        echo "✅ Successfully pulled $model"
    else
        echo "❌ Failed to pull $model"
    fi
    echo ""
done

echo "🎉 Model pulling complete!"
echo ""
echo "📋 Available models:"
ollama list

echo ""
echo "💡 Model recommendations:"
echo "  • Function Calling: llama3.2:3b (default), qwen2.5:7b (optional), codellama:7b (optional)"
echo "  • Code Generation: codellama:7b (optional), llama3.2:3b (default)"
echo "  • General Tasks: gemma3:2b (default), qwen2.5:7b (optional)"
echo "  • Fast Response: gemma3:2b (default), llama3.2:3b (default)"
echo "  • High Quality: qwen2.5:7b (optional), codellama:7b (optional)" 