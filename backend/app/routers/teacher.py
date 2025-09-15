from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.teacher import TeacherCreate, TeacherUpdate, Teacher as TeacherSchema
from app.database import SessionLocal, get_db
from app.services import teacher_service

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
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

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
