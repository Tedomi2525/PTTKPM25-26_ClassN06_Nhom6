from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import LoginRequest, Token, UserOut, UserPasswordUpdate
from app.services import auth_service
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter()

@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login_service(db, request)

@router.get("/me", response_model=UserOut)
def read_users_me(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return auth_service.get_current_user_service(db, token)

@router.put("/change-password", response_model=UserOut)
def change_password(payload: UserPasswordUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = auth_service.get_current_user_service(db, token)
    updated_user = auth_service.update_user_password(db, current_user.user_id, payload)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Password updated successfully"}