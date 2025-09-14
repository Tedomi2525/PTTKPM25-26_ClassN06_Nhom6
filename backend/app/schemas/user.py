from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., max_length=100, description="Username")
    school_email: Optional[EmailStr] = Field(None, max_length=150, description="User school email",alias="schoolEmail")
    role: str = Field(..., description="User role", pattern="^(admin|teacher|student)$")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=255, description="User password")

class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=8, max_length=255, description="User password")
    
class User(UserBase):
    user_id: int = Field(..., alias="userId")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    class Config:
        from_attributes = True
        populate_by_name = True
