"""
Security module for authentication and authorization.
Handles password hashing, JWT token generation, and validation.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

# Password hashing context using bcrypt with proper settings
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,  # Number of rounds for bcrypt
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against
        
    Returns:
        bool: True if password matches, False otherwise
    """
    try:
        # Truncate password to 72 bytes for bcrypt compatibility
        password_bytes = plain_password.encode('utf-8')[:72]
        return pwd_context.verify(password_bytes, hashed_password)
    except Exception as e:
        logger.error(f"Password verification failed: {str(e)}")
        return False


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        str: Hashed password
    """
    try:
        # Truncate password to 72 bytes for bcrypt compatibility
        password_bytes = password.encode('utf-8')[:72]
        hashed = pwd_context.hash(password_bytes)
        logger.debug("Password hashed successfully")
        return hashed
    except Exception as e:
        logger.error(f"Password hashing failed: {str(e)}")
        raise ValueError(f"Password hashing failed: {str(e)}")


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Dictionary containing claims to encode
        expires_delta: Optional custom expiration time
        
    Returns:
        str: JWT token string
    """
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    # Generate JWT token
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    logger.debug(f"JWT token created for user: {data.get('sub', 'unknown')}")
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Dict[str, Any]: Decoded token claims
        
    Raises:
        JWTError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        logger.debug(f"Token decoded successfully for user: {payload.get('sub', 'unknown')}")
        return payload
    except JWTError as e:
        logger.warning(f"Token validation failed: {str(e)}")
        raise


def get_token_data(token: str) -> Dict[str, Any]:
    """
    Extract data from a valid JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Dict[str, Any]: Token data including user information
    """
    payload = decode_token(token)
    
    # Extract user data from token
    return {
        "user_id": payload.get("sub"),
        "email": payload.get("email"),
        "role": payload.get("role"),
        "exp": payload.get("exp"),
        "iat": payload.get("iat")
    }


def is_token_expired(token: str) -> bool:
    """
    Check if a JWT token has expired.
    
    Args:
        token: JWT token string
        
    Returns:
        bool: True if expired, False otherwise
    """
    try:
        payload = decode_token(token)
        exp = payload.get("exp")
        if exp:
            return datetime.utcnow() > datetime.fromtimestamp(exp)
        return True
    except JWTError:
        return True