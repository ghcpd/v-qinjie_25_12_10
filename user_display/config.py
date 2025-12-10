"""
Configuration management for user_display module.
Supports defaults, environment overrides, and runtime overrides.
"""

import os
from typing import Any, Dict, Optional


_global_config = None


class Config:
    """
    Centralized configuration system with layered overrides.
    Priority: runtime > environment > defaults
    """
    
    # Default configuration
    _defaults = {
        "debug": False,
        "enable_caching": True,
        "cache_size": 1000,
        "enable_parallel_filtering": True,
        "parallel_batch_size": 1000,
        "enable_sharding": True,
        "shard_count": 4,
        "enable_snapshotting": True,
        "snapshot_max_versions": 10,
        "log_level": "INFO",
        "validate_on_insert": True,
        "strict_validation": False,
        "allow_partial_records": True,
        "default_formatter": "compact",
        "max_field_length": None,
        "enable_metrics": True,
        "frozen": False,
    }
    
    def __init__(self):
        """Initialize configuration with defaults and environment overrides."""
        self._config: Dict[str, Any] = dict(self._defaults)
        self._frozen = False
        self._load_environment_overrides()
    
    def _load_environment_overrides(self) -> None:
        """Load environment variable overrides (prefix: USER_DISPLAY_)."""
        for key, default_value in self._defaults.items():
            env_key = f"USER_DISPLAY_{key.upper()}"
            env_value = os.environ.get(env_key)
            if env_value is not None:
                # Simple type conversion
                if isinstance(default_value, bool):
                    self._config[key] = env_value.lower() in ("true", "1", "yes")
                elif isinstance(default_value, int):
                    try:
                        self._config[key] = int(env_value)
                    except ValueError:
                        pass
                else:
                    self._config[key] = env_value
    
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Retrieve a configuration value."""
        if key not in self._config:
            return default
        return self._config[key]
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value (unless frozen)."""
        if self._frozen:
            raise RuntimeError("Configuration is frozen and cannot be modified.")
        self._config[key] = value
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update multiple configuration values at once."""
        if self._frozen:
            raise RuntimeError("Configuration is frozen and cannot be modified.")
        self._config.update(updates)
    
    def freeze(self) -> None:
        """Freeze configuration to prevent further modifications."""
        self._frozen = True
    
    def is_frozen(self) -> bool:
        """Check if configuration is frozen."""
        return self._frozen
    
    def to_dict(self) -> Dict[str, Any]:
        """Export current configuration as a dictionary."""
        return dict(self._config)
    
    @classmethod
    def reset_defaults(cls) -> None:
        """Reset defaults to original values."""
        cls._defaults.clear()
        cls._defaults.update({
            "debug": False,
            "enable_caching": True,
            "cache_size": 1000,
            "enable_parallel_filtering": True,
            "parallel_batch_size": 1000,
            "enable_sharding": True,
            "shard_count": 4,
            "enable_snapshotting": True,
            "snapshot_max_versions": 10,
            "log_level": "INFO",
            "validate_on_insert": True,
            "strict_validation": False,
            "allow_partial_records": True,
            "default_formatter": "compact",
            "max_field_length": None,
            "enable_metrics": True,
            "frozen": False,
        })


# Global config instance
_global_config: Optional[Config] = None


def get_config() -> Config:
    """Get or create the global configuration instance."""
    global _global_config
    if _global_config is None:
        _global_config = Config()
    return _global_config


def reset_config() -> None:
    """Reset the global configuration."""
    global _global_config
    _global_config = None
    _global_config = None
