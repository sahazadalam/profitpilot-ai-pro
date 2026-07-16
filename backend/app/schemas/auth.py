"""
Authentication schemas for request/response validation.
Defines Pydantic models for auth endpoints.
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class UserSignupRequest(BaseModel):
    """
    Request schema for user registration.
    """
    full_name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, max_length=72, description="Password (8-72 characters)")
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """
        Validate password strength.
        """
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        if len(v) > 72:
            raise ValueError('Password cannot be longer than 72 characters')
        
        # Check for at least one digit
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        
        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "full_name": "Sahzad Alam",
                "email": "sahzad@example.com",
                "password": "StrongPass123!"
            }
        }
    }


class UserLoginRequest(BaseModel):
    """
    Request schema for user login.
    """
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=1, max_length=72, description="User's password")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "sahzad@example.com",
                "password": "StrongPass123!"
            }
        }
    }


class TokenResponse(BaseModel):
    """
    Response schema for authentication token.
    """
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    }


class UserResponse(BaseModel):
    """
    Response schema for user data (excludes sensitive information).
    """
    id: str = Field(..., description="User ID")
    full_name: str = Field(..., description="User's full name")
    email: str = Field(..., description="User's email address")
    role: str = Field(..., description="User role")
    is_active: bool = Field(..., description="Whether the user account is active")
    created_at: str = Field(..., description="Account creation timestamp")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "full_name": "Sahzad Alam",
                "email": "sahzad@example.com",
                "role": "admin",
                "is_active": True,
                "created_at": "2026-07-15T12:00:00"
            }
        }
    }


class SignupResponse(BaseModel):
    """
    Response schema for successful registration.
    """
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Success message")
    user: UserResponse = Field(..., description="Created user data")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "message": "User registered successfully",
                "user": {
                    "id": "507f1f77bcf86cd799439011",
                    "full_name": "Sahzad Alam",
                    "email": "sahzad@example.com",
                    "role": "user",
                    "is_active": True,
                    "created_at": "2026-07-15T12:00:00"
                }
            }
        }
    }