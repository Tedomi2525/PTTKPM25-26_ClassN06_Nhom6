from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.enrollment import Enrollment as EnrollmentModel
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate, Enrollment


def get_enrollments_by_student_id(db: Session, student_id: int):
    return db.query(EnrollmentModel).filter(EnrollmentModel.student_id == student_id).all()

def create_enrollment(db: Session, payload: EnrollmentCreate):
    new_enrollment = EnrollmentModel(**payload.dict())
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
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
    db.delete(enrollment)
    db.commit()
    return True