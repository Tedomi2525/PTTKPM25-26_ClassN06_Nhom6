from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from sqlalchemy.exc import IntegrityError

from app.models.teacher import Teacher as TeacherModel
from app.models.user import User as UserModel
from app.schemas.teacher import TeacherCreate, TeacherUpdate
from app.schemas.user import UserCreate

from passlib.context import CryptContext

def generate_teacher_code(db: Session) -> str:
    # Lấy teacher_code lớn nhất trong DB
    last_teacher = (
        db.query(TeacherModel)
        .order_by(TeacherModel.teacher_id.desc())
        .first()
    ) 
    if not last_teacher or not last_teacher.teacher_code:
        new_number = 1
    else:
        # Bóc số từ teacher_code, ví dụ GV000123 -> 123
        last_number = int(last_teacher.teacher_code.replace("GV", ""))
        new_number = last_number + 1

    return f"GV{new_number:06d}"  # padding 6 chữ số

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def get_teachers(db: Session):
    return db.query(TeacherModel).all()


def search_teachers(db: Session, q: str):
    return db.query(TeacherModel).filter(
        or_(
            func.lower(TeacherModel.first_name).like(func.lower(f"%{q}%")),
            func.lower(TeacherModel.last_name).like(func.lower(f"%{q}%")),
            func.lower(TeacherModel.email).like(func.lower(f"%{q}%")),
            func.lower(TeacherModel.teacher_code).like(func.lower(f"%{q}%"))
        ) 
    ).all()


def create_teacher(db: Session, teacher_payload: TeacherCreate):
    # 1. Sinh teacher_code
    teacher_code = generate_teacher_code(db)

    # 2. Tạo user trước
    user_payload = UserCreate(
        username=teacher_code,
        school_email=f"{teacher_code}@edunera.edu",
        password=get_password_hash(f"{teacher_code}@"),  # Mặc định password là 123456
        role="teacher"
    )

    # dict(by_alias=False) để lấy đúng field trong model
    new_user = UserModel(**user_payload.dict(by_alias=False))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 3. Tạo teacher, gán user_id
    teacher_data = teacher_payload.dict(by_alias=False)
    teacher_data["teacher_code"] = teacher_code
    teacher_data["user_id"] = new_user.user_id

    new_teacher = TeacherModel(**teacher_data)
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    return new_teacher


def update_teacher(db: Session, teacher_id: int, payload: TeacherUpdate):
    teacher = db.query(TeacherModel).filter(TeacherModel.teacher_id == teacher_id).first()
    if not teacher:
        return None

    for key, value in payload.dict(exclude_unset=True, by_alias=False).items():
        setattr(teacher, key, value)

    db.commit()
    db.refresh(teacher)
    return teacher


def delete_teacher(db: Session, teacher_id: int):
    teacher = db.query(TeacherModel).filter(TeacherModel.teacher_id == teacher_id).first()
    if not teacher:
        return None
    try:
        teacher.status = "inactive"
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        return False
