from sqlalchemy.orm import Session
from app.models.course_class import CourseClass
from app.schemas.course_class import CourseClassCreate, CourseClassUpdate

def create_course_class(db: Session, course_class: CourseClassCreate):
    db_course_class = CourseClass(
        course_id=course_class.course_id,
        teacher_id=course_class.teacher_id,
        semester=course_class.semester,
        year=course_class.year,
        section=course_class.section,
    )
    db.add(db_course_class)
    db.commit()
    db.refresh(db_course_class)
    return db_course_class

def get_course_class(db: Session, course_class_id: int):
    return db.query(CourseClass).filter(CourseClass.course_class_id == course_class_id).first()

def get_course_classes_by_course_id(db: Session, course_id: int):
    return db.query(CourseClass).filter(CourseClass.course_id == course_id).all()

def get_course_classes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CourseClass)\
        .join(CourseClass.course)\
        .join(CourseClass.teacher)\
        .offset(skip)\
        .limit(limit)\
        .all()

def update_course_class(db: Session, course_class_id: int, course_class: CourseClassUpdate):
    db_course_class = get_course_class(db, course_class_id)
    if not db_course_class:
        return None
    if course_class.teacher_id is not None:
        db_course_class.teacher_id = course_class.teacher_id
    if course_class.semester is not None:
        db_course_class.semester = course_class.semester
    if course_class.year is not None:
        db_course_class.year = course_class.year
    if course_class.section is not None:
        db_course_class.section = course_class.section
    db.commit()
    db.refresh(db_course_class)
    return db_course_class

def delete_course_class(db: Session, course_class_id: int):
    db_course_class = get_course_class(db, course_class_id)
    if not db_course_class:
        return None
    db.delete(db_course_class)
    db.commit()
    return db_course_class
