from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.services import course_service

router = APIRouter()

@router.post("/course", response_model=CourseResponse)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    return course_service.create_course(db, course)

@router.get("/courses", response_model=List[CourseResponse])
def get_all_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return course_service.get_courses(db, skip=skip, limit=limit)

@router.get("/course/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    db_course = course_service.get_course(db, course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@router.put("/course/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    db_course = course_service.update_course(db, course_id, course)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@router.delete("/course/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = course_service.delete_course(db, course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"detail": "Course hidden successfully"}

# Lấy các course đã ẩn
@router.get("/courses/deleted", response_model=List[CourseResponse])
def get_deleted_courses(db: Session = Depends(get_db)):
    return course_service.get_deleted_courses(db)

# Ẩn course (soft delete)
@router.put("/course/{course_id}/hide", response_model=CourseResponse)
def hide_course(course_id: int, db: Session = Depends(get_db)):
    course = course_service.delete_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# Khôi phục course
@router.put("/course/{course_id}/restore", response_model=CourseResponse)
def restore_course(course_id: int, db: Session = Depends(get_db)):
    course = course_service.restore_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
