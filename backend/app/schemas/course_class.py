from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CourseClassBase(BaseModel):
    course_id: int
    teacher_id: Optional[int] = None
    semester: str
    year: str
    section: Optional[str] = None

class CourseClassCreate(CourseClassBase):
    pass

class CourseClassUpdate(BaseModel):
    teacher_id: Optional[int] = None
    semester: Optional[str] = None
    year: Optional[str] = None
    section: Optional[str] = None

class CourseClassResponse(CourseClassBase):
    course_class_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
