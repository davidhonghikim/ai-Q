# AI-Q Knowledge Library System - Settings Configuration
# TOKEN COUNT: ~1,500 tokens
"""
Settings configuration for AI-Q Knowledge Library System.
Handles all configuration management using Pydantic settings.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import List, Optional

class PostgreSQLSettings(BaseSettings):
    port: int = Field(default=5432, description="PostgreSQL port")
    database: str = Field(default="aiq_knowledge", description="Database name")
    user: str = Field(default="aiq_user", description="Database user")
    password: str = Field(default="aiq_password", description="Database password")
    host: str = Field(default="postgres", description="Database host")
    initdb_args: str = Field(default="--auth-host=scram-sha-256", description="InitDB arguments")

class RedisSettings(BaseSettings):
    port: int = Field(default=6379, description="Redis port")
    password: str = Field(default="", description="Redis password")
    host: str = Field(default="redis", description="Redis host")
    database: int = Field(default=0, description="Redis database number")

class DatabaseSettings(BaseSettings):
    postgresql: PostgreSQLSettings = Field(default_factory=PostgreSQLSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)

class ElasticsearchSettings(BaseSettings):
    port: int = Field(default=9200, description="Elasticsearch port")
    cluster_port: int = Field(default=9300, description="Elasticsearch cluster port")
    password: str = Field(default="elastic", description="Elasticsearch password")
    host: str = Field(default="elasticsearch", description="Elasticsearch host")
    discovery_type: str = Field(default="single-node", description="Discovery type")
    xpack_security_enabled: bool = Field(default=True, description="X-Pack security enabled")
    java_opts: str = Field(default="-Xms512m -Xmx512m", description="Java options")

class SearchEngineSettings(BaseSettings):
    elasticsearch: ElasticsearchSettings = Field(default_factory=ElasticsearchSettings)

class Neo4jSettings(BaseSettings):
    browser_port: int = Field(default=7474, description="Neo4j browser port")
    bolt_port: int = Field(default=7687, description="Neo4j bolt port")
    user: str = Field(default="neo4j", description="Neo4j user")
    password: str = Field(default="password", description="Neo4j password")
    host: str = Field(default="neo4j", description="Neo4j host")
    plugins: List[str] = Field(default=["apoc", "graph-data-science"], description="Neo4j plugins")
    procedures_unrestricted: str = Field(default="gds.*,apoc.*", description="Unrestricted procedures")
    heap_initial_size: str = Field(default="512m", description="Heap initial size")
    heap_max_size: str = Field(default="1G", description="Heap max size")
    pagecache_size: str = Field(default="512m", description="Page cache size")
    
    @field_validator('plugins', mode='before')
    @classmethod
    def parse_plugins(cls, v):
        """Parse plugins from comma-separated string or list."""
        if isinstance(v, str):
            return [plugin.strip() for plugin in v.split(',')]
        return v

class GraphDatabaseSettings(BaseSettings):
    neo4j: Neo4jSettings = Field(default_factory=Neo4jSettings)

class WeaviateSettings(BaseSettings):
    port: int = Field(default=8080, description="Weaviate port")
    host: str = Field(default="weaviate", description="Weaviate host")
    query_defaults_limit: int = Field(default=25, description="Query defaults limit")
    authentication_anonymous_access_enabled: bool = Field(default=True, description="Anonymous access enabled")
    persistence_data_path: str = Field(default="/var/lib/weaviate", description="Persistence data path")
    default_vectorizer_module: str = Field(default="text2vec-transformers", description="Default vectorizer module")
    enable_modules: str = Field(default="text2vec-transformers,ref2vec-centroid,generative-openai,qna-openai", description="Enabled modules")
    transformers_inference_api: str = Field(default="http://t2v-transformers:8080", description="Transformers inference API")
    cluster_hostname: str = Field(default="node1", description="Cluster hostname")
    
    @field_validator('enable_modules', mode='before')
    @classmethod
    def parse_enable_modules(cls, v):
        """Parse enable_modules from comma-separated string."""
        if isinstance(v, str):
            return v  # Keep as string for Weaviate configuration
        return v

class VectorDatabaseSettings(BaseSettings):
    weaviate: WeaviateSettings = Field(default_factory=WeaviateSettings)

class MinIOSettings(BaseSettings):
    api_port: int = Field(default=9000, description="MinIO API port")
    console_port: int = Field(default=9001, description="MinIO console port")
    root_user: str = Field(default="minioadmin", description="MinIO root user")
    root_password: str = Field(default="minioadmin", description="MinIO root password")
    host: str = Field(default="minio", description="MinIO host")
    console_address: str = Field(default="minio:9001", description="MinIO console address")

class ObjectStorageSettings(BaseSettings):
    minio: MinIOSettings = Field(default_factory=MinIOSettings)

class FeatureFlags(BaseSettings):
    enable_rag: bool = Field(default=True, description="Enable RAG functionality")
    enable_knowledge_graph: bool = Field(default=True, description="Enable knowledge graph")
    enable_vector_search: bool = Field(default=True, description="Enable vector search")
    enable_object_storage: bool = Field(default=True, description="Enable object storage")
    enable_api_documentation: bool = Field(default=True, description="Enable API documentation")

class SecuritySettings(BaseSettings):
    allowed_hosts: List[str] = Field(default=["*"], description="Allowed hosts for TrustedHostMiddleware")
    cors_origins: List[str] = Field(default=["http://localhost:3000", "http://localhost:8000"], description="CORS allowed origins")
    rate_limit_requests_per_minute: int = Field(default=100, description="Rate limit requests per minute")
    jwt_expiration_hours: int = Field(default=24, description="JWT expiration hours")
    bcrypt_rounds: int = Field(default=12, description="BCrypt rounds")
    
    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from comma-separated string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    @field_validator('allowed_hosts', mode='before')
    @classmethod
    def parse_allowed_hosts(cls, v):
        """Parse allowed hosts from comma-separated string or list."""
        if isinstance(v, str):
            return [host.strip() for host in v.split(',')]
        return v

class APIServerSettings(BaseSettings):
    host: str = Field(default="0.0.0.0", description="API server host")
    port: int = Field(default=8000, description="API server port")
    environment: str = Field(default="development", description="Environment (development/production)")

class WebDashboardSettings(BaseSettings):
    host: str = Field(default="0.0.0.0", description="Web dashboard host")
    port: int = Field(default=3000, description="Web dashboard port")
    environment: str = Field(default="development", description="Environment (development/production)")

class LoggingSettings(BaseSettings):
    level: str = Field(default="info", description="Logging level")
    format: str = Field(default="JSON", description="Logging format")
    destination: str = Field(default="console", description="Logging destination")

class ExternalAPISettings(BaseSettings):
    placeholder_base_url: str = Field(default="https://jsonplaceholder.typicode.com", description="Base URL for placeholder API")
    knowledge_endpoint: str = Field(default="/posts/1", description="Path for knowledge demo endpoint")
    rag_endpoint: str = Field(default="/users/1", description="Path for RAG demo endpoint")
    system_endpoint: str = Field(default="/todos/1", description="Path for system demo endpoint")
    agent_name: str = Field(default="AnonymousAgent", description="Agent name for metadata")
    agent_version: str = Field(default="1.0.0", description="Agent version for metadata")

class Settings(BaseSettings):
    # Database settings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    
    # Search engine settings
    search_engine: SearchEngineSettings = Field(default_factory=SearchEngineSettings)
    
    # Graph database settings
    graph_database: GraphDatabaseSettings = Field(default_factory=GraphDatabaseSettings)
    
    # Vector database settings
    vector_database: VectorDatabaseSettings = Field(default_factory=VectorDatabaseSettings)
    
    # Object storage settings
    object_storage: ObjectStorageSettings = Field(default_factory=ObjectStorageSettings)
    
    # Feature flags
    feature_flags: FeatureFlags = Field(default_factory=FeatureFlags)
    
    # Security settings
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    
    # API server settings
    api_server: APIServerSettings = Field(default_factory=APIServerSettings)
    
    # Web dashboard settings
    web_dashboard: WebDashboardSettings = Field(default_factory=WebDashboardSettings)
    
    # Logging settings
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    
    # External API settings
    external_api: ExternalAPISettings = Field(default_factory=ExternalAPISettings)

    model_config = {
        "env_file": ".env",
        "env_nested_delimiter": "__",
        "extra": "ignore"
    }

# Singleton pattern for settings
_settings = None

def get_settings() -> Settings:
    """Get the settings singleton instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings 