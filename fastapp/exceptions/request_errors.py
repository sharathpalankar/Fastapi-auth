class BaseException(Exception):
    """Base class for all custom exceptions."""
    pass


class UserAlreadyExists(BaseException):
    """Exception raised when a user already exists."""

    def __init__(self, message="User already exists with this email."):
        self.message = message
        super().__init__(self.message)

class InvalidCredentials(BaseException):
    """Exception raised for invalid login credentials."""

    def __init__(self, message="Invalid email or password."):
        self.message = message
        super().__init__(self.message)

class RefreshTokenExpired(BaseException):
    """Exception raised when a refresh token has expired."""

    def __init__(self, message="Refresh token has expired. Please log in again."):
        self.message = message
        super().__init__(self.message)
