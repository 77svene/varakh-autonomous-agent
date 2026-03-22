"""
Configuration Management for VARAKH Agent
"""

import os
import yaml
import json
from typing import Dict, Any, Optional
from dataclasses import asdict
from .core import AgentConfig


class Config:
    """Handle agent configuration from various sources"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self._config: Dict[str, Any] = {}
        if config_path and os.path.exists(config_path):
            self.load(config_path)
    
    def load(self, path: str) -> None:
        """Load configuration from file"""
        _, ext = os.path.splitext(path)
        with open(path, 'r') as f:
            if ext.lower() in ['.yaml', '.yml']:
                self._config = yaml.safe_load(f)
            elif ext.lower() == '.json':
                self._config = json.load(f)
            else:
                raise ValueError(f"Unsupported config format: {ext}")
    
    def save(self, path: str) -> None:
        """Save configuration to file"""
        _, ext = os.path.splitext(path)
        with open(path, 'w') as f:
            if ext.lower() in ['.yaml', '.yml']:
                yaml.dump(self._config, f, default_flow_style=False)
            elif ext.lower() == '.json':
                json.dump(self._config, f, indent=2)
            else:
                raise ValueError(f"Unsupported config format: {ext}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value"""
        self._config[key] = value
    
    def to_agent_config(self) -> AgentConfig:
        """Convert to AgentConfig dataclass"""
        return AgentConfig(**self._config)
    
    @classmethod
    def from_agent_config(cls, agent_config: AgentConfig) -> 'Config':
        """Create Config from AgentConfig"""
        config = cls()
        config._config = asdict(agent_config)
        return config


# Default configuration
DEFAULT_CONFIG = {
    "name": "VARAKH",
    "max_thought_depth": 10,
    "action_timeout": 30.0,
    "learning_rate": 0.01,
    "memory_limit": 10000,
    "enable_self_modification": False,
    "log_level": "INFO"
}
