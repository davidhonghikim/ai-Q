"""
AI-Q Component Loader
Handles dynamic imports and lazy loading of components
"""

import importlib.util
import sys
import os
from typing import Any, Dict, Optional, Callable
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ComponentLoader:
    def __init__(self, base_path: str = "src"):
        self.base_path = Path(base_path)
        self.loaded_modules = {}
        self.module_cache = {}
    
    def load_module_from_path(self, module_path: str, class_name: str = None) -> Optional[Any]:
        """Load a module from a file path dynamically"""
        try:
            # Convert module path to file path
            file_path = self.base_path / f"{module_path.replace('.', '/')}.py"
            
            if not file_path.exists():
                logger.warning(f"Module file not found: {file_path}")
                return None
            
            # Load the module
            spec = importlib.util.spec_from_file_location(module_path, file_path)
            if spec is None or spec.loader is None:
                logger.error(f"Failed to create spec for module: {module_path}")
                return None
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_path] = module
            spec.loader.exec_module(module)
            
            self.loaded_modules[module_path] = module
            
            # Return the class if specified
            if class_name:
                if hasattr(module, class_name):
                    return getattr(module, class_name)
                else:
                    logger.error(f"Class {class_name} not found in module {module_path}")
                    return None
            
            return module
            
        except Exception as e:
            logger.error(f"Failed to load module {module_path}: {e}")
            return None
    
    def load_component(self, component_name: str, module_path: str, 
                      class_name: str = None, **kwargs) -> Optional[Any]:
        """Load a component with optional initialization parameters"""
        try:
            # Check cache first
            cache_key = f"{component_name}:{module_path}:{class_name}"
            if cache_key in self.module_cache:
                return self.module_cache[cache_key]
            
            # Load the module/class
            component_class = self.load_module_from_path(module_path, class_name)
            if component_class is None:
                return None
            
            # Instantiate the component
            if callable(component_class):
                component_instance = component_class(**kwargs)
                self.module_cache[cache_key] = component_instance
                logger.info(f"Successfully loaded component: {component_name}")
                return component_instance
            else:
                logger.error(f"Component class {class_name} is not callable")
                return None
                
        except Exception as e:
            logger.error(f"Failed to load component {component_name}: {e}")
            return None
    
    def lazy_load(self, component_name: str, module_path: str, 
                  class_name: str = None, **kwargs) -> Callable:
        """Create a lazy loading function for a component"""
        def load_when_needed():
            return self.load_component(component_name, module_path, class_name, **kwargs)
        
        return load_when_needed
    
    def reload_module(self, module_path: str) -> bool:
        """Reload a previously loaded module"""
        try:
            if module_path in self.loaded_modules:
                module = self.loaded_modules[module_path]
                importlib.reload(module)
                logger.info(f"Reloaded module: {module_path}")
                return True
            else:
                logger.warning(f"Module {module_path} not found in loaded modules")
                return False
        except Exception as e:
            logger.error(f"Failed to reload module {module_path}: {e}")
            return False
    
    def get_loaded_modules(self) -> Dict[str, Any]:
        """Get all loaded modules"""
        return self.loaded_modules.copy()
    
    def clear_cache(self):
        """Clear the module cache"""
        self.module_cache.clear()
        logger.info("Module cache cleared")
    
    def discover_components(self, directory: str = None) -> Dict[str, Dict[str, str]]:
        """Discover available components in a directory"""
        if directory is None:
            directory = self.base_path
        
        components = {}
        dir_path = Path(directory)
        
        for file_path in dir_path.rglob("*.py"):
            if file_path.name.startswith("__"):
                continue
            
            # Convert file path to module path
            relative_path = file_path.relative_to(self.base_path)
            module_path = str(relative_path).replace("/", ".").replace("\\", ".").replace(".py", "")
            
            # Try to extract component information from the file
            try:
                spec = importlib.util.spec_from_file_location(module_path, file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Look for classes that might be components
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (isinstance(attr, type) and 
                            not attr_name.startswith("_") and
                            hasattr(attr, "__module__")):
                            
                            components[f"{module_path}.{attr_name}"] = {
                                "module_path": module_path,
                                "class_name": attr_name,
                                "file_path": str(file_path)
                            }
            except Exception as e:
                logger.debug(f"Could not analyze {file_path}: {e}")
        
        return components

# Global component loader instance
component_loader = ComponentLoader() 