from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import User, Student, Teacher
from app.schemas.auth import LoginRequest, UserPasswordUpdate
from datetime import timedelta
from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.core.security import get_password_hash
from jose import jwt, JWTError

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        return None
    return user

def login_service(db: Session, request: LoginRequest):
    user = authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai username hoặc password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def update_user_password(db: Session, user_id: int, payload: UserPasswordUpdate):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None
    user.password = get_password_hash(payload.password)
    db.commit()
    db.refresh(user)
    return user 

def get_current_user_service(db: Session, token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Không thể xác thực người dùng",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise credentials_exception

    student = db.query(Student).filter(Student.user_id == user.user_id).first()
    if student:
        full_name = f"{student.first_name} {student.last_name}".strip()
    else:
        teacher = db.query(Teacher).filter(Teacher.user_id == user.user_id).first()
        if teacher:
            full_name = f"{teacher.first_name} {teacher.last_name}".strip()
        else:
            full_name = user.username

    return {
        "user_id": user.user_id,
        "student_id": student.student_id if student else None,
        "teacher_id": teacher.teacher_id if not student and teacher else None,
        "username": user.username,
        "full_name": full_name,
        "role": user.role,
        "disabled": False
    }