from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    username: str = Field(..., max_length=100, description="Username for login")
    password: str = Field(..., description="Password for login")
    
    class Config:
        populate_by_name = True

class UserCreate(BaseModel):
    username: str = Field(..., max_length=100, description="Username for the new user")
    password: str = Field(..., description="Password for the new user")
    full_name: Optional[str] = Field(None, alias="fullName", max_length=100, description="Full name of the user")
    
    class Config:
        populate_by_name = True

class Token(BaseModel):
    access_token: str = Field(..., alias="accessToken", description="JWT access token")
    token_type: str = Field(..., alias="tokenType", description="Type of token")
    
    class Config:
        populate_by_name = True

class UserOut(BaseModel):
    id: int = Field(..., description="User ID")
    username: str = Field(..., max_length=100, description="Username")
    full_name: Optional[str] = Field(None, alias="fullName", max_length=100, description="Full name of the user")
    disabled: Optional[bool] = Field(None, description="Whether the user is disabled")
    
    class Config:
        from_attributes = True
        populate_by_name = True
