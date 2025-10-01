from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.student import StudentCreate, StudentUpdate, Student as StudentSchema
from app.database import SessionLocal, get_db
from app.services import student_service
from typing import Optional

router = APIRouter()

@router.get("/students", response_model=list[StudentSchema])
def get_students(db: Session = Depends(get_db)):
    return student_service.get_students(db)

@router.get("/students/search", response_model=list[StudentSchema])
def search_students(q: str, db: Session = Depends(get_db)):
    return student_service.search_students(db, q)

@router.post("/students", response_model=StudentSchema)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    try:
        return student_service.create_student(db, payload)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in create_student endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.put("/students/{student_id}", response_model=StudentSchema)
def update_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    student = student_service.update_student(db, student_id, payload)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.delete("/students/{student_id}", response_model=dict)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    success = student_service.delete_student(db, student_id)
    if success is None:
        raise HTTPException(status_code=404, detail="Student not found")
    if not success:
        raise HTTPException(status_code=400, detail="Cannot delete student due to existing references")
    return {"detail": "Student deleted successfully"}

@router.get("/students/weekly-schedule")
def get_student_weekly_schedule(
    student_id: int,
    sunday_date: str = Query(..., description="Ngày chủ nhật của tuần (DD/MM/YYYY hoặc YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Lấy lịch học của sinh viên trong tuần cụ thể
    - student_id: ID của sinh viên (required)
    - sunday_date: Ngày chủ nhật của tuần, ví dụ: 21/09/2025 hoặc 2025-09-21
    """
    try:
        result = student_service.get_student_weekly_schedule(db, student_id, sunday_date)
        
        if result is None:
            raise HTTPException(status_code=404, detail="Student not found")
            
        return {
            "success": True,
            "data": result
        }
        
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get student weekly schedule: {str(e)}")
