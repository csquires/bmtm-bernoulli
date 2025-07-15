"""
Configuration manager for BMTM MLE experiments.
Handles loading and merging of configuration files.
"""
import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigManager:
    """Manages configuration loading and merging for BMTM MLE experiments."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to the configuration file. If None, uses default.
        """
        self.config = {}
        self.config_path = config_path or "configs/default.yaml"
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'sampling.num_trials')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'sampling.num_trials')
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
    
    def merge_config(self, override_config: Dict[str, Any]) -> None:
        """
        Merge additional configuration, overriding existing values.
        
        Args:
            override_config: Dictionary of configuration overrides
        """
        self._merge_dict(self.config, override_config)
    
    def _merge_dict(self, base: Dict[str, Any], override: Dict[str, Any]) -> None:
        """Recursively merge dictionaries."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_dict(base[key], value)
            else:
                base[key] = value
    
    def save_config(self, path: Optional[str] = None) -> None:
        """
        Save current configuration to file.
        
        Args:
            path: Path to save configuration. If None, uses original path.
        """
        save_path = path or self.config_path
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    def get_sampling_config(self) -> Dict[str, Any]:
        """Get sampling configuration."""
        return self.config.get('sampling', {})
    
    def get_tree_config(self) -> Dict[str, Any]:
        """Get tree configuration."""
        return self.config.get('tree', {})
    
    def get_reconstruction_config(self) -> Dict[str, Any]:
        """Get reconstruction configuration."""
        return self.config.get('reconstruction', {})
    
    def get_experiment_config(self) -> Dict[str, Any]:
        """Get experiment configuration."""
        return self.config.get('experiment', {})
    
    def get_output_config(self) -> Dict[str, Any]:
        """Get output configuration."""
        return self.config.get('output', {})
    
    def get_paths_config(self) -> Dict[str, Any]:
        """Get paths configuration."""
        return self.config.get('paths', {})
    
    def validate_config(self) -> bool:
        """
        Validate the configuration.
        
        Returns:
            True if configuration is valid
        """
        required_sections = ['sampling', 'tree', 'reconstruction', 'experiment', 'output', 'paths']
        
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required configuration section: {section}")
        
        # Validate sampling parameters
        sampling = self.get_sampling_config()
        if sampling.get('random_method') not in ['uniform', 'exponential', 'exponentialultrametric', 'symmetric']:
            raise ValueError(f"Invalid random_method: {sampling.get('random_method')}")
        
        # Validate tree parameters
        tree = self.get_tree_config()
        if tree.get('type') not in ['bin', 'long', 'star', 'random_bin']:
            raise ValueError(f"Invalid tree type: {tree.get('type')}")
        
        return True 