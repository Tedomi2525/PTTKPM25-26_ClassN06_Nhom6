from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.enrollment import Enrollment, EnrollmentCreate, EnrollmentUpdate as EnrollmentUpdate
from app.database import SessionLocal, get_db
from app.services import enrollment_service

router = APIRouter()

@router.get("/enrollments", response_model=list[Enrollment])
def get_enrollments_by_student_id(student_id: int, db: Session = Depends(get_db)):
    return enrollment_service.get_enrollments_by_student_id(db, student_id)

@router.post("/enrollments", response_model=Enrollment)
def create_enrollment(payload: EnrollmentCreate, db: Session = Depends(get_db)):
    try:
        return enrollment_service.create_enrollment(db, payload)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in create_enrollment endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.put("/enrollments/{enrollment_id}", response_model=Enrollment)
def update_enrollment(enrollment_id: int, payload: EnrollmentUpdate, db: Session = Depends(get_db)):
    db_enrollment = enrollment_service.update_enrollment(db, enrollment_id, payload)
    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return db_enrollment

@router.delete("/enrollments/{enrollment_id}", response_model=dict)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    success = enrollment_service.delete_enrollment(db, enrollment_id)
    if success is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    if not success:
        raise HTTPException(status_code=400, detail="Cannot delete enrollment due to existing references")
    return {"detail": "Enrollment deleted successfully"}

@router.get("/enrollments/course-class/{course_class_id}", response_model=list[Enrollment])
def get_enrollments_by_course_class_id(course_class_id: int, db: Session = Depends(get_db)):
    return enrollment_service.get_enrollments_by_course_class_id(db, course_class_id)