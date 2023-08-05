class LeanbaseException(Exception):
    pass

class BadConfigurationException(LeanbaseException):
    def __init__(self, message):
        self.message = message

class ReconfigurationException(LeanbaseException):
    pass

class NotConfiguredException(LeanbaseException):
    def __init__(self):
        self.message = 'leanbase.configure() must be called before leanbase.user()'