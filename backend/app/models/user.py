"""
User model for MongoDB.
Defines the structure of user documents in the database.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId


class User(BaseModel):
    """
    User model representing a user in the database.
    """
    id: Optional[str] = Field(default=None, alias="_id")
    full_name: str = Field(..., description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    hashed_password: str = Field(..., description="Hashed password using bcrypt")
    role: str = Field(default="user", description="User role: admin or user")
    is_active: bool = Field(default=True, description="Whether the user account is active")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = {
        "populate_by_name": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "full_name": "Sahzad Alam",
                "email": "sahzad@example.com",
                "role": "admin",
                "is_active": True
            }
        }
    }


class UserInDB(User):
    """
    User model as stored in the database.
    Includes all fields including hashed password.
    """
    pass


class UserResponse(BaseModel):
    """
    User response model (excludes sensitive data).
    """
    id: str = Field(..., description="User ID")
    full_name: str = Field(..., description="User's full name")
    email: str = Field(..., description="User's email address")
    role: str = Field(..., description="User role")
    is_active: bool = Field(..., description="Whether the user account is active")
    created_at: datetime = Field(..., description="Account creation timestamp")
    
    model_config = {
        "from_attributes": True,
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