from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from sqlalchemy.exc import IntegrityError

from app.models.student import Student as StudentModel
from app.models.user import User as UserModel
from app.schemas.student import StudentCreate, StudentUpdate
from app.schemas.user import UserCreate

from app.core.security import get_password_hash

def generate_student_code(db: Session) -> str:
    # Lấy student_code lớn nhất trong DB
    last_student = (
        db.query(StudentModel)
        .order_by(StudentModel.student_id.desc())
        .first()
    ) 
    if not last_student or not last_student.student_code:
        new_number = 1
    else:
        # Bóc số từ student_code, ví dụ SV000123 -> 123
        last_number = int(last_student.student_code.replace("SV", ""))
        new_number = last_number + 1

    return f"SV{new_number:06d}"  # padding 6 chữ số

def get_students(db: Session):
    return db.query(StudentModel).all()

def search_students(db: Session, q: str):
    return db.query(StudentModel).filter(
        or_(
            func.lower(StudentModel.first_name).like(func.lower(f"%{q}%")),
            func.lower(StudentModel.last_name).like(func.lower(f"%{q}%")),
            func.lower(StudentModel.email).like(func.lower(f"%{q}%")),
            func.lower(StudentModel.student_code).like(func.lower(f"%{q}%"))
        ) 
    ).all()

def create_student(db: Session, student_payload: StudentCreate):
    try:
        # 1. Sinh student_code
        student_code = generate_student_code(db)

        # 2. Tạo user trước
        user_payload = UserCreate(
            username=student_code,
            school_email=f"{student_code}@edunera.edu",
            password=get_password_hash(f"{student_code}@"),
            role="student"
        )

        # Sử dụng model_dump() thay vì dict() cho Pydantic v2
        user_data = user_payload.model_dump(by_alias=False)
        new_user = UserModel(**user_data)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # 3. Tạo student, gán user_id - xử lý các field đặc biệt
        student_data = student_payload.model_dump(by_alias=False, exclude_unset=True)
        student_data["student_code"] = student_code
        student_data["user_id"] = new_user.user_id
        
        # Xử lý field class_name nếu có
        if "class_name" in student_data and student_data["class_name"] is None:
            student_data.pop("class_name")

        new_student = StudentModel(**student_data)
        db.add(new_student)
        db.commit()
        db.refresh(new_student)

        return new_student
    
    except Exception as e:
        db.rollback()
        print(f"Error creating student: {e}")
        print(f"Student payload: {student_payload}")
        print(f"Student data: {student_data if 'student_data' in locals() else 'Not created yet'}")
        raise e
    
def update_student(db: Session, student_id: int, payload: StudentUpdate):
    student = db.query(StudentModel).filter(StudentModel.student_id == student_id).first()
    if not student:
        return None

    for key, value in payload.dict(exclude_unset=True, by_alias=False).items():
        setattr(student, key, value)

    try:
        db.commit()
        db.refresh(student)
        return student
    except IntegrityError as e:
        db.rollback()
        print(f"Integrity error updating student: {e}")
        return None
    except Exception as e:
        db.rollback()
        print(f"Error updating student: {e}")
        return None
    
def delete_student(db: Session, student_id: int):
    student = db.query(StudentModel).filter(StudentModel.student_id == student_id).first()
    if not student:
        return None
    try:
        db.delete(student)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        return False