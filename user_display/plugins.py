from typing import Dict

_PLUGINS: Dict[str, object] = {}


def register(name: str, obj):
    _PLUGINS[name] = obj


def get(name: str):
    return _PLUGINS.get(name)


def list_plugins():
    return list(_PLUGINS.keys())
