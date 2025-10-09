from sqlalchemy.orm import Session, joinedload
from app.models.course_class import CourseClass
from app.schemas.course_class import CourseClassCreate, CourseClassUpdate

def create_course_class(db: Session, course_class: CourseClassCreate):
    db_course_class = CourseClass(
        course_id=course_class.course_id,
        teacher_id=course_class.teacher_id,
        section=course_class.section,
        max_students=course_class.max_students,
        min_students=course_class.min_students,
    )
    db.add(db_course_class)
    db.commit()
    db.refresh(db_course_class)
    # Load relationships
    return get_course_class(db, db_course_class.course_class_id)

def get_course_class(db: Session, course_class_id: int):
    return db.query(CourseClass)\
        .options(joinedload(CourseClass.course), joinedload(CourseClass.teacher))\
        .filter(CourseClass.course_class_id == course_class_id)\
        .first()

def get_course_classes_by_course_id(db: Session, course_id: int):
    return db.query(CourseClass)\
        .options(joinedload(CourseClass.course), joinedload(CourseClass.teacher))\
        .filter(CourseClass.course_id == course_id)\
        .all()

def get_course_classes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CourseClass)\
        .options(joinedload(CourseClass.course), joinedload(CourseClass.teacher))\
        .offset(skip)\
        .limit(limit)\
        .all()

def update_course_class(db: Session, course_class_id: int, course_class: CourseClassUpdate):
    db_course_class = db.query(CourseClass).filter(CourseClass.course_class_id == course_class_id).first()
    if not db_course_class:
        return None
    if course_class.course_id is not None:
        db_course_class.course_id = course_class.course_id
    if course_class.teacher_id is not None:
        db_course_class.teacher_id = course_class.teacher_id
    if course_class.section is not None:
        db_course_class.section = course_class.section
    if course_class.max_students is not None:
        db_course_class.max_students = course_class.max_students
    if course_class.min_students is not None:
        db_course_class.min_students = course_class.min_students
    db.commit()
    # Reload with relationships
    return get_course_class(db, course_class_id)

def delete_course_class(db: Session, course_class_id: int):
    db_course_class = get_course_class(db, course_class_id)
    if not db_course_class:
        return None
    db.delete(db_course_class)
    db.commit()
    return db_course_class
