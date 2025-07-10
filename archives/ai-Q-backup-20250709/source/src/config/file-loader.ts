# TOKEN COUNT: ~981 tokens
/**
 * AI-Q Knowledge Library System - File Loader
 * Loads configuration from JSON files
 * Single responsibility: file loading only
 * 
 * Created by: Claude Sonnet 4
 * Model Version: Claude Sonnet 4
 * Timestamp: 2025-07-03T08:05:00Z
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync, statSync } from 'fs';
import { join, dirname } from 'path';
import { EnvironmentConfig } from './types';

export class FileLoader {
  private configPath: string | null = null;

  /**
   * Load configuration from JSON file
   * @param configPath - Path to configuration file
   * @returns Loaded configuration object
   */
  loadFromJson(configPath?: string): EnvironmentConfig {
    try {
      this.configPath = configPath || this.getDefaultConfigPath();
      
      if (!existsSync(this.configPath)) {
        throw new Error(`Configuration file not found: ${this.configPath}`);
      }

      const configData = readFileSync(this.configPath, 'utf8');
      const config = JSON.parse(configData) as EnvironmentConfig;

      return config;
    } catch (error) {
      throw new Error(`Failed to load configuration from JSON: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Load schema from JSON file
   * @param schemaPath - Path to schema file
   * @returns Loaded schema object
   */
  loadSchema(schemaPath?: string): any {
    try {
      const schemaPathToUse = schemaPath || this.getDefaultSchemaPath();
      
      if (!existsSync(schemaPathToUse)) {
        throw new Error(`Schema file not found: ${schemaPathToUse}`);
      }

      const schemaData = readFileSync(schemaPathToUse, 'utf8');
      return JSON.parse(schemaData);
    } catch (error) {
      throw new Error(`Failed to load schema: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Save configuration to JSON file
   * @param config - Configuration to save
   * @param outputPath - Output file path
   */
  saveToJson(config: EnvironmentConfig, outputPath: string): void {
    try {
      const dir = dirname(outputPath);
      if (!existsSync(dir)) {
        mkdirSync(dir, { recursive: true });
      }

      const configString = JSON.stringify(config, null, 2);
      writeFileSync(outputPath, configString, 'utf8');
    } catch (error) {
      throw new Error(`Failed to save configuration: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Check if file exists
   * @param filePath - Path to check
   * @returns True if file exists
   */
  fileExists(filePath: string): boolean {
    return existsSync(filePath);
  }

  /**
   * Get file size in bytes
   * @param filePath - Path to file
   * @returns File size in bytes
   */
  getFileSize(filePath: string): number {
    try {
      const stats = statSync(filePath);
      return stats.size;
    } catch (error) {
      throw new Error(`Failed to get file size: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Get file modification time
   * @param filePath - Path to file
   * @returns Last modification time
   */
  getFileModTime(filePath: string): Date {
    try {
      const stats = statSync(filePath);
      return stats.mtime;
    } catch (error) {
      throw new Error(`Failed to get file modification time: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  /**
   * Get default configuration path
   * @returns Default config path
   */
  private getDefaultConfigPath(): string {
    return join(process.cwd(), 'config/env/environment-template.json');
  }

  /**
   * Get default schema path
   * @returns Default schema path
   */
  private getDefaultSchemaPath(): string {
    return join(process.cwd(), 'config/validation/env-schema.json');
  }

  /**
   * Get the last loaded config path
   * @returns Config path or null
   */
  getLastConfigPath(): string | null {
    return this.configPath;
  }
} 