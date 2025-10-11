from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.course_class import CourseClassCreate, CourseClassUpdate, CourseClassResponse
from app.services import course_class_service

router = APIRouter()

@router.post("/course_classes", response_model=CourseClassResponse)
def create_course_class(course_class: CourseClassCreate, db: Session = Depends(get_db)):
    return course_class_service.create_course_class(db, course_class)

@router.get("/course_classes", response_model=List[CourseClassResponse])
def get_course_classes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return course_class_service.get_course_classes(db, skip=skip, limit=limit)

@router.get("/course_classes/{course_class_id}", response_model=CourseClassResponse)
def get_course_class(course_class_id: int, db: Session = Depends(get_db)):
    db_course_class = course_class_service.get_course_class(db, course_class_id)
    if not db_course_class:
        raise HTTPException(status_code=404, detail="CourseClass not found")
    return db_course_class

@router.get("/by_course/{course_id}", response_model=List[CourseClassResponse])
def get_course_classes_by_course_id(course_id: int, db: Session = Depends(get_db)):
    return course_class_service.get_course_classes_by_course_id(db, course_id)

@router.put("/course_classes/{course_class_id}", response_model=CourseClassResponse)
def update_course_class(course_class_id: int, course_class: CourseClassUpdate, db: Session = Depends(get_db)):
    db_course_class = course_class_service.update_course_class(db, course_class_id, course_class)
    if not db_course_class:
        raise HTTPException(status_code=404, detail="CourseClass not found")
    return db_course_class

@router.delete("/course_classes/{course_class_id}")
def delete_course_class(course_class_id: int, db: Session = Depends(get_db)):
    db_course_class = course_class_service.delete_course_class(db, course_class_id)
    if not db_course_class:
        raise HTTPException(status_code=404, detail="CourseClass not found")
    return {"detail": "CourseClass deleted successfully"}

@router.get("/by_program/{program_id}", response_model=List[CourseClassResponse])
def get_course_classes_by_program_id(program_id: int, student_id: int = None, db: Session = Depends(get_db)):
    return course_class_service.get_course_classes_by_program_id(db, program_id, student_id)