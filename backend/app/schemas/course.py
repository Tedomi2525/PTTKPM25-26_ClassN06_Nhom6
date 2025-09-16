from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class CourseBase(BaseModel):
    course_code: str = Field(..., alias="courseCode", description="Code of the course")
    name: str = Field(..., description="Name of the course")
    credits: int = Field(..., description="Credits of the course")

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name of the course")
    credits: Optional[int] = Field(None, description="Credits of the course")

class CourseResponse(CourseBase):
    course_id: int = Field(..., alias="courseId", description="ID of the course")
    created_at: datetime = Field(..., alias="createdAt", description="Creation timestamp")
    updated_at: datetime = Field(..., alias="updatedAt", description="Last update timestamp")

    class Config:
        orm_mode = True
