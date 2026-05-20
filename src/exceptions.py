import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""Custom exceptions for the application."""

class AppError(Exception):
    """Base application exception."""
    pass

class DatabaseError(AppError):
    """Raised when a database operation fails."""
    pass

class AuthenticationError(AppError):
    """Raised when login/registration fails."""
    pass

class ValidationError(AppError):
    """Raised when input validation fails."""
    pass

class ExportError(AppError):
    """Raised when exporting reports fails."""
    pass
