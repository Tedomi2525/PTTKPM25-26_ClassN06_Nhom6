from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.program_course import ProgramCourse
from app.models.program import Program
from app.models.course import Course
from app.schemas.program_course import (
    ProgramCourseCreate, 
    ProgramCourseUpdate, 
    ProgramCourseResponse,
    ProgramCourseWithDetails
)

router = APIRouter(
    prefix="/program-courses",
    tags=["program-courses"]
)

@router.post("/", response_model=ProgramCourseResponse, status_code=status.HTTP_201_CREATED)
def create_program_course(
    program_course: ProgramCourseCreate,
    db: Session = Depends(get_db)
):
    """Create a new program course relationship"""
    
    # Verify program exists
    program = db.query(Program).filter(Program.program_id == program_course.program_id).first()
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program not found"
        )
    
    # Verify course exists
    course = db.query(Course).filter(Course.course_id == program_course.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if the combination already exists
    existing = db.query(ProgramCourse).filter(
        ProgramCourse.program_id == program_course.program_id,
        ProgramCourse.course_id == program_course.course_id,
        ProgramCourse.semester_no == program_course.semester_no
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This program-course-semester combination already exists"
        )
    
    db_program_course = ProgramCourse(**program_course.dict())
    db.add(db_program_course)
    db.commit()
    db.refresh(db_program_course)
    
    return db_program_course

@router.get("/", response_model=List[ProgramCourseWithDetails])
def get_program_courses(
    program_id: int = None,
    semester_no: str = None,  # Changed from int to str
    is_required: bool = None,
    db: Session = Depends(get_db)
):
    """Get program courses with optional filters"""
    
    query = db.query(ProgramCourse).join(Course).join(Program)
    
    if program_id:
        query = query.filter(ProgramCourse.program_id == program_id)
    if semester_no:
        query = query.filter(ProgramCourse.semester_no == semester_no)
    if is_required is not None:
        query = query.filter(ProgramCourse.is_required == is_required)
    
    program_courses = query.all()
    
    # Transform to include details
    result = []
    for pc in program_courses:
        result.append(ProgramCourseWithDetails(
            program_course_id=pc.program_course_id,
            program_id=pc.program_id,
            course_id=pc.course_id,
            semester_no=pc.semester_no,
            is_required=pc.is_required,
            created_at=pc.created_at,
            updated_at=pc.updated_at,
            course_name=pc.course.name,
            course_code=pc.course.course_code,
            credits=pc.course.credits,
            program_name=pc.program.program_name
        ))
    
    return result

@router.get("/{program_course_id}", response_model=ProgramCourseWithDetails)
def get_program_course(
    program_course_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific program course by ID"""
    
    program_course = db.query(ProgramCourse).join(Course).join(Program).filter(
        ProgramCourse.program_course_id == program_course_id
    ).first()
    
    if not program_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program course not found"
        )
    
    return ProgramCourseWithDetails(
        program_course_id=program_course.program_course_id,
        program_id=program_course.program_id,
        course_id=program_course.course_id,
        semester_no=program_course.semester_no,
        is_required=program_course.is_required,
        created_at=program_course.created_at,
        updated_at=program_course.updated_at,
        course_name=program_course.course.name,
        course_code=program_course.course.course_code,
        credits=program_course.course.credits,
        program_name=program_course.program.program_name
    )

@router.put("/{program_course_id}", response_model=ProgramCourseResponse)
def update_program_course(
    program_course_id: int,
    program_course_update: ProgramCourseUpdate,
    db: Session = Depends(get_db)
):
    """Update a program course"""
    
    db_program_course = db.query(ProgramCourse).filter(
        ProgramCourse.program_course_id == program_course_id
    ).first()
    
    if not db_program_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program course not found"
        )
    
    # Update only provided fields
    update_data = program_course_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_program_course, field, value)
    
    db.commit()
    db.refresh(db_program_course)
    
    return db_program_course

@router.delete("/{program_course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_program_course(
    program_course_id: int,
    db: Session = Depends(get_db)
):
    """Delete a program course"""
    
    db_program_course = db.query(ProgramCourse).filter(
        ProgramCourse.program_course_id == program_course_id
    ).first()
    
    if not db_program_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program course not found"
        )
    
    db.delete(db_program_course)
    db.commit()
    
    return

@router.get("/program/{program_id}/current-semester", response_model=List[ProgramCourseWithDetails])
def get_current_semester_courses(
    program_id: int,
    db: Session = Depends(get_db)
):
    """Get courses for the current semester of a specific program"""
    
    # Verify program exists
    program = db.query(Program).filter(Program.program_id == program_id).first()
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program not found"
        )
    
    # Import here to avoid circular imports
    from backend.app.services.schedule_service import get_current_semester_for_program
    
    current_semester_code = get_current_semester_for_program(db, program_id)
    if not current_semester_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot determine current semester for this program"
        )
    
    # Get courses for current semester
    program_courses = db.query(ProgramCourse).join(Course).join(Program).filter(
        ProgramCourse.program_id == program_id,
        ProgramCourse.semester_no == current_semester_code
    ).all()
    
    # Transform to include details
    result = []
    for pc in program_courses:
        result.append(ProgramCourseWithDetails(
            program_course_id=pc.program_course_id,
            program_id=pc.program_id,
            course_id=pc.course_id,
            semester_no=pc.semester_no,
            is_required=pc.is_required,
            created_at=pc.created_at,
            updated_at=pc.updated_at,
            course_name=pc.course.name,
            course_code=pc.course.course_code,
            credits=pc.course.credits,
            program_name=pc.program.program_name
        ))
    
    return result