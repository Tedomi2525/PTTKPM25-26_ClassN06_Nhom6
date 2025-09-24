from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., max_length=100, description="Username")
    email: Optional[EmailStr] = Field(None, alias="email", max_length=150, description="User email")
    role: str = Field(..., description="User role", pattern="^(admin|teacher|student)$")
    
    class Config:
        populate_by_name = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=255, description="User password")

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=100, description="Username")
    email: Optional[EmailStr] = Field(None, alias="email", max_length=150, description="User email")
    role: Optional[str] = Field(None, description="User role", pattern="^(admin|teacher|student)$")
    password: Optional[str] = Field(None, min_length=8, max_length=255, description="User password")
    
    class Config:
        populate_by_name = True
    
class User(UserBase):
    user_id: int = Field(..., alias="userId", description="User ID")
    created_at: datetime = Field(..., alias="createdAt", description="Creation timestamp")
    updated_at: datetime = Field(..., alias="updatedAt", description="Last update timestamp")

    class Config:
        from_attributes = True
        populate_by_name = True
