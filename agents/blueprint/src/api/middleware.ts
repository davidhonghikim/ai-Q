/**
 * AI-Q Knowledge Library System - Middleware
 * Express middleware configuration
 * Single responsibility: middleware setup only
 * 
 * Created by: Claude Sonnet 4
 * Model Version: Claude Sonnet 4
 * Timestamp: 2025-07-03T08:25:00Z
 */

import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import compression from 'compression';
import morgan from 'morgan';
import { EnvironmentConfig } from '../config/types';

export class Middleware {
  private app: express.Application;
  private config: EnvironmentConfig;

  constructor(app: express.Application, config: EnvironmentConfig) {
    this.app = app;
    this.config = config;
  }

  /**
   * Configure all middleware
   */
  configure(): void {
    this.configureSecurity();
    this.configureCors();
    this.configureRateLimiting();
    this.configureCompression();
    this.configureLogging();
    this.configureBodyParsing();
    this.configureStaticFiles();
  }

  /**
   * Configure security middleware
   */
  private configureSecurity(): void {
    this.app.use(helmet({
      contentSecurityPolicy: {
        directives: {
          defaultSrc: ["'self'"],
          styleSrc: ["'self'", "'unsafe-inline'"],
          scriptSrc: ["'self'"],
          imgSrc: ["'self'", "data:", "https:"],
        },
      },
      hsts: {
        maxAge: 31536000,
        includeSubDomains: true,
        preload: true
      },
      noSniff: true,
      xssFilter: true,
      frameguard: {
        action: 'deny'
      }
    }));
  }

  /**
   * Configure CORS middleware
   */
  private configureCors(): void {
    const corsOrigins = this.config.security_configuration.cors_origins;
    this.app.use(cors({
      origin: corsOrigins.length > 0 ? corsOrigins : false,
      credentials: true,
      methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
      allowedHeaders: ['Content-Type', 'Authorization', 'X-API-Key'],
      exposedHeaders: ['X-Total-Count', 'X-Page-Count'],
      maxAge: 86400 // 24 hours
    }));
  }

  /**
   * Configure rate limiting middleware
   */
  private configureRateLimiting(): void {
    const rateLimitConfig = this.config.security_configuration.rate_limit_requests_per_minute;
    
    // Global rate limiter
    const globalLimiter = rateLimit({
      windowMs: 60 * 1000, // 1 minute
      max: rateLimitConfig || 100,
      message: {
        error: 'Too many requests from this IP, please try again later.',
        retryAfter: 60
      },
      standardHeaders: true,
      legacyHeaders: false,
      skipSuccessfulRequests: false,
      skipFailedRequests: false
    });

    // API-specific rate limiter (stricter)
    const apiLimiter = rateLimit({
      windowMs: 60 * 1000, // 1 minute
      max: Math.floor((rateLimitConfig || 100) * 0.5), // 50% of global limit
      message: {
        error: 'API rate limit exceeded, please try again later.',
        retryAfter: 60
      },
      standardHeaders: true,
      legacyHeaders: false
    });

    this.app.use('/api/', apiLimiter);
    this.app.use('/', globalLimiter);
  }

  /**
   * Configure compression middleware
   */
  private configureCompression(): void {
    this.app.use(compression({
      level: 6,
      threshold: 1024,
      filter: (req, res) => {
        if (req.headers['x-no-compression']) {
          return false;
        }
        return compression.filter(req, res);
      }
    }));
  }

  /**
   * Configure logging middleware
   */
  private configureLogging(): void {
    const logFormat = this.config.logging_configuration.format === 'JSON' ? 'combined' : 'dev';
    
    // Custom token for request ID
    morgan.token('id', (req: any) => req.id);
    
    // Custom format for JSON logging
    const jsonFormat = JSON.stringify({
      method: ':method',
      url: ':url',
      status: ':status',
      response_time: ':response-time',
      user_agent: ':user-agent',
      remote_addr: ':remote-addr',
      request_id: ':id',
      timestamp: ':date[iso]'
    });

    const format = this.config.logging_configuration.format === 'JSON' ? jsonFormat : logFormat;
    this.app.use(morgan(format));
  }

  /**
   * Configure body parsing middleware
   */
  private configureBodyParsing(): void {
    // JSON body parser
    this.app.use(express.json({
      limit: '10mb',
      strict: true,
      type: 'application/json'
    }));

    // URL-encoded body parser
    this.app.use(express.urlencoded({
      extended: true,
      limit: '10mb',
      parameterLimit: 1000
    }));

    // Raw body parser for specific content types
    this.app.use(express.raw({
      type: 'application/octet-stream',
      limit: '10mb'
    }));
  }

  /**
   * Configure static files middleware
   */
  private configureStaticFiles(): void {
    // Serve static files with security headers
    this.app.use('/static', express.static('public', {
      maxAge: '1d',
      etag: true,
      lastModified: true,
      setHeaders: (res, path) => {
        // Set security headers for static files
        res.setHeader('X-Content-Type-Options', 'nosniff');
        res.setHeader('X-Frame-Options', 'DENY');
        
        // Set cache headers based on file type
        if (path.endsWith('.css') || path.endsWith('.js')) {
          res.setHeader('Cache-Control', 'public, max-age=86400'); // 1 day
        } else if (path.endsWith('.png') || path.endsWith('.jpg') || path.endsWith('.jpeg') || path.endsWith('.gif')) {
          res.setHeader('Cache-Control', 'public, max-age=604800'); // 1 week
        }
      }
    }));

    // Serve API documentation
    this.app.use('/docs', express.static('docs', {
      maxAge: '1h',
      etag: true
    }));
  }

  /**
   * Add request ID middleware
   */
  addRequestId(): void {
    this.app.use((req: any, res, next) => {
      req.id = this.generateRequestId();
      res.setHeader('X-Request-ID', req.id);
      next();
    });
  }

  /**
   * Add error handling middleware
   */
  addErrorHandling(): void {
    // 404 handler
    this.app.use((req, res) => {
      res.status(404).json({
        error: 'Not Found',
        message: `Route ${req.method} ${req.path} not found`,
        timestamp: new Date().toISOString()
      });
    });

    // Global error handler
    this.app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
      const status = err.status || 500;
      const message = err.message || 'Internal Server Error';
      
      // Log error
      console.error(`Error ${status}: ${message}`, {
        url: req.url,
        method: req.method,
        ip: req.ip,
        userAgent: req.get('User-Agent'),
        stack: err.stack
      });

      // Send error response
      res.status(status).json({
        error: status === 500 ? 'Internal Server Error' : message,
        message: status === 500 ? 'An unexpected error occurred' : message,
        timestamp: new Date().toISOString(),
        path: req.path,
        method: req.method
      });
    });
  }

  /**
   * Generate unique request ID
   * @returns Request ID string
   */
  private generateRequestId(): string {
    return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
} 