"""
Configuration management for the user display system.
Supports defaults, environment overrides, and runtime overrides.
"""

import os
from typing import Dict, Any

class Config:
    """Configuration class with freeze support."""

    DEFAULTS = {
        'max_users': 200000,
        'shard_count': 4,
        'parallel_filtering': True,
        'log_level': 'INFO',
        'cache_enabled': True,
        'validation_strict': False,
    }

    def __init__(self):
        self._config = self.DEFAULTS.copy()
        self._frozen = False
        self._load_from_env()

    def _load_from_env(self):
        """Load configuration from environment variables."""
        env_mappings = {
            'USER_DISPLAY_MAX_USERS': 'max_users',
            'USER_DISPLAY_SHARD_COUNT': 'shard_count',
            'USER_DISPLAY_PARALLEL_FILTERING': 'parallel_filtering',
            'USER_DISPLAY_LOG_LEVEL': 'log_level',
            'USER_DISPLAY_CACHE_ENABLED': 'cache_enabled',
            'USER_DISPLAY_VALIDATION_STRICT': 'validation_strict',
        }
        for env_var, key in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                self._config[key] = self._parse_value(value, type(self.DEFAULTS[key]))

    def _parse_value(self, value: str, expected_type: type) -> Any:
        """Parse string value to expected type."""
        if expected_type == bool:
            return value.lower() in ('true', '1', 'yes', 'on')
        elif expected_type == int:
            return int(value)
        elif expected_type == float:
            return float(value)
        else:
            return value

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)

    def set(self, key: str, value: Any):
        """Set configuration value if not frozen."""
        if self._frozen:
            raise ValueError("Configuration is frozen")
        self._config[key] = value

    def freeze(self):
        """Freeze the configuration to prevent further changes."""
        self._frozen = True

    def unfreeze(self):
        """Unfreeze the configuration."""
        self._frozen = False

    def to_dict(self) -> Dict[str, Any]:
        """Return a copy of the configuration as dict."""
        return self._config.copy()

# Global config instance
config = Config()