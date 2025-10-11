from sqlalchemy.orm import Session, joinedload
from app.models.course_class import CourseClass
from app.schemas.course_class import CourseClassCreate, CourseClassUpdate
from app.models.program import Program
from app.models.course import Course
from app.models.program_course import ProgramCourse
from app.models.enrollment import Enrollment

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

def get_course_classes_by_program_id(db: Session, program_id: int, student_id: int = None):
    
    # First get the program's current semester
    program = db.query(Program).filter(Program.program_id == program_id).first()
    if not program:
        return []
    
    current_sem = program.current_semester
    
    # Get course classes where the course's semester_no in ProgramCourse matches current_semester
    query = db.query(CourseClass)\
        .options(joinedload(CourseClass.course), joinedload(CourseClass.teacher))\
        .join(Course, CourseClass.course_id == Course.course_id)\
        .join(ProgramCourse, ProgramCourse.course_id == Course.course_id)\
        .filter(ProgramCourse.program_id == program_id)\
        .filter(ProgramCourse.semester_no == current_sem)
    
    # If student_id is provided, exclude all course classes of courses that the student has already enrolled in
    if student_id is not None:
        # Subquery to get course_ids that the student has enrolled in (via any course_class)
        enrolled_course_ids = db.query(CourseClass.course_id)\
            .join(Enrollment, Enrollment.course_class_id == CourseClass.course_class_id)\
            .filter(Enrollment.student_id == student_id)\
            .subquery()
        
        # Exclude all course classes with those course_ids
        query = query.filter(~CourseClass.course_id.in_(enrolled_course_ids))
    
    return query.all()