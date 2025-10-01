from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, User as UserSchema
from app.database import SessionLocal, get_db
from app.services import user_service

router = APIRouter()

@router.get("/users", response_model=list[UserSchema])
def get_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)

@router.get("/users/search", response_model=list[UserSchema])
def search_users(q: str, db: Session = Depends(get_db)):
    return user_service.search_users(db, q)

@router.post("/users", response_model=UserSchema)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, payload)