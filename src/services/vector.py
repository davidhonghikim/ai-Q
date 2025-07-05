# AI-Q Knowledge Library System - Vector Database Service
# TOKEN COUNT: ~1,200 tokens
"""
Vector database service for AI-Q Knowledge Library System.
Handles Weaviate vector database operations and embeddings.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager

import weaviate

from src.config.settings import get_settings

# Configure logging
logger = logging.getLogger(__name__)

class VectorService:
    """Vector database service for managing Weaviate operations."""
    
    def __init__(self):
        self.settings = get_settings()
        self.client: Optional[weaviate.Client] = None
    
    async def initialize(self) -> None:
        """Initialize Weaviate client connection."""
        try:
            logger.info("Initializing vector database service...")
            
            # Create Weaviate client (for weaviate-client 3.x)
            self.client = weaviate.Client(
                url=f"http://{self.settings.vector_database.weaviate.host}:{self.settings.vector_database.weaviate.port}",
                # TODO: Add authentication if needed
            )
            
            # Test connection
            await self._test_connection()
            
            logger.info("Vector database service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize vector database service: {e}")
            raise
    
    async def _test_connection(self) -> None:
        """Test Weaviate connection."""
        try:
            if self.client:
                is_ready = self.client.is_ready()
                if not is_ready:
                    raise ConnectionError("Weaviate is not ready")
            logger.info("Vector database connection test successful")
        except Exception as e:
            logger.error(f"Vector database connection test failed: {e}")
            raise
    
    async def create_collection(self, collection_name: str, properties: List[Dict[str, Any]]) -> None:
        """Create a new collection in Weaviate."""
        try:
            if not self.client:
                raise RuntimeError("Vector service not initialized")
            
            # Create collection schema
            collection = self.client.collections.create(
                name=collection_name,
                properties=properties,
                vectorizer_config=weaviate.classes.config.Configure.Vectorizer.text2vec_transformers()
            )
            
            logger.info(f"Collection '{collection_name}' created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create collection '{collection_name}': {e}")
            raise
    
    async def add_document(self, collection_name: str, document: Dict[str, Any]) -> str:
        """Add a document to a collection."""
        try:
            if not self.client:
                raise RuntimeError("Vector service not initialized")
            
            collection = self.client.collections.get(collection_name)
            uuid = collection.data.insert(document)
            
            logger.info(f"Document added to collection '{collection_name}' with UUID: {uuid}")
            return uuid
            
        except Exception as e:
            logger.error(f"Failed to add document to collection '{collection_name}': {e}")
            raise
    
    async def search_similar(self, collection_name: str, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for similar documents in a collection."""
        try:
            if not self.client:
                raise RuntimeError("Vector service not initialized")
            
            collection = self.client.collections.get(collection_name)
            response = collection.query.near_text(
                query=query,
                limit=limit
            )
            
            results = []
            for obj in response.objects:
                results.append({
                    'uuid': obj.uuid,
                    'properties': obj.properties,
                    'score': obj.metadata.score if hasattr(obj.metadata, 'score') else None
                })
            
            logger.info(f"Found {len(results)} similar documents in collection '{collection_name}'")
            return results
            
        except Exception as e:
            logger.error(f"Failed to search collection '{collection_name}': {e}")
            raise
    
    async def delete_document(self, collection_name: str, uuid: str) -> None:
        """Delete a document from a collection."""
        try:
            if not self.client:
                raise RuntimeError("Vector service not initialized")
            
            collection = self.client.collections.get(collection_name)
            collection.data.delete_by_id(uuid)
            
            logger.info(f"Document {uuid} deleted from collection '{collection_name}'")
            
        except Exception as e:
            logger.error(f"Failed to delete document {uuid} from collection '{collection_name}': {e}")
            raise
    
    async def update_document(self, collection_name: str, uuid: str, properties: Dict[str, Any]) -> None:
        """Update a document in a collection."""
        try:
            if not self.client:
                raise RuntimeError("Vector service not initialized")
            
            collection = self.client.collections.get(collection_name)
            collection.data.update(
                uuid=uuid,
                properties=properties
            )
            
            logger.info(f"Document {uuid} updated in collection '{collection_name}'")
            
        except Exception as e:
            logger.error(f"Failed to update document {uuid} in collection '{collection_name}': {e}")
            raise
    
    async def get_document(self, collection_name: str, uuid: str) -> Optional[Dict[str, Any]]:
        """Get a document from a collection."""
        try:
            if not self.client:
                raise RuntimeError("Vector service not initialized")
            
            collection = self.client.collections.get(collection_name)
            obj = collection.query.fetch_object_by_id(uuid)
            
            if obj:
                return {
                    'uuid': obj.uuid,
                    'properties': obj.properties
                }
            return None
            
        except Exception as e:
            logger.error(f"Failed to get document {uuid} from collection '{collection_name}': {e}")
            raise
    
    async def close(self) -> None:
        """Close Weaviate client connection."""
        try:
            if self.client:
                self.client.close()
            logger.info("Vector database connections closed")
        except Exception as e:
            logger.error(f"Error closing vector database connections: {e}")

# Global vector service instance
_vector_service: Optional[VectorService] = None

async def init_vector_service() -> None:
    """Initialize the vector service."""
    global _vector_service
    
    try:
        _vector_service = VectorService()
        await _vector_service.initialize()
        logger.info("Vector service initialization completed")
    except Exception as e:
        logger.error(f"Vector service initialization failed: {e}")
        raise

async def get_vector_service() -> VectorService:
    """Get the vector service instance."""
    if not _vector_service:
        raise RuntimeError("Vector service not initialized")
    return _vector_service

async def close_vector_service() -> None:
    """Close vector service connections."""
    global _vector_service
    if _vector_service:
        await _vector_service.close()
        _vector_service = None 