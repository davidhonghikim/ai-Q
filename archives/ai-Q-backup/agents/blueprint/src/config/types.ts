# TOKEN COUNT: ~901 tokens
/**
 * AI-Q Knowledge Library System - Configuration Types
 * Type definitions for environment configuration
 * 
 * Created by: Claude Sonnet 4
 * Model Version: Claude Sonnet 4
 * Timestamp: 2025-07-03T08:00:00Z
 */

export interface Metadata {
  version: string;
  timestamp: string;
  created_by: string;
  model_version: string;
  purpose: string;
}

export interface ProjectConfiguration {
  name: string;
  version: string;
  environment: string;
  node_env: string;
}

export interface NetworkConfiguration {
  subnet: string;
  gateway: string;
  container_prefix: string;
  service_namespace: string;
}

export interface DatabaseConfiguration {
  postgresql: {
    port: number;
    database: string;
    user: string;
    password: string;
    host: string;
    initdb_args: string;
  };
  redis: {
    port: number;
    password: string;
    host: string;
    database: number;
  };
}

export interface SearchEngineConfiguration {
  elasticsearch: {
    port: number;
    cluster_port: number;
    password: string;
    host: string;
    discovery_type: string;
    xpack_security_enabled: boolean;
    java_opts: string;
  };
}

export interface GraphDatabaseConfiguration {
  neo4j: {
    browser_port: number;
    bolt_port: number;
    user: string;
    password: string;
    host: string;
    plugins: string[];
    procedures_unrestricted: string;
    heap_initial_size: string;
    heap_max_size: string;
    pagecache_size: string;
  };
}

export interface VectorDatabaseConfiguration {
  weaviate: {
    port: number;
    host: string;
    query_defaults_limit: number;
    authentication_anonymous_access_enabled: boolean;
    persistence_data_path: string;
    default_vectorizer_module: string;
    enable_modules: string;
    transformers_inference_api: string;
    cluster_hostname: string;
  };
}

export interface ObjectStorageConfiguration {
  minio: {
    api_port: number;
    console_port: number;
    root_user: string;
    root_password: string;
    host: string;
    console_address: string;
  };
}

export interface ApiServerConfiguration {
  port: number;
  host: string;
  jwt_secret: string;
  environment: string;
}

export interface WebDashboardConfiguration {
  port: number;
  host: string;
  environment: string;
}

export interface SecurityConfiguration {
  cors_origins: string[];
  rate_limit_requests_per_minute: number;
  jwt_expiration_hours: number;
  bcrypt_rounds: number;
}

export interface LoggingConfiguration {
  level: string;
  format: string;
  destination: string;
}

export interface FeatureFlags {
  enable_rag: boolean;
  enable_knowledge_graph: boolean;
  enable_vector_search: boolean;
  enable_object_storage: boolean;
  enable_api_documentation: boolean;
}

export interface EnvironmentConfig {
  metadata: Metadata;
  project_configuration: ProjectConfiguration;
  network_configuration: NetworkConfiguration;
  database_configuration: DatabaseConfiguration;
  search_engine_configuration: SearchEngineConfiguration;
  graph_database_configuration: GraphDatabaseConfiguration;
  vector_database_configuration: VectorDatabaseConfiguration;
  object_storage_configuration: ObjectStorageConfiguration;
  api_server_configuration: ApiServerConfiguration;
  web_dashboard_configuration: WebDashboardConfiguration;
  security_configuration: SecurityConfiguration;
  logging_configuration: LoggingConfiguration;
  feature_flags: FeatureFlags;
}

export interface ValidationError {
  path: string;
  message: string;
  value?: any;
}

export interface ValidationResult {
  isValid: boolean;
  errors: ValidationError[];
  warnings: string[];
} 