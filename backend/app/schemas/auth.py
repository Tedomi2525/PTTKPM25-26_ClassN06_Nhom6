from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    username: str = Field(..., max_length=100)
    password: str
class UserCreate(BaseModel):
    username: str = Field(..., max_length=100)
    password: str
    full_name: str | None = Field(None, max_length=100)
class Token(BaseModel):
    access_token: str
    token_type: str
class UserOut(BaseModel):
    id: int
    username: str = Field(..., max_length=100)
    full_name: str | None = Field(None, max_length=100)
    disabled: bool | None = None
    class Config:
        orm_mode = True
