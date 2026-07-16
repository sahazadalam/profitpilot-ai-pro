"""
Authentication endpoints for user registration, login, and profile management.
"""
from fastapi import APIRouter, Depends, status
from typing import Any

# Import from schemas
from app.schemas.auth import (
    UserSignupRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse,
    SignupResponse
)
from app.services.auth_service import auth_service
from app.dependencies.auth import get_current_active_user, require_admin
from app.core.exceptions import AppException

import logging

logger = logging.getLogger(__name__)

# Create router with prefix and tags
router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password"
)
async def signup(user_data: UserSignupRequest) -> SignupResponse:
    """
    Register a new user.
    
    Args:
        user_data: User registration data
        
    Returns:
        SignupResponse: Success message and user data
        
    Raises:
        AppException: If email already exists or validation fails
    """
    try:
        # Create user
        user = await auth_service.create_user(user_data)
        
        return SignupResponse(
            success=True,
            message="User registered successfully",
            user=user
        )
        
    except AppException as e:
        # Re-raise AppException for centralized handling
        logger.error(f"AppException in signup: {e.message} (Status: {e.status_code})")
        raise
    except Exception as e:
        # Log the full error with traceback
        logger.error(f"Unexpected error during signup: {str(e)}", exc_info=True)
        # Return the actual error message for debugging
        raise AppException(
            message=f"Registration failed: {str(e)}",
            status_code=500,
            error_code="REGISTRATION_FAILED"
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Login and get JWT token",
    description="Authenticate user and return JWT access token"
)
async def login(login_data: UserLoginRequest) -> TokenResponse:
    """
    Login user and generate access token.
    
    Args:
        login_data: User login credentials
        
    Returns:
        TokenResponse: JWT access token
        
    Raises:
        UnauthorizedException: If credentials are invalid
    """
    try:
        # Authenticate user
        auth_result = await auth_service.authenticate_user(login_data)
        
        return TokenResponse(
            access_token=auth_result["access_token"],
            token_type=auth_result["token_type"]
        )
        
    except AppException as e:
        # Re-raise AppException for centralized handling
        raise
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}", exc_info=True)
        raise AppException(
            message="Login failed",
            status_code=500,
            error_code="LOGIN_FAILED"
        )


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
    description="Get the profile of the currently authenticated user"
)
async def get_current_user_profile(
    current_user: UserResponse = Depends(get_current_active_user)
) -> UserResponse:
    """
    Get current user profile.
    
    Args:
        current_user: Current authenticated user (injected)
        
    Returns:
        UserResponse: Current user data
    """
    return current_user


@router.get(
    "/admin-only",
    status_code=status.HTTP_200_OK,
    summary="Admin only endpoint",
    description="Test endpoint that requires admin privileges"
)
async def admin_only_endpoint(
    admin_user: UserResponse = Depends(require_admin)
) -> dict:
    """
    Test endpoint for admin-only access.
    
    Args:
        admin_user: Current admin user (injected)
        
    Returns:
        dict: Success message
    """
    return {
        "success": True,
        "message": "Welcome admin!",
        "user": admin_user
    }