from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.teacher import TeacherCreate, TeacherUpdate, Teacher as TeacherSchema
from app.database import SessionLocal, get_db
from app.services import teacher_service
from typing import Optional

router = APIRouter()
        
@router.get("/teachers", response_model=list[TeacherSchema])
def get_teachers(db: Session = Depends(get_db)):
    return teacher_service.get_teachers(db)

@router.get("/teachers/search", response_model=list[TeacherSchema])
def search_teachers(q: str, db: Session = Depends(get_db)):
    return teacher_service.search_teachers(db, q)

@router.post("/teachers", response_model=TeacherSchema)
def create_teacher(payload: TeacherCreate, db: Session = Depends(get_db)):
    try:
        return teacher_service.create_teacher(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/teachers/weekly-schedule")
def get_teacher_weekly_schedule(
    teacher_id: int,
    sunday_date: str = Query(..., description="Ngày chủ nhật của tuần (DD/MM/YYYY hoặc YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Lấy lịch giảng dạy của giáo viên trong tuần cụ thể
    - teacher_id: ID của giáo viên (required)
    - sunday_date: Ngày chủ nhật của tuần, ví dụ: 21/09/2025 hoặc 2025-09-21
    """
    try:
        result = teacher_service.get_teacher_weekly_schedule(db, teacher_id, sunday_date)
        
        if result is None:
            raise HTTPException(status_code=404, detail="Teacher not found")
            
        return {
            "success": True,
            "data": result
        }
        
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get teacher weekly schedule: {str(e)}")

@router.get("/teachers/{teacher_id}", response_model=TeacherSchema)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = teacher_service.get_teacher_by_id(db, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@router.put("/teachers/{teacher_id}", response_model=TeacherSchema)
def update_teacher(teacher_id: int, payload: TeacherUpdate, db: Session = Depends
(get_db)):
    teacher = teacher_service.update_teacher(db, teacher_id, payload)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@router.delete("/teachers/{teacher_id}", response_model=dict)
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    success = teacher_service.delete_teacher(db, teacher_id)
    if success is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    if not success:
        raise HTTPException(status_code=400, detail="Cannot delete teacher due to existing references")
    return {"detail": "Teacher deleted successfully"}
@router.get("/teachers/{teacher_id}/school")
def get_teacher_school(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(TeacherSchema).filter(TeacherSchema.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {"school_id": teacher.teacher_id}