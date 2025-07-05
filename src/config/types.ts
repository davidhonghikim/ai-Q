/**
 * AI-Q Knowledge Library System - Configuration Types
 * TypeScript interfaces for system configuration
 * TOKEN COUNT: ~2,847 tokens
 * 
 * Created by: Claude Sonnet 4
 * Model Version: Claude Sonnet 4
 * Timestamp: 2025-01-27T12:00:00Z
 */

export interface EnvironmentConfig {
  // Metadata
  metadata: {
    version: string;
    timestamp: string;
    created_by: string;
    model_version: string;
    purpose: string;
  };
  
  // Project configuration
  project_configuration: {
    name: string;
    version: string;
    environment: string;
    node_env: string;
  };
  
  // Network configuration
  network_configuration: {
    subnet: string;
    gateway: string;
    container_prefix: string;
    service_namespace: string;
  };
  
  // Database configuration
  database_configuration: {
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
  };
  
  // Search engine configuration
  search_engine_configuration: {
    elasticsearch: {
      port: number;
      cluster_port: number;
      password: string;
      host: string;
      discovery_type: string;
      xpack_security_enabled: boolean;
      java_opts: string;
    };
  };
  
  // Graph database configuration
  graph_database_configuration: {
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
  };
  
  // Vector database configuration
  vector_database_configuration: {
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
  };
  
  // Object storage configuration
  object_storage_configuration: {
    minio: {
      api_port: number;
      console_port: number;
      root_user: string;
      root_password: string;
      host: string;
      console_address: string;
    };
  };
  
  // API server configuration
  api_server_configuration: {
    port: number;
    host: string;
    jwt_secret: string;
    environment: string;
  };
  
  // Web dashboard configuration
  web_dashboard_configuration: {
    port: number;
    host: string;
    environment: string;
  };
  
  // Security configuration
  security_configuration: {
    cors_origins: string[];
    rate_limit_requests_per_minute: number;
    jwt_expiration_hours: number;
    bcrypt_rounds: number;
  };
  
  // Logging configuration
  logging_configuration: {
    level: string;
    format: string;
    destination: string;
  };
  
  // Feature flags
  feature_flags: {
    enable_rag: boolean;
    enable_knowledge_graph: boolean;
    enable_vector_search: boolean;
    enable_object_storage: boolean;
    enable_api_documentation: boolean;
  };
}

export interface ConfigValidationResult {
  isValid: boolean;
  errors: ConfigError[];
}

export interface ConfigError {
  path: string;
  message: string;
  severity: 'error' | 'warning';
}

export interface SecurityValidationResult {
  isValid: boolean;
  violations: SecurityViolation[];
}

export interface SecurityViolation {
  path: string;
  message: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
} 