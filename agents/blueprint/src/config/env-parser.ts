# TOKEN COUNT: ~2,501 tokens
/**
 * AI-Q Knowledge Library System - Environment Parser
 * Parses .env files and converts to configuration structure
 * Single responsibility: .env parsing only
 * 
 * Created by: Claude Sonnet 4
 * Model Version: Claude Sonnet 4
 * Timestamp: 2025-07-03T08:10:00Z
 */

import { EnvironmentConfig } from './types';

export class EnvParser {
  /**
   * Parse .env file content into key-value pairs
   * @param envData - Raw .env file content
   * @returns Parsed environment variables
   */
  parseEnvFile(envData: string): Record<string, string> {
    const envVars: Record<string, string> = {};
    const lines = envData.split('\n');

    for (const line of lines) {
      const trimmedLine = line.trim();
      
      // Skip empty lines and comments
      if (!trimmedLine || trimmedLine.startsWith('#')) {
        continue;
      }

      const equalIndex = trimmedLine.indexOf('=');
      if (equalIndex > 0) {
        const key = trimmedLine.substring(0, equalIndex).trim();
        const value = trimmedLine.substring(equalIndex + 1).trim();
        
        // Remove quotes if present
        const cleanValue = value.replace(/^["']|["']$/g, '');
        envVars[key] = cleanValue;
      }
    }

    return envVars;
  }

  /**
   * Convert .env variables to configuration structure
   * @param envVars - Environment variables from .env file
   * @returns Structured configuration object
   */
  convertEnvToConfig(envVars: Record<string, string>): EnvironmentConfig {
    return {
      metadata: {
        version: "1.0.0",
        timestamp: new Date().toISOString(),
        created_by: "Claude Sonnet 4",
        model_version: "Claude Sonnet 4",
        purpose: "Environment configuration loaded from .env file"
      },
      project_configuration: {
        name: envVars.PROJECT_NAME || "",
        version: envVars.PROJECT_VERSION || "",
        environment: envVars.ENVIRONMENT || "",
        node_env: envVars.NODE_ENV || ""
      },
      network_configuration: {
        subnet: envVars.NETWORK_SUBNET || "",
        gateway: envVars.NETWORK_GATEWAY || "",
        container_prefix: envVars.CONTAINER_PREFIX || "aiq",
        service_namespace: envVars.SERVICE_NAMESPACE || "aiq"
      },
      database_configuration: {
        postgresql: {
          port: parseInt(envVars.POSTGRES_PORT) || 5432,
          database: envVars.POSTGRES_DB || "",
          user: envVars.POSTGRES_USER || "",
          password: envVars.POSTGRES_PASSWORD || "",
          host: envVars.POSTGRES_HOST || "",
          initdb_args: envVars.POSTGRES_INITDB_ARGS || ""
        },
        redis: {
          port: parseInt(envVars.REDIS_PORT) || 6379,
          password: envVars.REDIS_PASSWORD || "",
          host: envVars.REDIS_HOST || "",
          database: parseInt(envVars.REDIS_DB) || 0
        }
      },
      search_engine_configuration: {
        elasticsearch: {
          port: parseInt(envVars.ELASTICSEARCH_PORT) || 9200,
          cluster_port: parseInt(envVars.ELASTICSEARCH_CLUSTER_PORT) || 9300,
          password: envVars.ELASTICSEARCH_PASSWORD || "",
          host: envVars.ELASTICSEARCH_HOST || "",
          discovery_type: envVars.ELASTICSEARCH_DISCOVERY_TYPE || "single-node",
          xpack_security_enabled: envVars.ELASTICSEARCH_XPACK_SECURITY_ENABLED === "true",
          java_opts: envVars.ELASTICSEARCH_JAVA_OPTS || ""
        }
      },
      graph_database_configuration: {
        neo4j: {
          browser_port: parseInt(envVars.NEO4J_BROWSER_PORT) || 7474,
          bolt_port: parseInt(envVars.NEO4J_BOLT_PORT) || 7687,
          user: envVars.NEO4J_USER || "",
          password: envVars.NEO4J_PASSWORD || "",
          host: envVars.NEO4J_HOST || "",
          plugins: envVars.NEO4J_PLUGINS ? JSON.parse(envVars.NEO4J_PLUGINS) : [],
          procedures_unrestricted: envVars.NEO4J_PROCEDURES_UNRESTRICTED || "",
          heap_initial_size: envVars.NEO4J_HEAP_INITIAL_SIZE || "",
          heap_max_size: envVars.NEO4J_HEAP_MAX_SIZE || "",
          pagecache_size: envVars.NEO4J_PAGECACHE_SIZE || ""
        }
      },
      vector_database_configuration: {
        weaviate: {
          port: parseInt(envVars.WEAVIATE_PORT) || 8080,
          host: envVars.WEAVIATE_HOST || "",
          query_defaults_limit: parseInt(envVars.WEAVIATE_QUERY_DEFAULTS_LIMIT) || 25,
          authentication_anonymous_access_enabled: envVars.WEAVIATE_AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED === "true",
          persistence_data_path: envVars.WEAVIATE_PERSISTENCE_DATA_PATH || "",
          default_vectorizer_module: envVars.WEAVIATE_DEFAULT_VECTORIZER_MODULE || "",
          enable_modules: envVars.WEAVIATE_ENABLE_MODULES || "",
          transformers_inference_api: envVars.WEAVIATE_TRANSFORMERS_INFERENCE_API || "",
          cluster_hostname: envVars.WEAVIATE_CLUSTER_HOSTNAME || ""
        }
      },
      object_storage_configuration: {
        minio: {
          api_port: parseInt(envVars.MINIO_API_PORT) || 9000,
          console_port: parseInt(envVars.MINIO_CONSOLE_PORT) || 9001,
          root_user: envVars.MINIO_ROOT_USER || "",
          root_password: envVars.MINIO_ROOT_PASSWORD || "",
          host: envVars.MINIO_HOST || "",
          console_address: envVars.MINIO_CONSOLE_ADDRESS || ""
        }
      },
      api_server_configuration: {
        port: parseInt(envVars.API_SERVER_PORT) || 8000,
        host: envVars.API_SERVER_HOST || "",
        jwt_secret: envVars.JWT_SECRET || "",
        environment: envVars.API_ENVIRONMENT || ""
      },
      web_dashboard_configuration: {
        port: parseInt(envVars.WEB_DASHBOARD_PORT) || 3000,
        host: envVars.WEB_DASHBOARD_HOST || "",
        environment: envVars.WEB_ENVIRONMENT || ""
      },
      security_configuration: {
        cors_origins: envVars.CORS_ORIGINS ? envVars.CORS_ORIGINS.split(',') : [],
        rate_limit_requests_per_minute: parseInt(envVars.RATE_LIMIT_REQUESTS_PER_MINUTE) || 100,
        jwt_expiration_hours: parseInt(envVars.JWT_EXPIRATION_HOURS) || 24,
        bcrypt_rounds: parseInt(envVars.BCRYPT_ROUNDS) || 12
      },
      logging_configuration: {
        level: envVars.LOG_LEVEL || "info",
        format: envVars.LOG_FORMAT || "JSON",
        destination: envVars.LOG_DESTINATION || "console"
      },
      feature_flags: {
        enable_rag: envVars.ENABLE_RAG === "true",
        enable_knowledge_graph: envVars.ENABLE_KNOWLEDGE_GRAPH === "true",
        enable_vector_search: envVars.ENABLE_VECTOR_SEARCH === "true",
        enable_object_storage: envVars.ENABLE_OBJECT_STORAGE === "true",
        enable_api_documentation: envVars.ENABLE_API_DOCUMENTATION === "true"
      }
    };
  }

  /**
   * Convert configuration back to .env format
   * @param config - Configuration object
   * @returns .env file content
   */
  convertConfigToEnv(config: EnvironmentConfig): string {
    const envLines: string[] = [];
    
    // Project configuration
    envLines.push(`PROJECT_NAME=${config.project_configuration.name}`);
    envLines.push(`PROJECT_VERSION=${config.project_configuration.version}`);
    envLines.push(`ENVIRONMENT=${config.project_configuration.environment}`);
    envLines.push(`NODE_ENV=${config.project_configuration.node_env}`);
    
    // Network configuration
    envLines.push(`NETWORK_SUBNET=${config.network_configuration.subnet}`);
    envLines.push(`NETWORK_GATEWAY=${config.network_configuration.gateway}`);
    envLines.push(`CONTAINER_PREFIX=${config.network_configuration.container_prefix}`);
    envLines.push(`SERVICE_NAMESPACE=${config.network_configuration.service_namespace}`);
    
    // Database configuration
    envLines.push(`POSTGRES_PORT=${config.database_configuration.postgresql.port}`);
    envLines.push(`POSTGRES_DB=${config.database_configuration.postgresql.database}`);
    envLines.push(`POSTGRES_USER=${config.database_configuration.postgresql.user}`);
    envLines.push(`POSTGRES_PASSWORD=${config.database_configuration.postgresql.password}`);
    envLines.push(`POSTGRES_HOST=${config.database_configuration.postgresql.host}`);
    envLines.push(`POSTGRES_INITDB_ARGS=${config.database_configuration.postgresql.initdb_args}`);
    
    envLines.push(`REDIS_PORT=${config.database_configuration.redis.port}`);
    envLines.push(`REDIS_PASSWORD=${config.database_configuration.redis.password}`);
    envLines.push(`REDIS_HOST=${config.database_configuration.redis.host}`);
    envLines.push(`REDIS_DB=${config.database_configuration.redis.database}`);
    
    // API configuration
    envLines.push(`API_SERVER_PORT=${config.api_server_configuration.port}`);
    envLines.push(`API_SERVER_HOST=${config.api_server_configuration.host}`);
    envLines.push(`JWT_SECRET=${config.api_server_configuration.jwt_secret}`);
    envLines.push(`API_ENVIRONMENT=${config.api_server_configuration.environment}`);
    
    // Security configuration
    envLines.push(`CORS_ORIGINS=${config.security_configuration.cors_origins.join(',')}`);
    envLines.push(`RATE_LIMIT_REQUESTS_PER_MINUTE=${config.security_configuration.rate_limit_requests_per_minute}`);
    envLines.push(`JWT_EXPIRATION_HOURS=${config.security_configuration.jwt_expiration_hours}`);
    envLines.push(`BCRYPT_ROUNDS=${config.security_configuration.bcrypt_rounds}`);
    
    // Logging configuration
    envLines.push(`LOG_LEVEL=${config.logging_configuration.level}`);
    envLines.push(`LOG_FORMAT=${config.logging_configuration.format}`);
    envLines.push(`LOG_DESTINATION=${config.logging_configuration.destination}`);
    
    // Feature flags
    envLines.push(`ENABLE_RAG=${config.feature_flags.enable_rag}`);
    envLines.push(`ENABLE_KNOWLEDGE_GRAPH=${config.feature_flags.enable_knowledge_graph}`);
    envLines.push(`ENABLE_VECTOR_SEARCH=${config.feature_flags.enable_vector_search}`);
    envLines.push(`ENABLE_OBJECT_STORAGE=${config.feature_flags.enable_object_storage}`);
    envLines.push(`ENABLE_API_DOCUMENTATION=${config.feature_flags.enable_api_documentation}`);
    
    return envLines.join('\n');
  }
} 