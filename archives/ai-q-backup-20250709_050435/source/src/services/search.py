# AI-Q Knowledge Library System - Search Service
# TOKEN COUNT: ~1,300 tokens
"""
Search service for AI-Q Knowledge Library System.
Handles Elasticsearch initialization and search operations.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError
from src.config.settings import get_settings

# Configure logging
logger = logging.getLogger(__name__)

class SearchService:
    """Search service for managing Elasticsearch operations."""
    
    def __init__(self):
        self.settings = get_settings()
        self.es_client: Optional[AsyncElasticsearch] = None
        self.index_prefix = "aiq"
    
    async def initialize(self) -> None:
        """Initialize Elasticsearch connection and create indices."""
        try:
            logger.info("Initializing search service...")
            
            # Create Elasticsearch client
            self.es_client = AsyncElasticsearch(
                hosts=[{
                    'host': self.settings.search_engine.elasticsearch.host,
                    'port': self.settings.search_engine.elasticsearch.port
                }],
                http_auth=('elastic', self.settings.search_engine.elasticsearch.password),
                use_ssl=False,
                verify_certs=False,
                timeout=30,
                max_retries=3,
                retry_on_timeout=True
            )
            
            # Test connection
            await self._test_connection()
            
            # Create indices
            await self._create_indices()
            
            logger.info("Search service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize search service: {e}")
            raise
    
    async def _test_connection(self) -> None:
        """Test Elasticsearch connection."""
        try:
            info = await self.es_client.info()
            logger.info(f"Elasticsearch connection test successful - Version: {info['version']['number']}")
        except Exception as e:
            logger.error(f"Elasticsearch connection test failed: {e}")
            raise
    
    async def _create_indices(self) -> None:
        """Create Elasticsearch indices if they don't exist."""
        indices = [
            f"{self.index_prefix}_knowledge",
            f"{self.index_prefix}_documents",
            f"{self.index_prefix}_users",
            f"{self.index_prefix}_sessions"
        ]
        
        for index_name in indices:
            await self._create_index(index_name)
    
    async def _create_index(self, index_name: str) -> None:
        """Create a specific index with mapping."""
        try:
            if not await self.es_client.indices.exists(index=index_name):
                # Define mapping for knowledge index
                if index_name == f"{self.index_prefix}_knowledge":
                    mapping = {
                        "mappings": {
                            "properties": {
                                "id": {"type": "keyword"},
                                "title": {"type": "text", "analyzer": "standard"},
                                "content": {"type": "text", "analyzer": "standard"},
                                "tags": {"type": "keyword"},
                                "category": {"type": "keyword"},
                                "author": {"type": "keyword"},
                                "created_at": {"type": "date"},
                                "updated_at": {"type": "date"},
                                "metadata": {"type": "object", "enabled": True}
                            }
                        },
                        "settings": {
                            "number_of_shards": 1,
                            "number_of_replicas": 0,
                            "analysis": {
                                "analyzer": {
                                    "aiq_analyzer": {
                                        "type": "custom",
                                        "tokenizer": "standard",
                                        "filter": ["lowercase", "stop", "snowball"]
                                    }
                                }
                            }
                        }
                    }
                else:
                    # Default mapping for other indices
                    mapping = {
                        "mappings": {
                            "properties": {
                                "id": {"type": "keyword"},
                                "content": {"type": "text", "analyzer": "standard"},
                                "created_at": {"type": "date"},
                                "updated_at": {"type": "date"}
                            }
                        },
                        "settings": {
                            "number_of_shards": 1,
                            "number_of_replicas": 0
                        }
                    }
                
                await self.es_client.indices.create(index=index_name, body=mapping)
                logger.info(f"Created index: {index_name}")
            else:
                logger.info(f"Index already exists: {index_name}")
                
        except Exception as e:
            logger.error(f"Failed to create index {index_name}: {e}")
            raise
    
    async def index_document(self, index_name: str, document_id: str, document: Dict[str, Any]) -> bool:
        """Index a document in Elasticsearch."""
        try:
            full_index_name = f"{self.index_prefix}_{index_name}"
            
            # Add timestamps
            document["updated_at"] = datetime.utcnow().isoformat()
            if "created_at" not in document:
                document["created_at"] = document["updated_at"]
            
            await self.es_client.index(
                index=full_index_name,
                id=document_id,
                body=document
            )
            
            # Refresh index to make document searchable immediately
            await self.es_client.indices.refresh(index=full_index_name)
            
            logger.debug(f"Indexed document {document_id} in {full_index_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to index document {document_id}: {e}")
            return False
    
    async def search_documents(self, index_name: str, query: str, size: int = 10, 
                              filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search documents in Elasticsearch."""
        try:
            full_index_name = f"{self.index_prefix}_{index_name}"
            
            # Build search query
            search_body = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "multi_match": {
                                    "query": query,
                                    "fields": ["title^2", "content", "tags"],
                                    "type": "best_fields",
                                    "fuzziness": "AUTO"
                                }
                            }
                        ]
                    }
                },
                "size": size,
                "sort": [
                    {"_score": {"order": "desc"}},
                    {"updated_at": {"order": "desc"}}
                ]
            }
            
            # Add filters if provided
            if filters:
                search_body["query"]["bool"]["filter"] = []
                for field, value in filters.items():
                    search_body["query"]["bool"]["filter"].append({
                        "term": {field: value}
                    })
            
            response = await self.es_client.search(
                index=full_index_name,
                body=search_body
            )
            
            # Extract results
            results = []
            for hit in response["hits"]["hits"]:
                result = hit["_source"]
                result["_score"] = hit["_score"]
                result["_id"] = hit["_id"]
                results.append(result)
            
            logger.debug(f"Search returned {len(results)} results for query: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Failed to search documents: {e}")
            return []
    
    async def get_document(self, index_name: str, document_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific document by ID."""
        try:
            full_index_name = f"{self.index_prefix}_{index_name}"
            
            response = await self.es_client.get(
                index=full_index_name,
                id=document_id
            )
            
            return response["_source"]
            
        except NotFoundError:
            logger.debug(f"Document {document_id} not found in {full_index_name}")
            return None
        except Exception as e:
            logger.error(f"Failed to get document {document_id}: {e}")
            return None
    
    async def delete_document(self, index_name: str, document_id: str) -> bool:
        """Delete a document from Elasticsearch."""
        try:
            full_index_name = f"{self.index_prefix}_{index_name}"
            
            await self.es_client.delete(
                index=full_index_name,
                id=document_id
            )
            
            logger.debug(f"Deleted document {document_id} from {full_index_name}")
            return True
            
        except NotFoundError:
            logger.debug(f"Document {document_id} not found for deletion")
            return False
        except Exception as e:
            logger.error(f"Failed to delete document {document_id}: {e}")
            return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get Elasticsearch cluster statistics."""
        try:
            cluster_stats = await self.es_client.cluster.stats()
            indices_stats = await self.es_client.indices.stats()
            
            return {
                "cluster_name": cluster_stats["cluster_name"],
                "number_of_nodes": cluster_stats["nodes"]["count"]["total"],
                "indices_count": cluster_stats["indices"]["count"],
                "total_docs": cluster_stats["indices"]["docs"]["count"],
                "total_size": cluster_stats["indices"]["store"]["size_in_bytes"]
            }
        except Exception as e:
            logger.error(f"Failed to get search stats: {e}")
            return {}
    
    async def close(self) -> None:
        """Close Elasticsearch connection."""
        try:
            if self.es_client:
                await self.es_client.close()
            logger.info("Search connections closed")
        except Exception as e:
            logger.error(f"Error closing search connections: {e}")

# Global search service instance
_search_service: Optional[SearchService] = None

async def init_search() -> None:
    """Initialize the search service."""
    global _search_service
    
    try:
        _search_service = SearchService()
        await _search_service.initialize()
        logger.info("Search initialization completed")
    except Exception as e:
        logger.error(f"Search initialization failed: {e}")
        raise

async def get_search_service() -> SearchService:
    """Get the search service instance."""
    if not _search_service:
        raise RuntimeError("Search service not initialized")
    return _search_service

async def close_search() -> None:
    """Close search connections."""
    global _search_service
    if _search_service:
        await _search_service.close()
        _search_service = None 