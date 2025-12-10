class PluginRegistry:
    def __init__(self):
        self.formatters = {}
        self.filters = {}
        self.validators = {}

    def register_formatter(self, name, callable_):
        self.formatters[name] = callable_

    def register_filter(self, name, callable_):
        self.filters[name] = callable_

    def register_validator(self, name, callable_):
        self.validators[name] = callable_


DEFAULT_REGISTRY = PluginRegistry()
