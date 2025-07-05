# TOKEN COUNT: ~1,805 tokens
/**
 * AI-Q Knowledge Library System - Schema Validator
 * Validates configuration against JSON schema
 * Single responsibility: schema validation only
 * 
 * Created by: Claude Sonnet 4
 * Model Version: Claude Sonnet 4
 * Timestamp: 2025-07-03T08:15:00Z
 */

import { ValidationError, ValidationResult } from '../config/types';

export class SchemaValidator {
  private validationErrors: ValidationError[] = [];
  private validationWarnings: string[] = [];

  /**
   * Validate configuration against JSON schema
   * @param config - Configuration object to validate
   * @param schema - JSON schema to validate against
   * @returns Validation result
   */
  validate(config: any, schema: any): ValidationResult {
    this.validationErrors = [];
    this.validationWarnings = [];

    try {
      this.validateAgainstSchema(config, schema, '');
      return {
        isValid: this.validationErrors.length === 0,
        errors: this.validationErrors,
        warnings: this.validationWarnings
      };
    } catch (error) {
      this.validationErrors.push({
        path: '',
        message: `Validation error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        value: config
      });
      return {
        isValid: false,
        errors: this.validationErrors,
        warnings: this.validationWarnings
      };
    }
  }

  /**
   * Validate configuration against JSON schema
   * @param config - Configuration object
   * @param schema - JSON schema
   * @param path - Current validation path
   */
  private validateAgainstSchema(config: any, schema: any, path: string): void {
    // Check required fields
    if (schema.required && Array.isArray(schema.required)) {
      for (const requiredField of schema.required) {
        if (!(requiredField in config)) {
          this.validationErrors.push({
            path: path ? `${path}.${requiredField}` : requiredField,
            message: 'Missing required field',
            value: undefined
          });
        }
      }
    }

    // Check properties
    if (schema.properties && typeof schema.properties === 'object') {
      for (const [key, value] of Object.entries(config)) {
        const currentPath = path ? `${path}.${key}` : key;
        
        if (key in schema.properties) {
          const propertySchema = schema.properties[key];
          this.validateProperty(value, propertySchema, currentPath);
        } else if (!schema.additionalProperties) {
          this.validationErrors.push({
            path: currentPath,
            message: 'Unexpected property',
            value: value
          });
        }
      }
    }
  }

  /**
   * Validate a single property against its schema
   * @param value - Property value
   * @param schema - Property schema
   * @param path - Property path
   */
  private validateProperty(value: any, schema: any, path: string): void {
    // Check type
    if (schema.type) {
      if (!this.validateType(value, schema.type)) {
        this.validationErrors.push({
          path: path,
          message: `Invalid type: expected ${schema.type}, got ${typeof value}`,
          value: value
        });
        return;
      }
    }

    // Check enum values
    if (schema.enum && Array.isArray(schema.enum)) {
      if (!schema.enum.includes(value)) {
        this.validationErrors.push({
          path: path,
          message: `Invalid value: must be one of [${schema.enum.join(', ')}]`,
          value: value
        });
        return;
      }
    }

    // Check pattern
    if (schema.pattern && typeof value === 'string') {
      const regex = new RegExp(schema.pattern);
      if (!regex.test(value)) {
        this.validationErrors.push({
          path: path,
          message: `Invalid format: must match pattern ${schema.pattern}`,
          value: value
        });
        return;
      }
    }

    // Check minimum/maximum for numbers
    if (typeof value === 'number') {
      if (schema.minimum !== undefined && value < schema.minimum) {
        this.validationErrors.push({
          path: path,
          message: `Value must be >= ${schema.minimum}`,
          value: value
        });
      }
      if (schema.maximum !== undefined && value > schema.maximum) {
        this.validationErrors.push({
          path: path,
          message: `Value must be <= ${schema.maximum}`,
          value: value
        });
      }
    }

    // Check string length
    if (typeof value === 'string') {
      if (schema.minLength !== undefined && value.length < schema.minLength) {
        this.validationErrors.push({
          path: path,
          message: `String length must be >= ${schema.minLength}`,
          value: value
        });
      }
      if (schema.maxLength !== undefined && value.length > schema.maxLength) {
        this.validationErrors.push({
          path: path,
          message: `String length must be <= ${schema.maxLength}`,
          value: value
        });
      }
    }

    // Check array
    if (Array.isArray(value)) {
      if (schema.minItems !== undefined && value.length < schema.minItems) {
        this.validationErrors.push({
          path: path,
          message: `Array must have at least ${schema.minItems} items`,
          value: value
        });
      }
      if (schema.maxItems !== undefined && value.length > schema.maxItems) {
        this.validationErrors.push({
          path: path,
          message: `Array must have at most ${schema.maxItems} items`,
          value: value
        });
      }
      
      // Validate array items
      if (schema.items) {
        for (let i = 0; i < value.length; i++) {
          this.validateProperty(value[i], schema.items, `${path}[${i}]`);
        }
      }
    }

    // Recursively validate objects
    if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      if (schema.properties) {
        this.validateAgainstSchema(value, schema, path);
      }
    }
  }

  /**
   * Validate type of value
   * @param value - Value to check
   * @param expectedType - Expected type
   * @returns True if type matches
   */
  private validateType(value: any, expectedType: string): boolean {
    switch (expectedType) {
      case 'string':
        return typeof value === 'string';
      case 'number':
        return typeof value === 'number' && !isNaN(value);
      case 'integer':
        return typeof value === 'number' && Number.isInteger(value);
      case 'boolean':
        return typeof value === 'boolean';
      case 'object':
        return typeof value === 'object' && value !== null && !Array.isArray(value);
      case 'array':
        return Array.isArray(value);
      case 'null':
        return value === null;
      default:
        return true; // Unknown type, assume valid
    }
  }

  /**
   * Get validation errors
   * @returns Array of validation errors
   */
  getErrors(): ValidationError[] {
    return this.validationErrors;
  }

  /**
   * Get validation warnings
   * @returns Array of validation warnings
   */
  getWarnings(): string[] {
    return this.validationWarnings;
  }

  /**
   * Clear validation state
   */
  clear(): void {
    this.validationErrors = [];
    this.validationWarnings = [];
  }
} 