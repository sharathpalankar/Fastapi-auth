class BaseException(Exception):
    """Base class for all custom exceptions."""
    pass


class UserAlreadyExists(BaseException):
    """Exception raised when a user already exists."""

    def __init__(self, message="User already exists with this email."):
        self.message = message
        super().__init__(self.message)
