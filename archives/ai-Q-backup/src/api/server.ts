# TOKEN COUNT: ~1,190 tokens
/**
 * AI-Q Knowledge Library System - API Server
 * Modular server with route composition
 * Single responsibility: server lifecycle only
 * 
 * Created by: Claude Sonnet 4
 * Model Version: Claude Sonnet 4
 * Timestamp: 2025-07-03T08:45:00Z
 */

import express from 'express';
import { createServer, Server as HttpServer } from 'http';
import { EnvironmentConfig } from '../config/types';
import { Middleware } from './middleware';
import { KnowledgeRoutes } from './routes/knowledge-routes';
import { RagRoutes } from './routes/rag-routes';
import { SystemRoutes } from './routes/system-routes';

export class ApiServer {
  private app: express.Application;
  private server: HttpServer | null = null;
  private config: EnvironmentConfig;
  private middleware: Middleware;
  private isInitialized = false;

  constructor(config: EnvironmentConfig) {
    this.config = config;
    this.app = express();
    this.middleware = new Middleware(this.app, config);
  }

  /**
   * Initialize the API server
   */
  async initialize(): Promise<void> {
    try {
      // Configure middleware
      this.middleware.addRequestId();
      this.middleware.configure();

      // Setup routes
      this.setupRoutes();

      // Setup error handling
      this.middleware.addErrorHandling();

      this.isInitialized = true;
    } catch (error) {
      throw new Error(`Failed to initialize API server: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Setup all routes
   */
  private setupRoutes(): void {
    // Health check endpoint
    this.app.get('/health', (req, res) => {
      res.status(200).json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        version: this.config.project_configuration.version,
        environment: this.config.project_configuration.environment
      });
    });

    // API status endpoint
    this.app.get('/api/status', (req, res) => {
      res.json({
        status: 'operational',
        timestamp: new Date().toISOString(),
        version: this.config.project_configuration.version,
        environment: this.config.project_configuration.environment,
        features: this.config.feature_flags
      });
    });

    // Knowledge routes
    const knowledgeRoutes = new KnowledgeRoutes(this.config);
    this.app.use('/api/knowledge', knowledgeRoutes.getRouter());

    // RAG routes
    const ragRoutes = new RagRoutes(this.config);
    this.app.use('/api/rag', ragRoutes.getRouter());

    // System routes
    const systemRoutes = new SystemRoutes(this.config);
    this.app.use('/api/system', systemRoutes.getRouter());

    // Default route
    this.app.get('/', (req, res) => {
      res.json({
        name: this.config.project_configuration.name,
        version: this.config.project_configuration.version,
        description: 'AI-Q Knowledge Library System API',
        documentation: '/api/docs',
        health: '/health'
      });
    });
  }

  /**
   * Start the server
   */
  async start(): Promise<void> {
    if (!this.isInitialized) {
      throw new Error('Server must be initialized before starting');
    }

    return new Promise((resolve, reject) => {
      try {
        const port = this.config.api_server_configuration.port;
        const host = this.config.api_server_configuration.host;

        this.server = createServer(this.app);
        
        this.server.listen(port, host, () => {
          console.log(`AI-Q API Server started on ${host}:${port}`);
          console.log(`Environment: ${this.config.project_configuration.environment}`);
          console.log(`Version: ${this.config.project_configuration.version}`);
          resolve();
        });

        this.server.on('error', (error) => {
          reject(new Error(`Server error: ${error.message}`));
        });
      } catch (error) {
        reject(new Error(`Failed to start server: ${error instanceof Error ? error.message : 'Unknown error'}`));
      }
    });
  }

  /**
   * Stop the server
   */
  async stop(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (!this.server) {
        resolve();
        return;
      }

      this.server.close((error) => {
        if (error) {
          reject(new Error(`Failed to stop server: ${error.message}`));
        } else {
          console.log('AI-Q API Server stopped');
          this.server = null;
          resolve();
        }
      });
    });
  }

  /**
   * Get Express app instance
   */
  getApp(): express.Application {
    return this.app;
  }

  /**
   * Get HTTP server instance
   */
  getServer(): HttpServer | null {
    return this.server;
  }

  /**
   * Check if server is initialized
   */
  isServerInitialized(): boolean {
    return this.isInitialized;
  }
} 