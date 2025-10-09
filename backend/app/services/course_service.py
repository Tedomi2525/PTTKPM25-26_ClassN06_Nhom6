from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate

def create_course(db: Session, course: CourseCreate):
    db_course = Course(
        course_code=course.course_code,
        name=course.name,
        credits=course.credits,
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_course(db: Session, course_id: int):
    return db.query(Course).filter(Course.course_id == course_id).first()

# def get_courses(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(Course).offset(skip).limit(limit).all()

def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Course)
        .filter(Course.is_deleted == False)   # chỉ lấy course chưa bị xóa
        .offset(skip)
        .limit(limit)
        .all()
    )

def update_course(db: Session, course_id: int, course: CourseUpdate):
    db_course = get_course(db, course_id)
    if not db_course:
        return None
    if course.name is not None:
        db_course.name = course.name
    if course.credits is not None:
        db_course.credits = course.credits
    db.commit()
    db.refresh(db_course)
    return db_course

def delete_course(db: Session, course_id: int):
    db_course = get_course(db, course_id)
    if not db_course:
        return None
    
    # Xóa mềm
    db_course.is_deleted = True
    db.commit()
    db.refresh(db_course)
    return db_course

# Lấy các course đã ẩn
def get_deleted_courses(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Course)
        .filter(Course.is_deleted == True)
        .offset(skip)
        .limit(limit)
        .all()
    )

def restore_course(db: Session, course_id: int):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        return None
    course.is_deleted = False   # phục hồi
    db.commit()
    db.refresh(course)
    return course

