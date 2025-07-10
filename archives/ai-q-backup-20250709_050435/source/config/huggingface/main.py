from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import torch
from sentence_transformers import SentenceTransformer
import os
import logging

# Read config from environment variables
MODEL_NAME = os.getenv("MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
DEVICE = os.getenv("DEVICE", "cuda" if torch.cuda.is_available() else "cpu")
MAX_BATCH_SIZE = int(os.getenv("MAX_BATCH_SIZE", "32"))
MAX_BATCH_WAIT = float(os.getenv("MAX_BATCH_WAIT", "0.1"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", None)

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))
logger = logging.getLogger(__name__)

app = FastAPI(title="HuggingFace Transformers Inference", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

model = None

class EmbeddingRequest(BaseModel):
    texts: List[str]

class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]

@app.on_event("startup")
async def load_model():
    global model
    try:
        logger.info(f"Loading model: {MODEL_NAME} on device: {DEVICE}")
        if HUGGINGFACE_TOKEN:
            model = SentenceTransformer(MODEL_NAME, device=DEVICE, use_auth_token=HUGGINGFACE_TOKEN)
        else:
            model = SentenceTransformer(MODEL_NAME, device=DEVICE)
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise e

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/embeddings", response_model=EmbeddingResponse)
async def get_embeddings(request: EmbeddingRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    try:
        embeddings = model.encode(request.texts, convert_to_tensor=False, batch_size=MAX_BATCH_SIZE)
        embeddings_list = embeddings.tolist() if hasattr(embeddings, 'tolist') else embeddings
        return EmbeddingResponse(embeddings=embeddings_list)
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        raise HTTPException(status_code=500, detail=f"Embedding generation failed: {str(e)}")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/api/info")
async def api_info():
    return {
        "service": "HuggingFace Transformers Inference",
        "version": "1.0.0",
        "model": MODEL_NAME,
        "device": DEVICE,
        "max_batch_size": MAX_BATCH_SIZE,
        "max_batch_wait": MAX_BATCH_WAIT,
        "log_level": LOG_LEVEL,
        "huggingface_token": bool(HUGGINGFACE_TOKEN),
        "endpoints": {
            "health": "/health",
            "embeddings": "/embeddings",
            "ui": "/static/index.html"
        }
    } 