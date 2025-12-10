class UserDisplayError(Exception):
    pass

class ValidationError(UserDisplayError):
    pass

class ExportError(UserDisplayError):
    pass