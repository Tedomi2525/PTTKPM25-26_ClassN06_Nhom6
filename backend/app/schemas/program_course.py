from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProgramCourseBase(BaseModel):
    program_id: int
    course_id: int
    semester_no: str  # Format: HK_1_1, HK_1_2, etc.
    is_required: bool = True

class ProgramCourseCreate(ProgramCourseBase):
    pass

class ProgramCourseUpdate(BaseModel):
    semester_no: Optional[str] = None
    is_required: Optional[bool] = None

class ProgramCourseResponse(ProgramCourseBase):
    program_course_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProgramCourseWithDetails(ProgramCourseResponse):
    course_name: Optional[str] = None
    course_code: Optional[str] = None
    credits: Optional[int] = None
    program_name: Optional[str] = None