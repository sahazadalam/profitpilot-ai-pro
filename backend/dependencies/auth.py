"""
Authentication dependencies for route protection.
Provides dependency injection for JWT validation and user authorization.
"""
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
import logging

from app.core.security import get_token_data
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.services.auth_service import auth_service
from app.schemas.auth import UserResponse

logger = logging.getLogger(__name__)

# OAuth2 scheme for JWT token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    """
    Get current authenticated user from JWT token.
    
    Args:
        token: JWT token from Authorization header
        
    Returns:
        UserResponse: Current user data
        
    Raises:
        UnauthorizedException: If token is invalid or user not found
    """
    try:
        # Decode token
        token_data = get_token_data(token)
        user_id = token_data.get("user_id")
        
        if not user_id:
            raise UnauthorizedException(message="Invalid token")
        
        # Get user from database
        user = await auth_service.get_current_user(user_id)
        
        return user
        
    except Exception as e:
        logger.warning(f"Authentication failed: {str(e)}")
        raise UnauthorizedException(message="Could not validate credentials")


async def get_current_active_user(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    """
    Get current active user.
    
    Args:
        current_user: Current user from token
        
    Returns:
        UserResponse: Current active user
        
    Raises:
        ForbiddenException: If user is inactive
    """
    if not current_user.is_active:
        raise ForbiddenException(message="Inactive user account")
    return current_user


async def require_admin(current_user: UserResponse = Depends(get_current_active_user)) -> UserResponse:
    """
    Require admin role for access.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserResponse: Current user with admin role
        
    Raises:
        ForbiddenException: If user is not an admin
    """
    if current_user.role != "admin":
        logger.warning(f"Access denied for non-admin user: {current_user.email}")
        raise ForbiddenException(message="Admin access required")
    return current_user


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """
    Get current user ID from token.
    
    Args:
        token: JWT token
        
    Returns:
        str: User ID
        
    Raises:
        UnauthorizedException: If token is invalid
    """
    try:
        token_data = get_token_data(token)
        user_id = token_data.get("user_id")
        
        if not user_id:
            raise UnauthorizedException(message="Invalid token")
        
        return user_id
        
    except Exception as e:
        logger.warning(f"Failed to extract user ID from token: {str(e)}")
        raise UnauthorizedException(message="Could not validate credentials")


async def get_optional_user(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[UserResponse]:
    """
    Get current user if authenticated, return None otherwise.
    
    Args:
        token: Optional JWT token
        
    Returns:
        Optional[UserResponse]: User data or None
    """
    if not token:
        return None
    
    try:
        return await get_current_user(token)
    except UnauthorizedException:
        return None