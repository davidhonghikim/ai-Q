# TOKEN COUNT: ~2,327 tokens
/**
 * AI-Q Knowledge Library System - Security Validator
 * Validates security-related configuration
 * Single responsibility: security validation only
 * 
 * Created by: Claude Sonnet 4
 * Model Version: Claude Sonnet 4
 * Timestamp: 2025-07-03T08:20:00Z
 */

import { ValidationError } from '../config/types';

export class SecurityValidator {
  private validationErrors: ValidationError[] = [];

  /**
   * Validate security configuration
   * @param config - Configuration object
   * @returns Array of validation errors
   */
  validateSecurity(config: any): ValidationError[] {
    this.validationErrors = [];

    try {
      this.validateJwtSecret(config);
      this.validatePasswordStrength(config);
      this.validateCorsConfiguration(config);
      this.validateRateLimiting(config);
      this.validateNetworkSecurity(config);
      this.validateDatabaseSecurity(config);
      this.validateApiSecurity(config);
    } catch (error) {
      this.validationErrors.push({
        path: 'security',
        message: `Security validation error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        value: config
      });
    }

    return this.validationErrors;
  }

  /**
   * Validate JWT secret configuration
   * @param config - Configuration object
   */
  private validateJwtSecret(config: any): void {
    const jwtSecret = config?.api_server_configuration?.jwt_secret;
    
    if (!jwtSecret) {
      this.validationErrors.push({
        path: 'api_server_configuration.jwt_secret',
        message: 'JWT secret is required',
        value: jwtSecret
      });
      return;
    }

    if (typeof jwtSecret !== 'string') {
      this.validationErrors.push({
        path: 'api_server_configuration.jwt_secret',
        message: 'JWT secret must be a string',
        value: jwtSecret
      });
      return;
    }

    if (jwtSecret.length < 32) {
      this.validationErrors.push({
        path: 'api_server_configuration.jwt_secret',
        message: 'JWT secret must be at least 32 characters long',
        value: jwtSecret
      });
    }

    // Check for common weak secrets
    const weakSecrets = ['secret', 'password', '123456', 'admin', 'test'];
    if (weakSecrets.includes(jwtSecret.toLowerCase())) {
      this.validationErrors.push({
        path: 'api_server_configuration.jwt_secret',
        message: 'JWT secret is too weak',
        value: jwtSecret
      });
    }
  }

  /**
   * Validate password strength requirements
   * @param config - Configuration object
   */
  private validatePasswordStrength(config: any): void {
    const bcryptRounds = config?.security_configuration?.bcrypt_rounds;
    
    if (bcryptRounds !== undefined) {
      if (typeof bcryptRounds !== 'number') {
        this.validationErrors.push({
          path: 'security_configuration.bcrypt_rounds',
          message: 'BCrypt rounds must be a number',
          value: bcryptRounds
        });
      } else if (bcryptRounds < 10 || bcryptRounds > 14) {
        this.validationErrors.push({
          path: 'security_configuration.bcrypt_rounds',
          message: 'BCrypt rounds must be between 10 and 14',
          value: bcryptRounds
        });
      }
    }

    // Validate database passwords
    const postgresPassword = config?.database_configuration?.postgresql?.password;
    if (postgresPassword && postgresPassword.length < 8) {
      this.validationErrors.push({
        path: 'database_configuration.postgresql.password',
        message: 'PostgreSQL password must be at least 8 characters long',
        value: postgresPassword
      });
    }

    const redisPassword = config?.database_configuration?.redis?.password;
    if (redisPassword && redisPassword.length < 8) {
      this.validationErrors.push({
        path: 'database_configuration.redis.password',
        message: 'Redis password must be at least 8 characters long',
        value: redisPassword
      });
    }
  }

  /**
   * Validate CORS configuration
   * @param config - Configuration object
   */
  private validateCorsConfiguration(config: any): void {
    const corsOrigins = config?.security_configuration?.cors_origins;
    
    if (!Array.isArray(corsOrigins)) {
      this.validationErrors.push({
        path: 'security_configuration.cors_origins',
        message: 'CORS origins must be an array',
        value: corsOrigins
      });
      return;
    }

    // Check for wildcard in production
    const environment = config?.project_configuration?.environment;
    if (environment === 'production' && corsOrigins.includes('*')) {
      this.validationErrors.push({
        path: 'security_configuration.cors_origins',
        message: 'Wildcard CORS origin not allowed in production',
        value: corsOrigins
      });
    }

    // Validate origin URLs
    for (let i = 0; i < corsOrigins.length; i++) {
      const origin = corsOrigins[i];
      if (origin !== '*' && !this.isValidUrl(origin)) {
        this.validationErrors.push({
          path: `security_configuration.cors_origins[${i}]`,
          message: 'Invalid CORS origin URL',
          value: origin
        });
      }
    }
  }

  /**
   * Validate rate limiting configuration
   * @param config - Configuration object
   */
  private validateRateLimiting(config: any): void {
    const rateLimit = config?.security_configuration?.rate_limit_requests_per_minute;
    
    if (rateLimit !== undefined) {
      if (typeof rateLimit !== 'number') {
        this.validationErrors.push({
          path: 'security_configuration.rate_limit_requests_per_minute',
          message: 'Rate limit must be a number',
          value: rateLimit
        });
      } else if (rateLimit < 1 || rateLimit > 10000) {
        this.validationErrors.push({
          path: 'security_configuration.rate_limit_requests_per_minute',
          message: 'Rate limit must be between 1 and 10000',
          value: rateLimit
        });
      }
    }
  }

  /**
   * Validate network security configuration
   * @param config - Configuration object
   */
  private validateNetworkSecurity(config: any): void {
    const subnet = config?.network_configuration?.subnet;
    if (subnet && !this.isValidSubnet(subnet)) {
      this.validationErrors.push({
        path: 'network_configuration.subnet',
        message: 'Invalid subnet format',
        value: subnet
      });
    }

    const gateway = config?.network_configuration?.gateway;
    if (gateway && !this.isValidIpAddress(gateway)) {
      this.validationErrors.push({
        path: 'network_configuration.gateway',
        message: 'Invalid gateway IP address',
        value: gateway
      });
    }
  }

  /**
   * Validate database security configuration
   * @param config - Configuration object
   */
  private validateDatabaseSecurity(config: any): void {
    // Check for default credentials
    const postgresUser = config?.database_configuration?.postgresql?.user;
    if (postgresUser === 'postgres' || postgresUser === 'admin') {
      this.validationErrors.push({
        path: 'database_configuration.postgresql.user',
        message: 'Default PostgreSQL user not allowed',
        value: postgresUser
      });
    }

    const redisPassword = config?.database_configuration?.redis?.password;
    if (!redisPassword) {
      this.validationErrors.push({
        path: 'database_configuration.redis.password',
        message: 'Redis password is required',
        value: redisPassword
      });
    }
  }

  /**
   * Validate API security configuration
   * @param config - Configuration object
   */
  private validateApiSecurity(config: any): void {
    const apiPort = config?.api_server_configuration?.port;
    if (apiPort === 80 || apiPort === 443) {
      this.validationErrors.push({
        path: 'api_server_configuration.port',
        message: 'API server should not use standard HTTP/HTTPS ports',
        value: apiPort
      });
    }

    const environment = config?.project_configuration?.environment;
    if (environment === 'production') {
      const apiHost = config?.api_server_configuration?.host;
      if (apiHost === '0.0.0.0' || apiHost === 'localhost') {
        this.validationErrors.push({
          path: 'api_server_configuration.host',
          message: 'Production API should not bind to 0.0.0.0 or localhost',
          value: apiHost
        });
      }
    }
  }

  /**
   * Check if string is a valid URL
   * @param url - URL to validate
   * @returns True if valid URL
   */
  private isValidUrl(url: string): boolean {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Check if string is a valid subnet
   * @param subnet - Subnet to validate
   * @returns True if valid subnet
   */
  private isValidSubnet(subnet: string): boolean {
    const subnetRegex = /^(\d{1,3}\.){3}\d{1,3}\/\d{1,2}$/;
    return subnetRegex.test(subnet);
  }

  /**
   * Check if string is a valid IP address
   * @param ip - IP address to validate
   * @returns True if valid IP
   */
  private isValidIpAddress(ip: string): boolean {
    const ipRegex = /^(\d{1,3}\.){3}\d{1,3}$/;
    if (!ipRegex.test(ip)) return false;
    
    const parts = ip.split('.');
    return parts.every(part => {
      const num = parseInt(part);
      return num >= 0 && num <= 255;
    });
  }
} 