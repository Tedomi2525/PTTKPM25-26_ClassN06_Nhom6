from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserUpdate
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

def update_user(db: Session, user_id: int, payload: UserUpdate):
    user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not user:
        return None
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
# def delete_user(db: Session, user_id: int):
#     user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
#     if not user:
#         return None
#     try:
#         db.delete(user)
#         db.commit()
#         return True
#     except IntegrityError:
#         db.rollback()
#         return False