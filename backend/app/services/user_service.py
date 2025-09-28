from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from app.models.user import User as UserModel
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from sqlalchemy import func

def get_users(db: Session):
    return db.query(UserModel).all()

def search_users(db: Session, q: str):
    return db.query(UserModel).filter(
        or_(
            func.lower(UserModel.username).like(func.lower(f"%{q}%")),
            func.lower(UserModel.email).like(func.lower(f"%{q}%"))
        )
    ).all()
    
def create_user(db: Session, payload: UserCreate):
    new_user = UserModel(**payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user