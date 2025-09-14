from pydantic import BaseModel
class LoginRequest(BaseModel):
    username: str
    password: str
class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str | None = None
class Token(BaseModel):
    access_token: str
    token_type: str
class UserOut(BaseModel):
    id: int
    username: str
    full_name: str | None = None
    disabled: bool | None = None
    class Config:
        orm_mode = True
