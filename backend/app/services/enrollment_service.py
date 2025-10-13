from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.models.enrollment import Enrollment as EnrollmentModel
from app.models.course_class import CourseClass as CourseClassModel
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate, Enrollment


def get_enrollments_by_student_id(db: Session, student_id: int):
    return db.query(EnrollmentModel).filter(EnrollmentModel.student_id == student_id).options(
        joinedload(EnrollmentModel.course_class).joinedload(CourseClassModel.course),
        joinedload(EnrollmentModel.course_class).joinedload(CourseClassModel.teacher)
    ).all()

def get_enrollments_by_course_class_id(db: Session, course_class_id: int):
    return db.query(EnrollmentModel).filter(EnrollmentModel.course_class_id == course_class_id).options(
        joinedload(EnrollmentModel.student),
        joinedload(EnrollmentModel.course_class).joinedload(CourseClassModel.course),
        joinedload(EnrollmentModel.course_class).joinedload(CourseClassModel.teacher)
    ).all()

def create_enrollment(db: Session, payload: EnrollmentCreate):
    new_enrollment = EnrollmentModel(**payload.dict())
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    
    # Increment the current_students count for the course class
    increment_course_class_students(db, new_enrollment.course_class_id)
    
    return new_enrollment

def update_enrollment(db: Session, enrollment_id: int, payload: EnrollmentUpdate):
    enrollment = db.query(EnrollmentModel).filter(EnrollmentModel.enrollment_id == enrollment_id).first()
    if not enrollment:
        return None
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(enrollment, key, value)
    enrollment.updated_at = func.now()
    db.commit()
    db.refresh(enrollment)
    return enrollment

def delete_enrollment(db: Session, enrollment_id: int):
    enrollment = db.query(EnrollmentModel).filter(EnrollmentModel.enrollment_id == enrollment_id).first()
    if not enrollment:
        return None
    
    course_class_id = enrollment.course_class_id
    db.delete(enrollment)
    db.commit()
    
    # Decrement the current_students count for the course class
    decrement_course_class_students(db, course_class_id)
    
    return True

def increment_course_class_students(db: Session, course_class_id: int):
    """Increment the current_students count for a course class by 1"""
    course_class = db.query(CourseClassModel).filter(CourseClassModel.course_class_id == course_class_id).first()
    if not course_class:
        return None
    course_class.current_students += 1
    course_class.updated_at = func.now()
    db.commit()
    db.refresh(course_class)
    return course_class

def decrement_course_class_students(db: Session, course_class_id: int):
    """Decrement the current_students count for a course class by 1"""
    course_class = db.query(CourseClassModel).filter(CourseClassModel.course_class_id == course_class_id).first()
    if not course_class:
        return None
    if course_class.current_students > 0:
        course_class.current_students -= 1
        course_class.updated_at = func.now()
        db.commit()
        db.refresh(course_class)
    return course_class