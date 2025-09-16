from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CourseClassBase(BaseModel):
    course_id: int = Field(..., description="ID of the course", alias="courseId")
    teacher_id: Optional[int] = Field(None, description="ID of the teacher", alias="teacherId")
    semester: str = Field(..., description="Semester")
    year: str = Field(..., description="Year")
    section: Optional[str] = Field(None, description="Section")

class CourseClassCreate(CourseClassBase):
    pass

class CourseClassUpdate(BaseModel):
    teacher_id: Optional[int] = Field(None, description="ID of the teacher", alias="teacherId")
    semester: Optional[str] = Field(None, description="Semester")
    year: Optional[str] = Field(None, description="Year")
    section: Optional[str] = Field(None, description="Section")

class CourseClassResponse(CourseClassBase):
    course_class_id: int = Field(..., description="ID of the course class", alias="courseClassId")
    created_at: datetime = Field(..., description="Creation timestamp", alias="createdAt")
    updated_at: datetime = Field(..., description="Last update timestamp", alias="updatedAt")

    class Config:
        orm_mode = True
