"""
AI-Q Dynamic Feature Manager
Handles runtime component loading and dynamic imports based on feature flags
"""

import importlib
import yaml
import asyncio
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class DynamicFeatureManager:
    def __init__(self, config_path: str = "config/feature-flags.yml"):
        self.config_path = config_path
        self.features = self.load_features()
        self.loaded_components = {}
        self.component_registry = {}
        self.initialize_component_registry()
    
    def load_features(self) -> Dict[str, Any]:
        """Load feature flags from YAML file"""
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.warning(f"Feature flags file not found at {self.config_path}")
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
    
    def initialize_component_registry(self):
        """Initialize the component registry with available modules"""
        self.component_registry = {
            # Core components
            'api_server': {
                'module': 'src.api.server',
                'class': 'APIServer',
                'init_method': 'initialize',
                'dependencies': ['postgresql', 'redis']
            },
            'web_dashboard': {
                'module': 'src.web.dashboard',
                'class': 'WebDashboard',
                'init_method': 'start',
                'dependencies': ['api_server']
            },
            'health_monitoring': {
                'module': 'src.monitoring.health',
                'class': 'HealthMonitor',
                'init_method': 'start_monitoring',
                'dependencies': []
            },
            
            # Database components
            'postgresql': {
                'module': 'src.databases.postgresql',
                'class': 'PostgreSQLManager',
                'init_method': 'connect',
                'dependencies': []
            },
            'redis': {
                'module': 'src.databases.redis',
                'class': 'RedisManager',
                'init_method': 'connect',
                'dependencies': []
            },
            'elasticsearch': {
                'module': 'src.databases.elasticsearch',
                'class': 'ElasticsearchManager',
                'init_method': 'connect',
                'dependencies': []
            },
            'neo4j': {
                'module': 'src.databases.neo4j',
                'class': 'Neo4jManager',
                'init_method': 'connect',
                'dependencies': []
            },
            'weaviate': {
                'module': 'src.databases.weaviate',
                'class': 'WeaviateManager',
                'init_method': 'connect',
                'dependencies': []
            },
            
            # Storage components
            'minio': {
                'module': 'src.storage.minio',
                'class': 'MinIOManager',
                'init_method': 'connect',
                'dependencies': []
            },
            
            # Monitoring components
            'prometheus': {
                'module': 'src.monitoring.prometheus',
                'class': 'PrometheusManager',
                'init_method': 'start',
                'dependencies': []
            },
            'grafana': {
                'module': 'src.monitoring.grafana',
                'class': 'GrafanaManager',
                'init_method': 'start',
                'dependencies': ['prometheus']
            },
            'cadvisor': {
                'module': 'src.monitoring.cadvisor',
                'class': 'CadvisorManager',
                'init_method': 'start',
                'dependencies': []
            },
            
            # AI/ML components
            'rag': {
                'module': 'src.ai.rag',
                'class': 'RAGManager',
                'init_method': 'initialize',
                'dependencies': ['elasticsearch', 'weaviate']
            },
            'vector_search': {
                'module': 'src.ai.vector_search',
                'class': 'VectorSearchManager',
                'init_method': 'initialize',
                'dependencies': ['weaviate']
            },
            'graph_analytics': {
                'module': 'src.ai.graph_analytics',
                'class': 'GraphAnalyticsManager',
                'init_method': 'initialize',
                'dependencies': ['neo4j']
            }
        }
    
    def is_enabled(self, category: str, feature: str) -> bool:
        """Check if a specific feature is enabled"""
        return self.features.get(category, {}).get(feature, False)
    
    def get_enabled_components(self) -> List[str]:
        """Get list of enabled components"""
        enabled = []
        for category, features in self.features.items():
            for feature, enabled_flag in features.items():
                if enabled_flag and feature in self.component_registry:
                    enabled.append(feature)
        return enabled
    
    def get_component_dependencies(self, component: str) -> List[str]:
        """Get dependencies for a specific component"""
        if component in self.component_registry:
            return self.component_registry[component].get('dependencies', [])
        return []
    
    def resolve_dependency_order(self) -> List[str]:
        """Resolve the order in which components should be loaded based on dependencies"""
        enabled_components = self.get_enabled_components()
        dependency_graph = {}
        
        # Build dependency graph
        for component in enabled_components:
            dependencies = self.get_component_dependencies(component)
            dependency_graph[component] = [dep for dep in dependencies if dep in enabled_components]
        
        # Topological sort
        visited = set()
        temp_visited = set()
        order = []
        
        def dfs(component):
            if component in temp_visited:
                raise ValueError(f"Circular dependency detected: {component}")
            if component in visited:
                return
            
            temp_visited.add(component)
            for dep in dependency_graph.get(component, []):
                dfs(dep)
            temp_visited.remove(component)
            visited.add(component)
            order.append(component)
        
        for component in enabled_components:
            if component not in visited:
                dfs(component)
        
        return order
    
    async def load_component(self, component_name: str) -> Optional[Any]:
        """Dynamically load a component based on feature flags"""
        if component_name in self.loaded_components:
            return self.loaded_components[component_name]
        
        if component_name not in self.component_registry:
            logger.warning(f"Component {component_name} not found in registry")
            return None
        
        if not self.is_component_enabled(component_name):
            logger.info(f"Component {component_name} is disabled")
            return None
        
        try:
            component_info = self.component_registry[component_name]
            module_name = component_info['module']
            class_name = component_info['class']
            
            # Dynamic import
            module = importlib.import_module(module_name)
            component_class = getattr(module, class_name)
            
            # Initialize component
            component_instance = component_class()
            
            # Call initialization method if it exists
            init_method = component_info.get('init_method')
            if init_method and hasattr(component_instance, init_method):
                init_func = getattr(component_instance, init_method)
                if asyncio.iscoroutinefunction(init_func):
                    await init_func()
                else:
                    init_func()
            
            self.loaded_components[component_name] = component_instance
            logger.info(f"Successfully loaded component: {component_name}")
            return component_instance
            
        except ImportError as e:
            logger.error(f"Failed to import component {component_name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to initialize component {component_name}: {e}")
            return None
    
    def is_component_enabled(self, component_name: str) -> bool:
        """Check if a component is enabled based on feature flags"""
        for category, features in self.features.items():
            if component_name in features:
                return features[component_name]
        return False
    
    async def load_all_components(self) -> Dict[str, Any]:
        """Load all enabled components in dependency order"""
        load_order = self.resolve_dependency_order()
        logger.info(f"Loading components in order: {load_order}")
        
        for component_name in load_order:
            await self.load_component(component_name)
        
        return self.loaded_components
    
    def get_component(self, component_name: str) -> Optional[Any]:
        """Get a loaded component instance"""
        return self.loaded_components.get(component_name)
    
    def register_component(self, name: str, module: str, class_name: str, 
                          init_method: str = None, dependencies: List[str] = None):
        """Register a new component dynamically"""
        self.component_registry[name] = {
            'module': module,
            'class': class_name,
            'init_method': init_method,
            'dependencies': dependencies or []
        }
        logger.info(f"Registered new component: {name}")
    
    def unload_component(self, component_name: str):
        """Unload a component and clean up resources"""
        if component_name in self.loaded_components:
            component = self.loaded_components[component_name]
            
            # Call cleanup method if it exists
            if hasattr(component, 'cleanup'):
                cleanup_func = getattr(component, 'cleanup')
                if asyncio.iscoroutinefunction(cleanup_func):
                    asyncio.create_task(cleanup_func())
                else:
                    cleanup_func()
            
            del self.loaded_components[component_name]
            logger.info(f"Unloaded component: {component_name}")
    
    def reload_component(self, component_name: str) -> Optional[Any]:
        """Reload a component"""
        self.unload_component(component_name)
        return asyncio.create_task(self.load_component(component_name))
    
    def get_component_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all components"""
        status = {}
        for component_name in self.component_registry:
            status[component_name] = {
                'enabled': self.is_component_enabled(component_name),
                'loaded': component_name in self.loaded_components,
                'dependencies': self.get_component_dependencies(component_name)
            }
        return status

# Global feature manager instance
feature_manager = DynamicFeatureManager() 