from sqlalchemy.orm import Session
from datetime import datetime
from app.models.semester import Semester


def get_all_semesters(db: Session):
    return db.query(Semester).all()

def get_semester_by_id(db: Session, semester_id: int):
    return db.query(Semester).filter(Semester.semester_id == semester_id).first()

def get_semester_by_name(db: Session, semester_name: str):
    return db.query(Semester).filter(Semester.semester_name == semester_name).first()


def create_semester(db: Session, semester_name: str, start_time: datetime, end_time: datetime):
    new_semester = Semester(
        semester_name=semester_name,
        start_time=start_time,
        end_time=end_time,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_semester)
    db.commit()
    db.refresh(new_semester)
    return new_semester

def update_semester(db: Session, semester_id: int, semester_name: str = None, start_time: datetime = None, end_time: datetime = None):
    semester = db.query(Semester).filter(Semester.semester_id == semester_id).first()
    if not semester:
        return None
    
    if semester_name:
        semester.semester_name = semester_name
    if start_time:
        semester.start_time = start_time
    if end_time:
        semester.end_time = end_time
    
    semester.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(semester)
    return semester

def delete_semester(db: Session, semester_id: int):
    semester = db.query(Semester).filter(Semester.semester_id == semester_id).first()
    if not semester:
        return None
    db.delete(semester)
    db.commit()
    return semester
