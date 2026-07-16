from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
import logging

from app.core.security import get_token_data
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.services.auth_service import auth_service
from app.schemas.auth import UserResponse

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    try:
        token_data = get_token_data(token)
        user_id = token_data.get("user_id")
        if not user_id:
            raise UnauthorizedException(message="Invalid token")
        user = await auth_service.get_current_user(user_id)
        return user
    except Exception as e:
        logger.warning(f"Authentication failed: {str(e)}")
        raise UnauthorizedException(message="Could not validate credentials")

async def get_current_active_user(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    if not current_user.is_active:
        raise ForbiddenException(message="Inactive user account")
    return current_user

async def require_admin(current_user: UserResponse = Depends(get_current_active_user)) -> UserResponse:
    if current_user.role != "admin":
        logger.warning(f"Access denied for non-admin user: {current_user.email}")
        raise ForbiddenException(message="Admin access required")
    return current_user

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
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
    if not token:
        return None
    try:
        return await get_current_user(token)
    except UnauthorizedException:
        return None
