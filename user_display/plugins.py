class PluginManager:
    def __init__(self):
        self.filters = {}
        self.formatters = {}
        self.validators = {}

    def register_filter(self, name, cls):
        self.filters[name] = cls

    def register_formatter(self, name, cls):
        self.formatters[name] = cls

    def register_validator(self, name, cls):
        self.validators[name] = cls


plugin_manager = PluginManager()
