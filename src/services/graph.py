# AI-Q Knowledge Library System - Graph Service
# TOKEN COUNT: ~1,200 tokens
"""
Graph service for AI-Q Knowledge Library System.
Handles Neo4j graph database initialization and operations.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime

from neo4j import AsyncGraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError
from src.config.settings import get_settings

# Configure logging
logger = logging.getLogger(__name__)

class GraphService:
    """Graph service for managing Neo4j operations."""
    
    def __init__(self):
        self.settings = get_settings()
        self.driver: Optional[AsyncGraphDatabase.driver] = None
    
    async def initialize(self) -> None:
        """Initialize Neo4j connection and create constraints."""
        try:
            logger.info("Initializing graph service...")
            
            # Create Neo4j driver
            uri = f"bolt://{self.settings.graph_database.neo4j.host}:{self.settings.graph_database.neo4j.bolt_port}"
            self.driver = AsyncGraphDatabase.driver(
                uri,
                auth=(self.settings.graph_database.neo4j.user, self.settings.graph_database.neo4j.password),
                max_connection_lifetime=3600,
                max_connection_pool_size=50,
                connection_acquisition_timeout=60
            )
            
            # Test connection
            await self._test_connection()
            
            # Create constraints and indexes
            await self._create_constraints()
            
            logger.info("Graph service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize graph service: {e}")
            raise
    
    async def _test_connection(self) -> None:
        """Test Neo4j connection."""
        try:
            async with self.driver.session() as session:
                result = await session.run("RETURN 1 as test")
                record = await result.single()
                if record and record["test"] == 1:
                    logger.info("Neo4j connection test successful")
                else:
                    raise Exception("Neo4j connection test failed")
        except Exception as e:
            logger.error(f"Neo4j connection test failed: {e}")
            raise
    
    async def _create_constraints(self) -> None:
        """Create Neo4j constraints and indexes."""
        try:
            async with self.driver.session() as session:
                # Create constraints for unique properties
                constraints = [
                    "CREATE CONSTRAINT knowledge_id IF NOT EXISTS FOR (k:Knowledge) REQUIRE k.id IS UNIQUE",
                    "CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE",
                    "CREATE CONSTRAINT session_id IF NOT EXISTS FOR (s:Session) REQUIRE s.id IS UNIQUE",
                    "CREATE CONSTRAINT tag_name IF NOT EXISTS FOR (t:Tag) REQUIRE t.name IS UNIQUE"
                ]
                
                for constraint in constraints:
                    try:
                        await session.run(constraint)
                        logger.debug(f"Created constraint: {constraint}")
                    except Exception as e:
                        logger.warning(f"Constraint may already exist: {e}")
                
                # Create indexes for better performance
                indexes = [
                    "CREATE INDEX knowledge_title IF NOT EXISTS FOR (k:Knowledge) ON (k.title)",
                    "CREATE INDEX knowledge_category IF NOT EXISTS FOR (k:Knowledge) ON (k.category)",
                    "CREATE INDEX knowledge_created_at IF NOT EXISTS FOR (k:Knowledge) ON (k.created_at)",
                    "CREATE INDEX user_email IF NOT EXISTS FOR (u:User) ON (u.email)"
                ]
                
                for index in indexes:
                    try:
                        await session.run(index)
                        logger.debug(f"Created index: {index}")
                    except Exception as e:
                        logger.warning(f"Index may already exist: {e}")
                        
        except Exception as e:
            logger.error(f"Failed to create constraints: {e}")
            raise
    
    async def create_knowledge_node(self, knowledge_data: Dict[str, Any]) -> bool:
        """Create a knowledge node in the graph."""
        try:
            async with self.driver.session() as session:
                query = """
                CREATE (k:Knowledge {
                    id: $id,
                    title: $title,
                    content: $content,
                    category: $category,
                    author: $author,
                    created_at: $created_at,
                    updated_at: $updated_at
                })
                """
                
                await session.run(query, knowledge_data)
                logger.debug(f"Created knowledge node: {knowledge_data['id']}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to create knowledge node: {e}")
            return False
    
    async def create_user_node(self, user_data: Dict[str, Any]) -> bool:
        """Create a user node in the graph."""
        try:
            async with self.driver.session() as session:
                query = """
                CREATE (u:User {
                    id: $id,
                    email: $email,
                    name: $name,
                    role: $role,
                    created_at: $created_at,
                    updated_at: $updated_at
                })
                """
                
                await session.run(query, user_data)
                logger.debug(f"Created user node: {user_data['id']}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to create user node: {e}")
            return False
    
    async def create_relationship(self, from_id: str, to_id: str, relationship_type: str, 
                                properties: Optional[Dict[str, Any]] = None) -> bool:
        """Create a relationship between two nodes."""
        try:
            async with self.driver.session() as session:
                if properties:
                    query = f"""
                    MATCH (a), (b)
                    WHERE a.id = $from_id AND b.id = $to_id
                    CREATE (a)-[r:{relationship_type} $properties]->(b)
                    """
                    await session.run(query, {
                        "from_id": from_id,
                        "to_id": to_id,
                        "properties": properties
                    })
                else:
                    query = f"""
                    MATCH (a), (b)
                    WHERE a.id = $from_id AND b.id = $to_id
                    CREATE (a)-[r:{relationship_type}]->(b)
                    """
                    await session.run(query, {
                        "from_id": from_id,
                        "to_id": to_id
                    })
                
                logger.debug(f"Created relationship: {from_id} -[{relationship_type}]-> {to_id}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to create relationship: {e}")
            return False
    
    async def find_knowledge_by_category(self, category: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Find knowledge nodes by category."""
        try:
            async with self.driver.session() as session:
                query = """
                MATCH (k:Knowledge)
                WHERE k.category = $category
                RETURN k
                ORDER BY k.updated_at DESC
                LIMIT $limit
                """
                
                result = await session.run(query, {"category": category, "limit": limit})
                records = await result.data()
                
                return [record["k"] for record in records]
                
        except Exception as e:
            logger.error(f"Failed to find knowledge by category: {e}")
            return []
    
    async def find_related_knowledge(self, knowledge_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Find related knowledge through relationships."""
        try:
            async with self.driver.session() as session:
                query = """
                MATCH (k:Knowledge {id: $knowledge_id})-[r]-(related:Knowledge)
                RETURN related, type(r) as relationship_type
                ORDER BY related.updated_at DESC
                LIMIT $limit
                """
                
                result = await session.run(query, {"knowledge_id": knowledge_id, "limit": limit})
                records = await result.data()
                
                return [{"knowledge": record["related"], "relationship": record["relationship_type"]} 
                       for record in records]
                
        except Exception as e:
            logger.error(f"Failed to find related knowledge: {e}")
            return []
    
    async def search_knowledge_graph(self, search_term: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search knowledge nodes using graph traversal."""
        try:
            async with self.driver.session() as session:
                query = """
                MATCH (k:Knowledge)
                WHERE k.title CONTAINS $search_term OR k.content CONTAINS $search_term
                OPTIONAL MATCH (k)-[r]-(related)
                RETURN k, collect(DISTINCT related) as related_nodes
                ORDER BY k.updated_at DESC
                LIMIT $limit
                """
                
                result = await session.run(query, {"search_term": search_term, "limit": limit})
                records = await result.data()
                
                return [{"knowledge": record["k"], "related": record["related_nodes"]} 
                       for record in records]
                
        except Exception as e:
            logger.error(f"Failed to search knowledge graph: {e}")
            return []
    
    async def get_graph_stats(self) -> Dict[str, Any]:
        """Get graph database statistics."""
        try:
            async with self.driver.session() as session:
                # Get node counts
                node_query = """
                MATCH (n)
                RETURN labels(n) as labels, count(n) as count
                """
                node_result = await session.run(node_query)
                node_stats = await node_result.data()
                
                # Get relationship counts
                rel_query = """
                MATCH ()-[r]->()
                RETURN type(r) as type, count(r) as count
                """
                rel_result = await session.run(rel_query)
                rel_stats = await rel_result.data()
                
                return {
                    "nodes": {stat["labels"][0] if stat["labels"] else "Unknown": stat["count"] 
                             for stat in node_stats},
                    "relationships": {stat["type"]: stat["count"] for stat in rel_stats}
                }
                
        except Exception as e:
            logger.error(f"Failed to get graph stats: {e}")
            return {}
    
    async def close(self) -> None:
        """Close Neo4j connection."""
        try:
            if self.driver:
                await self.driver.close()
            logger.info("Graph connections closed")
        except Exception as e:
            logger.error(f"Error closing graph connections: {e}")

# Global graph service instance
_graph_service: Optional[GraphService] = None

async def init_graph() -> None:
    """Initialize the graph service."""
    global _graph_service
    
    try:
        _graph_service = GraphService()
        await _graph_service.initialize()
        logger.info("Graph initialization completed")
    except Exception as e:
        logger.error(f"Graph initialization failed: {e}")
        raise

async def get_graph_service() -> GraphService:
    """Get the graph service instance."""
    if not _graph_service:
        raise RuntimeError("Graph service not initialized")
    return _graph_service

async def close_graph() -> None:
    """Close graph connections."""
    global _graph_service
    if _graph_service:
        await _graph_service.close()
        _graph_service = None 