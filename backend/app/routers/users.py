from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate, User as UserSchema
from app.database import SessionLocal
from app.services import user_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users", response_model=list[UserSchema])
def get_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)

@router.get("/users/search", response_model=list[UserSchema])
def search_users(q: str, db: Session = Depends(get_db)):
    return user_service.search_users(db, q)

@router.post("/users", response_model=UserSchema)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, payload)

@router.put("/users/{user_id}", response_model=UserSchema)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = user_service.update_user(db, user_id, payload)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# @router.delete("/users/{user_id}", response_model=dict)
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     success = user_service.delete_user(db, user_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="User not found")
#     return {"detail": "User deleted successfully"}