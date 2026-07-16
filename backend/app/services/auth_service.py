"""
Authentication service for user management.
Handles business logic for registration, login, and user operations.
"""
from datetime import datetime
from typing import Optional, Dict, Any
from bson import ObjectId
import logging

from app.database.mongodb import mongodb
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.exceptions import (
    AppException,
    NotFoundException,
    UnauthorizedException,
    ForbiddenException
)
from app.schemas.auth import UserSignupRequest, UserLoginRequest, UserResponse

logger = logging.getLogger(__name__)


class AuthService:
    """
    Authentication service handling user registration, login, and profile management.
    """
    
    def __init__(self):
        """Initialize the auth service."""
        self.collection_name = "users"
    
    async def get_collection(self):
        """
        Get the users collection from MongoDB.
        
        Returns:
            Collection: MongoDB users collection
        """
        try:
            logger.info(f"Attempting to get collection: {self.collection_name}")
            # Get the collection from the database
            collection = mongodb.get_collection(self.collection_name)
            logger.info(f"Successfully got collection: {self.collection_name}")
            return collection
        except Exception as e:
            logger.error(f"Failed to get collection: {str(e)}", exc_info=True)
            raise AppException(
                message=f"Database connection error: {str(e)}",
                status_code=500,
                error_code="DATABASE_ERROR"
            )
    
    async def create_user(self, user_data: UserSignupRequest) -> UserResponse:
        """
        Register a new user.
        
        Args:
            user_data: User registration data
            
        Returns:
            UserResponse: Created user data
            
        Raises:
            AppException: If email already exists or database error
        """
        try:
            logger.info(f"Attempting to create user with email: {user_data.email}")
            
            # Get the collection
            collection = await self.get_collection()
            logger.info(f"Collection obtained successfully")
            
            # Check if user already exists
            logger.info(f"Checking if email exists: {user_data.email}")
            existing_user = await collection.find_one({"email": user_data.email})
            if existing_user:
                logger.warning(f"Registration attempt with existing email: {user_data.email}")
                raise AppException(
                    message="Email already registered",
                    status_code=409,
                    error_code="EMAIL_EXISTS"
                )
            
            logger.info(f"Email is unique, proceeding with registration")
            
            # Hash the password
            hashed_password = get_password_hash(user_data.password)
            logger.info(f"Password hashed successfully")
            
            # Create user document
            user_dict = {
                "full_name": user_data.full_name,
                "email": user_data.email,
                "hashed_password": hashed_password,
                "role": "user",  # Default role
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # Insert user into database
            logger.info(f"Inserting user into database")
            result = await collection.insert_one(user_dict)
            logger.info(f"User inserted with ID: {result.inserted_id}")
            
            # Get created user
            logger.info(f"Retrieving created user")
            created_user = await collection.find_one({"_id": result.inserted_id})
            
            if not created_user:
                logger.error(f"Failed to retrieve created user")
                raise AppException(
                    message="Failed to retrieve created user",
                    status_code=500,
                    error_code="USER_RETRIEVAL_FAILED"
                )
            
            logger.info(f"User registered successfully: {user_data.email}")
            
            # Convert to response model
            return UserResponse(
                id=str(created_user["_id"]),
                full_name=created_user["full_name"],
                email=created_user["email"],
                role=created_user["role"],
                is_active=created_user["is_active"],
                created_at=created_user["created_at"].isoformat()
            )
            
        except AppException:
            raise
        except Exception as e:
            logger.error(f"Error in create_user: {str(e)}", exc_info=True)
            # Raise with the actual error message
            raise AppException(
                message=f"Registration failed: {str(e)}",
                status_code=500,
                error_code="REGISTRATION_FAILED"
            )
    
    async def authenticate_user(self, login_data: UserLoginRequest) -> Dict[str, Any]:
        """
        Authenticate a user and generate JWT token.
        
        Args:
            login_data: User login credentials
            
        Returns:
            Dict[str, Any]: Access token and user data
            
        Raises:
            UnauthorizedException: If credentials are invalid
            ForbiddenException: If user account is inactive
        """
        try:
            collection = await self.get_collection()
            
            # Find user by email
            user = await collection.find_one({"email": login_data.email})
            if not user:
                logger.warning(f"Login attempt with non-existent email: {login_data.email}")
                raise UnauthorizedException(message="Invalid email or password")
            
            # Check if user is active
            if not user.get("is_active", True):
                logger.warning(f"Login attempt by inactive user: {login_data.email}")
                raise ForbiddenException(message="Account is deactivated")
            
            # Verify password
            if not verify_password(login_data.password, user["hashed_password"]):
                logger.warning(f"Login attempt with wrong password for: {login_data.email}")
                raise UnauthorizedException(message="Invalid email or password")
            
            # Update last login time
            await collection.update_one(
                {"_id": user["_id"]},
                {"$set": {"updated_at": datetime.utcnow()}}
            )
            
            # Create access token
            token_data = {
                "sub": str(user["_id"]),
                "email": user["email"],
                "role": user["role"]
            }
            access_token = create_access_token(token_data)
            
            logger.info(f"User logged in successfully: {login_data.email}")
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": str(user["_id"]),
                    "full_name": user["full_name"],
                    "email": user["email"],
                    "role": user["role"]
                }
            }
        except AppException:
            raise
        except Exception as e:
            logger.error(f"Error in authenticate_user: {str(e)}", exc_info=True)
            raise AppException(
                message=f"Login failed: {str(e)}",
                status_code=500,
                error_code="LOGIN_FAILED"
            )
    
    async def get_current_user(self, user_id: str) -> UserResponse:
        """
        Get current user by ID.
        
        Args:
            user_id: User ID string
            
        Returns:
            UserResponse: User data
            
        Raises:
            NotFoundException: If user not found
            ForbiddenException: If user account is inactive
        """
        try:
            collection = await self.get_collection()
            
            # Find user by ID
            try:
                user = await collection.find_one({"_id": ObjectId(user_id)})
            except Exception as e:
                logger.error(f"Error finding user by ID: {str(e)}")
                raise NotFoundException(message="User not found")
            
            if not user:
                raise NotFoundException(message="User not found")
            
            # Check if user is active
            if not user.get("is_active", True):
                raise ForbiddenException(message="Account is deactivated")
            
            # Return user data
            return UserResponse(
                id=str(user["_id"]),
                full_name=user["full_name"],
                email=user["email"],
                role=user["role"],
                is_active=user["is_active"],
                created_at=user["created_at"].isoformat()
            )
        except AppException:
            raise
        except Exception as e:
            logger.error(f"Error in get_current_user: {str(e)}", exc_info=True)
            raise AppException(
                message=f"Failed to get user: {str(e)}",
                status_code=500,
                error_code="GET_USER_FAILED"
            )


# Create singleton instance
auth_service = AuthService()