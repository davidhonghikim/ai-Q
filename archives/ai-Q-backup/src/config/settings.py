from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class FeatureFlags(BaseSettings):
    enable_api_documentation: bool = Field(True, description="Enable API docs UI")
    enable_rag: bool = Field(True, description="Enable RAG endpoints")

class SecuritySettings(BaseSettings):
    allowed_hosts: List[str] = Field(["*"], description="Allowed hosts for TrustedHostMiddleware")
    cors_origins: List[str] = Field(["*"], description="CORS allowed origins")

class APIServerSettings(BaseSettings):
    host: str = Field("0.0.0.0", description="API server host")
    port: int = Field(8000, description="API server port")
    environment: str = Field("development", description="Environment (development/production)")

class LoggingSettings(BaseSettings):
    level: str = Field("info", description="Logging level")

class ExternalAPISettings(BaseSettings):
    placeholder_base_url: str = Field("https://jsonplaceholder.typicode.com", description="Base URL for placeholder API")
    knowledge_endpoint: str = Field("/posts/1", description="Path for knowledge demo endpoint")
    rag_endpoint: str = Field("/users/1", description="Path for RAG demo endpoint")
    system_endpoint: str = Field("/todos/1", description="Path for system demo endpoint")
    agent_name: str = Field("AnonymousAgent", description="Agent name for metadata")
    agent_version: str = Field("1.0.0", description="Agent version for metadata")

class Settings(BaseSettings):
    feature_flags: FeatureFlags = FeatureFlags()
    security: SecuritySettings = SecuritySettings()
    api_server: APIServerSettings = APIServerSettings()
    logging: LoggingSettings = LoggingSettings()
    external_api: ExternalAPISettings = ExternalAPISettings()

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"

# Singleton pattern for settings
_settings = None

def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings 