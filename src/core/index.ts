# TOKEN COUNT: ~974 tokens
/**
 * AI-Q Knowledge Library System - Entry Point
 * Demonstrates modular architecture
 * 
 * Created by: Claude Sonnet 4
 * Model Version: Claude Sonnet 4
 * Timestamp: 2025-07-03T08:50:00Z
 */

import { FileLoader } from './config/file-loader';
import { EnvParser } from './config/env-parser';
import { SchemaValidator } from './validation/schema-validator';
import { SecurityValidator } from './validation/security-validator';
import { ApiServer } from './api/server';
import { EnvironmentConfig } from './config/types';

class Application {
  private config: EnvironmentConfig | null = null;
  private server: ApiServer | null = null;

  /**
   * Initialize the application
   */
  async initialize(): Promise<void> {
    try {
      console.log('Initializing AI-Q Knowledge Library System...');

      // Load configuration
      await this.loadConfiguration();

      // Validate configuration
      await this.validateConfiguration();

      // Initialize API server
      await this.initializeServer();

      console.log('Application initialized successfully');
    } catch (error) {
      console.error('Failed to initialize application:', error);
      process.exit(1);
    }
  }

  /**
   * Load configuration from file
   */
  private async loadConfiguration(): Promise<void> {
    const fileLoader = new FileLoader();
    this.config = fileLoader.loadFromJson();
    console.log('Configuration loaded successfully');
  }

  /**
   * Validate configuration
   */
  private async validateConfiguration(): Promise<void> {
    if (!this.config) {
      throw new Error('Configuration not loaded');
    }

    // Load schema
    const fileLoader = new FileLoader();
    const schema = fileLoader.loadSchema();

    // Validate against schema
    const schemaValidator = new SchemaValidator();
    const schemaResult = schemaValidator.validate(this.config, schema);

    if (!schemaResult.isValid) {
      console.error('Schema validation failed:');
      schemaResult.errors.forEach(error => {
        console.error(`  ${error.path}: ${error.message}`);
      });
      throw new Error('Configuration validation failed');
    }

    // Validate security
    const securityValidator = new SecurityValidator();
    const securityErrors = securityValidator.validateSecurity(this.config);

    if (securityErrors.length > 0) {
      console.error('Security validation failed:');
      securityErrors.forEach(error => {
        console.error(`  ${error.path}: ${error.message}`);
      });
      throw new Error('Security validation failed');
    }

    console.log('Configuration validation passed');
  }

  /**
   * Initialize API server
   */
  private async initializeServer(): Promise<void> {
    if (!this.config) {
      throw new Error('Configuration not loaded');
    }

    this.server = new ApiServer(this.config);
    await this.server.initialize();
    console.log('API server initialized');
  }

  /**
   * Start the application
   */
  async start(): Promise<void> {
    if (!this.server) {
      throw new Error('Server not initialized');
    }

    await this.server.start();
    console.log('Application started successfully');
  }

  /**
   * Stop the application
   */
  async stop(): Promise<void> {
    if (this.server) {
      await this.server.stop();
      console.log('Application stopped');
    }
  }
}

// Handle graceful shutdown
process.on('SIGINT', async () => {
  console.log('\nReceived SIGINT, shutting down gracefully...');
  if (app) {
    await app.stop();
  }
  process.exit(0);
});

process.on('SIGTERM', async () => {
  console.log('\nReceived SIGTERM, shutting down gracefully...');
  if (app) {
    await app.stop();
  }
  process.exit(0);
});

// Start application
const app = new Application();

app.initialize()
  .then(() => app.start())
  .catch((error) => {
    console.error('Failed to start application:', error);
    process.exit(1);
  }); 