#!/usr/bin/env python3
"""
AI-Q Feature Flag Parser
Parses feature flags and generates dynamic Docker configurations
"""

import yaml
import os
import sys
from pathlib import Path
from typing import Dict, Any, List

class FeatureFlagParser:
    def __init__(self, config_path: str = "config/feature-flags.yml"):
        self.config_path = config_path
        self.features = self.load_features()
    
    def load_features(self) -> Dict[str, Any]:
        """Load feature flags from YAML file"""
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Warning: Feature flags file not found at {self.config_path}")
            return self.get_default_features()
    
    def get_default_features(self) -> Dict[str, Any]:
        """Return default feature configuration"""
        return {
            'core': {
                'api_server': True,
                'web_dashboard': True,
                'health_monitoring': True
            },
            'databases': {
                'postgresql': True,
                'redis': True,
                'elasticsearch': True,
                'neo4j': True,
                'weaviate': True
            },
            'storage': {
                'minio': True
            },
            'monitoring': {
                'prometheus': True,
                'grafana': True,
                'cadvisor': True
            }
        }
    
    def is_enabled(self, category: str, feature: str) -> bool:
        """Check if a specific feature is enabled"""
        return self.features.get(category, {}).get(feature, False)
    
    def get_enabled_services(self) -> List[str]:
        """Get list of enabled services for Docker Compose"""
        services = []
        
        # Core services
        if self.is_enabled('core', 'api_server'):
            services.append('ai-q-app')
        
        # Database services
        if self.is_enabled('databases', 'postgresql'):
            services.append('postgres')
        if self.is_enabled('databases', 'redis'):
            services.append('redis')
        if self.is_enabled('databases', 'elasticsearch'):
            services.append('elasticsearch')
        if self.is_enabled('databases', 'neo4j'):
            services.append('neo4j')
        if self.is_enabled('databases', 'weaviate'):
            services.append('weaviate')
        
        # Storage services
        if self.is_enabled('storage', 'minio'):
            services.append('minio')
        
        # Monitoring services
        if self.is_enabled('monitoring', 'prometheus'):
            services.append('prometheus')
        if self.is_enabled('monitoring', 'grafana'):
            services.append('grafana')
        
        return services
    
    def generate_docker_compose(self, output_path: str = "docker/compose/docker-compose.feature-flags.yml"):
        """Generate Docker Compose file based on feature flags"""
        enabled_services = self.get_enabled_services()
        
        # Read the base Docker Compose file
        base_compose_path = "docker/compose/docker-compose.unified.yml"
        if not os.path.exists(base_compose_path):
            print(f"Error: Base Docker Compose file not found: {base_compose_path}")
            return False
        
        with open(base_compose_path, 'r') as file:
            compose_content = yaml.safe_load(file)
        
        # Filter services based on feature flags
        filtered_services = {}
        for service_name, service_config in compose_content.get('services', {}).items():
            if service_name in enabled_services:
                filtered_services[service_name] = service_config
        
        # Update the compose content
        compose_content['services'] = filtered_services
        
        # Write the filtered Docker Compose file
        with open(output_path, 'w') as file:
            yaml.dump(compose_content, file, default_flow_style=False, sort_keys=False)
        
        print(f"Generated feature-flag-based Docker Compose: {output_path}")
        print(f"Enabled services: {', '.join(enabled_services)}")
        return True
    
    def generate_environment_vars(self) -> Dict[str, str]:
        """Generate environment variables based on feature flags"""
        env_vars = {}
        
        # Core features
        env_vars['ENABLE_API_SERVER'] = str(self.is_enabled('core', 'api_server')).lower()
        env_vars['ENABLE_WEB_DASHBOARD'] = str(self.is_enabled('core', 'web_dashboard')).lower()
        env_vars['ENABLE_HEALTH_MONITORING'] = str(self.is_enabled('core', 'health_monitoring')).lower()
        
        # Database features
        env_vars['ENABLE_POSTGRESQL'] = str(self.is_enabled('databases', 'postgresql')).lower()
        env_vars['ENABLE_REDIS'] = str(self.is_enabled('databases', 'redis')).lower()
        env_vars['ENABLE_ELASTICSEARCH'] = str(self.is_enabled('databases', 'elasticsearch')).lower()
        env_vars['ENABLE_NEO4J'] = str(self.is_enabled('databases', 'neo4j')).lower()
        env_vars['ENABLE_WEAVIATE'] = str(self.is_enabled('databases', 'weaviate')).lower()
        
        # Storage features
        env_vars['ENABLE_MINIO'] = str(self.is_enabled('storage', 'minio')).lower()
        
        # Monitoring features
        env_vars['ENABLE_PROMETHEUS'] = str(self.is_enabled('monitoring', 'prometheus')).lower()
        env_vars['ENABLE_GRAFANA'] = str(self.is_enabled('monitoring', 'grafana')).lower()
        env_vars['ENABLE_CADVISOR'] = str(self.is_enabled('monitoring', 'cadvisor')).lower()
        
        # AI/ML features
        env_vars['ENABLE_RAG'] = str(self.is_enabled('ai_ml', 'rag_enabled')).lower()
        env_vars['ENABLE_VECTOR_SEARCH'] = str(self.is_enabled('ai_ml', 'vector_search')).lower()
        env_vars['ENABLE_GRAPH_ANALYTICS'] = str(self.is_enabled('ai_ml', 'graph_analytics')).lower()
        
        # Development features
        env_vars['ENABLE_HOT_RELOAD'] = str(self.is_enabled('development', 'hot_reload')).lower()
        env_vars['ENABLE_DEBUG_MODE'] = str(self.is_enabled('development', 'debug_mode')).lower()
        env_vars['ENABLE_VERBOSE_LOGGING'] = str(self.is_enabled('development', 'verbose_logging')).lower()
        
        return env_vars
    
    def generate_env_file(self, output_path: str = ".env.feature-flags"):
        """Generate .env file based on feature flags"""
        env_vars = self.generate_environment_vars()
        
        with open(output_path, 'w') as file:
            file.write("# AI-Q Feature Flags Environment Variables\n")
            file.write("# Generated automatically from feature-flags.yml\n\n")
            
            for key, value in env_vars.items():
                file.write(f"{key}={value}\n")
        
        print(f"Generated environment file: {output_path}")
        return True

def main():
    """Main function for command-line usage"""
    parser = FeatureFlagParser()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "generate-compose":
            parser.generate_docker_compose()
        elif command == "generate-env":
            parser.generate_env_file()
        elif command == "list-services":
            services = parser.get_enabled_services()
            print("Enabled services:")
            for service in services:
                print(f"  - {service}")
        elif command == "check":
            feature = sys.argv[2] if len(sys.argv) > 2 else None
            category = sys.argv[3] if len(sys.argv) > 3 else None
            
            if feature and category:
                enabled = parser.is_enabled(category, feature)
                print(f"{category}.{feature}: {'enabled' if enabled else 'disabled'}")
            else:
                print("Usage: python feature-flag-parser.py check <feature> <category>")
        else:
            print("Unknown command. Available commands:")
            print("  generate-compose - Generate Docker Compose file")
            print("  generate-env     - Generate environment file")
            print("  list-services    - List enabled services")
            print("  check <feature> <category> - Check specific feature")
    else:
        # Default: generate both files
        parser.generate_docker_compose()
        parser.generate_env_file()

if __name__ == "__main__":
    main() 