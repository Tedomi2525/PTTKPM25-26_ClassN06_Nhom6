from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
import app.models.semester as models
import app.schemas.semester as schemas

router = APIRouter(
    prefix="/semesters",
    tags=["semesters"]
)

@router.get("/", response_model=List[schemas.Semester])
def get_semesters(db: Session = Depends(get_db)):
    return db.query(models.Semester).all()

@router.get("/{semester_id}", response_model=schemas.Semester)
def get_semester(semester_id: int, db: Session = Depends(get_db)):
    semester = db.query(models.Semester).filter(models.Semester.semester_id == semester_id).first()
    if not semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    return semester

@router.post("/", response_model=schemas.Semester)
def create_semester(semester: schemas.SemesterCreate, db: Session = Depends(get_db)):
    new_semester = models.Semester(**semester.dict())
    db.add(new_semester)
    db.commit()
    db.refresh(new_semester)
    return new_semester

@router.put("/{semester_id}", response_model=schemas.Semester)
def update_semester(semester_id: int, semester_update: schemas.SemesterUpdate, db: Session = Depends(get_db)):
    semester = db.query(models.Semester).filter(models.Semester.semester_id == semester_id).first()
    if not semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    
    for key, value in semester_update.dict().items():
        setattr(semester, key, value)
    
    db.commit()
    db.refresh(semester)
    return semester

@router.delete("/{semester_id}")
def delete_semester(semester_id: int, db: Session = Depends(get_db)):
    semester = db.query(models.Semester).filter(models.Semester.semester_id == semester_id).first()
    if not semester:
        raise HTTPException(status_code=404, detail="Semester not found")
    db.delete(semester)
    db.commit()
    return {"detail": "Semester deleted successfully"}
