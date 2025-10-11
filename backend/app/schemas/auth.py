from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    username: str = Field(..., max_length=100, description="Username for login")
    password: str = Field(..., description="Password for login")
    
    class Config:
        populate_by_name = True

class Token(BaseModel):
    access_token: str = Field(..., alias="accessToken", description="JWT access token")
    token_type: str = Field(..., alias="tokenType", description="Type of token")
    
    class Config:
        populate_by_name = True

class UserOut(BaseModel):
    user_id: int = Field(..., description="User ID")
    username: str = Field(..., max_length=100, description="Username")
    full_name: Optional[str] = Field(
        None, alias="fullName", max_length=100, description="Full name of the user"
    )
    disabled: Optional[bool] = Field(None, description="Whether the user is disabled")
    role: str = Field(..., description="Role of the user (e.g., admin, teacher, student)")
    school_id: Optional[int] = Field(
        None, alias="schoolId", description="School ID (student_id or teacher_id)"
    )
    avatar: Optional[str] = Field(None, description="Avatar URL of the user")

    class Config:
        from_attributes = True
        populate_by_name = True

class UserPasswordUpdate(BaseModel):
    current_password: str = Field(
        ...,
        alias="currentPassword",
        description="Current user password for verification"
    )
    new_password: str = Field(
        ...,
        alias="newPassword",
        min_length=8,
        max_length=255,
        description="New user password"
    )
    confirm_password: str = Field(
        ...,
        alias="confirmPassword",
        min_length=8,
        max_length=255,
        description="Confirm new password"
    )
    
    class Config:
        populate_by_name = True

class MessageResponse(BaseModel):
    message: str = Field(..., description="Response message")