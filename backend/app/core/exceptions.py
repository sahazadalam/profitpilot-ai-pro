"""
Centralized exception handling module for ProfitPilot AI Pro.
Defines custom exceptions and error response handlers.
"""
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)


class AppException(Exception):
    """
    Base exception class for application-specific errors.
    """
    def __init__(self, message: str, status_code: int = 400, error_code: str = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)


class NotFoundException(AppException):
    """Exception for resource not found."""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404, error_code="NOT_FOUND")


class ValidationException(AppException):
    """Exception for validation errors."""
    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status_code=422, error_code="VALIDATION_ERROR")


class DatabaseException(AppException):
    """Exception for database errors."""
    def __init__(self, message: str = "Database error"):
        super().__init__(message, status_code=500, error_code="DATABASE_ERROR")


class UnauthorizedException(AppException):
    """Exception for unauthorized access."""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401, error_code="UNAUTHORIZED")


class ForbiddenException(AppException):
    """Exception for forbidden access."""
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=403, error_code="FORBIDDEN")


class AuthenticationException(AppException):
    """Exception for authentication errors."""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401, error_code="AUTHENTICATION_ERROR")


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Handle application-specific exceptions.
    
    Args:
        request: FastAPI request object
        exc: Application exception
        
    Returns:
        JSONResponse: Structured error response
    """
    logger.error(f"AppException: {exc.message} (Status: {exc.status_code}, Code: {exc.error_code})")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "message": exc.message,
                "code": exc.error_code,
                "status_code": exc.status_code
            }
        }
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle all other exceptions.
    
    Args:
        request: FastAPI request object
        exc: Exception object
        
    Returns:
        JSONResponse: Structured error response
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "message": f"Internal server error: {str(exc)}",
                "code": "INTERNAL_ERROR",
                "status_code": 500
            }
        }
    )