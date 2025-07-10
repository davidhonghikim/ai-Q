# TOKEN COUNT: ~1,614 tokens
/**
 * AI-Q Knowledge Library System - System Routes
 * System management API endpoints
 * Single responsibility: system routes only
 * 
 * Created by: Claude Sonnet 4
 * Model Version: Claude Sonnet 4
 * Timestamp: 2025-07-03T08:40:00Z
 */

import { Router, Request, Response } from 'express';
import { EnvironmentConfig } from '../../config/types';

export class SystemRoutes {
  private router: Router;
  private config: EnvironmentConfig;

  constructor(config: EnvironmentConfig) {
    this.router = Router();
    this.config = config;
    this.setupRoutes();
  }

  /**
   * Setup all system routes
   */
  private setupRoutes(): void {
    this.router.get('/metrics', this.getMetrics.bind(this));
    this.router.get('/health', this.getHealth.bind(this));
    this.router.get('/logs', this.getLogs.bind(this));
    this.router.get('/config', this.getConfig.bind(this));
    this.router.get('/status', this.getStatus.bind(this));
  }

  /**
   * Get system metrics
   */
  private async getMetrics(req: Request, res: Response): Promise<void> {
    try {
      const memUsage = process.memoryUsage();
      const cpuUsage = process.cpuUsage();

      const metrics = {
        timestamp: new Date().toISOString(),
        process: {
          pid: process.pid,
          uptime: process.uptime(),
          memory: {
            rss: memUsage.rss,
            heapTotal: memUsage.heapTotal,
            heapUsed: memUsage.heapUsed,
            external: memUsage.external,
            arrayBuffers: memUsage.arrayBuffers
          },
          cpu: {
            user: cpuUsage.user,
            system: cpuUsage.system
          }
        },
        system: {
          platform: process.platform,
          arch: process.arch,
          nodeVersion: process.version,
          env: this.config.project_configuration.environment
        },
        features: this.config.feature_flags
      };

      res.json(metrics);
    } catch (error) {
      res.status(500).json({ 
        error: 'Failed to retrieve system metrics',
        message: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }

  /**
   * Get system health
   */
  private async getHealth(req: Request, res: Response): Promise<void> {
    try {
      const health = {
        status: 'healthy',
        timestamp: new Date().toISOString(),
        version: this.config.project_configuration.version,
        environment: this.config.project_configuration.environment,
        uptime: process.uptime(),
        memory: {
          used: process.memoryUsage().heapUsed,
          total: process.memoryUsage().heapTotal,
          percentage: (process.memoryUsage().heapUsed / process.memoryUsage().heapTotal * 100).toFixed(2)
        },
        services: {
          api: 'healthy',
          database: 'unknown',
          search: 'unknown',
          vector_db: 'unknown',
          object_storage: 'unknown'
        }
      };

      res.json(health);
    } catch (error) {
      res.status(500).json({ 
        error: 'Failed to retrieve system health',
        message: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }

  /**
   * Get system logs
   */
  private async getLogs(req: Request, res: Response): Promise<void> {
    try {
      const { level = 'info', limit = '100', page = '1' } = req.query;
      
      const limitNum = parseInt(limit as string);
      const pageNum = parseInt(page as string);

      if (limitNum > 1000) {
        res.status(400).json({ error: 'Log limit cannot exceed 1000' });
        return;
      }

      // TODO: Implement log retrieval logic
      res.json({
        logs: [],
        total: 0,
        level: level as string,
        limit: limitNum,
        page: pageNum,
        hasNext: false,
        hasPrev: pageNum > 1
      });
    } catch (error) {
      res.status(500).json({ 
        error: 'Failed to retrieve system logs',
        message: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }

  /**
   * Get system configuration (public)
   */
  private async getConfig(req: Request, res: Response): Promise<void> {
    try {
      const publicConfig = {
        project: {
          name: this.config.project_configuration.name,
          version: this.config.project_configuration.version,
          environment: this.config.project_configuration.environment
        },
        features: this.config.feature_flags,
        api: {
          port: this.config.api_server_configuration.port,
          host: this.config.api_server_configuration.host
        },
        web: {
          port: this.config.web_dashboard_configuration.port,
          host: this.config.web_dashboard_configuration.host
        },
        services: {
          database: {
            type: 'postgresql',
            port: this.config.database_configuration.postgresql.port
          },
          search: {
            type: 'elasticsearch',
            port: this.config.search_engine_configuration.elasticsearch.port
          },
          vector_db: {
            type: 'weaviate',
            port: this.config.vector_database_configuration.weaviate.port
          },
          object_storage: {
            type: 'minio',
            api_port: this.config.object_storage_configuration.minio.api_port
          }
        }
      };

      res.json(publicConfig);
    } catch (error) {
      res.status(500).json({ 
        error: 'Failed to retrieve system configuration',
        message: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }

  /**
   * Get system status
   */
  private async getStatus(req: Request, res: Response): Promise<void> {
    try {
      const status = {
        status: 'operational',
        timestamp: new Date().toISOString(),
        version: this.config.project_configuration.version,
        environment: this.config.project_configuration.environment,
        features: this.config.feature_flags,
        endpoints: {
          health: '/api/system/health',
          metrics: '/api/system/metrics',
          logs: '/api/system/logs',
          config: '/api/system/config'
        }
      };

      res.json(status);
    } catch (error) {
      res.status(500).json({ 
        error: 'Failed to retrieve system status',
        message: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }

  /**
   * Get router instance
   */
  getRouter(): Router {
    return this.router;
  }
} 