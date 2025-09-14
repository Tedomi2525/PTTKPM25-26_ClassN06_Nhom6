from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CourseBase(BaseModel):
    course_code: str
    name: str
    credits: int

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    credits: Optional[int] = None

class CourseResponse(CourseBase):
    course_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
