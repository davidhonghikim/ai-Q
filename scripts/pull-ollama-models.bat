@echo off
REM AI-Q Ollama Model Puller (Windows)
REM This script pulls the default models for the AI-Q system

echo 🚀 AI-Q Ollama Model Puller
echo ==========================

REM Default models to pull (smallest/fastest for quick startup)
set MODELS=gemma3:2b llama3.2:3b

REM Optional larger models (uncomment to include)
REM set MODELS=%MODELS% codellama:7b qwen2.5:7b

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Ollama is not running on localhost:11434
    echo Please start Ollama first: docker-compose up ollama
    pause
    exit /b 1
)

echo ✅ Ollama is running
echo 📥 Pulling default models...

REM Pull each model
for %%m in (%MODELS%) do (
    echo 📦 Pulling %%m...
    ollama pull %%m
    if errorlevel 1 (
        echo ❌ Failed to pull %%m
    ) else (
        echo ✅ Successfully pulled %%m
    )
    echo.
)

echo 🎉 Model pulling complete!
echo.
echo 📋 Available models:
ollama list

echo.
echo 💡 Model recommendations:
echo   • Function Calling: llama3.2:3b (default), qwen2.5:7b (optional), codellama:7b (optional)
echo   • Code Generation: codellama:7b (optional), llama3.2:3b (default)
echo   • General Tasks: gemma3:2b (default), qwen2.5:7b (optional)
echo   • Fast Response: gemma3:2b (default), llama3.2:3b (default)
echo   • High Quality: qwen2.5:7b (optional), codellama:7b (optional)

pause 