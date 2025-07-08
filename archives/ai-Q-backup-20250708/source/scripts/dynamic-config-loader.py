#!/usr/bin/env python3

"""
AI-Q Dynamic Configuration Loader
Version: 1.0.0
Created: 2025-01-28
Purpose: Load dynamic port and IP configuration from JSON files with advanced functionality
"""

import json
import os
import sys
import argparse
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import subprocess
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DynamicConfigLoader:
    """Dynamic configuration loader for AI-Q system"""
    
    def __init__(self, config_root: str = "/opt/ai-q/config"):
        self.config_root = Path(config_root)
        self.dynamic_config_file = self.config_root / "dynamic" / "dynamic-config.json"
        self.network_config_file = self.config_root / "network" / "ip-config.json"
        self.env_file = Path("/opt/ai-q/.env.dynamic")
        self.docker_env_file = Path("/opt/ai-q/docker/.env.dynamic")
        
        self.config = {}
        self.network_profile = os.getenv("AIQ_NETWORK_PROFILE", "local_network")
        
    def load_configuration(self) -> bool:
        """Load configuration files"""
        try:
            # Load dynamic configuration
            if not self.dynamic_config_file.exists():
                logger.error(f"Dynamic configuration file not found: {self.dynamic_config_file}")
                return False
                
            with open(self.dynamic_config_file, 'r') as f:
                self.config = json.load(f)
                
            # Load network configuration
            if not self.network_config_file.exists():
                logger.error(f"Network configuration file not found: {self.network_config_file}")
                return False
                
            with open(self.network_config_file, 'r') as f:
                self.network_config = json.load(f)
                
            logger.info("Configuration files loaded successfully")
            return True
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {e}")
            return False
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return False
    
    def get_network_profile(self) -> Dict[str, Any]:
        """Get current network profile configuration"""
        profiles = self.config.get("network_profiles", {})
        profile = profiles.get(self.network_profile)
        
        if not profile:
            logger.error(f"Network profile '{self.network_profile}' not found")
            return {}
            
        return profile
    
    def generate_service_urls(self) -> Dict[str, str]:
        """Generate URLs for all services"""
        network_profile = self.get_network_profile()
        base_url = network_profile.get("base_url", "http://localhost")
        
        service_urls = {}
        port_config = self.config.get("port_configuration", {})
        
        for category, category_config in port_config.items():
            services = category_config.get("services", {})
            
            for service_key, service_config in services.items():
                port = service_config.get("port")
                name = service_config.get("name", service_key)
                url_template = service_config.get("url_template", "{base_url}:{port}")
                
                if port:
                    url = url_template.format(base_url=base_url, port=port)
                    service_urls[service_key] = {
                        "name": name,
                        "port": port,
                        "url": url,
                        "category": category,
                        "health_check": service_config.get("health_check", "")
                    }
        
        return service_urls
    
    def generate_environment_variables(self) -> Dict[str, str]:
        """Generate environment variables"""
        network_profile = self.get_network_profile()
        service_urls = self.generate_service_urls()
        
        env_vars = {
            "AIQ_NETWORK_PROFILE": self.network_profile,
            "AIQ_BIND_ADDRESS": network_profile.get("bind_address", "0.0.0.0"),
            "AIQ_EXTERNAL_ADDRESS": network_profile.get("external_address", "localhost"),
            "AIQ_BASE_URL": network_profile.get("base_url", "http://localhost"),
            "AIQ_SUBNET": network_profile.get("subnet", "127.0.0.0/8"),
            "AIQ_GATEWAY": network_profile.get("gateway", "127.0.0.1")
        }
        
        # Add service-specific variables
        for service_key, service_info in service_urls.items():
            service_upper = service_key.upper()
            env_vars[f"{service_upper}_PORT"] = str(service_info["port"])
            env_vars[f"{service_upper}_URL"] = service_info["url"]
            env_vars[f"{service_upper}_HEALTH_CHECK"] = service_info["health_check"]
        
        return env_vars
    
    def write_environment_file(self, env_vars: Dict[str, str]) -> bool:
        """Write environment variables to file"""
        try:
            # Create directory if it doesn't exist
            self.env_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.env_file, 'w') as f:
                f.write(f"# AI-Q Dynamic Configuration\n")
                f.write(f"# Generated: {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}\n")
                f.write(f"# Network Profile: {self.network_profile}\n\n")
                
                # Write network configuration
                f.write("# Network Configuration\n")
                for key, value in env_vars.items():
                    if key.startswith("AIQ_"):
                        f.write(f"{key}={value}\n")
                f.write("\n")
                
                # Write service configuration
                f.write("# Service Configuration\n")
                for key, value in env_vars.items():
                    if not key.startswith("AIQ_"):
                        f.write(f"{key}={value}\n")
            
            logger.info(f"Environment file written: {self.env_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error writing environment file: {e}")
            return False
    
    def write_docker_env_file(self, env_vars: Dict[str, str]) -> bool:
        """Write Docker-specific environment file"""
        try:
            # Create directory if it doesn't exist
            self.docker_env_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.docker_env_file, 'w') as f:
                f.write(f"# AI-Q Docker Dynamic Configuration\n")
                f.write(f"# Generated: {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}\n\n")
                
                # Write network configuration
                f.write("# Network Configuration\n")
                for key, value in env_vars.items():
                    if key.startswith("AIQ_"):
                        f.write(f"{key}={value}\n")
                f.write("\n")
                
                # Write service ports
                f.write("# Service Ports\n")
                for key, value in env_vars.items():
                    if key.endswith("_PORT"):
                        f.write(f"{key}={value}\n")
            
            logger.info(f"Docker environment file written: {self.docker_env_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error writing Docker environment file: {e}")
            return False
    
    def validate_configuration(self) -> bool:
        """Validate configuration"""
        try:
            # Check required files
            if not self.dynamic_config_file.exists():
                logger.error(f"Dynamic configuration file not found: {self.dynamic_config_file}")
                return False
            
            if not self.network_config_file.exists():
                logger.error(f"Network configuration file not found: {self.network_config_file}")
                return False
            
            # Validate network profile
            network_profile = self.get_network_profile()
            if not network_profile:
                return False
            
            # Validate IP format
            external_address = network_profile.get("external_address")
            if external_address and external_address != "localhost":
                ip_pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
                if not re.match(ip_pattern, external_address):
                    logger.error(f"Invalid IP address format: {external_address}")
                    return False
            
            logger.info("Configuration validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False
    
    def display_configuration(self, env_vars: Dict[str, str], service_urls: Dict[str, Any]):
        """Display current configuration"""
        logger.info("Current Configuration:")
        logger.info(f"  Network Profile: {self.network_profile}")
        logger.info(f"  Bind Address: {env_vars.get('AIQ_BIND_ADDRESS', 'N/A')}")
        logger.info(f"  External Address: {env_vars.get('AIQ_EXTERNAL_ADDRESS', 'N/A')}")
        logger.info(f"  Base URL: {env_vars.get('AIQ_BASE_URL', 'N/A')}")
        logger.info(f"  Environment File: {self.env_file}")
        
        print("\nService URLs:")
        for service_key, service_info in service_urls.items():
            print(f"  {service_info['name']}: {service_info['url']} (port {service_info['port']})")
    
    def run(self) -> bool:
        """Run the configuration loader"""
        logger.info("Starting dynamic configuration loader...")
        
        # Load configuration
        if not self.load_configuration():
            return False
        
        # Validate configuration
        if not self.validate_configuration():
            return False
        
        # Generate environment variables
        env_vars = self.generate_environment_variables()
        service_urls = self.generate_service_urls()
        
        # Write files
        if not self.write_environment_file(env_vars):
            return False
        
        if not self.write_docker_env_file(env_vars):
            return False
        
        # Display configuration
        self.display_configuration(env_vars, service_urls)
        
        logger.info("Dynamic configuration loading completed successfully")
        logger.info(f"To use this configuration, source the environment file:")
        logger.info(f"  source {self.env_file}")
        
        return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="AI-Q Dynamic Configuration Loader")
    parser.add_argument("--config-root", default="/opt/ai-q/config", help="Configuration root directory")
    parser.add_argument("--network-profile", help="Network profile to use")
    parser.add_argument("--validate-only", action="store_true", help="Only validate configuration")
    
    args = parser.parse_args()
    
    # Set network profile if provided
    if args.network_profile:
        os.environ["AIQ_NETWORK_PROFILE"] = args.network_profile
    
    # Create loader
    loader = DynamicConfigLoader(args.config_root)
    
    # Run loader
    success = loader.run()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main() 